from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from .W_SocketBase import *
from .BP_Json import BP_Json

#每个插槽所具备的内容，连接端、文字、输入控件
class W_CheckBox(QCheckBox):
    def __init__(self,parent:QWidget=None):
        super(W_CheckBox,self).__init__(parent)
        self.setText("")
        self.setPalette(QPalette(QColor("#00000000")))
        self.setAutoFillBackground(True) #自动填充背景
    
class w_input(QLineEdit):
    def __init__(self,parent:QWidget=None):
        super(w_input,self).__init__(parent)
        self.textChanged['QString'].connect(self.setTextSize)
        self.setTextValidator()
    
    def setTextValidator(self):
        regx = QRegExp("^-?\d+$")
        self.setValidator(QRegExpValidator(regx,self))
        self.setText("0")
    
    def setTextSize(self, a0: str):
        """重载-内容变更"""
        if len(a0)>1:
            if a0[0]=='-':
                if a0[1]=='0':
                    a=0
                    for i in a0:
                        if i == '-' or i == '0':
                            a=a+1 
                        else:break
                    a0='-'+a0[a:]
                    self.setText(a0)
                    return
            
            if a0[0]=='0':
                a=0
                for i in a0:
                    if i == '0':
                        a=a+1 
                    else:break
                a0=a0[a:]
                self.setText(a0)
                return
            
        self.setFont(QFont("SimSun",10))
        font_metrics = QFontMetrics(self.font())
        font_width = font_metrics.width(a0,len(a0))
        text_len = font_width + 10
        if text_len<18:
            text_len = 18
        self.resize(text_len,self.height())

    def focusOutEvent(self, event):
        """重载-失去焦点"""
        if self.text() == "" or self.text() == "-":
            self.setText("0")
        return super().focusOutEvent(event)

class w_inputSrting(w_input):
    def __init__(self,parent:QWidget=None):
        super(w_inputSrting,self).__init__(parent)
    def setTextValidator(self):
        pass
    def setTextSize(self, a0: str):
        """重载-内容变更"""
        self.setFont(QFont("SimSun",10))
        font_metrics = QFontMetrics(self.font())
        font_width = font_metrics.width(a0,len(a0))
        text_len = font_width + 10
        if text_len<18:
            text_len = 18
        self.resize(text_len,self.height())
    def focusOutEvent(self, event):
        """重载-失去焦点"""
        return super(w_input,self).focusOutEvent(event)

class w_inputFloat(w_input):
    def __init__(self,parent:QWidget=None):
        super(w_inputFloat,self).__init__(parent)
    def setTextValidator(self):
        regx = QRegExp("^(-?\d+)(\.\d+)?$")
        self.setValidator(QRegExpValidator(regx,self))
        self.setText("0.0")
    def setTextSize(self, a0: str):
        """重载-内容变更"""
        self.setFont(QFont("SimSun",10))
        font_metrics = QFontMetrics(self.font())
        font_width = font_metrics.width(a0,len(a0))
        text_len = font_width + 10
        if text_len<18:
            text_len = 18
        self.resize(text_len,self.height())
    def focusOutEvent(self, event):
        """重载-失去焦点"""
        if self.text() == "" or self.text() == "-":
            self.setText("0.0")
        if self.text() == "0" or self.text() == "-0":
            self.setText("0.0")
        if self.text() == "0." or self.text() == "-0.":
            self.setText("0.0")
        if self.text() == "-0.0":
            self.setText("0.0")
        
        a0 = self.text()
        list1 = a0.split('.', 1)#以小数点为分割
        int0 = list1[0]
        try:
            float0 = list1[1]#说明没有找到小浮点
        except:
            float0 = '0'
            
        if len(a0)>1:
            if int0[0]!='-':#如果是正数
                a=0
                for i in int0:
                    if i == '0':
                        a=a+1 
                    else:break
                int0=int0[a:]
                if int0=='':int0='0'
                a=0
                for i in reversed(float0):#逆序遍历
                    if i == '0':
                        a=a+1 
                    else:break
                float0=float0[:len(float0)-a]
                if float0=='':float0='0'
                self.setText(int0+'.'+float0)
            elif int0[0]=='-':#如果是负数
                int0 = int0[1:]
                if int0[0]!='-':#如果是正数
                    a=0
                    for i in int0:
                        if i == '0':
                            a=a+1 
                        else:break
                    int0=int0[a:]
                    if int0=='':int0='0'
                    a=0
                    for i in reversed(float0):#逆序遍历
                        if i == '0':
                            a=a+1 
                        else:break
                    float0=float0[:len(float0)-a]
                    if float0=='':float0='0'
                    self.setText('-'+int0+'.'+float0)
            else:
                self.setText(int0+'.'+float0)
                            
        # if len(a0)>1:
        #     if a0[0]=='-':
        #         if a0[1]=='0':
        #             a=0
        #             for i in a0:
        #                 if i == '-' or i == '0':
        #                     a=a+1 
        #                 else:break
        #             a0='-'+a0[a:]
        #             self.setText(a0)
            
        #     if a0[0]=='0':
        #         a=0
        #         for i in a0:
        #             if i == '0':
        #                 a=a+1 
        #             else:break
        #         a0=a0[a:]
        #         self.setText(a0)
        return super().focusOutEvent(event)

