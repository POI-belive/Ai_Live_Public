from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QFrame, QVBoxLayout, QWidget, QLabel, \
    QScrollArea, QStackedWidget
from qfluentwidgets import PlainTextEdit, LineEdit, FluentIcon, ToolButton, PushButton, CommandBar, Action, qrouter
from qfluentwidgets.components.widgets.frameless_window import FramelessWindow

from DateBase.knowledgeQA import KnowledgeQA
from DeepSeekChat.deepseek_api import deepseek_chat
from TTS.tts import tts
from qfluentwidgets import qrouter

#调用deepseek线程
class ChatWorker(QThread):
    resultSignal = pyqtSignal(str)  # 信号，传递 deepseek_chat 结果

    def __init__(self, message, qa_instance=None):
        super().__init__()
        self.message = message

        #传入知识库实例
        self.qa = qa_instance

    def run(self):
        # text = deepseek_chat(self.message)
        text = self.qa.ask(self.message)    #传入知识库
        self.resultSignal.emit(text)  # 发送结果信号

#调用TTS线程
class TTSThread(QThread):
    def __init__(self, text,character):
        super().__init__()
        self.text = text
        self.character = character

    def run(self):
        tts(self.text, character=self.character)

class CommandBarWrapper(CommandBar):
    muteToggled = pyqtSignal(bool)  #静音信号


    def __init__(self, parent=None):
        super().__init__(parent)
        self.muted = False  # 初始不静音

        # 逐个添加动作
        self.addAction(Action(FluentIcon.ADD, '添加', triggered=lambda: print("添加")))

        # 添加分隔符
        self.addSeparator()

        # 批量添加动作
        self.addActions([
            Action(FluentIcon.MUTE, '静音', checkable=True, triggered=self.onMuteAction),
            Action(FluentIcon.SYNC, '更换角色',triggered=self.onSyncAction),
            Action(FluentIcon.DELETE, '清空',triggered=self.onDeleteAction),
        ])

        # 添加始终隐藏的动作
        self.addHiddenAction(Action(FluentIcon.SCROLL, '排序', triggered=lambda: print('排序')))
        self.addHiddenAction(Action(FluentIcon.SETTING, '设置', shortcut='Ctrl+S',triggered=self.onSettingAction))

    def onMuteAction(self,checked):
        print("切换静音")
        self.muted = checked
        print("静音状态:", self.muted)
        self.muteToggled.emit(self.muted)  # 发出信号

    def onSyncAction(self):
        print("切换角色")
        parent_window = self.window()  # 获取顶层窗口
        if isinstance(parent_window, FramelessWindow):
            parent_window.switchTo(parent_window.chooseInterface)

    def onDeleteAction(self):
        print(("清空聊天框"))
        # 通知 ChatInterface 执行清空操作
        parent_interface = self.parent()
        if hasattr(parent_interface, 'clearChat'):
            parent_interface.clearChat()

    def onSettingAction(self):
        print("切换设置界面")
        parent_window = self.window()  # 获取顶层窗口
        if isinstance(parent_window, FramelessWindow):
            parent_window.switchTo(parent_window.settingInterface)



class ChatInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.current_character = "静静"

        self.setObjectName("ChatInterface")
        self.initUI()

        #初始化知识库实例（可传入知识库地址）
        self.qa_instance = KnowledgeQA()  # 或者你自己的路径

        # 静音信号初始化
        self.commandBar.muteToggled.connect(self.onMuteToggled)
        self.muted = False  # 默认不静音

        #界面初始化
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

        #创建命令栏
        self.commandBar = CommandBarWrapper(self)
        self.vlayout.addWidget(self.commandBar)
        self.commandBar.setStyleSheet("background-color: #f0f0f0;")

        # 创建滚动区域
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)  # 允许内容自适应大小
        self.scrollArea.setFrameShape(QFrame.NoFrame)

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
        # self.lineEdit.setText("杂鱼~从这里输入哦~")

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
            self.worker = ChatWorker(message, self.qa_instance)
            self.worker.resultSignal.connect(self.handleResponse)
            self.worker.start()

    #回调函数，接收deepseek返回值
    def handleResponse(self, text):
        self.addMessage('DeepSeek', text)
        if not self.muted:
            self.ttsWorker = TTSThread(text, self.current_character)
            self.ttsWorker.start()      #子线程中调用TTS
        else:
            print("静音中，未调用TTS")

    #静音信号
    def onMuteToggled(self, muted):
        self.muted = muted
        print("ChatInterface收到静音状态:", self.muted)

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

    #清空聊天气泡
    def clearChat(self):
        while self.chatLayout.count():
            item = self.chatLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        print("聊天记录已清空")