import sys
import PyQt5
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import minecraft_mod_controller as mmc
import MMCListWidget


class ModControllerGUI(QMainWindow):

    def __init__(self) -> None:
        super(ModControllerGUI, self).__init__()

        self.title = "Mod Manager"
        self.left = 10
        self.top = 40
        self.width = 640
        self.height = 480

        self.mods_folders_list_widget = None
        self.options_files_list_widget = None

        self.initUI()
        self.show()

    def initUI(self) -> None:
        """
        Initializes the user interface
        :return: None
        """

        # TODO Remember the order of the mods and options files lists across sessions
        #   Currently implemented: drag and drop items, and store changes
        #   How to order items when program restarts:
        #   Check items against mods_folders dir/options_folder dir
        #   if there are no changes: keep order the same
        #   if items are removed: remove from list
        #   if new items are added: add to bottom (top?) of list

        # TODO Create button to refresh mods folders and options files
        #   Button should retrieve the folders and files in the directorys and update the respective lists as necessary,
        #   much like is done on start up

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        mod_controller = mmc.ModController()

        # Create mods area
        self.mods_folders_list_widget = MMCListWidget.MMCListWidget("mods_widget")
        self.mods_folders_list_widget.addItems(mod_controller.get_mods_folders())
        self.mods_folders_list_widget.customContextMenuRequested.connect(self.mods_folders_list_context_menu)
        # self.mods_folders_list_widget.itemClicked.connect(self.mods_folders_list_clicked)

        apply_mods_btn = QPushButton("Apply Mods")
        apply_mods_btn.pressed.connect(self.mods_apply_btn_pressed)

        mods_layout = QVBoxLayout()
        mods_layout.addWidget(self.mods_folders_list_widget)
        mods_layout.addWidget(apply_mods_btn)

        # Create options area
        self.options_files_list_widget = MMCListWidget.MMCListWidget("options_widget")
        self.options_files_list_widget.addItems(mod_controller.get_options_files())
        self.options_files_list_widget.customContextMenuRequested.connect(self.options_files_list_context_menu)

        apply_options_btn = QPushButton("Apply Options")
        apply_options_btn.pressed.connect(self.options_apply_btn_pressed)

        options_layout = QVBoxLayout()
        options_layout.addWidget(self.options_files_list_widget)
        options_layout.addWidget(apply_options_btn)

        # Assemble the layouts together
        central_widget = QWidget()
        central_layout = QHBoxLayout()
        central_layout.addLayout(mods_layout)
        central_layout.addLayout(options_layout)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

    def mods_apply_btn_pressed(self) -> None:
        """
        Called when the apply button is pressed and attempts to apply the changes to the mods folders
        :return: None
        """

        selected_mods_folder = self.mods_folders_list_widget.currentItem().text()

        if selected_mods_folder is None:
            self.statusBar().showMessage(f"Please select a mods folder first", 5_000)
            return

        mod_controller = mmc.ModController()
        mod_controller.transfer_mods_folder(selected_mods_folder)
        print(f"Mods apply button pressed: {selected_mods_folder}")
        self.statusBar().showMessage(f"Loaded mods: {selected_mods_folder}", 5_000)

    def mods_folders_list_context_menu(self, position: PyQt5.QtCore.QPoint) -> None:
        """
        Create context menu for the mods folders list
        :param position: Position of the right click
        :return: None
        """

        right_click_menu = QMenu()
        rename_action = QAction("Rename", self)
        # Check if it is on the item when you right-click, if it is not, delete and modify will not be displayed.
        right_click_menu.addAction(rename_action)
        rename_action.triggered.connect(self.rename_mods_folder)
        right_click_menu.exec_(self.mods_folders_list_widget.mapToGlobal(position))

    def rename_mods_folder(self) -> None:
        """
        Renames the selected mods folder
        :return: None
        """

        # TODO Rename Mods folder here

        selected_mods_folder = self.mods_folders_list_widget.currentItem().text()
        mod_controller = mmc.ModController()
        mod_controller.rename_mods_folder(selected_mods_folder, "test")
        print(selected_mods_folder)

    def mods_folders_list_clicked(self):
        print("mods list clicked")

    def options_apply_btn_pressed(self) -> None:
        """
        Called when the options apply button is pressed and attempts to apply the changes to the options file
        :return: None
        """

        selected_options_file = self.options_files_list_widget.currentItem().text()

        if selected_options_file is None:
            self.statusBar().showMessage(f"Please select an options file first", 5_000)
            return

        mod_controller = mmc.ModController()
        mod_controller.transfer_options_file(selected_options_file)
        print(f"Options apply button pressed: {selected_options_file}")
        self.statusBar().showMessage(f"Loaded options: {selected_options_file}", 5_000)

    def options_files_list_context_menu(self, position: PyQt5.QtCore.QPoint) -> None:
        """
        Create context menu for the options files list
        :param position: Position of the right click
        :return: None
        """

        right_click_menu = QMenu()
        rename_action = QAction("Rename", self)
        # Check if it is on the item when you right-click, if it is not, delete and modify will not be displayed.
        right_click_menu.addAction(rename_action)
        rename_action.triggered.connect(self.rename_options_file)
        right_click_menu.exec_(self.options_files_list_widget.mapToGlobal(position))

    def rename_options_file(self) -> None:
        """
        Renames the selected options file
        :return: None
        """

        # TODO Rename Options file here

        selected_options_file = self.options_files_list_widget.currentItem().text()
        mod_controller = mmc.ModController()
        mod_controller.rename_options_file(selected_options_file, "test")
        print(selected_options_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ModControllerGUI()
    sys.exit(app.exec_())
