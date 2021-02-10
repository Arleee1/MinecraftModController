import sys
import PyQt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import minecraft_mod_controller as mmc
import MMCListWidget
from print_debug import print_debug


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

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create mods area
        self.mods_folders_list_widget = MMCListWidget.MMCListWidget("mods_widget")
        self.mods_folders_list_widget.set_drop_event_func(self.populate_mods_and_options_lists)
        self.mods_folders_list_widget.customContextMenuRequested.connect(self.mods_folders_list_context_menu)

        apply_mods_btn = QPushButton("Apply Mods")
        apply_mods_btn.pressed.connect(self.mods_apply_btn_pressed)

        mods_layout = QVBoxLayout()
        mods_layout.addWidget(self.mods_folders_list_widget)
        mods_layout.addWidget(apply_mods_btn)

        # Create options area
        self.options_files_list_widget = MMCListWidget.MMCListWidget("options_widget")
        self.options_files_list_widget.set_drop_event_func(self.populate_mods_and_options_lists)
        self.options_files_list_widget.customContextMenuRequested.connect(self.options_files_list_context_menu)

        self.populate_mods_and_options_lists()

        apply_options_btn = QPushButton("Apply Options")
        apply_options_btn.pressed.connect(self.options_apply_btn_pressed)

        options_layout = QVBoxLayout()
        options_layout.addWidget(self.options_files_list_widget)
        options_layout.addWidget(apply_options_btn)

        # Create populate_mods_and_options_lists button
        refresh_button = QPushButton("Refresh")
        refresh_button.pressed.connect(self.populate_mods_and_options_lists)
        # TODO make populate_mods_and_options_lists button look nicer

        # Create selection area
        selection_layout = QHBoxLayout()
        selection_layout.addLayout(mods_layout)
        selection_layout.addLayout(options_layout)

        # Assemble the layouts together
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addLayout(selection_layout)
        central_layout.addWidget(refresh_button)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

    def mods_apply_btn_pressed(self) -> None:
        """
        Called when the apply button is pressed and attempts to apply the changes to the mods folders
        :return: None
        """

        if len(self.mods_folders_list_widget.selectedItems()) == 0:
            self.statusBar().showMessage(f"Please select a mods folder first", 5_000)
            return

        selected_mods_folder = self.mods_folders_list_widget.currentItem().text()
        mod_controller = mmc.ModController()

        print_debug(f"Mods apply button pressed: {selected_mods_folder}")

        try:
            if mod_controller.transfer_mods_or_options(selected_mods_folder, is_mods=True):
                self.statusBar().showMessage(f"Loaded mods: {selected_mods_folder}", 5_000)
                print_debug(f"Loaded mods: {selected_mods_folder}")
            else:
                self.statusBar().showMessage(f"You must enable user creation of symbolic links", 5_000)
                print_debug("You must enable user creation of symbolic links")
        except NotADirectoryError:
            print_debug(f"{selected_mods_folder} no longer exists")
            self.statusBar().showMessage(f"{selected_mods_folder} no longer exists", 5_000)
            self.populate_mods_and_options_lists()
            return

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
        mod_controller.rename_mods_or_options(selected_mods_folder, "test", is_mods=True)
        print_debug(selected_mods_folder)

    def mods_folders_list_clicked(self):
        print_debug("mods list clicked")

    def options_apply_btn_pressed(self) -> None:
        """
        Called when the options apply button is pressed and attempts to apply the changes to the options file
        :return: None
        """

        if len(self.options_files_list_widget.selectedItems()) == 0:
            self.statusBar().showMessage(f"Please select an options file first", 5_000)
            return

        selected_options_file = self.options_files_list_widget.currentItem().text()
        mod_controller = mmc.ModController()

        print_debug(f"Options apply button pressed: {selected_options_file}")

        try:
            if mod_controller.transfer_mods_or_options(selected_options_file, is_mods=False):
                self.statusBar().showMessage(f"Loaded options: {selected_options_file}", 5_000)
                print_debug(f"Loaded options: {selected_options_file}")
            else:
                self.statusBar().showMessage(f"You must enable user creation of symbolic links", 5_000)
                print_debug("You must enable user creation of symbolic links")
        except FileNotFoundError:
            print_debug(f"{selected_options_file} no longer exists")
            self.statusBar().showMessage(f"{selected_options_file} no longer exists", 5_000)
            self.populate_mods_and_options_lists()
            return

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
        mod_controller.rename_mods_or_options(selected_options_file, "test", is_mods=False)
        print_debug(selected_options_file)

    def populate_mods_and_options_lists(self):
        mod_controller = mmc.ModController()

        self.mods_folders_list_widget.clear()
        resolved_mods_list = mod_controller.resolve_mods_or_options_list(is_mods=True)
        self.mods_folders_list_widget.addItems(resolved_mods_list)

        self.options_files_list_widget.clear()
        resolved_options_list = mod_controller.resolve_mods_or_options_list(is_mods=False)
        self.options_files_list_widget.addItems(resolved_options_list)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ModControllerGUI()
    sys.exit(app.exec_())
