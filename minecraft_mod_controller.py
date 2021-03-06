import json
import os
import typing
from print_debug import print_debug
import shutil
import sys


class ModController:
    def __init__(self) -> None:

        # Set constants
        # TODO Get .minecraft folder dynamically

        #self.CURRENT_DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
            os.chdir(application_path)
        self.CURRENT_DIR = os.getcwd()
        self.DATA_DIR = os.path.join(self.CURRENT_DIR, "data")

        self.MINECRAFT_DIR_INFO_FILE = os.path.join(self.DATA_DIR, "dot_minecraft_location.txt")
        self.MINECRAFT_DIR = self.get_minecraft_dir()

        self.MODS_FOLDERS_DIR = os.path.join(self.MINECRAFT_DIR, r"mods_folders")
        self.MODS_DIR = os.path.join(self.MINECRAFT_DIR, r"mods")

        self.OPTIONS_FOLDER_DIR = os.path.join(self.MINECRAFT_DIR, r"options_folder")
        self.OPTIONS_FILE = os.path.join(self.MINECRAFT_DIR, r"options.txt")

        self.MODS_ORDER_JSON_FILE = os.path.join(self.DATA_DIR, "mods_list.json")
        self.OPTIONS_ORDER_JSON_FILE = os.path.join(self.DATA_DIR, "options_list.json")

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

        # Check if any options files exist, and create 2 default ones if none exist
        options_1_16 = os.path.join(self.OPTIONS_FOLDER_DIR, "1.16 options")
        options_1_8 = os.path.join(self.OPTIONS_FOLDER_DIR, "1.8 options")

        if len(os.listdir(self.OPTIONS_FOLDER_DIR)) == 0 and not os.path.islink(self.OPTIONS_FILE) and os.path.exists(self.OPTIONS_FILE):
            shutil.copyfile(self.OPTIONS_FILE, options_1_16, follow_symlinks=True)
            shutil.copyfile(self.OPTIONS_FILE, options_1_8, follow_symlinks=True)
        elif len(os.listdir(self.OPTIONS_FOLDER_DIR)) == 0:
            if not os.path.isfile(options_1_16):
                open(options_1_16, "w").close()
            if not os.path.isfile(options_1_8):
                open(options_1_8, "w").close()

        # Check if any mods folders are available, and if possible create one with the preinstalled mods
        if len(os.listdir(self.MODS_FOLDERS_DIR)) == 0:
            os.mkdir(os.path.join(self.MODS_FOLDERS_DIR, "example mods folder"))

    def verify_folder(self, folder: str, folder_name: str) -> None:
        """
        Check if each folder exists, and create it if it doesn't
        :param folder: Folder to be checked
        :param folder_name: Display name of the folder
        :return: None
        """
        print(f"{folder_name} exists: {os.path.exists(folder)}")
        if not os.path.exists(folder):
            print_debug(f"{folder_name}: {folder} does not exist")
            if os.path.islink(folder):
                os.rmdir(folder)
            os.mkdir(folder)

    def set_mods_or_options_order(self, mods_list: typing.List[str], *, is_mods: bool) -> None:
        """
        Stores the ordered list of mods/options in a json file
        :param mods_list: The list of mods/options to be stored
        :param is_mods: True: stored as a list of mods, False: stored as a list of options
        :return: None
        """

        file = self.MODS_ORDER_JSON_FILE if is_mods else self.OPTIONS_ORDER_JSON_FILE

        self.verify_folder(self.DATA_DIR, "Data")

        if not os.path.isfile(file):
            open(file, "w").close()

        with open(file, "w") as outfile:
            json.dump(mods_list, outfile)

    def get_mods_or_options_order(self, *, is_mods: bool) -> typing.List[str]:
        """
        Retrieves the ordered list of mods/options
        :param is_mods: True: retrieves the ordered list of mods, False: retrieves the ordered list of options
        :return: The ordered list of options or mods
        """

        file = self.MODS_ORDER_JSON_FILE if is_mods else self.OPTIONS_ORDER_JSON_FILE

        self.verify_folder(self.DATA_DIR, "Data")

        if not os.path.isfile(file):
            open(file, "w").close()

        with open(file, "r") as f:
            try:
                result_list = json.load(f)
            except json.decoder.JSONDecodeError:
                f.close()
                os.remove(file)
                return None

        return result_list

    def get_mods_or_options(self, *, is_mods: bool) -> typing.List[str]:
        """
        Retrieves the available mods folders/options files
        :param is_mods: True: retrieves the available mods folders, False: retrieves the available options files
        :return: The list of mods folders/options files
        """

        # TODO if you wanted to be fancy you could get the folders in subdirectories, I don't want to be fancy though

        target_dir = self.MODS_FOLDERS_DIR if is_mods else self.OPTIONS_FOLDER_DIR

        # ignore files if looking for mods folders, and ignore folders if looking for options files
        if is_mods:
            result_list = [item for item in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, item))]
        else:
            result_list = [item for item in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, item))]

        return result_list

    def transfer_mods_or_options(self, src_location: str, *, is_mods: bool) -> bool:
        """
        Makes a link to the mods/options folder/file to be used by Forge/Minecraft
        :param src_location: Mods/Options folder/file to be linked to
        :param is_mods: True: linked as mods folder, False: linked as options file
        :return: Whether or not the function succeeded
        """

        print_debug(f"transfer_mods_options called, src: {src_location}, is_mods: {is_mods}")

        partial_src_dir = self.MODS_FOLDERS_DIR if is_mods else self.OPTIONS_FOLDER_DIR
        src_file_or_dir = os.path.join(partial_src_dir, src_location)

        if (not os.path.isdir(src_file_or_dir)) and is_mods:
            raise NotADirectoryError(f"{src_file_or_dir} is not a directory")

        if (not os.path.isfile(src_file_or_dir)) and (not is_mods):
            raise FileNotFoundError(f"{src_file_or_dir} is not a file")

        # TODO Perhaps implement a check to verify if the folder/file is backed up in the other folder doesnt get deleted without saving

        dst_dir = self.MODS_DIR if is_mods else self.OPTIONS_FILE
        if os.path.isfile(dst_dir):
            os.remove(dst_dir)
        elif os.path.isdir(dst_dir):
            os.rmdir(dst_dir)
        elif os.path.islink(dst_dir):
            os.unlink(dst_dir)

        try:
            os.symlink(src_file_or_dir, dst_dir)
        except OSError:
            print_debug("you need to enable symlinks")
            return False

        return True

    def rename_mods_or_options(self, src_name: str, dst_name: str, *, is_mods: bool) -> None:
        """
        Renames the mods/options folder/file
        :param src_name: The name of the folder/file to be renamed
        :param dst_name: The name the folder/file will be renamed to
        :param is_mods: True: renames a mods folder, False: renames an options file
        :return: None
        """
        partial_src = self.MODS_FOLDERS_DIR if is_mods else self.OPTIONS_FOLDER_DIR
        src_path = os.path.join(partial_src, src_name)
        dst_path = os.path.join(partial_src, dst_name)
        print_debug(f"renamed {src_path} to {dst_path}")
        # os.rename(src_path, dst_path)

    def resolve_mods_or_options_list(self, *, is_mods: bool) -> typing.List[str]:
        """
        Resolves the list of files/folders against the ordered list
        :param is_mods: True: resolves the list of mods folders, False: resolves the list of options files
        :return: The resolved list of mods folders/options files
        """

        file_list = self.get_mods_or_options(is_mods=is_mods)
        order_list = self.get_mods_or_options_order(is_mods=is_mods)

        if order_list is None:
            self.set_mods_or_options_order(file_list, is_mods=is_mods)
            return file_list

        reversed_result_list = order_list
        reversed_result_list.reverse()  # List is reversed so append() works at the beginning

        # Find each item that is in the list of files, but not in the ordered list, and adds it to the beginning of the ordered list
        for file_item in file_list:
            same = False
            for order_item in order_list:
                if file_item == order_item:
                    same = True
            if not same:
                reversed_result_list.append(file_item)

        # Find each item that is in the ordered list but not in the files list, and removes it from the ordered list
        for order_item in order_list:
            same = False
            for file_item in file_list:
                if file_item == order_item:
                    same = True
            if not same:
                reversed_result_list.remove(order_item)

        reversed_result_list.reverse()
        print_debug(f"list: {reversed_result_list}")
        self.set_mods_or_options_order(reversed_result_list, is_mods=is_mods)
        return reversed_result_list

    def get_minecraft_dir(self):
        self.verify_folder(self.DATA_DIR, "Data")

        minecraft_dir_info_file_default = "# Replace the line below with the path to your .minecraft folder\nInsert .minecraft path here\n# Note that entering a wrong or incomplete .minecraft path could have unintended affects, and the program will not run if the line is unchanged."

        print_debug(f"reading from: {self.MINECRAFT_DIR_INFO_FILE}")

        if not os.path.isfile(self.MINECRAFT_DIR_INFO_FILE):
            with open(self.MINECRAFT_DIR_INFO_FILE, "w") as f:
                f.write(minecraft_dir_info_file_default)

        with open(self.MINECRAFT_DIR_INFO_FILE) as f:
            if f.read() == minecraft_dir_info_file_default:
                raise IOError(f"Please change the .minecraft location info, in the file: {self.MINECRAFT_DIR_INFO_FILE}")

        with open(self.MINECRAFT_DIR_INFO_FILE) as f:
            minecraft_dir = [line.strip() for line in f.readlines() if not line[0] == "#"][0]

        print(minecraft_dir)
        return minecraft_dir


if __name__ == "__main__":
    mod_controller = ModController()
    print_debug(mod_controller.get_mods_or_options(is_mods=True))
    print_debug(mod_controller.get_mods_or_options(is_mods=False))
