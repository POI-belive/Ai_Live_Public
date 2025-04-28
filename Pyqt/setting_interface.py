import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QWidget, QScrollArea, QFrame
from qfluentwidgets import CardWidget, IconWidget, BodyLabel, CaptionLabel, PushButton, TransparentToolButton, \
    FluentIcon, GroupHeaderCardWidget, SwitchButton


#app卡片组件
class AppCard(CardWidget):

    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.openButton = PushButton('Open', self)
        self.moreButton = TransparentToolButton(FluentIcon.MORE, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(48, 48)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.openButton.setFixedWidth(120)

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.openButton, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignRight)

        self.moreButton.setFixedSize(32, 32)

def addAppCard():
    card = AppCard(
        icon=":/qfluentwidgets/images/logo.png",
        title="外观设置",
        content="neko Inc."
    )
    card.clicked.connect(lambda: print("点击卡片"))
    return card


#设置组件
class SettingsCard(GroupHeaderCardWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("基本设置")
        self.setBorderRadius(8)

        #按钮组件初始化
        self.switchbutton1 = SwitchButton()
        self.switchbutton2 = SwitchButton()
        self.switchbutton3 = SwitchButton()
        self.switchbutton4 = SwitchButton()
        self.switchbutton5 = SwitchButton()
        self.switchbutton6 = SwitchButton()
        self.switchbutton7 = SwitchButton()
        self.switchbutton8 = SwitchButton()


        #按钮组件格式设置
        for switch in [self.switchbutton1, self.switchbutton2, self.switchbutton3,
                       self.switchbutton4, self.switchbutton5, self.switchbutton6,
                       self.switchbutton7, self.switchbutton8]:
            switch.setFixedWidth(120)

        # 添加组件到分组中
        self.addGroup("resource/Rocket.svg", "切换状态", "切换深色模式和浅色模式", self.switchbutton1)
        self.addGroup("resource/Rocket.svg", "超频模式", "选择是否超频", self.switchbutton2)
        self.addGroup("resource/Joystick.svg", "效率提升模式", "以几何倍数提升效率", self.switchbutton3)
        self.addGroup("resource/Rocket.svg", "切换状态", "切换深色模式和浅色模式", self.switchbutton1)
        self.addGroup("resource/Rocket.svg", "超频模式", "选择是否超频", self.switchbutton2)
        self.addGroup("resource/Joystick.svg", "效率提升模式", "以几何倍数提升效率", self.switchbutton3)
        self.addGroup("resource/Rocket.svg", "切换状态", "切换深色模式和浅色模式", self.switchbutton1)
        self.addGroup("resource/Rocket.svg", "超频模式", "选择是否超频", self.switchbutton2)
        self.addGroup("resource/Joystick.svg", "效率提升模式", "以几何倍数提升效率", self.switchbutton3)
        self.addGroup("resource/Rocket.svg", "切换状态", "切换深色模式和浅色模式", self.switchbutton6)
        self.addGroup("resource/Rocket.svg", "超频模式", "选择是否超频", self.switchbutton7)
        self.addGroup("resource/Joystick.svg", "效率提升模式", "以几何倍数提升效率", self.switchbutton8)
        group = self.addGroup("resource/Python.svg", "CAS模式", "近距离空地支援打击", self.switchbutton4)
        group.setSeparatorVisible(True)

#设置子页面
class SettingsInterface(QWidget):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("滚动设置界面")
        self.setGeometry(100, 100, 400, 300)

        # 创建主布局
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 40, 0, 0)  # 左上右下

        # 创建一个QScrollArea
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)  # 设置可以自适应大小
        scrollArea.setFrameShape(QFrame.NoFrame)

        # 创建一个容器窗口，作为滚动区域的内容
        scrollContentWidget = QWidget()

        # 创建一个垂直布局，用于放置设置项
        settingsLayout = QVBoxLayout(scrollContentWidget)

        # 实例化添加卡片和设置项
        card = addAppCard()
        settingsLayout.addWidget(card)

        settingsCard = SettingsCard()
        settingsLayout.addWidget(settingsCard)

        # 设置滚动区域的内容
        scrollArea.setWidget(scrollContentWidget)

        # 将QScrollArea添加到主布局中
        mainLayout.addWidget(scrollArea)

        # 设置主窗口的布局
        self.setLayout(mainLayout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsInterface()
    window.show()
    sys.exit(app.exec_())
