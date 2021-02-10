import json
import os
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

        self.CURRENT_DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep
        self.MODS_ORDER_JSON_FILE = os.path.join(self.CURRENT_DIR, "mods_list.json")
        self.OPTIONS_ORDER_JSON_FILE = os.path.join(self.CURRENT_DIR, "options_list.json")

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

    def set_mods_or_options_order(self, mods_list: typing.List[str], *, is_mods: bool) -> None:
        """
        Stores the ordered list of mods/options in a json file
        :param mods_list: The list of mods/options to be stored
        :param is_mods: True: stored as a list of mods, False: stored as a list of options
        :return: None
        """

        file = self.MODS_ORDER_JSON_FILE if is_mods else self.OPTIONS_ORDER_JSON_FILE

        with open(file, "w") as outfile:
            json.dump(mods_list, outfile)

    def get_mods_or_options_order(self, *, is_mods: bool) -> typing.List[str]:
        """
        Retrieves the ordered list of mods/options
        :param is_mods: True: retrieves the ordered list of mods, False: retrieves the ordered list of options
        :return: The ordered list of options or mods
        """

        file = self.MODS_ORDER_JSON_FILE if is_mods else self.OPTIONS_ORDER_JSON_FILE

        with open(file, "r") as f:
            result_list = json.load(f)

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

    def transfer_mods_or_options(self, src_location: str, *, is_mods: bool) -> None:
        """
        Makes a link to the mods/options folder/file to be used by Forge/Minecraft
        :param src_location: Mods/Options folder/file to be linked to
        :param is_mods: True: linked as mods folder, False: linked as options file
        :return: None
        """

        partial_src_dir = self.MODS_FOLDERS_DIR if is_mods else self.OPTIONS_FOLDER_DIR
        src_file_or_dir = os.path.join(partial_src_dir, src_location)

        if (not os.path.isdir(src_file_or_dir)) and is_mods:
            raise NotADirectoryError(f"{src_file_or_dir} is not a directory")

        if (not os.path.isfile(src_file_or_dir)) and (not is_mods):
            raise FileNotFoundError(f"{src_file_or_dir} is not a file")

        # TODO Perhaps implement a check to verify if the folder/file is backed up in the other folder doesnt get deleted without saving

        dst_dir = self.MODS_DIR if is_mods else self.OPTIONS_FILE
        os.unlink(dst_dir)
        os.symlink(src_file_or_dir, dst_dir)

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
        print(f"renamed {src_path} to {dst_path}")
        # os.rename(src_path, dst_path)

    def resolve_mods_or_options_list(self, *, is_mods: bool) -> typing.List[str]:
        """
        Resolves the list of files/folders against the ordered list
        :param is_mods: True: resolves the list of mods folders, False: resolves the list of options files
        :return: The resolved list of mods folders/options files
        """

        file_list = self.get_mods_or_options(is_mods=is_mods)
        order_list = self.get_mods_or_options_order(is_mods=is_mods)

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
        print(f"list: {reversed_result_list}")
        self.set_mods_or_options_order(reversed_result_list, is_mods=is_mods)
        return reversed_result_list


if __name__ == "__main__":
    mod_controller = ModController()
    print(mod_controller.get_mods_folders())
    print(mod_controller.get_options_files())
