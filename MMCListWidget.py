import PyQt5
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView
import minecraft_mod_controller as mmc
import typing


class MMCListWidget(PyQt5.QtWidgets.QListWidget):
    def __init__(self, label):
        super(MMCListWidget, self).__init__()

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)

        self.label = label

        self.drop_event_func = None

    def dropEvent(self, e):
        mod_controller = mmc.ModController()
        print("drop event")
        e.ignore()
        super(MMCListWidget, self).dropEvent(e)
        self.takeItem(self.currentRow())
        items_text_list = [str(self.item(i).text()) for i in range(self.count())]
        mod_controller.set_mods_or_options_order(items_text_list, is_mods=(self.label == "mods_widget"))
        print(items_text_list)
        if self.drop_event_func is not None:
            self.drop_event_func()

    def dragMoveEvent(self, e):
        super(MMCListWidget, self).dragMoveEvent(e)
        print("drag move event")

    def dragLeaveEvent(self, e):
        super(MMCListWidget, self).dragLeaveEvent(e)
        print("drag leave event")

    def set_drop_event_func(self, func: typing.Callable):
        self.drop_event_func = func
