from ctypes.wintypes import *
from PySide2.QtWidgets import QWidget

PADDING = 2
UP,DOWN,LEFT,RIGHT,LEFTTOP,LEFTBOTTOM,RIGHTTOP,RIGHTBOTTOM,UNDIRECT = range(9)
HTLEFT = 10
HTRIGHT = 11
HTTOP = 12
HTTOPLEFT = 13
HTTOPRIGHT = 14
HTBOTTOM = 15
HTBOTTOMLEFT = 16
HTBOTTOMRIGHT = 17
HTCAPTION = 2


class System():
	def __init__(self,widget:QWidget):
		self.ss = widget
		#告诉windows缩放
	def GET_X_LPARAM(self, param):
		return param & 0xffff

	def GET_Y_LPARAM(self, param):
		return param >> 16
	
	def nativeEvent(self, eventType, message):
		result = 0
		msg2 = MSG.from_address(message.__int__())
		minV,maxV = 0,5
		if msg2.message == 0x0084:
			xPos = self.GET_X_LPARAM(msg2.lParam) - self.ss.frameGeometry().x()
			yPos = self.GET_Y_LPARAM(msg2.lParam) - self.ss.frameGeometry().y()
			if(xPos > minV and xPos < maxV):
				result = HTLEFT#左
			elif(xPos > (self.ss.width() - maxV) and xPos < (self.ss.width() - minV)):
				result = HTRIGHT#右
			elif(yPos > minV and yPos < maxV):
				result = HTTOP#上
			elif(yPos > (self.ss.height() - maxV) and yPos < (self.ss.height() - minV)):
				result = HTBOTTOM#下
			if(xPos > minV and xPos < maxV and yPos > minV and yPos < maxV):
				result = HTTOPLEFT
			elif(xPos > (self.ss.width() - maxV) and xPos < (self.ss.width() - minV) and yPos > minV and yPos < maxV):
				result = HTTOPRIGHT
			elif(xPos > minV and xPos < maxV and yPos > (self.ss.height() - maxV) and yPos < (self.ss.height() - minV)):
				result = HTBOTTOMLEFT
			elif(xPos > (self.ss.width() - maxV) and xPos < (self.ss.width() - minV) and yPos > (self.ss.height() - maxV) and yPos < (self.ss.height() - minV)):
				result = HTBOTTOMRIGHT
			elif(xPos > maxV and xPos < (self.ss.width() - maxV) and yPos > maxV and yPos < (self.ss.height() - maxV)):
				return False,0
			return (True,result)
		return False,0
