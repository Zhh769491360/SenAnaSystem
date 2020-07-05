import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Drawing(QWidget):
    def __init__(self, parent=None):
        super(Drawing, self).__init__(parent)
        self.resize(1150, 900)
        self.setWindowTitle("具体结果图像")
        self.name = ""

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.begin(self)
        self.drawGraph(qp)
        qp.end()

    def drawGraph(self, qp):
        # size = self.size()

        f = open("result/test_result_" + self.name + ".txt", "r", encoding="utf-8")
        content = f.readline()

        commentId = []
        pos_score = []
        neg_score = []

        while content != "":
            commentId.append(content.split("|")[0])
            pos_score.append(int(content.split("|")[1]))
            neg_score.append(int(content.split("|")[2]))
            content = f.readline()
        f.close()

        pos_dict = {}
        neg_dict = {}

        for i in range(len(pos_score)):
            if pos_score[i] in pos_dict.keys():
                pos_dict[pos_score[i]] += 1
            else:
                pos_dict[pos_score[i]] = 1
            if neg_score[i] in neg_dict.keys():
                neg_dict[neg_score[i]] += 1
            else:
                neg_dict[neg_score[i]] = 1

        max_pos_num = max(zip(pos_dict.values(), pos_dict.keys()))[0]
        max_neg_num = max(zip(neg_dict.values(), neg_dict.keys()))[0]

        if max_pos_num > max_neg_num:
            max_num = max_pos_num
        else:
            max_num = max_neg_num

        dy = 400 / (max_num + 10)
        dx = 10

        qp.setPen(QPen(Qt.red, 5, Qt.CustomDashLine))
        for key in pos_dict:
            qp.drawLine((int(key) + 1) * dx + 50, 450, (int(key) + 1) * dx + 50, 450 - int(pos_dict[key]) * dy)
        qp.drawLine(600, 20, 700, 20)

        qp.setPen(QPen(Qt.green, 5, Qt.CustomDashLine))
        for key in neg_dict:
            qp.drawLine((int(key) + 1) * dx + 50, 450, (int(key) + 1) * dx + 50, 450 + int(neg_dict[key]) * dy)
        qp.drawLine(800, 20, 900, 20)

        qp.setPen(QPen(Qt.black, 3))
        qp.drawRect(50, 50, 1030, 800)

        # 横轴
        for j in range(11):
            qp.drawLine((int(j * 10) + 1) * dx + 50, 850, (int(j * 10) + 1) * dx + 50, 860)
            qp.drawText((int(j * 10) + 1) * dx + 43, 890, str(j * 10))
        qp.drawText(1100, 870, "分数")

        # 竖轴
        dnum = int(max_num / 5)
        for k in range(11):
            qp.drawLine(40, k * 80 + 50, 50, k * 80 + 50)
        for k in range(6):
            qp.drawText(4, 457 + k * 80, str(k * dnum))
            qp.drawText(4, 457 - k * 80, str(k * dnum))
        qp.drawText(10, 30, "评论数目")

        qp.drawText(720, 30, "积极倾向")
        qp.drawText(920, 30, "消极倾向")


def start():
    app = QApplication(sys.argv)
    demo = Drawing()
    demo.name = sys.argv[1]
    demo.show()
    sys.exit(app.exec_())


start()
