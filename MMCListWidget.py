import PyQt5
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView
import json
import minecraft_mod_controller as mmc


class MMCListWidget(PyQt5.QtWidgets.QListWidget):
    def __init__(self, label):
        super(MMCListWidget, self).__init__()

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)

        self.label = label

    def dropEvent(self, e):
        mod_controller = mmc.ModController()
        print("drop event")
        e.ignore()
        super(MMCListWidget, self).dropEvent(e)
        self.takeItem(self.currentRow())
        items_text_list = [str(self.item(i).text()) for i in range(self.count())]
        mod_controller.set_mods_or_options_list(items_text_list, is_mods=(self.label == "mods_widget"))
        print(items_text_list)
