###################################################################################
# (c) Lightmap Ltd 2018
#
# Container class enabling logging in HDR Light Studio Connections
###################################################################################
from functools import wraps
import os
import sys
import logging
from datetime import date
import lightmap.HdrlsUtils as HdrlsUtils  # pylint: disable=import-error, no-name-in-module

PRINT_STRING_LIMIT = 200


###################################################################################
# Logger Definition
###################################################################################
@HdrlsUtils.Singleton
class HdrlsLogger(HdrlsUtils.SingletonInterface):
    LOG_FILE_ENV_VAR = "HDRLS_LOG_FILE"
    LOG_LEVEL_ENV_VAR = "HDRLS_LOG_LEVEL"
    VERBOSE_LEVEL = 10
    GENERAL_LEVEL = 20
    ERROR_LEVEL = 40  # This level is unused but is left in for future reference
    FORMAT = "%(asctime)s%(levelname)s: %(message)s"  # %H:%M:%S asctime
    DATE_FORMAT = "%H:%M:%S"

    # Uses args and kwargs to ensure a standard interface for the singleton wrapper.
    # It helps ensure that the number of params is correct
    # noinspection PyUnusedLocal
    def __init__(self, *args, **kwargs):  # pylint: disable=unused-argument
        super(HdrlsLogger.type(), self).__init__(*args, **kwargs)
        if self.LOG_FILE_ENV_VAR not in os.environ:
            self.m_bLoggingEnabled = False
            self.setActive(False)
            return

        reload(logging)  # Reload logging to ensure that the module is clean between projects in the same session.
        logging.addLevelName(self.VERBOSE_LEVEL, " Verbose")
        logging.addLevelName(self.GENERAL_LEVEL, "Base Log")
        logging.addLevelName(self.ERROR_LEVEL, "   Error")

        self.strHostName = "connection"
        if "strHostName" in kwargs.keys():
            self.strHostName = kwargs['strHostName']

        self.m_bLoggingEnabled = True

        # Setup Log output file
        strLogFile = os.getenv(self.LOG_FILE_ENV_VAR)
        self.m_strLogFile = "{0}.{1}{2}".format(strLogFile[:strLogFile.rfind(".")], self.strHostName,
                                                strLogFile[strLogFile.rfind("."):])

        try:
            if os.path.isfile(self.m_strLogFile):
                strLogFile1 = self.m_strLogFile + ".1"
                strLogFile2 = self.m_strLogFile + ".2"
                strLogFile3 = self.m_strLogFile + ".3"

                if os.path.isfile(strLogFile3):
                    os.remove(strLogFile3)

                if os.path.isfile(strLogFile2):
                    os.rename(strLogFile2, strLogFile3)

                if os.path.isfile(strLogFile1):
                    os.rename(strLogFile1, strLogFile2)

                os.rename(self.m_strLogFile, strLogFile1)
        except OSError, e:
            self.m_bLoggingEnabled = False
            print ("HDR Light Studio Connection failed to start logging: {0}".format(e.message))
            return

        self.setActive(True)

        # Setup log level
        nLogLevel = 0
        if self.LOG_LEVEL_ENV_VAR in os.environ:
            nLogLevel = os.getenv(self.LOG_FILE_ENV_VAR)

        self.pyLogLevel = self.GENERAL_LEVEL
        if nLogLevel != 0:
            self.pyLogLevel = self.VERBOSE_LEVEL

        self.m_cStreamLogFile = open(self.m_strLogFile, mode="w", buffering=0)

        logging.basicConfig(stream=self.m_cStreamLogFile, level=self.pyLogLevel, format=self.FORMAT,
                            datefmt=self.DATE_FORMAT)
        self.pyLogger = logging.getLogger()
        self.logDebugMessage("***********************************************************")
        self.logDebugMessage("Logging Started Successfully")
        self.logDebugMessage("Host: {0}".format(self.strHostName))
        self.logDebugMessage("Date: {0}".format(date.today().strftime("%Y/%m/%d")))
        self.logDebugMessage("***********************************************************")

    def shutdownLogger(self):
        if self.m_bLoggingEnabled:
            self.logDebugMessage("LOGGING SHUTTING DOWN")
            logging.shutdown()
            self.m_cStreamLogFile.close()
            self.m_cStreamLogFile = None
            self.setActive(False)

    def _logMessage(self, strMessage, pyLevel):
        if self.m_bLoggingEnabled and self.isActive():
            self.pyLogger.log(pyLevel, strMessage)

    def logErrorMessage(self, strMessage):
        self._logMessage(strMessage, self.ERROR_LEVEL)

    def logDebugMessage(self, strMessage):
        self._logMessage(strMessage, self.GENERAL_LEVEL)

    def logVerboseMessage(self, strMessage):
        self._logMessage(strMessage, self.VERBOSE_LEVEL)


###################################################################################
# Accessors and Decorators
###################################################################################
# Deviates from the style guide as it's usage is as a function e.g. @HdrlsLogging.functionLogger()
# pylint: disable=too-few-public-methods
class functionLogger(object):
    def __call__(self, func):
        def logArgs(*args, **kwargs):
            strArgDebugMessage = "Args: "
            for index, arg in enumerate(args):
                    strArg = sanitizeLogMessage(arg)
                    strArgDebugMessage = "{0},\n\t {1}: {2}".format(strArgDebugMessage,
                                                                    "Arg{0}".format(index + 1),
                                                                    ''.join(strArg.splitlines()))
            HdrlsLogger.instance().logDebugMessage(strArgDebugMessage)

            strKwargDebugMessage = "Kwarg Pairs: "
            for strKwargKey in kwargs:
                    strKwarg = sanitizeLogMessage(kwargs[strKwargKey])
                    strKwargDebugMessage = "{0},\n\t {1}: {2}".format(strKwargDebugMessage,
                                                                      strKwargKey,
                                                                      strKwarg)
            HdrlsLogger.instance().logDebugMessage(strKwargDebugMessage)

        @wraps(func)
        def functionWrapper(*args, **kwargs):
            HdrlsLogger.instance().logDebugMessage("Entering {0}".format(func.__name__))
            logArgs(*args, **kwargs)

            oRetVal = func(*args, **kwargs)

            HdrlsLogger.instance().logDebugMessage("Exiting {0}".format(func.__name__))

            return oRetVal

        return functionWrapper


def sanitizeLogMessage(strMessage):
    if strMessage is None:
        return "Failed to sanitize log message - No message provided - sanitizeLogMessage"
    try:
        strMessage = str(strMessage)
        if len(strMessage) > PRINT_STRING_LIMIT:
            strMessage = strMessage[:PRINT_STRING_LIMIT - 3] + "... {0} bytes of data found".format(
                            sys.getsizeof(strMessage))
    except UnicodeEncodeError, uniError:
        strMessage = "Failed to sanitize log message: {0}".format(uniError.message)
    return strMessage


def logErrorMessage(strMessage):
    HdrlsLogger.instance().logErrorMessage(sanitizeLogMessage(strMessage))


def logDebugMessage(strMessage):
    HdrlsLogger.instance().logDebugMessage(sanitizeLogMessage(strMessage))


def logVerboseMessage(strMessage):
    HdrlsLogger.instance().logVerboseMessage(sanitizeLogMessage(strMessage))


def shutdownLogger():
    HdrlsLogger.instance().shutdownLogger()
