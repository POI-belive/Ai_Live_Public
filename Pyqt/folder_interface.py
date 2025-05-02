# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QAbstractAnimation
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QWidget, QApplication, QLabel
from qfluentwidgets import (
    ScrollArea, PushButton, ElevatedCardWidget, BodyLabel, CaptionLabel,
    FlowLayout, ImageLabel, MessageBox, isDarkTheme, FluentIcon, LineEdit, ToolButton, InfoBar, InfoBarPosition
)


class VoiceModelCard(ElevatedCardWidget):
    """ 语音模型卡片组件 """
    clicked = pyqtSignal()

    def __init__(self, iconPath: str, title: str, description: str, parent=None):
        super().__init__(parent)
        self.setFixedSize(240, 280)
        self.iconPath = iconPath
        self.title = title
        self.description = description
        self.isSelected = False

        # 初始化方法调用
        self.initUI()
        self.initStyle()
        self.initAnimation()

    def initUI(self):
        """ 初始化界面布局 """
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        # 图片区域
        self.iconLabel = ImageLabel(self.iconPath)
        self.iconLabel.setScaledContents(True)
        self.iconLabel.setMinimumSize(240, 160)
        self.iconLabel.setAlignment(Qt.AlignCenter)

        # 分隔线
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFixedHeight(1)
        self.separator.setStyleSheet("background-color: rgba(0, 0, 0, 0.1);")

        # 文字区域
        textContainer = QWidget()
        textLayout = QVBoxLayout(textContainer)
        textLayout.setContentsMargins(16, 12, 16, 16)
        textLayout.setSpacing(8)
        self.titleLabel = BodyLabel(self.title)
        self.descLabel = CaptionLabel(self.description)
        textLayout.addWidget(self.titleLabel, 0, Qt.AlignCenter)
        textLayout.addWidget(self.descLabel, 0, Qt.AlignCenter)

        # 组合布局
        mainLayout.addWidget(self.iconLabel)
        mainLayout.addWidget(self.separator)
        mainLayout.addWidget(textContainer)

    def initStyle(self):
        """ 初始化样式 """
        self.setBorderRadius(12)
        self.setProperty('isSelected', 'false')
        self.titleLabel.setObjectName("cardTitle")
        self.descLabel.setObjectName("cardDesc")

    def initAnimation(self):
        """ 初始化动画效果 """
        self.pressAnim = QPropertyAnimation(self, b"geometry")
        self.pressAnim.setDuration(120)
        self.pressAnim.setEasingCurve(QEasingCurve.OutQuad)

    def setSelected(self, selected: bool):
        """ 设置选中状态 """
        self.isSelected = selected
        self.setProperty('isSelected', 'true' if selected else 'false')
        self.style().polish(self)

        # 动态更新分隔线颜色
        lineColor = "#666666" if selected else "rgba(0, 0, 0, 0.1)"
        if isDarkTheme():
            lineColor = "#AAAAAA" if selected else "rgba(255, 255, 255, 0.1)"
        self.separator.setStyleSheet(f"background-color: {lineColor};")

        # 选中动画效果
        if selected:
            anim = QPropertyAnimation(self, b"geometry")
            anim.setDuration(200)
            anim.setEasingCurve(QEasingCurve.OutBack)
            anim.setStartValue(self.geometry())
            anim.setEndValue(self.geometry().adjusted(-2, -2, 2, 2))
            anim.start(QAbstractAnimation.DeleteWhenStopped)

    def mousePressEvent(self, event):
        """ 按压动画 """
        self.pressAnim.stop()
        self.pressAnim.setStartValue(self.geometry())
        self.pressAnim.setEndValue(self.geometry().adjusted(0, 2, 0, 2))
        self.pressAnim.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """ 释放事件处理 """
        self.pressAnim.setDirection(QPropertyAnimation.Backward)
        self.pressAnim.start()
        super().mouseReleaseEvent(event)
        self.clicked.emit()


class FolderInterface(QFrame):
    """ 主界面"""
    modelChanged = pyqtSignal(str)
    characterChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentModel = None
        self.currentCharacter = None

        # 初始化流程
        self.initUI()
        self.loadDemoData()

    def initUI(self):
        """ 主界面初始化 """
        self.setObjectName("FolderInterface")
        self.setMinimumSize(800, 600)

        # 主布局
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 40, 0, 0)    #左上右下
        mainLayout.setSpacing(0)

        # 滚动区域
        self.initScrollArea()
        # 样式
        self.initStyle()

    def initScrollArea(self):
        """ 初始化滚动区域 """
        self.scrollArea = ScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFrameShape(QFrame.NoFrame)

        # 流式布局
        self.flowLayout = FlowLayout(isTight=True, needAni=False)
        self.flowLayout.setContentsMargins(20, 20, 20, 20)
        self.flowLayout.setHorizontalSpacing(20)
        self.flowLayout.setVerticalSpacing(20)

        container = QWidget()
        container.setLayout(self.flowLayout)
        self.scrollArea.setWidget(container)

        self.layout().addWidget(self.scrollArea)





    def loadDemoData(self):
        """ 加载演示数据 """
        demoModels = [
            {'iconPath': 'resource/model/model1.png', 'title': '胡桃', 'description': '适合对话场景的可爱声线'},
            {'iconPath': 'resource/model/model2.png', 'title': '静静', 'description': '专业播音级质量声线'},
            {'iconPath': 'resource/model/model3.png', 'title': '晓晓', 'description': '适合有声读物的声线'},
            {'iconPath': 'resource/model/model4.png', 'title': '云溪', 'description': '营销号专用声线'},


        ]

        for model in demoModels:
            card = VoiceModelCard(**model)
            card.clicked.connect(lambda c=card: self.updateSelection(c))
            self.flowLayout.addWidget(card)

    def updateSelection(self, selectedCard):
        """ 更新选中状态并发射信号 """
        for i in range(self.flowLayout.count()):
            widget = self.flowLayout.itemAt(i).widget()
            if isinstance(widget, VoiceModelCard):
                # 更新选中状态，这里会调用 setSelected 方法
                is_selected = (widget is selectedCard)
                widget.setSelected(is_selected)

                # 如果是选中的卡片，更新当前角色
                if is_selected:
                    self.currentCharacter = widget.title

        # 发射当前选中的角色名称
        self.characterChanged.emit(self.currentCharacter)
        print(f"发射角色信号: {self.currentCharacter}")  # 调试用


    def initStyle(self):
        """ 初始化样式表 """
        self.setStyleSheet("""
        /* 基础样式 */
        VoiceModelCard {
            background-color: palette(base);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 12px;
        }
        VoiceModelCard[isSelected="true"] {
            border: 2px solid #666666;
            background-color: rgba(128, 128, 128, 0.1);
        }
        #cardTitle {
            font: 16px 'Microsoft YaHei';
            color: #333;
        }
        #cardDesc {
            font: 13px 'Microsoft YaHei';
            color: #666;
        }
        /* 暗色主题适配 */
        DarkTheme VoiceModelCard {
            border-color: rgba(255, 255, 255, 0.1);
            background-color: rgba(255, 255, 255, 0.05);
        }
        DarkTheme VoiceModelCard[isSelected="true"] {
            border-color: #AAAAAA;
            background-color: rgba(170, 170, 170, 0.1);
        }
        DarkTheme #cardTitle {
            color: #FFFFFF;
        }
        DarkTheme #cardDesc {
            color: #CCCCCC;
        }
        """)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = FolderInterface()
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec_())