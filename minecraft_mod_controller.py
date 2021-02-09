import json
import os
import shutil
import typing


class ModController:
    def __init__(self) -> None:

        # Set constants
        # TODO Get .minecraft folder dynamically
        self.MINECRAFT_DIR = r"C:\Users\eeerm\AppData\Roaming\.minecraft"

        self.MODS_FOLDERS_DIR = os.path.join(self.MINECRAFT_DIR, r"mods_folders")
        self.MODS_DIR = os.path.join(self.MINECRAFT_DIR, r"mods")

        self.OPTIONS_FOLDER_DIR = os.path.join(self.MINECRAFT_DIR, r"options_folder")
        self.OPTIONS_FILE = os.path.join(self.MINECRAFT_DIR, r"options.txt")

        self.refresh()

    def refresh(self) -> None:
        """
        Ensure the proper folders exist
        :return: None
        """

        if not os.path.isdir(self.MINECRAFT_DIR):
            raise NotADirectoryError(".minecraft is not a directory")

        self.verify_folder(self.MODS_FOLDERS_DIR, "mods_folders")
        self.verify_folder(self.MODS_DIR, "mods")
        self.verify_folder(self.OPTIONS_FOLDER_DIR, "options_folder")

    def verify_folder(self, folder: str, folder_name: str) -> None:
        """
        Check if each folder exists, and create it if it doesn't
        :param folder: Folder to be checked
        :param folder_name: Display name of the folder
        :return: None
        """

        if not os.path.isdir(folder):
            if not os.path.isfile(folder):
                os.mkdir(folder)
            else:
                raise NotADirectoryError(f"{folder_name} is not a directory")

    def transfer_mods_folder(self, folder: str) -> None:
        """
        Makes a link to the mods folder to be used by Forge
        :param folder: Mods folder to be linked to
        :return: None
        """

        src_dir = os.path.join(self.MODS_FOLDERS_DIR, folder)

        if not os.path.isdir(src_dir):
            raise NotADirectoryError(f"{src_dir} is not a directory")

        # TODO Perhaps implement a check to verify if mods dir is backed up in mods_folder dir, so that mods dir doesnt get deleted without saving
        os.unlink(self.MODS_DIR)
        dst_dir = self.MODS_DIR
        os.symlink(src_dir, dst_dir)

    def get_mods_folders(self) -> typing.List[str]:
        """
        Retrieves the folders in the mods_folders directory
        :return: A list of the folders in the mods_folders directory
        """

        return list(os.listdir(self.MODS_FOLDERS_DIR))

    def rename_mods_folder(self, src_name: str, dst_name: str) -> None:
        src_path = os.path.join(self.MODS_FOLDERS_DIR, src_name)
        dst_path = os.path.join(self.MODS_FOLDERS_DIR, dst_name)
        print(f"renamed {src_path} to {dst_path}")
        # os.rename(src_path, dst_path)

    def set_mods_or_options_list(self, mods_list: typing.List[str], *, is_mods: bool) -> None:
        """
        Stores the list of mods in a json file
        :param mods_list: The list of mods to be stored
        :param is_mods: True: stored as a list of mods, False: stored as a list of options
        :return: None
        """

        file = "mods_list.json" if is_mods else "options_list.json"

        with open(file, "w") as outfile:
            json.dump(mods_list, outfile)

    def transfer_options_file(self, options_file: str) -> None:
        """
        Makes a link to the options file to be used by Minecraft
        :param options_file: Options file to be linked to
        :return: None
        """

        src_file = os.path.join(self.OPTIONS_FOLDER_DIR, options_file)

        if not os.path.isfile(src_file):
            raise FileNotFoundError(f"{src_file} is not a file")

        # TODO Perhaps implement a check to verify if options file is backed up in options_folder dir, so that the options file doesnt get deleted without saving
        os.unlink(self.OPTIONS_FILE)
        dst_dir = self.OPTIONS_FILE
        os.symlink(src_file, dst_dir)

    def get_options_files(self) -> typing.List[str]:
        """
        Retrieves the files in the options_folder directory
        :return: A list of the folders in the options_folder directory
        """

        return list(os.listdir(self.OPTIONS_FOLDER_DIR))

    def rename_options_file(self, src_name: str, dst_name: str) -> None:
        src_path = os.path.join(self.OPTIONS_FOLDER_DIR, src_name)
        dst_path = os.path.join(self.OPTIONS_FOLDER_DIR, dst_name)
        print(f"renamed {src_path} to {dst_path}")
        # os.rename(src_path, dst_path)


if __name__ == "__main__":
    mod_controller = ModController()
    print(mod_controller.get_mods_folders())
    print(mod_controller.get_options_files())
