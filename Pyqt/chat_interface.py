import asyncio

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QFrame, QVBoxLayout, QWidget, QLabel, \
    QScrollArea
from qfluentwidgets import PlainTextEdit, LineEdit, FluentIcon, ToolButton, PushButton
from DeepSeekChat.deepseek_api import deepseek_chat
from TTS.tts import tts

#调用deepseek线程
class ChatWorker(QThread):
    resultSignal = pyqtSignal(str)  # 信号，传递 deepseek_chat 结果

    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        text = deepseek_chat(self.message)
        self.resultSignal.emit(text)  # 发送结果信号

#调用TTS线程
class TTSThread(QThread):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        tts(self.text, character="胡桃")


class ChatInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("ChatInterface")
        self.initUI()
        self.vlayout.setAlignment(Qt.AlignCenter)           #设置居中
        self.vlayout.setContentsMargins(200, 40, 200, 20)   # 设置布局的边距（左、上、右、下）

        #设置组件边界大小
        # self.textEdit.setMaximumSize(600,1080)
        self.lineEdit.setMaximumSize(550,100)
        self.scrollArea.setMaximumSize(600,1080)

        # self.textEdit.setMinimumSize(300, 500)
        self.lineEdit.setMinimumSize(250, 20)
        self.scrollArea.setMinimumSize(300, 500)


    def initUI(self):
        #设置布局
        self.vlayout = QVBoxLayout(self)
        self.hlayout = QHBoxLayout(self)

        # 创建滚动区域
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)  # 允许内容自适应大小

        # 创建聊天记录的布局
        self.chatLayout = QVBoxLayout()
        self.chatLayout.setAlignment(Qt.AlignTop)  # 内容从顶部开始排列

        # 创建一个容器用于存放聊天记录
        self.chatContainer = QWidget()
        self.chatContainer.setLayout(self.chatLayout)

        # 将容器放入滚动区域
        self.scrollArea.setWidget(self.chatContainer)

        # 添加滚动区域到主布局
        self.vlayout.addWidget(self.scrollArea)

        # 初始化头像路径
        self.you_avatar_path = 'resource/avatars/you.png'
        self.DeepSeek_avatar_path = 'resource/avatars/deepseek.png'


        #添加输入框
        self.lineEdit=LineEdit()
        self.lineEdit.setText("杂鱼~从这里输入哦~")

        #添加发送按钮
        self.toolButton=ToolButton(FluentIcon.SEND,self)
        self.toolButton.clicked.connect(self.sendMessage)

        # 将组件添加进布局中
        self.hlayout.addWidget(self.lineEdit)
        self.hlayout.addWidget(self.toolButton)

        self.vlayout.addLayout(self.hlayout)



    def sendMessage(self):
        #发送消息
        message = self.lineEdit.text()
        if message:
            # 将消息添加到聊天记录中
            self.addMessage('You',message)
            self.lineEdit.clear()
            # text=deepseek_chat(message)
            # self.addMessage('XiaoJi',text)
            # tts(text, character="胡桃")

            # 开启新线程处理 deepseek_chat
            self.worker = ChatWorker(message)
            self.worker.resultSignal.connect(self.handleResponse)
            self.worker.start()

    #回调函数，接收deepseek返回值
    def handleResponse(self, text):
        self.addMessage('DeepSeek', text)
        self.ttsWorker = TTSThread(text)
        self.ttsWorker.start()  # 在子线程播放 TTS

    #创建聊天气泡
    def addMessage(self, sender, message):
        # 创建消息容器
        message_widget = QWidget()
        message_layout = QHBoxLayout()
        message_widget.setLayout(message_layout)

        # 创建头像标签
        avatar_label = QLabel()
        avatar_label.setFixedSize(40, 40)  # 设置头像尺寸

        # 加载头像图片
        if sender == 'You':
            avatar_pixmap = QPixmap(self.you_avatar_path).scaled(
                40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            avatar_label.setPixmap(avatar_pixmap)
        elif sender == 'DeepSeek':
            avatar_pixmap = QPixmap(self.DeepSeek_avatar_path).scaled(
                40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            avatar_label.setPixmap(avatar_pixmap)

        # 创建消息文本
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setMaximumWidth(800)  # 设置最大宽度，防止气泡过长
        message_label.setStyleSheet("padding: 10px; border-radius: 10px;")

        if sender == 'You':
            # 右侧对齐，绿色背景，头像在右
            message_label.setStyleSheet("""
                background-color: #DCF8C6;
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
                color: #000000;
            """)
            # 添加外部布局，控制消息的对齐和间距
            inner_layout = QHBoxLayout()
            inner_layout.addStretch()
            inner_layout.addWidget(message_label)
            inner_layout.addWidget(avatar_label)
            message_layout.addLayout(inner_layout)
        elif sender == 'DeepSeek':
            # 左侧对齐，白色背景，头像在左
            message_label.setStyleSheet("""
                background-color: #FFFFFF;
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
                color: #000000;
            """)
            # 添加外部布局，控制消息的对齐和间距
            inner_layout = QHBoxLayout()
            inner_layout.addWidget(avatar_label)
            inner_layout.addWidget(message_label)
            inner_layout.addStretch()
            message_layout.addLayout(inner_layout)
        else:
            # 系统消息，居中显示
            message_label.setAlignment(Qt.AlignCenter)
            message_label.setStyleSheet("""
                background-color: #E0E0E0;
                padding: 10px;
                border-radius: 10px;
                font-size: 12px;
                color: #555555;
            """)
            message_layout.addStretch()
            message_layout.addWidget(message_label)
            message_layout.addStretch()

        # 将消息容器添加到聊天记录布局中
        self.chatLayout.addWidget(message_widget)

        # 自动滚动到最底部
        self.scrollArea.verticalScrollBar().setValue(
            self.scrollArea.verticalScrollBar().maximum())