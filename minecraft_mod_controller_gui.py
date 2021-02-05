import sys
from PyQt5.QtWidgets import *
import minecraft_mod_controller as mmc


class ModControllerGUI(QMainWindow):

    def __init__(self):
        super(ModControllerGUI, self).__init__()

        self.title = "Mod Manager"
        self.left = 10
        self.top = 40
        self.width = 640
        self.height = 480

        self.selected_item = None

        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        mod_controller = mmc.ModController()
        mods_folders_list_widget = QListWidget()
        mods_folders_list_widget.addItems(mod_controller.get_mods_folders())
        mods_folders_list_widget.itemClicked.connect(self.mods_folders_list_clicked)

        apply_btn = QPushButton("Apply")
        apply_btn.pressed.connect(self.apply_btn_pressed)

        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addWidget(mods_folders_list_widget)
        central_layout.addWidget(apply_btn)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

    def mods_folders_list_clicked(self, item):
        self.selected_item = item.text()

    def apply_btn_pressed(self):
        if self.selected_item is None:
            self.statusBar().showMessage(f"Please select a mods folder first", 5_000)
            return

        mod_controller = mmc.ModController()
        mod_controller.transfer_mods_folder(self.selected_item)
        print(f"Apply button pressed: {self.selected_item}")
        self.statusBar().showMessage(f"Loaded mods: {self.selected_item}", 5_000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ModControllerGUI()
    sys.exit(app.exec_())
