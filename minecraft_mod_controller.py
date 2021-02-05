import os
import shutil


class ModController:
    def __init__(self):
        self.MINECRAFT_DIR = r"C:\Users\eeerm\AppData\Roaming\.minecraft"
        self.MODS_FOLDERS_DIR = os.path.join(self.MINECRAFT_DIR, r"mods_folders")
        self.MODS_DIR = os.path.join(self.MINECRAFT_DIR, r"mods")
        self.refresh()

    def refresh(self):
        if not os.path.isdir(self.MINECRAFT_DIR):
            raise NotADirectoryError(".minecraft is not a directory")

        if not os.path.isdir(self.MODS_FOLDERS_DIR):
            if not os.path.isfile(self.MODS_FOLDERS_DIR):
                os.mkdir(self.MODS_FOLDERS_DIR)
            else:
                raise NotADirectoryError("mods_folders is not a directory")

        if not os.path.isdir(self.MODS_DIR):
            if not os.path.isfile(self.MODS_DIR):
                os.mkdir(self.MODS_DIR)
            else:
                raise NotADirectoryError("mods_folders is not a directory")

    def transfer_mods_folder(self, folder):
        src_dir = os.path.join(self.MODS_FOLDERS_DIR, folder)

        if not os.path.isdir(src_dir):
            raise NotADirectoryError(f"{src_dir} is not a directory")

        # TODO Perhaps implement a check to verify if mods dir is backed up in mods_folder dir, so that mods dir doesnt get deleted without saving
        shutil.rmtree(self.MODS_DIR)
        dst_dir = self.MODS_DIR
        shutil.copytree(src_dir, dst_dir)

    def get_mods_folders(self):
        return os.listdir(self.MODS_FOLDERS_DIR)


if __name__ == "__main__":
    # TODO Implement GUI
    mod_controller = ModController()
    mod_controller.transfer_mods_folder("mods 1.16.3 create")
    print(mod_controller.get_mods_folders())
