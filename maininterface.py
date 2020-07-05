import sys
import qtawesome
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QStackedWidget, QWidget, QFileDialog, QMessageBox

from mythread import *


# 主窗体及UI
class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.process_bar1_value = 0
        self.train_key = False
        self.test_key = False
        self.separate_key = False
        self.init_ui()

        self.myTimer = myThreadTime()
        self.myTimer.update_date.connect(self.myClock)
        self.myTimer.start()

        self.spider_time = myThreadSpiderTime()
        self.spider_time.update_date.connect(self.mySpiderTime)

        self.spider_start_img_th = myThreadImg()
        self.spider_start_img_th.update_img.connect(self.spider_start_img)

        self.spider_ip_th = myThreadSpiderIP()
        self.spider_ip_th.update_str.connect(self.addAppToqtbIp)
        self.spider_ip_th.update_int.connect(self.addProcessBar)

        self.spiders_th = myThreadSpiders()
        self.spiders_th.update_str.connect(self.addAppToqtb)

        self.train_test_th = myThreadTrainTest()
        self.train_test_th.update_str.connect(self.addAppToqtbTrainTest)

        self.separate_th = myThreadSeparate()
        self.separate_th.update_str.connect(self.addAppToqtbSeparate)

        self.test_result_table_th = myThreadResultTable()
        self.test_result_graph_th = myThreadResultGraph()

        self.app_result_th = myThreadApplication()
        self.app_result_th.update_str.connect(self.addAppToqtbApplication)

        self.app_result_table_th = myThreadResultTable()
        self.app_result_graph_th = myThreadResultGraph()

        self.assistUI = assistUi()
        self.assistUI.update_data.connect(self.changeClass)

        print("初始化成功！")

    def init_ui(self):
        # 主窗口及布局
        self.setFixedSize(1000, 720)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.main_widget.setFixedSize(1000, 720);  # 禁止调整窗口大小

        # 左侧部件及布局
        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        # 右侧部件及布局
        self.right_stacked_Widget = QStackedWidget()
        self.right_stacked_Widget.setObjectName('right_stacked_Widget')

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 5)  # 左侧部件在第0行第0列，占12行5列
        self.main_layout.addWidget(self.right_stacked_Widget, 0, 6, 12, 15)  # 右侧部件在第0行第6列，占12行15列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        # 主窗口美化
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)  # 去除左侧部件和右侧部件中的缝隙

        # 左侧部件的组件布局
        # 1. 顶部三个按钮
        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_visit = QtWidgets.QPushButton("")  # 空白按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮
        self.left_close.clicked.connect(self.close)  # 关闭窗口
        self.left_mini.clicked.connect(self.showMinimized)  # 最小化窗口

        # 2. 左侧菜单栏选项(隐藏不使用的按钮)
        self.left_label_1 = QtWidgets.QPushButton("功能列表")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("系统设置")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("")
        self.left_label_3.setObjectName('left_label')

        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.cloud-download', color='white'), "代理IP更新")
        self.left_button_1.setObjectName('left_button')
        self.left_button_1.clicked.connect(self.left_button1_clicked)
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.download', color='white'), "数据爬取")
        self.left_button_2.setObjectName('left_button')
        self.left_button_2.clicked.connect(self.left_button2_clicked)
        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.line-chart', color='white'), "数据分析")
        self.left_button_3.setObjectName('left_button')
        self.left_button_3.clicked.connect(self.left_button3_clicked)
        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.user', color='white'), "实际应用")
        self.left_button_4.setObjectName('left_button')
        self.left_button_4.clicked.connect(self.left_button4_clicked)

        self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "敬请期待")
        self.left_button_5.setObjectName('left_button')
        # self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "期待")
        # self.left_button_6.setObjectName('left_button')
        # self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "")
        # self.left_button_6.setObjectName('left_button')

        self.left_button_7 = QtWidgets.QPushButton("电影评论情感分析系统")
        self.left_button_7.setObjectName('left_button')
        self.left_button_8 = QtWidgets.QPushButton("")
        self.left_button_8.setObjectName('left_button')
        self.left_button_9 = QtWidgets.QPushButton()
        self.left_button_9.setObjectName('left_button')

        self.left_xxx = QtWidgets.QPushButton(" ")

        # 禁用不展示的按钮, 按钮名称为空，然后设置按钮不可点击, 这样实现按钮占位，避免布局不协调
        # self.left_button_1.setDisabled(True)
        # self.left_button_2.setDisabled(True)
        # self.left_button_3.setDisabled(True)
        #
        # self.left_label_2.setDisabled(True)
        # self.left_button_4.setDisabled(True)
        self.left_button_5.setDisabled(True)
        # self.left_button_6.setDisabled(True)

        self.left_label_3.setDisabled(True)
        self.left_button_7.setDisabled(True)
        self.left_button_8.setDisabled(True)
        self.left_button_9.setDisabled(True)

        self.left_layout.addWidget(self.left_mini, 0, 4, 1, 1)
        self.left_layout.addWidget(self.left_visit, 0, 8, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 12, 1, 1)
        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 15)
        self.left_layout.addWidget(self.left_button_1, 2, 0, 1, 15)
        self.left_layout.addWidget(self.left_button_2, 3, 0, 1, 15)
        self.left_layout.addWidget(self.left_button_3, 4, 0, 1, 15)
        self.left_layout.addWidget(self.left_button_4, 5, 0, 1, 15)
        self.left_layout.addWidget(self.left_label_2, 6, 0, 1, 15)
        self.left_layout.addWidget(self.left_button_5, 7, 0, 1, 15)
        # self.left_layout.addWidget(self.left_button_6, 8, 0, 1, 15)
        self.left_layout.addWidget(self.left_label_3, 8, 0, 1, 15)
        self.left_layout.addWidget(self.left_button_7, 9, 0, 1, 15)
        self.left_layout.addWidget(self.left_button_8, 10, 0, 1, 15)
        self.left_layout.addWidget(self.left_button_9, 11, 0, 1, 15)

        # 左侧部件美化
        # 1. 左侧顶部三个按钮美化
        self.left_close.setFixedSize(20, 20)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(20, 20)  # 设置按钮大小
        self.left_mini.setFixedSize(20, 20)  # 设置最小化按钮大小
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        # 2. 左侧部件菜单美化及整体美化
        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid SteelBlue;
                font-size:20px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}

            QWidget#left_widget{
                background:SteelBlack;
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
            }
        ''')

        # 右侧边栏
        # 1. 数据爬取页面(form1)
        self.form1 = QWidget()
        self.right_stacked_Widget.addWidget(self.form1)
        self.formLayout1 = QtWidgets.QGridLayout(self.form1)

        # 1.1 标题
        self.right_label1_title = QtWidgets.QLabel("欢迎来到数据爬取页面")
        self.right_label1_title.setObjectName('right_label1')
        self.right_label1_title.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.formLayout1.addWidget(self.right_label1_title, 0, 0, 1, 15)

        # 1.2 搜索框
        self.right_search_input = QtWidgets.QLineEdit()
        self.right_search_input.setPlaceholderText("请输入要爬取的电影名称")
        self.right_search_input.setObjectName('right_input')

        self.right_button1_start = QtWidgets.QPushButton("开始爬取")
        self.right_button1_start.setObjectName('right_button')
        self.right_button1_start.clicked.connect(self.start_spider)  # 绑定槽函数
        self.right_button1_stop = QtWidgets.QPushButton("停止爬取")
        self.right_button1_stop.setObjectName('right_button')
        self.right_button1_stop.clicked.connect(self.stop_spider)
        self.right_button1_stop.setDisabled(True)
        self.right_button1_clear = QtWidgets.QPushButton("清空日志")
        self.right_button1_clear.setObjectName('right_button')
        self.right_button1_clear.clicked.connect(self.clearQtb1)

        self.formLayout1.addWidget(self.right_search_input, 1, 0, 1, 15)
        self.formLayout1.addWidget(self.right_button1_start, 2, 2, 1, 2)
        self.formLayout1.addWidget(self.right_button1_stop, 2, 6, 1, 2)
        self.formLayout1.addWidget(self.right_button1_clear, 2, 11, 1, 2)

        # 1.3 日志
        self.right_textbrower1 = QtWidgets.QTextBrowser(self)
        self.formLayout1.addWidget(self.right_textbrower1, 4, 0, 8, 15)

        # 1.4 爬取用时
        self.right_label_time = QtWidgets.QLabel("已用时: 0s")
        self.right_label_time.setObjectName('right_label2')
        self.right_label_time.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.formLayout1.addWidget(self.right_label_time, 12, 0, 1, 3)

        # 1.5 进度
        self.right_label_img = QtWidgets.QLabel()
        self.right_label_img.setPixmap(QtGui.QPixmap('./img/a0.jpg'))
        self.formLayout1.addWidget(self.right_label_img, 12, 13, 2, 2)

        # 2. 代理ip更新页面(form2)
        self.form2 = QWidget()
        self.right_stacked_Widget.addWidget(self.form2)
        self.formLayout2 = QtWidgets.QGridLayout(self.form2)

        # 2.1 标题
        self.right_label2_title = QtWidgets.QLabel("欢迎来到代理IP更新页面")
        self.right_label2_title.setObjectName('right_label1')
        self.right_label2_title.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.formLayout2.addWidget(self.right_label2_title, 0, 0, 1, 15)

        # 2.2 爬取按钮
        self.right_button2_start = QtWidgets.QPushButton("开始爬取")
        self.right_button2_start.setObjectName('right_button')
        self.right_button2_start.clicked.connect(self.start_spider_ip)  # 绑定槽函数
        self.right_button2_stop = QtWidgets.QPushButton("停止爬取")
        self.right_button2_stop.setObjectName('right_button')
        self.right_button2_stop.clicked.connect(self.stop_spider_ip)
        self.right_button2_stop.setDisabled(True)
        self.right_button2_clear = QtWidgets.QPushButton("清空日志")
        self.right_button2_clear.setObjectName('right_button')
        self.right_button2_clear.clicked.connect(self.clearQtb2)

        self.formLayout2.addWidget(self.right_button2_start, 2, 2, 1, 2)
        self.formLayout2.addWidget(self.right_button2_stop, 2, 6, 1, 2)
        self.formLayout2.addWidget(self.right_button2_clear, 2, 11, 1, 2)

        # 2.3 日志
        self.right_textbrower2 = QtWidgets.QTextBrowser(self)
        self.formLayout2.addWidget(self.right_textbrower2, 4, 0, 5, 15)

        # 2.4 进度条
        self.right_process_bar1 = QtWidgets.QProgressBar()
        self.right_process_bar1.setFixedHeight(15)  # 设置进度条高度
        self.right_process_bar1.setMaximum(100)
        # self.right_process_bar1.setTextVisible(False)  # 不显示进度条文字
        self.formLayout2.addWidget(self.right_process_bar1, 10, 0, 1, 15)

        # 2.5 添加代理ip
        self.right_add_input = QtWidgets.QLineEdit()
        self.right_add_input.setPlaceholderText("请输入要添加的代理ip，格式  *.*.*.*:*")
        self.right_add_input.setObjectName('right_input')
        self.right_button_add = QtWidgets.QPushButton("添加")
        self.right_button_add.setObjectName('right_button')
        self.right_button_add.clicked.connect(self.addIp)

        self.formLayout2.addWidget(self.right_add_input, 12, 0, 1, 8)
        self.formLayout2.addWidget(self.right_button_add, 12, 9, 1, 2)

        # 2.6删除代理ip
        self.right_delete_input = QtWidgets.QLineEdit()
        self.right_delete_input.setPlaceholderText("请输入要删除的代理ip，格式  *.*.*.*:*")
        self.right_delete_input.setObjectName('right_input')
        self.right_button_delete = QtWidgets.QPushButton("删除")
        self.right_button_delete.setObjectName('right_button')
        self.right_button_delete.clicked.connect(self.deleteIp)

        self.formLayout2.addWidget(self.right_delete_input, 14, 0, 1, 8)
        self.formLayout2.addWidget(self.right_button_delete, 14, 9, 1, 2)

        # 2.7查询代理ip
        self.right_button_check = QtWidgets.QPushButton("查询")
        self.right_button_check.setObjectName('right_button')
        self.right_button_check.clicked.connect(self.checkIp)
        self.formLayout2.addWidget(self.right_button_check, 12, 12, 1, 2)

        # 2.8清空代理ip
        self.right_button_clear = QtWidgets.QPushButton("清空")
        self.right_button_clear.setObjectName('right_button')
        self.right_button_clear.clicked.connect(self.clearIp)
        self.formLayout2.addWidget(self.right_button_clear, 14, 12, 1, 2)

        # 3 数据分析界面
        self.form3 = QWidget()
        self.right_stacked_Widget.addWidget(self.form3)
        self.formLayout3 = QtWidgets.QGridLayout(self.form3)

        # 3.1 标题
        self.right_label3_title = QtWidgets.QLabel("欢迎来到数据分析页面")
        self.right_label3_title.setObjectName('right_label1')
        self.right_label3_title.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.formLayout3.addWidget(self.right_label3_title, 0, 0, 1, 15)

        # 3.2 选择文件夹
        self.right_folder1_button = QtWidgets.QPushButton(qtawesome.icon('fa.folder', color='GoldenRod'), "")
        self.right_folder1_button.setFont(qtawesome.font('fa', 16))
        self.right_folder1_button.setObjectName("right_folder_button")
        self.right_folder1_button.clicked.connect(self.right_folder1_button_clicked)
        self.right_folder1_button.setFixedSize(30, 30)  # 设置按钮大小

        self.right_folder1_input = QtWidgets.QLineEdit()
        self.right_folder1_input.setPlaceholderText("请选择带有训练数据的文件夹")
        self.right_folder1_input.setObjectName("right_input")

        self.right_folder_check = QtWidgets.QPushButton("开始载入")
        self.right_folder_check.setObjectName("right_button")
        self.right_folder_check.clicked.connect(self.folderCheck)

        self.right_folder_separate = QtWidgets.QPushButton("数据分离")
        self.right_folder_separate.setObjectName("right_button")
        self.right_folder_separate.clicked.connect(self.folderSeparate)

        self.formLayout3.addWidget(self.right_folder1_button, 1, 0, 1, 1)
        self.formLayout3.addWidget(self.right_folder1_input, 1, 1, 1, 7)
        self.formLayout3.addWidget(self.right_folder_check, 1, 8, 1, 3)
        self.formLayout3.addWidget(self.right_folder_separate, 1, 11, 1, 3)

        # 3.4 训练相关
        self.right_name_label = QtWidgets.QLabel("分类器名称:")
        self.right_name_input = QtWidgets.QLineEdit()
        self.right_name_input.setPlaceholderText("请输入")
        self.right_name_input.setObjectName('right_input')
        self.formLayout3.addWidget(self.right_name_label, 2, 0, 1, 3)
        self.formLayout3.addWidget(self.right_name_input, 2, 3, 1, 3)

        # tip
        self.right_folder_tip = QtWidgets.QLabel("Tip:")
        self.right_folder_tip.setObjectName("right_label3")
        self.formLayout3.addWidget(self.right_folder_tip, 2, 7, 1, 6)

        self.right_posNum_label = QtWidgets.QLabel("积极评论样本数:")
        self.right_posNum_input = QtWidgets.QLineEdit()
        self.right_posNum_input.setPlaceholderText("请输入")
        self.right_posNum_input.setObjectName('right_input')

        self.right_negNum_label = QtWidgets.QLabel("消极评论样本数:")
        self.right_negNum_input = QtWidgets.QLineEdit()
        self.right_negNum_input.setPlaceholderText("请输入")
        self.right_negNum_input.setObjectName('right_input')

        self.formLayout3.addWidget(self.right_posNum_label, 3, 0, 1, 3)
        self.formLayout3.addWidget(self.right_posNum_input, 3, 3, 1, 3)
        self.formLayout3.addWidget(self.right_negNum_label, 3, 7, 1, 3)
        self.formLayout3.addWidget(self.right_negNum_input, 3, 10, 1, 3)

        self.right_bigram_label = QtWidgets.QLabel("双词数目:")
        self.right_bigram_input = QtWidgets.QLineEdit()
        self.right_bigram_input.setPlaceholderText("请输入    默认3000")
        self.right_bigram_input.setObjectName('right_input')

        self.right_feature_label = QtWidgets.QLabel("特征维度:")
        self.right_feature_input = QtWidgets.QLineEdit()
        self.right_feature_input.setPlaceholderText("请输入    默认2000")
        self.right_feature_input.setObjectName('right_input')

        self.formLayout3.addWidget(self.right_bigram_label, 4, 0, 1, 3)
        self.formLayout3.addWidget(self.right_bigram_input, 4, 3, 1, 3)
        self.formLayout3.addWidget(self.right_feature_label, 4, 7, 1, 3)
        self.formLayout3.addWidget(self.right_feature_input, 4, 10, 1, 3)

        self.right_class_button = QtWidgets.QPushButton("请选择分类方法:")
        self.right_class_button.setObjectName("right_button")
        self.right_class_button.clicked.connect(self.assistUiShow)
        self.right_class_label = QtWidgets.QLabel("BernoulliNB")
        # self.right_class_input = QtWidgets.QLineEdit()
        # self.right_class_input.setPlaceholderText("请输入    默认1000")
        # self.right_class_input.setObjectName('right_input')
        self.formLayout3.addWidget(self.right_class_button, 5, 0, 1, 4)
        self.formLayout3.addWidget(self.right_class_label, 5, 4, 1, 4)

        self.right_train_start = QtWidgets.QPushButton("开始训练")
        self.right_train_start.setObjectName("right_button")
        self.right_train_start.clicked.connect(self.start_train)
        self.right_train_stop = QtWidgets.QPushButton("停止训练")
        self.right_train_stop.setObjectName("right_button")
        self.right_train_stop.clicked.connect(self.stop_train)
        self.right_train_stop.setDisabled(True)
        self.formLayout3.addWidget(self.right_train_start, 6, 4, 1, 2)
        self.formLayout3.addWidget(self.right_train_stop, 6, 7, 1, 3)

        self.right_test_graph = QtWidgets.QPushButton("查看结果图像")
        self.right_test_graph.setObjectName("right_button")
        self.right_test_graph.clicked.connect(self.testGraph)
        self.right_test_graph.setDisabled(True)

        self.formLayout3.addWidget(self.right_test_graph, 6, 11, 1, 3)

        # 3.5 测试相关
        self.right_folder2_button = QtWidgets.QPushButton(qtawesome.icon('fa.folder', color='GoldenRod'), "")
        self.right_folder2_button.setFont(qtawesome.font('fa', 16))
        self.right_folder2_button.setObjectName("right_folder_button")
        self.right_folder2_button.clicked.connect(self.right_folder2_button_clicked)
        self.right_folder2_button.setFixedSize(30, 30)  # 设置按钮大小

        self.right_folder2_input = QtWidgets.QLineEdit()
        self.right_folder2_input.setPlaceholderText("请选择要测试的评论数据")
        self.right_folder2_input.setObjectName("right_input")
        self.formLayout3.addWidget(self.right_folder2_button, 7, 0, 1, 1)
        self.formLayout3.addWidget(self.right_folder2_input, 7, 1, 1, 7)

        self.right_folder3_button = QtWidgets.QPushButton(qtawesome.icon('fa.folder', color='GoldenRod'), "")
        self.right_folder3_button.setFont(qtawesome.font('fa', 16))
        self.right_folder3_button.setObjectName("right_folder_button")
        self.right_folder3_button.clicked.connect(self.right_folder3_button_clicked)
        self.right_folder3_button.setFixedSize(30, 30)  # 设置按钮大小

        self.right_folder3_input = QtWidgets.QLineEdit()
        self.right_folder3_input.setPlaceholderText("请选择分类器")
        self.right_folder3_input.setObjectName("right_input")
        self.formLayout3.addWidget(self.right_folder3_button, 7, 8, 1, 1)
        self.formLayout3.addWidget(self.right_folder3_input, 7, 9, 1, 5)

        self.right_button3_clear = QtWidgets.QPushButton("清空日志")
        self.right_button3_clear.setObjectName('right_button')
        self.right_button3_clear.clicked.connect(self.clearQtb3)
        self.right_test_start = QtWidgets.QPushButton("开始测试")
        self.right_test_start.setObjectName("right_button")
        self.right_test_start.clicked.connect(self.start_test)
        self.right_test_stop = QtWidgets.QPushButton("停止测试")
        self.right_test_stop.setObjectName("right_button")
        self.right_test_stop.clicked.connect(self.stop_test)
        self.right_test_stop.setDisabled(True)
        self.right_test_result = QtWidgets.QPushButton("查看具体结果")
        self.right_test_result.setObjectName("right_button")
        self.right_test_result.clicked.connect(self.testResult)
        self.right_test_result.setDisabled(True)
        self.formLayout3.addWidget(self.right_button3_clear, 8, 0, 1, 3)
        self.formLayout3.addWidget(self.right_test_start, 8, 4, 1, 2)
        self.formLayout3.addWidget(self.right_test_stop, 8, 7, 1, 3)
        self.formLayout3.addWidget(self.right_test_result, 8, 11, 1, 3)

        # 3.6 日志
        self.right_textbrower3 = QtWidgets.QTextBrowser(self)
        self.formLayout3.addWidget(self.right_textbrower3, 9, 0, 4, 15)

        # 4
        self.form4 = QWidget()
        self.right_stacked_Widget.addWidget(self.form4)
        self.formLayout4 = QtWidgets.QGridLayout(self.form4)

        self.right_label4_title = QtWidgets.QLabel("欢迎来到数据分离页面")
        self.right_label4_title.setObjectName('right_label1')
        self.right_label4_title.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.formLayout4.addWidget(self.right_label4_title, 0, 0, 1, 15)

        # 4.1 选择文件夹
        self.right_folder4_button = QtWidgets.QPushButton(qtawesome.icon('fa.folder', color='GoldenRod'), "")
        self.right_folder4_button.setFont(qtawesome.font('fa', 16))
        self.right_folder4_button.setObjectName("right_folder_button")
        self.right_folder4_button.clicked.connect(self.right_folder4_button_clicked)
        self.right_folder4_button.setFixedSize(30, 30)  # 设置按钮大小

        self.right_folder4_input = QtWidgets.QLineEdit()
        self.right_folder4_input.setPlaceholderText("请选择带有分离数据的文件夹")
        self.right_folder4_input.setObjectName("right_input")

        self.formLayout4.addWidget(self.right_folder4_button, 1, 0, 1, 1)
        self.formLayout4.addWidget(self.right_folder4_input, 1, 1, 1, 14)

        # tip
        self.right_folder4_tip = QtWidgets.QLabel("Tip:")
        self.right_folder4_tip.setObjectName("right_label3")
        self.formLayout4.addWidget(self.right_folder4_tip, 2, 0, 1, 10)

        self.right_folder4_check = QtWidgets.QPushButton("开始检测")
        self.right_folder4_check.setObjectName("right_button")
        self.right_folder4_check.clicked.connect(self.folderCheck_2)
        self.formLayout4.addWidget(self.right_folder4_check, 2, 11, 1, 4)

        self.right_trainPosNum_label = QtWidgets.QLabel("积极评论训练数目:")
        self.right_trainPosNum_input = QtWidgets.QLineEdit()
        self.right_trainPosNum_input.setPlaceholderText("请输入")
        self.right_trainPosNum_input.setObjectName('right_input')

        self.right_trainNegNum_label = QtWidgets.QLabel("消极评论训练数目:")
        self.right_trainNegNum_input = QtWidgets.QLineEdit()
        self.right_trainNegNum_input.setPlaceholderText("请输入")
        self.right_trainNegNum_input.setObjectName('right_input')

        self.formLayout4.addWidget(self.right_trainPosNum_label, 3, 0, 1, 4)
        self.formLayout4.addWidget(self.right_trainPosNum_input, 3, 4, 1, 3)
        self.formLayout4.addWidget(self.right_trainNegNum_label, 3, 8, 1, 3)
        self.formLayout4.addWidget(self.right_trainNegNum_input, 3, 11, 1, 3)

        self.right_testPosNum_label = QtWidgets.QLabel("积极评论测试数目:")
        self.right_testPosNum_input = QtWidgets.QLineEdit()
        self.right_testPosNum_input.setPlaceholderText("请输入")
        self.right_testPosNum_input.setObjectName('right_input')

        self.right_testNegNum_label = QtWidgets.QLabel("消极评论测试数目:")
        self.right_testNegNum_input = QtWidgets.QLineEdit()
        self.right_testNegNum_input.setPlaceholderText("请输入")
        self.right_testNegNum_input.setObjectName('right_input')

        self.formLayout4.addWidget(self.right_testPosNum_label, 4, 0, 1, 4)
        self.formLayout4.addWidget(self.right_testPosNum_input, 4, 4, 1, 3)
        self.formLayout4.addWidget(self.right_testNegNum_label, 4, 8, 1, 3)
        self.formLayout4.addWidget(self.right_testNegNum_input, 4, 11, 1, 3)

        self.right_button3_clear = QtWidgets.QPushButton("清空日志")
        self.right_button3_clear.setObjectName('right_button')
        self.right_button3_clear.clicked.connect(self.clearQtb4)
        self.formLayout4.addWidget(self.right_button3_clear, 5, 0, 1, 3)

        self.right_separate_start = QtWidgets.QPushButton("开始分离")
        self.right_separate_start.setObjectName("right_button")
        self.right_separate_start.clicked.connect(self.start_separate)
        self.formLayout4.addWidget(self.right_separate_start, 5, 4, 1, 3)

        self.right_return = QtWidgets.QPushButton("返回数据分析页面")
        self.right_return.setObjectName("right_button")
        self.right_return.clicked.connect(self.myReturn)
        self.formLayout4.addWidget(self.right_return, 5, 11, 1, 4)

        self.right_textbrower4 = QtWidgets.QTextBrowser(self)
        self.formLayout4.addWidget(self.right_textbrower4, 6, 0, 6, 15)

        # 5
        self.form5 = QWidget()
        self.right_stacked_Widget.addWidget(self.form5)
        self.formLayout5 = QtWidgets.QGridLayout(self.form5)

        self.right_label5_title = QtWidgets.QLabel("欢迎来到实际应用页面")
        self.right_label5_title.setObjectName('right_label1')
        self.right_label5_title.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.formLayout5.addWidget(self.right_label5_title, 0, 0, 1, 15)

        self.right_folder5_button = QtWidgets.QPushButton(qtawesome.icon('fa.folder', color='GoldenRod'), "")
        self.right_folder5_button.setFont(qtawesome.font('fa', 16))
        self.right_folder5_button.setObjectName("right_folder_button")
        self.right_folder5_button.clicked.connect(self.right_folder5_button_clicked)
        self.right_folder5_button.setFixedSize(30, 30)
        
        self.right_folder5_input = QtWidgets.QLineEdit()
        self.right_folder5_input.setPlaceholderText("请选择要测试的评论数据")
        self.right_folder5_input.setObjectName("right_input")
        self.formLayout5.addWidget(self.right_folder5_button, 1, 0, 1, 1)
        self.formLayout5.addWidget(self.right_folder5_input, 1, 1, 1, 8)

        self.right_folder6_button = QtWidgets.QPushButton(qtawesome.icon('fa.folder', color='GoldenRod'), "")
        self.right_folder6_button.setFont(qtawesome.font('fa', 16))
        self.right_folder6_button.setObjectName("right_folder_button")
        self.right_folder6_button.clicked.connect(self.right_folder6_button_clicked)
        self.right_folder6_button.setFixedSize(30, 30)  # 设置按钮大小

        self.right_folder6_input = QtWidgets.QLineEdit()
        self.right_folder6_input.setPlaceholderText("请选择分类器")
        self.right_folder6_input.setObjectName("right_input")
        self.formLayout5.addWidget(self.right_folder6_button, 1, 9, 1, 1)
        self.formLayout5.addWidget(self.right_folder6_input, 1, 10, 1, 5)
        
        self.right_ana_start = QtWidgets.QPushButton("开始分类")
        self.right_ana_start.setObjectName('right_button')
        self.right_ana_start.clicked.connect(self.start_ana)

        self.right_ana_stop = QtWidgets.QPushButton("停止分类")
        self.right_ana_stop.setObjectName('right_button')
        self.right_ana_stop.setDisabled(True)
        self.right_ana_stop.clicked.connect(self.stop_ana)
        self.formLayout5.addWidget(self.right_ana_start, 2, 4, 1, 3)
        self.formLayout5.addWidget(self.right_ana_stop, 2, 8, 1, 3)

        self.right_button4_clear = QtWidgets.QPushButton("清空日志")
        self.right_button4_clear.setObjectName('right_button')
        self.right_button4_clear.clicked.connect(self.clearQtb5)

        self.right_button_checkPos = QtWidgets.QPushButton("查看积极评论")
        self.right_button_checkPos.setObjectName('right_button')
        self.right_button_checkPos.setDisabled(True)
        self.right_button_checkPos.clicked.connect(self.appResultPos)

        self.right_button_checkNeg = QtWidgets.QPushButton("查看消极评论")
        self.right_button_checkNeg.setObjectName('right_button')
        self.right_button_checkNeg.setDisabled(True)
        self.right_button_checkNeg.clicked.connect(self.appResultNeg)

        self.right_button_result = QtWidgets.QPushButton("查看结果图像")
        self.right_button_result.setObjectName('right_button')
        self.right_button_result.setDisabled(True)
        self.right_button_result.clicked.connect(self.appGraph)
        self.formLayout5.addWidget(self.right_button4_clear, 3, 0, 1, 3)
        self.formLayout5.addWidget(self.right_button_checkPos, 3, 4, 1, 3)
        self.formLayout5.addWidget(self.right_button_checkNeg, 3, 8, 1, 3)
        self.formLayout5.addWidget(self.right_button_result, 3, 12, 1, 3)

        self.right_textbrower5 = QtWidgets.QTextBrowser(self)
        self.formLayout5.addWidget(self.right_textbrower5, 4, 0, 6, 15)

        # 右边栏美化
        # 右边框整体风格美化
        self.right_stacked_Widget.setStyleSheet('''
            QStackedWidget#right_stacked_Widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }

            QLabel#right_label1{
                font:20pt '楷体';
                border-width: 1px;
                border-style: solid;
                border-color: rgb(10, 10, 10);
                border-radius:10px;
                font-size:20px;
                color: rgb(0, 0, 200);
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QLabel#right_label2{
                font:20pt '楷体';
                font-size:18px;
                color: rgb(200, 0, 0);
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QLabel#right_label3{
                font:20pt '楷体';
                font-size:16px;
                color: rgb(200, 0, 0);
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            
            QPushButton#right_button{
                background-color:rgba(240,240,240,180);
                color:#555555;
                border-radius:10px;
                padding:12px 14px
            }
            QPushButton#right_button:hover{
                background-color:rgba(170,170,170,180);
                color:#555555;
                border-radius:10px;
                padding:12px 14px
            }
            QLineEdit#right_input{
                    border:1px solid gray;
                    width:300px;
                    border-radius:10px;
                    padding:2px 4px;
            }
            QComboBox#right_combobox{
                background-color: white;
                font-size:16px;
                font-weight:500;
                border-radius:10px;
                padding:2px 4px;
                border:1px solid gray;             
            }
            QPushButton#right_folder_button{
                border-radius:5px;
                font-size:16px;
                font-weight:300;
            }     
            QPushButton#right_folder_button:hover{background-color: GoldenRod;}
        ''')

    def myClock(self, myT):
        self.left_button_8.setText(myT)

    def mySpiderTime(self, myTS):
        self.right_label_time.setText("已用时: " + myTS)

    def spider_start_img(self, num):
        self.right_label_img.setPixmap(QtGui.QPixmap('./img/a' + num[0] + '.jpg'))

    # 1. left_button1, 面板选取, 选择页面2
    def left_button1_clicked(self):
        self.right_stacked_Widget.setCurrentIndex(1)

    def left_button2_clicked(self):
        self.right_stacked_Widget.setCurrentIndex(0)

    def left_button3_clicked(self):
        self.right_stacked_Widget.setCurrentIndex(2)

    def left_button4_clicked(self):
        self.right_stacked_Widget.setCurrentIndex(4)

    def folderSeparate(self):
        self.right_stacked_Widget.setCurrentIndex(3)

    def myReturn(self):
        self.right_stacked_Widget.setCurrentIndex(2)

    def appToqtb(self, s, key):
        t = time.localtime(int(time.time()))
        if key == 1:
            self.right_textbrower1.append(time.strftime("%Y-%m-%d %H:%M:%S  ", t) + s)  # 文本框逐条添加数据
            self.right_textbrower1.moveCursor(self.right_textbrower1.textCursor().End)  # 文本框显示到底部
        elif key == 2:
            self.right_textbrower2.append(time.strftime("%Y-%m-%d %H:%M:%S  ", t) + s)
            self.right_textbrower2.moveCursor(self.right_textbrower2.textCursor().End)
        elif key == 3:
            self.right_textbrower3.append(time.strftime("%Y-%m-%d %H:%M:%S  ", t) + s)
            self.right_textbrower3.moveCursor(self.right_textbrower3.textCursor().End)
        elif key == 4:
            self.right_textbrower4.append(time.strftime("%Y-%m-%d %H:%M:%S  ", t) + s)
            self.right_textbrower4.moveCursor(self.right_textbrower4.textCursor().End)
        elif key == 5:
            self.right_textbrower5.append(time.strftime("%Y-%m-%d %H:%M:%S  ", t) + s)
            self.right_textbrower5.moveCursor(self.right_textbrower5.textCursor().End)
        # time.sleep(1)

    # def wordAnalysis(self):
    #     self.appToqtb('开始进行词云分析......')
    #     f = open('SenAnaSystem/json/comment_long.json', 'r', encoding='utf-8')
    #     content = f.read()
    #     f.close()
    #     ls = jieba.lcut(content)
    #     txt = ' '.join(ls)
    #     w = wordcloud.WordCloud(font_path='msyh.ttc', width=1000, height=700, background_color='white')
    #     w.generate(txt)
    #     w.to_file('./SenAnaSystem/png/comment_long.png')
    #     self.appToqtb('词云分析完成！')

    # def changeProxyIp(self, ip):
    #     if self.proxy_key != 0:
    #         self.nextIp = ip
    #         if self.nextIp != self.nowIp:
    #             self.appToqtb("目前使用的代理ip为: " + self.nextIp, 1)
    #             self.nowIp = self.nextIp
    #     else:
    #         self.nowIp = ip
    #         self.proxy_key = 1

    def spider_total(self):
        short = 0
        long = 0
        moviename = self.right_search_input.text()
        f = open("./SenAnaSystem/json/" + moviename + "/comment_short_neg.json", "r",
                 encoding="utf-8")
        shortNegStr = f.read().strip()
        f.close()
        # time.sleep(0.5)
        f = open("./SenAnaSystem/json/" + moviename + "/comment_short_pos.json", "r",
                 encoding="utf-8")
        shortPosStr = f.read().strip()
        f.close()
        # time.sleep(0.5)
        f = open("./SenAnaSystem/json/" + moviename + "/comment_long_neg.json", "r",
                 encoding="utf-8")
        longNegStr = f.read().strip()
        f.close()
        # time.sleep(0.5)
        f = open("./SenAnaSystem/json/" + moviename + "/comment_long_pos.json", "r",
                 encoding="utf-8")
        longPosStr = f.read().strip()
        f.close()
        # time.sleep(0.5)

        short = len(shortNegStr.split("\n")) + len(shortPosStr.split("\n"))
        long = len(longNegStr.split("\n")) + len(longPosStr.split("\n"))

        f = open("./SenAnaSystem/json/" + moviename + "/comment_short_neg.json", "w",
                 encoding="utf-8")
        f.write("[" + shortNegStr[:-1] + "]")
        f.close()
        # time.sleep(0.5)
        f = open("./SenAnaSystem/json/" + moviename + "/comment_short_pos.json", "w",
                 encoding="utf-8")
        f.write("[" + shortPosStr[:-1] + "]")
        f.close()
        # time.sleep(0.5)
        f = open("./SenAnaSystem/json/" + moviename + "/comment_long_neg.json", "w",
                 encoding="utf-8")
        f.write("[" + longNegStr[:-1] + "]")
        f.close()
        # time.sleep(0.5)
        f = open("./SenAnaSystem/json/" + moviename + "/comment_long_pos.json", "w",
                 encoding="utf-8")
        f.write("[" + longPosStr[:-1] + "]")
        f.close()
        # time.sleep(0.5)

        return "共爬取 短评" + str(short) + "条, 长评" + str(long) + "条"

    def stop_spider_per(self):
        self.left_button_1.setDisabled(False)
        self.spider_start_img_th.alive = False
        self.spider_start_img_th.quit()
        self.spider_start_img_th.wait()
        self.spider_time.alive = False
        self.spider_time.num = 0
        self.spider_time.quit()
        self.spider_time.wait()
        self.right_button1_start.setDisabled(False)
        self.right_button1_stop.setDisabled(True)
        self.spiders_th.alive = False
        self.spiders_th.quit()
        self.spiders_th.wait()

    def addAppToqtb(self, str):
        if str != "error":
            if str != "success":
                self.appToqtb(str, 1)
            else:
                self.stop_spider_per()
                self.total = self.spider_total()
                self.appToqtb(self.total, 1)
        else:
            self.appToqtb("找不到该电影或者ip异常，请重新输入或者更换ip！", 1)
            self.stop_spider_per()

    # 开始爬取
    def start_spider(self):
        # print(threading.active_count())
        if self.right_search_input.text() == "":
            reply = QMessageBox.information(self, "提示", "请输入要爬取的电影名称", QMessageBox.Ok)
        else:
            self.left_button_1.setDisabled(True)
            self.appToqtb('开始进行评论爬取......', 1)
            self.appToqtb('正在获取电影id......请耐心等待', 1)
            self.spider_time.alive = True
            self.spider_time.start()
            self.spider_start_img_th.alive = True
            self.spider_start_img_th.start()
            self.right_button1_start.setDisabled(True)
            self.right_button1_stop.setDisabled(False)

            self.spiders_th.setMovieName(self.right_search_input.text())
            self.spiders_th.alive = True
            self.spiders_th.start()

    def stop_spider(self):
        self.appToqtb("正在停止，请耐心等待.....", 1)
        self.stop_spider_per()
        self.appToqtb("已停止", 1)

    def clearQtb1(self):
        self.right_textbrower1.clear()

    def clearQtb2(self):
        self.right_textbrower2.clear()

    def clearQtb3(self):
        self.right_textbrower3.clear()

    def clearQtb4(self):
        self.right_textbrower4.clear()

    def clearQtb5(self):
        self.right_textbrower5.clear()

    def addAppToqtbIp(self, str):
        self.appToqtb(str, 2)
        # self.text.append(str)

    def stop_spider_ip_per(self):
        self.left_button_2.setDisabled(False)
        self.right_button2_start.setDisabled(False)
        self.right_button2_stop.setDisabled(True)
        self.spider_ip_th.alive = False
        # time.sleep(0.5)
        # self.spider_ip_th.quit()
        # self.spider_ip_th.wait()

    def addProcessBar(self, num):
        self.right_process_bar1.setValue(num)
        if num == 100:
            self.stop_spider_ip_per()

    def start_spider_ip(self):
        self.left_button_2.setDisabled(True)
        self.right_button2_start.setDisabled(True)
        self.right_button2_stop.setDisabled(False)
        self.spider_ip_th.start()
        self.spider_ip_th.alive = True

    def stop_spider_ip(self):
        self.appToqtb("正在停止，请耐心等待.....", 2)
        self.stop_spider_ip_per()
        self.appToqtb("已停止", 2)

    def myMessageBox(self, title, text):
        messageBox = QMessageBox()
        messageBox.setWindowTitle(title)
        messageBox.setText(text)
        messageBox.setStandardButtons(QMessageBox.Yes)
        buttonY = messageBox.button(QMessageBox.Yes)
        buttonY.setText('确定')
        messageBox.exec_()

    def addIp(self):
        input = self.right_add_input.text()
        if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
                    r":[0-9]{1,5}$", input):
            f = open("./SenAnaSystem/json/ip.json", "r", encoding="utf-8")
            hadIp = json.loads(f.read())
            f.close()
            hadKey = False
            httpsInput = "https://" + input

            for i in range(len(hadIp)):
                if hadIp[i]["ip"] == httpsInput:
                    hadKey = True
            if hadKey:
                self.myMessageBox("警告", "输入的ip已存在，请重新输入！")
            else:
                hadIp.append("{'ip':" + "'" + httpsInput + "'}")
                f = open("./SenAnaSystem/json/ip.json", "w", encoding="utf-8")
                f.write(str(hadIp).replace('"', "").replace("'", '"'))
                f.close()
                self.appToqtb("添加一个代理ip: " + input, 2)
                self.myMessageBox("提示", "ip已添加")

        else:
            self.myMessageBox("警告", "输入的ip有误，请重新输入！")

        self.right_add_input.setText("")

    def deleteIp(self):
        input = self.right_delete_input.text()
        if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
                    r":[0-9]{1,5}$", input):
            f = open("./SenAnaSystem/json/ip.json", "r", encoding="utf-8")
            hadIp = json.loads(f.read())
            f.close()
            hadKey = False
            httpsInput = "https://" + input
            hadIpNow = []
            for i in range(len(hadIp)):
                if hadIp[i]["ip"] == httpsInput:
                    hadKey = True
                    continue
                hadIpNow.append(hadIp[i])

            f = open("./SenAnaSystem/json/ip.json", "w", encoding="utf-8")
            f.write(str(hadIpNow).replace('"', "").replace("'", '"'))
            f.close()
            if hadKey:
                self.appToqtb("删除一个代理ip:" + input, 2)
                self.myMessageBox("提示", "ip已删除")
            else:
                self.myMessageBox("警告", "要删除的ip不存在，请重新输入！")

        else:
            self.myMessageBox("警告", "输入的ip有误，请重新输入！")

        self.right_delete_input.setText("")

    def checkIp(self):
        f = open("./SenAnaSystem/json/ip.json", "r", encoding="utf-8")
        hadIp = json.loads(f.read())
        f.close()
        if len(hadIp) > 0:
            self.appToqtb("已拥有的代理ip如下", 2)
            for i in range(len(hadIp)):
                self.appToqtb(hadIp[i]["ip"], 2)
        else:
            self.appToqtb("没有代理ip", 2)

    def clearIp(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("提示")
        messageBox.setText("确定要清空所有代理ip？")
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = messageBox.button(QMessageBox.Yes)
        buttonY.setText('确定')
        buttonN = messageBox.button(QMessageBox.No)
        buttonN.setText('取消')
        messageBox.exec_()
        if messageBox.clickedButton() == buttonY:
            f = open("./SenAnaSystem/json/ip.json", "w", encoding="utf-8")
            f.write("[]")
            f.close()
            self.appToqtb("代理ip被清空", 2)

    # 选择文件
    def right_folder1_button_clicked(self):
        try:
            dir_choose = QFileDialog.getExistingDirectory(self, "选取文件夹", "./train")  # 起始路径
            if dir_choose == "":
                self.myMessageBox("提示", "未选择任何文件夹!")
                return
            if os.path.isdir(dir_choose):
                for filename in os.listdir(dir_choose):
                    if filename.endswith('.pkl'):
                        self.right_folder1_input.setText(dir_choose)
                        self.train_test_th.folder = dir_choose
                        self.right_folder_check.setDisabled(False)
                        return
                    self.myMessageBox("提示", "所选文件夹中没有pkl数据, 请重新选择!")
                    return
        except:
            self.myMessageBox("提示", "所选文件夹中没有pkl数据, 请重新选择!")
            return

    def right_folder2_button_clicked(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./test", "Text Files (*.pkl)")
        if fileName == "":
            self.myMessageBox("提示", "未选择任何数据!")
        else:
            self.right_folder2_input.setText(fileName)

        return

    def right_folder3_button_clicked(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./classifiers", "Text Files (*.pkl)")
        if fileName == "":
            self.myMessageBox("提示", "未选择分类器!")
        else:
            self.right_folder3_input.setText(fileName)

        return

    def right_folder4_button_clicked(self):
        try:
            dir_choose = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")  # 起始路径
            if dir_choose == "":
                self.myMessageBox("提示", "未选择任何文件夹!")
                return
            if os.path.isdir(dir_choose):
                for filename in os.listdir(dir_choose):
                    if filename.endswith('.json'):  # \
                        # and filename != "ip.json" \
                        # and filename != "movie_id.json" \
                        # and filename != "movie_name.json":
                        self.right_folder4_input.setText(dir_choose)
                        self.separate_th.folder = dir_choose
                        self.separate_th.movie_list = [""]
                        self.right_folder4_check.setDisabled(False)
                        return
                    else:
                        if os.path.isdir(dir_choose + "/" + filename):
                            for filename2 in os.listdir(dir_choose + "/" + filename):
                                if filename2.endswith('.json'):
                                    self.right_folder4_input.setText(dir_choose)
                                    self.separate_th.folder = dir_choose + "/"
                                    self.separate_th.movie_list = []
                                    for filename in os.listdir(dir_choose):
                                        self.separate_th.movie_list.append(filename)
                                    self.right_folder4_check.setDisabled(False)
                                    return
                                self.myMessageBox("提示", "所选文件夹中没有json数据, 请重新选择!")
                                return
                    self.myMessageBox("提示", "所选文件夹中没有json数据, 请重新选择!")
                    return
        except:
            self.myMessageBox("提示", "所选文件夹中没有json数据, 请重新选择!")
            return

    def right_folder5_button_clicked(self):
        try:
            dir_choose = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")  # 起始路径
            if dir_choose == "":
                self.myMessageBox("提示", "未选择任何文件夹!")
                return
            if os.path.isdir(dir_choose):
                for filename in os.listdir(dir_choose):
                    if filename.endswith('.json'):
                        self.right_folder5_input.setText(dir_choose)
                        self.app_result_th.folder = dir_choose
                        self.app_result_th.movie_list = [""]
                        return
                    else:
                        if os.path.isdir(dir_choose + "/" + filename):
                            for filename2 in os.listdir(dir_choose + "/" + filename):
                                if filename2.endswith('.json'):
                                    self.right_folder5_input.setText(dir_choose)
                                    self.app_result_th.folder = dir_choose + "/"
                                    self.app_result_th.movie_list = []
                                    for filename in os.listdir(dir_choose):
                                        self.app_result_th.movie_list.append(filename)
                                    return
                                self.myMessageBox("提示", "所选文件夹中没有json数据, 请重新选择!")
                                return
                    self.myMessageBox("提示", "所选文件夹中没有json数据, 请重新选择!")
                    return
        except:
            self.myMessageBox("提示", "所选文件夹中没有json数据, 请重新选择!")
            return

    def right_folder6_button_clicked(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./classifiers", "Text Files (*.pkl)")
        if fileName == "":
            self.myMessageBox("提示", "未选择分类器!")
        else:
            self.right_folder6_input.setText(fileName)
            self.app_result_th.file = fileName

        return

    def addAppToqtbApplication(self, s):
        if s[:3] != "end":
            if s.split("&")[0] == "result":
                self.app_result_graph_th.name = s.split("&")[1]
                self.app_result_table_th.name = s.split("&")[1]
            else:
                self.appToqtb(s, 5)
        else:
            self.app_result_th.alive = False
            self.app_result_th.key = -1
            self.app_result_th.quit()
            self.app_result_th.wait()
            self.right_ana_start.setDisabled(False)
            self.right_ana_stop.setDisabled(True)
            self.right_button_checkPos.setDisabled(False)
            self.right_button_checkNeg.setDisabled(False)
            self.right_button_result.setDisabled(False)

    def start_ana(self):
        if self.right_folder5_input.text() != "" and self.right_folder6_input.text() != "":
            self.test_key = True

        if self.test_key:
            self.appToqtb("开始进行影评数据转换......请耐心等待", 5)
            self.app_result_th.file = self.right_folder6_input.text()
            self.right_ana_start.setDisabled(True)
            self.right_ana_stop.setDisabled(False)
            self.test_key = False
            if self.app_result_th.key == -1:
                self.app_result_th.key = 1
                self.app_result_th.alive = True
                self.app_result_th.start()
            else:
                self.app_result_th.key = 1
        else:
            if self.right_folder5_input.text() == "":
                self.myMessageBox("提示", "请选择要分类的影评数据所在文件夹!")
            elif self.right_folder6_input.text() == "":
                self.myMessageBox("提示", "请选择分类器!")

    def stop_ana(self):
        self.app_result_th.key = -1
        self.app_result_th.alive = False
        self.app_result_th.quit()
        self.app_result_th.wait()

    def appResultPos(self):
        self.app_result_table_th.commentAddress = "./test/" + self.right_folder5_input.text().split("/")[-1] + ".pkl"
        self.app_result_table_th.condition = "Pos"
        self.app_result_table_th.alive = True
        self.app_result_table_th.start()

    def appResultNeg(self):
        self.app_result_table_th.commentAddress = "./test/" + self.right_folder5_input.text().split("/")[-1] + ".pkl"
        self.app_result_table_th.condition = "Neg"
        self.app_result_table_th.alive = True
        self.app_result_table_th.start()

    def appGraph(self):
        self.app_result_graph_th.alive = True
        self.app_result_graph_th.start()

    def addAppToqtbTrainTest(self, s):
        if s[:3] != "Tip":
            if s[:2] == "所测":
                self.right_test_result.setDisabled(False)
                self.right_test_graph.setDisabled(False)
            if s.split("&")[0] == "result":
                self.test_result_table_th.name = s.split("&")[1]
                self.test_result_graph_th.name = s.split("&")[1]
            else:
                self.appToqtb(s, 3)
                if s[:2] != "载入" and s[:2] != "所测" and self.train_test_th.key != -1:
                    self.train_test_th.key = -1
                    self.train_test_th.alive = False
                    self.train_test_th.quit()
                    self.train_test_th.wait()
        else:
            self.right_posNum_input.setText(s.split("[")[1].split("]")[0])
            self.right_negNum_input.setText(s.split("[")[2].split("]")[0])
            self.right_folder_tip.setText(s)
            self.train_key = True
        self.right_train_start.setDisabled(False)
        self.right_test_start.setDisabled(False)
        self.right_train_stop.setDisabled(True)
        self.right_test_stop.setDisabled(True)

    def folderCheck(self):
        if self.right_folder1_input.text() != "":
            self.appToqtb("开始载入......请耐心等待", 3)
            self.right_folder_check.setDisabled(True)
            self.right_train_start.setDisabled(True)
            self.right_test_start.setDisabled(True)
            self.right_train_stop.setDisabled(True)
            self.right_test_stop.setDisabled(True)
            if self.train_test_th.key == -1:
                self.train_test_th.key = 1
                self.train_test_th.alive = True
                self.train_test_th.start()
            else:
                self.train_test_th.key = 1
        else:
            self.myMessageBox("提示", "请先选择训练数据集!")

    def start_train(self):
        if self.train_key:
            posNum = self.right_posNum_input.text()
            negNum = self.right_negNum_input.text()
            name = self.right_name_input.text()
            bigram = self.right_bigram_input.text()
            feature = self.right_feature_input.text()
            if re.match("[1-9][0-9]*", posNum) and re.match("[1-9][0-9]*", negNum):
                self.train_test_th.pos_num = int(posNum)
                self.train_test_th.neg_num = int(negNum)
                if name != "":
                    self.train_test_th.classifier_name = name
                if bigram != "" and re.match("[1-9][0-9]*", bigram):
                    self.train_test_th.bigram_num = int(bigram)
                if feature != "" and re.match("[1-9][0-9]*", feature):
                    self.train_test_th.feature_num = int(feature)
                self.appToqtb("开始训练......请耐心等待", 3)
                self.right_train_stop.setDisabled(False)
                self.right_train_start.setDisabled(True)
                self.right_test_stop.setDisabled(True)
                self.right_test_start.setDisabled(True)
                self.train_test_th.key = 2
                self.train_key = False

            else:
                self.myMessageBox("提示", "样本数输入格式错误!")
        else:
            self.myMessageBox("提示", "请重新载入训练数据集!")

    def stop_train(self):
        self.train_test_th.key = 0
        self.right_train_start.setDisabled(False)
        self.right_train_stop.setDisabled(True)
        self.right_test_start.setDisabled(False)

    def start_test(self):
        if self.right_folder2_input.text() != "":
            self.train_test_th.file1 = self.right_folder2_input.text()
        if self.right_folder3_input.text() != "":
            self.train_test_th.file2 = self.right_folder3_input.text()
        if self.right_folder2_input.text() != "" and self.right_folder3_input.text() != "":
            self.test_key = True

        if self.test_key:
            self.appToqtb("开始测试......请耐心等待", 3)
            self.right_train_start.setDisabled(True)
            self.right_test_stop.setDisabled(False)
            self.right_test_start.setDisabled(True)
            self.test_key = False
            if self.train_test_th.key == -1:
                self.train_test_th.key = 3
                self.train_test_th.alive = True
                self.train_test_th.start()
            else:
                self.train_test_th.key = 3
        else:
            if self.right_folder2_input.text() == "":
                self.myMessageBox("提示", "请选择要测试的数据!")
            elif self.right_folder3_input.text() == "":
                self.myMessageBox("提示", "请选择分类器!")

    def stop_test(self):
        self.train_test_th.key = 0
        self.right_train_start.setDisabled(False)
        self.right_train_stop.setDisabled(True)
        self.right_test_start.setDisabled(False)

    def testResult(self):
        self.test_result_table_th.commentAddress = self.right_folder2_input.text()
        if self.right_folder2_input.text().split("/")[-1].split(".")[0] == "Neg":
            self.test_result_table_th.condition = "Neg"
        else:
            self.test_result_table_th.condition = "Pos"
        self.test_result_table_th.alive = True
        self.test_result_table_th.start()

    def testGraph(self):
        self.test_result_graph_th.alive = True
        self.test_result_graph_th.start()

    def addAppToqtbSeparate(self, s):
        if s[:3] != "Tip":
            self.appToqtb(s, 4)
            if s[:2] != "检测" and self.train_test_th.key != -1:
                self.separate_th.key = -1
                self.separate_th.alive = False
                self.separate_th.quit()
                self.separate_th.wait()
            self.right_separate_start.setDisabled(False)
            self.right_return.setDisabled(False)
        else:
            self.right_folder4_tip.setText(s)
            self.separate_key = True

    def folderCheck_2(self):
        if self.right_folder4_input.text() != "":
            self.appToqtb("开始检测......请耐心等待", 4)
            self.right_folder4_check.setDisabled(True)
            self.right_separate_start.setDisabled(True)
            self.right_return.setDisabled(True)
            if self.separate_th.key == -1:
                self.separate_th.key = 1
                self.separate_th.alive = True
                self.separate_th.start()
            else:
                self.separate_th.key = 1
        else:
            self.myMessageBox("提示", "请先选择要分离的数据集!")

    def start_separate(self):
        if self.separate_key:
            trainPosNum = self.right_trainPosNum_input.text()
            trainNegNum = self.right_trainNegNum_input.text()
            testPosNum = self.right_testPosNum_input.text()
            testNegNum = self.right_testNegNum_input.text()
            if re.match("[1-9][0-9]*", trainPosNum) \
                    and re.match("[1-9][0-9]*", trainNegNum) \
                    and re.match("[1-9][0-9]*", testPosNum) \
                    and re.match("[1-9][0-9]*", testNegNum):
                posNum = int(trainPosNum) + int(testPosNum)
                negNum = int(trainNegNum) + int(testNegNum)
                realPosNum = int(self.right_folder4_tip.text().split("[")[1].split("]")[0])
                realNegNum = int(self.right_folder4_tip.text().split("[")[2].split("]")[0])
                if posNum > realPosNum or negNum > realNegNum:
                    self.myMessageBox("提示", "分离的积极或者消极样本数目总和超过最大值，请重新输入!")
                else:
                    self.separate_th.train_pos_num = int(trainPosNum)
                    self.separate_th.train_neg_num = int(trainNegNum)
                    self.separate_th.test_pos_num = int(testPosNum)
                    self.separate_th.test_neg_num = int(testNegNum)

                    self.appToqtb("开始分离......请耐心等待", 4)
                    self.right_separate_start.setDisabled(True)
                    self.right_return.setDisabled(True)
                    self.separate_th.key = 2
                    self.train_key = False

            else:
                self.myMessageBox("提示", "样本数目输入格式错误!")
        else:
            self.myMessageBox("提示", "请重新选择要分离的数据集!")

    def assistUiShow(self):
        self.assistUI.show()

    def changeClass(self, i):
        self.train_test_th.cla = i
        if i == 0:
            self.right_class_label.setText("BernoulliNB")
        elif i == 1:
            self.right_class_label.setText("MultinomialNB")
        elif i == 2:
            self.right_class_label.setText("LogisticRegression")
        elif i == 3:
            self.right_class_label.setText("SVC")
        elif i == 4:
            self.right_class_label.setText("LinearSVC")
        elif i == 5:
            self.right_class_label.setText("NuSVC")

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.Qt.LeftButton:
            self.flag = True
            self.m_Position = QMouseEvent.globalPos() - self.pos()
            QMouseEvent.accept()
            self.setCursor(Qt.QCursor(Qt.Qt.ArrowCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.Qt.LeftButton and self.flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.flag = False
        self.setCursor(Qt.QCursor(Qt.Qt.ArrowCursor))

class assistUi(QWidget):
    update_data = pyqtSignal(int)  # 自定义信号（int类型）

    def __init__(self):
        super().__init__()

        self.choice = 0
        self.setWindowTitle('请选择分类方法')
        self.resize(400, 300)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(0.9)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.ok_button = QtWidgets.QPushButton('确 定', self)
        self.ok_button.clicked.connect(self.btn_ok)
        self.close_button = QtWidgets.QPushButton('关 闭', self)
        self.close_button.clicked.connect(self.btn_close)  # 去到关闭前的处理

        layout = QtWidgets.QVBoxLayout()  # 实例化一个布局

        self.btn1 = QtWidgets.QRadioButton("BernoulliNB")  # 实例化一个选择的按钮
        self.btn1.setChecked(True)  # 设置按钮点点击状态
        self.btn1.toggled.connect(lambda: self.btnstate(self.btn1))  # 绑定点击事件
        layout.addWidget(self.btn1)  # 布局添加组件

        self.btn2 = QtWidgets.QRadioButton("MultinomialNB")
        self.btn2.toggled.connect(lambda: self.btnstate(self.btn2))
        layout.addWidget(self.btn2)

        self.btn3 = QtWidgets.QRadioButton("LogisticRegression")
        self.btn3.toggled.connect(lambda: self.btnstate(self.btn3))
        layout.addWidget(self.btn3)

        # self.btn4 = QtWidgets.QRadioButton("SVC")
        # self.btn4.toggled.connect(lambda: self.btnstate(self.btn4))
        # layout.addWidget(self.btn4)
        #
        # self.btn5= QtWidgets.QRadioButton("LinearSVC")
        # self.btn5.toggled.connect(lambda: self.btnstate(self.btn5))
        # layout.addWidget(self.btn5)
        #
        # self.btn6 = QtWidgets.QRadioButton("NuSVC")
        # self.btn6.toggled.connect(lambda: self.btnstate(self.btn6))
        # layout.addWidget(self.btn6)

        self.setLayout(layout)  # 界面添加 layout

        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(self.ok_button)
        layout2.addWidget(self.close_button)

        layout.addLayout(layout2)

    def btnstate(self, btn):  # 自定义点击事件函数
        if btn.text() == "BernoulliNB":
            if btn.isChecked() == True:
                self.choice = 0

        if btn.text() == "MultinomialNB":
            if btn.isChecked() == True:
                self.choice = 1

        if btn.text() == "LogisticRegression":
            if btn.isChecked() == True:
                self.choice = 2

        # if btn.text() == "SVC":
        #     if btn.isChecked() == True:
        #         self.choice = 3
        #
        # if btn.text() == "LinearSVC":
        #     if btn.isChecked() == True:
        #         self.choice = 4
        #
        # if btn.text() == "NuSVC":
        #     if btn.isChecked() == True:
        #         self.choice = 5

    def btn_ok(self):
        self.update_data.emit(self.choice)
        self.close()

    def btn_close(self):
        self.close()

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.Qt.LeftButton:
            self.flag = True
            self.m_Position = QMouseEvent.globalPos() - self.pos()
            QMouseEvent.accept()
            self.setCursor(Qt.QCursor(Qt.Qt.ArrowCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.Qt.LeftButton and self.flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.flag = False
        self.setCursor(Qt.QCursor(Qt.Qt.ArrowCursor))

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
