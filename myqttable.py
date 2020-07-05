import pickle
import sys

import pandas as pd
from qdarkstyle import load_stylesheet_pyqt5
from PyQt5.QtWidgets import QApplication, QTableView, QHeaderView
from PyQt5.QtCore import QAbstractTableModel, Qt


class QtTable(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


def render():
    app = QApplication(sys.argv)
    name = sys.argv[1]
    commentAddress = sys.argv[2]
    condition = sys.argv[3]
    f = open("./result/test_result_" + name + ".txt", "r", encoding="utf-8")
    content = f.readline()

    commentId = []
    pos_score = []
    neg_score = []
    result = []
    realId = []
    num = 0

    if condition == "Pos":
        while content != "":
            if int(content.split("|")[1]) > int(content.split("|")[2]):
                num += 1
                realId.append(num)
                commentId.append(int(content.split("|")[0]) - 1)
                pos_score.append(int(content.split("|")[1]))
                neg_score.append(int(content.split("|")[2]))
                result.append(content.split("|")[3].strip())
            content = f.readline()
    elif condition == "Neg":
        while content != "":
            if int(content.split("|")[1]) < int(content.split("|")[2]):
                num += 1
                realId.append(num)
                commentId.append(int(content.split("|")[0]) - 1)
                pos_score.append(int(content.split("|")[1]))
                neg_score.append(int(content.split("|")[2]))
                result.append(content.split("|")[3].strip())
            content = f.readline()
    else:
        while content != "":
            num += 1
            realId.append(num)
            commentId.append(int(content.split("|")[0]) - 1)
            pos_score.append(int(content.split("|")[1]))
            neg_score.append(int(content.split("|")[2]))
            result.append(content.split("|")[3].strip())
            content = f.readline()
    f.close()

    output = open(commentAddress, "rb")
    comment_content = pickle.load(output)
    output.close()

    comment = []
    for i in commentId:
        _comment = ""
        for j in range(len(comment_content[i])):
            _comment = _comment + comment_content[i][j]
        comment.append(_comment)

    if condition == "Pos":
        df = pd.DataFrame({'id': realId,
                           '积极倾向得分': pos_score,
                           # '消极倾向得分': neg_score,
                           '情感倾向': result,
                           '评论内容': comment})
    elif condition == "Neg":
        df = pd.DataFrame({'id': realId,
                           # '积极倾向得分': pos_score,
                           '消极倾向得分': neg_score,
                           '情感倾向': result,
                           '评论内容': comment})
    else:
        df = pd.DataFrame({'id': realId,
                           '积极倾向得分': pos_score,
                           '消极倾向得分': neg_score,
                           '情感倾向': result,
                           '评论内容': comment})

    model = QtTable(df)
    view = QTableView()
    # app.setStyleSheet(load_stylesheet_pyqt5())
    fnt = view.font()
    fnt.setPointSize(9)
    view.setFont(fnt)
    view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    view.setModel(model)

    view.setWindowTitle("具体结果")
    view.resize(1080, 900)
    view.show()
    sys.exit(app.exec_())


render()
