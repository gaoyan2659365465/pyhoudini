###################################################################################
# (c) Lightmap Ltd 2018
#
# Miscellaneous Util functions for use in HDR Light Studio Connections
###################################################################################


class SingletonImplementationException(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.strMessage = "Singleton Decorated Classes must inherit the SingletonInterface class"

    def __str__(self):
        return repr(self.strMessage)


class SingletonUsageException(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.strMessage = "The Singleton Class is a decorator to be applied to other classes, " \
                          "it is not for standalone usage"

    def __str__(self):
        return repr(self.strMessage)


class SingletonInterface(object):
    """
    The SingletonInterface class is a signaling layer which allows the Singleton decorator
    to check the state of the decorated object.

    Setting the active flag to false indicates that the Singleton may delete the stored
    instance safely in the event it attempts to recreate a new instance through a reboot
    operation.
    """

    # noinspection PyUnusedLocal
    def __init__(self, *args, **kwargs):
        self._bActive = False

    def isActive(self):
        # Allows singleton to detect when the logger has been shutdown to enable
        # a reboot if the connection is reinstalled (e.g.  in a new scene)
        return self._bActive

    def setActive(self, bActiveState):
        self._bActive = bActiveState


class Singleton(object):
    # https://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons
    def __init__(self, cDecorated):
        if cDecorated is None:
            raise SingletonUsageException()
        if not issubclass(cDecorated, SingletonInterface):
            raise SingletonImplementationException()
        self._cDecorated = cDecorated
        self._cInstance = None

    def type(self):
        return self._cDecorated

    def instance(self, *args, **kwargs):
        if self._cInstance is not None:
            return self._cInstance

        self._cInstance = self._cDecorated(*args, **kwargs)
        return self._cInstance

    def reboot(self, *args, **kwargs):
        if self._cInstance is not None:
            if self._cInstance.isActive():
                return False

        self._cInstance = self._cDecorated(*args, **kwargs)
        return True

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cDecorated)


###################################################################################
# Maths Utils
###################################################################################
class HdrlsVec2(object):
    def __init__(self, fX, fY):
        self.fX = fX
        self.fY = fY

    def __str__(self):
        return "[[x: {0}], [y: {1}]]".format(self.fX, self.fY)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return HdrlsVec2(self.fX + other.fX, self.fY + other.fY)
        elif isinstance(other, (int, float)):
            return HdrlsVec2(self.fX + other, self.fY + other)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return HdrlsVec2(self.fX * other.fX, self.fY * other.fY)
        elif isinstance(other, (int, float)):
            return HdrlsVec2(self.fX * other, self.fY * other)

    def asTuple(self):
        return self.fX, self.fY


class HdrlsVec3(object):
    def __init__(self, fX, fY, fZ):
        self.fX = fX
        self.fY = fY
        self.fZ = fZ

    def __str__(self):
        return "[[x: {0}], [y: {1}], [z: {2}]]".format(self.fX, self.fY, self.fZ)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return HdrlsVec3(self.fX + other.fX, self.fY + other.fY, self.fZ + other.fZ)
        elif isinstance(other, (int, float)):
            return HdrlsVec3(self.fX + other, self.fY + other, self.fZ + other)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return HdrlsVec3(self.fX * other.fX, self.fY * other.fY, self.fZ * other.fZ)
        elif isinstance(other, (int, float)):
            return HdrlsVec3(self.fX * other, self.fY * other, self.fZ * other)

    def asTuple(self):
        return self.fX, self.fY, self.fZ


###################################################################################
# Validators
###################################################################################
def tupleValidator(tTupleToValidate, nExpectedLength):
    if not isinstance(tTupleToValidate, tuple):
        return False
    if len(tTupleToValidate) != nExpectedLength:
        return False
    return True
