import PyQt5
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView
import json


class MMCListWidget(PyQt5.QtWidgets.QListWidget):
    def __init__(self, label):
        super(MMCListWidget, self).__init__()

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)

        self.label = label

    def dropEvent(self, e):
        print("drop event")
        e.ignore()
        super(MMCListWidget, self).dropEvent(e)
        self.takeItem(self.currentRow())
        items_text_list = [str(self.item(i).text()) for i in range(self.count())]
        file = "mods_list.json" if self.label == "mods_widget" else "options_list.json"
        print(file)
        with open(file, "w") as outfile:
            json.dump(items_text_list, outfile)
        print(items_text_list)
