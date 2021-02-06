import sys
import PyQt5
from PyQt5.QtWidgets import *
import minecraft_mod_controller as mmc


class ModControllerGUI(QMainWindow):

    def __init__(self) -> None:
        super(ModControllerGUI, self).__init__()

        self.title = "Mod Manager"
        self.left = 10
        self.top = 40
        self.width = 640
        self.height = 480

        self.selected_mods_folder = None
        self.selected_options_file = None

        self.initUI()
        self.show()

    def initUI(self) -> None:
        """
        Initializes the user interface
        :return: None
        """

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        mod_controller = mmc.ModController()

        # Create mods area
        mods_folders_list_widget = QListWidget()
        mods_folders_list_widget.addItems(mod_controller.get_mods_folders())
        mods_folders_list_widget.itemClicked.connect(self.mods_folders_list_clicked)

        apply_mods_btn = QPushButton("Apply Mods")
        apply_mods_btn.pressed.connect(self.mods_apply_btn_pressed)

        mods_layout = QVBoxLayout()
        mods_layout.addWidget(mods_folders_list_widget)
        mods_layout.addWidget(apply_mods_btn)

        # Create options area
        options_files_list_widget = QListWidget()
        options_files_list_widget.addItems(mod_controller.get_options_files())
        options_files_list_widget.itemClicked.connect(self.options_files_list_clicked)

        apply_options_btn = QPushButton("Apply Options")
        apply_options_btn.pressed.connect(self.options_apply_btn_pressed)

        options_layout = QVBoxLayout()
        options_layout.addWidget(options_files_list_widget)
        options_layout.addWidget(apply_options_btn)

        # Assemble the layouts together
        central_widget = QWidget()
        central_layout = QHBoxLayout()
        central_layout.addLayout(mods_layout)
        central_layout.addLayout(options_layout)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

    def mods_folders_list_clicked(self, selected_item: PyQt5.QtWidgets.QListWidgetItem) -> None:
        """
        Called when mods_folders_list is clicked, and stores the clicked item
        :param selected_item: Mods list item that was clicked
        :return: None
        """

        self.selected_mods_folder = selected_item.text()

    def mods_apply_btn_pressed(self) -> None:
        """
        Called when the apply button is pressed and attempts to apply the changes to the mods folders
        :return: None
        """

        if self.selected_mods_folder is None:
            self.statusBar().showMessage(f"Please select a mods folder first", 5_000)
            return

        mod_controller = mmc.ModController()
        mod_controller.transfer_mods_folder(self.selected_mods_folder)
        print(f"Mods apply button pressed: {self.selected_mods_folder}")
        self.statusBar().showMessage(f"Loaded mods: {self.selected_mods_folder}", 5_000)

    def options_files_list_clicked(self, selected_item: PyQt5.QtWidgets.QListWidgetItem) -> None:
        """
        Called when options_files_list is clicked, and stores the clicked item
        :param selected_item: Options list item that was clicked
        :return: None
        """

        self.selected_options_file = selected_item.text()

    def options_apply_btn_pressed(self) -> None:
        """
        Called when the options apply button is pressed and attempts to apply the changes to the options file
        :return: None
        """

        if self.selected_options_file is None:
            self.statusBar().showMessage(f"Please select an options file first", 5_000)
            return

        print(self.selected_options_file)
        mod_controller = mmc.ModController()
        mod_controller.transfer_options_file(self.selected_options_file)
        print(f"Options apply button pressed: {self.selected_options_file}")
        self.statusBar().showMessage(f"Loaded options: {self.selected_options_file}", 5_000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ModControllerGUI()
    sys.exit(app.exec_())