class W_SocketContent(QGraphicsItem,BP_Json):
    def __init__(self,parent=None,data_type:int=0,direction:int=0,logic_type:int=0):
        super().__init__(parent)
        self.width = 26
        self.height = 20
        self.data_type = data_type
        self.direction = direction      #插槽方向(0/1)左右
        self.logic_type = logic_type
        self.mouse_stay = False         #鼠标停留状态
        self._color_mouse_enter_label_1 = QColor("#7fffffff") #鼠标悬浮时背景亮片颜色
        self._color_mouse_enter_label_0 = QColor("#00ffffff") #鼠标悬浮时背景亮片颜色--渐变
        self.setAcceptHoverEvents(True)#接受悬停事件
        self.w_socket = W_SocketBase(self,data_type,direction,logic_type)
        self.pen_Text = QPen(QColor("#dee1e2"))#文字颜色
        self.font = QFont("Arial",11)
        self.setSocketText('')
        self.createInputWidget()
        
        if self.direction == VALUE_INPUT:
            self.text_x = 24
        elif self.direction == VALUE_OUTPUT:
            self.text_x = 9
            self.w_socket.setGeometry(self.width-26,0,26,20)
        
    
    def setGeometry(self,x,y,width,height):
        """设置位置尺寸"""
        self.setPos(x,y)
        self.width = width
        self.height = height
    
    def boundingRect(self) -> QRectF:
        """定义Qt的边框"""
        return QRectF(0,0,self.width,self.height).normalized()
    
    def getRequiredSize(self):
        """获取所需尺寸用来让父控件延展"""
        font_metrics = QFontMetrics(self.font)
        font_width = font_metrics.width(self.socket_text,len(self.socket_text))
        text_len = font_width+7
        #加上文字的长度
        return self.width+text_len,self.height
    
    def createInputWidget(self):
        """创建输入控件"""
        if self.direction == VALUE_OUTPUT:return
        if self.logic_type == SOCKET_TYPE_LOGIC:return
        
        self.socket_widget = QGraphicsProxyWidget(self)
        if self.data_type == SOCKET_TYPE_BOOL:
            self.w_input = W_CheckBox()
            self.w_input.setGeometry(self.width, 0, 10, 20)
            size = self.w_input.sizeHint()#获取控件尺寸
            text_len = self.getSocketTextLen()#获取文字长度
            self.width = 26+text_len+size.width()+5
            self.height = 20
            self.socket_widget.setWidget(self.w_input)
        if self.data_type == SOCKET_TYPE_FLOAT:
            self.w_input = w_inputFloat()
            self.w_input.textChanged['QString'].connect(self.updateInputWidget)
            self.w_input.setGeometry(self.width, 1, 31, 18)
            self.updateInputWidget()
            self.socket_widget.setWidget(self.w_input)
        if self.data_type == SOCKET_TYPE_INT:
            self.w_input = w_input()
            self.w_input.textChanged['QString'].connect(self.updateInputWidget)
            self.w_input.setGeometry(self.width, 1, 20, 18)
            self.updateInputWidget()
            self.socket_widget.setWidget(self.w_input)
        if self.data_type == SOCKET_TYPE_STRING:
            self.w_input = w_inputSrting()
            self.w_input.textChanged['QString'].connect(self.updateInputWidget)
            self.w_input.setGeometry(self.width, 1, 20, 18)
            self.updateInputWidget()
            self.socket_widget.setWidget(self.w_input)
    
    def updateInputWidget(self):
        """事件调度-更新输入控件"""
        input_width = self.w_input.width()
        self.updateWidgetSize(input_width)
        
    def updateWidgetSize(self,input_width):
        """更新控件尺寸"""
        text_len = self.getSocketTextLen()#获取文字长度
        self.width = 26+text_len+input_width+5
        self.height = 20
        node_content = self.parentItem()
        w_node = node_content.parentItem()
        w_node.setAutomaticSize()
        if self.direction == VALUE_OUTPUT:
            self.w_socket.setGeometry(self.width-26,0,26,20)
    
    def getSocketLocation(self):
        """获取插槽的绝对位置"""
        return self.pos() + self.w_socket.getSocketLocation()    
    
    def getSocketDirection(self,socket_num:int=0)->bool:
        """获取插槽是左边还是右边"""
        return self.direction
    
    def setSocketState(self,isLink:bool=False):
        """设置端口状态是否已连接"""
        self.w_socket.setSocketState(isLink)
        #此处不合理，应该考虑多种类型
        if isLink:
            try:
                self.w_checkBox.hide()
            except:pass
            try:
                self.w_input.hide()
            except:pass
        else:
            try:
                self.w_checkBox.show()
            except:pass
            try:
                self.w_input.show()
            except:pass
    
    def getSocketColor(self)-> QColor:
        """获取插槽的颜色"""
        return self.w_socket.getSocketColor()
    
    def setSocketColor(self,color:str='#000000'):
        """设置端口颜色
        :param color: 不同颜色表示不同数据类型
        """
        color = self.w_socket.setSocketColor(color)
        #更新背景悬浮亮片颜色
        if self.logic_type == SOCKET_TYPE_VALUE:
            color = '#7f' + color[1:]#透明0.5
            self._color_mouse_enter_label_1 = QColor(color)
        return color
    
    def getSocketTextLen(self):
        """获取端口文字长度"""
        font_metrics = QFontMetrics(self.font)
        text = self.socket_text
        text_len = len(text)
        font_width = font_metrics.width(text,text_len)
        text_len = font_width+7
        return text_len
    
    def setSocketText(self,text:str=''):
        """设置端口文字"""
        self.socket_text = text
        text_len = self.getSocketTextLen()
        self.width = 26+text_len
        try:
            self.w_input.setGeometry(self.width, 1, 20, 18)
        except:pass
        input_width = 0
        try:
            input_width = self.w_input.width()
        except:pass
        self.updateWidgetSize(input_width)
    
    def drawMouseEnterLabel(self,painter):
        """绘制鼠标悬浮时高亮效果"""
        if self.mouse_stay == True:
            lg = QLinearGradient(0, 0, self.width, 0)
            lg.setColorAt(0, self._color_mouse_enter_label_0)
            lg.setColorAt(0.1, self._color_mouse_enter_label_1)
            lg.setColorAt(0.9, self._color_mouse_enter_label_1)
            lg.setColorAt(1, self._color_mouse_enter_label_0)
            painter.setBrush(lg)
            painter.setPen(Qt.transparent)
            painter.drawRect(0, 0, self.width, self.height)
    
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """重载-绘制"""
        """
        self.brush_background = QBrush(QColor("#00FFFFFF"))
        path_content1 = QPainterPath()
        path_content1.setFillRule(Qt.WindingFill)
        path_content1.addRect(0, 0, self.width, self.height)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush_background)
        painter.drawPath(path_content1.simplified())
        """
        self.drawMouseEnterLabel(painter)
        
        #绘制文字
        painter.setFont(self.font)
        painter.setPen(self.pen_Text)
        painter.drawText(self.text_x,15,self.socket_text)
    
    #region 序列化
    def dump(self):
        """保存"""
        value = ''
        if hasattr(self,'w_input'):
            if isinstance(self.w_input,w_input):
                value = self.w_input.text()
            elif isinstance(self.w_input,W_CheckBox):
                if self.w_input.isChecked():
                    value = 'True'
                else:
                    value = 'False'
            else:
                value = ''
        
        # if self.direction == VALUE_OUTPUT:#如果方向=输出
        #     if self.logic_type == SOCKET_TYPE_LOGIC:#如果插槽=逻辑类型
        #         for item in self.scene().items():
        #             if isinstance(item, W_NodeBase):
        #                 pass
        data = {'data_type':self.data_type,
                'direction':self.direction,
                'logic_type':self.logic_type,
                'socket_text':self.socket_text,
                'input_value':value,
                }
        return data
    def load(self,obj):
        """加载"""
        self.data_type = obj['data_type']
        self.direction = obj['direction']
        self.logic_type = obj['logic_type']
        self.socket_text = obj['socket_text']
        try:
            if obj['input_value'] == 'True':
                value = self.w_input.setChecked(True)
            elif obj['input_value'] == 'False':
                value = self.w_input.setChecked(False)
            else:
                value = self.w_input.setText(obj['input_value']) 
        except:
            try:
                value = self.w_input.setText(obj['input_value']) 
            except:pass
        return
    #endregion