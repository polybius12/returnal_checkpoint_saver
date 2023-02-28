import os
import time
import shutil
import tkinter as tk
from datetime import datetime


class ReturnalGame:
    """
    This class represents the Returnal game and provides methods for saving and loading Checkpoints.

    Attributes:
        returnal_folder (str): The path to the folder where the Returnal Checkpoints are stored.
        backup_folder (str): The path to the folder where the Checkpoints backups will be stored.
    """

    def __init__(self):
        self.returnal_folder = os.path.join(
            os.environ['USERPROFILE'], 'AppData\Local\Returnal\Steam\Saved\\')
        self.backup_folder = self.returnal_folder+'Backup'

    def check_current_saved(self) -> datetime:
        """
        Check the timestamp of the current Returnal Checkpoint file.

        Returns:
            datetime: The timestamp of the current Checkpoint file.
        """
        file_path = os.path.join(self.returnal_folder,
                                 'SaveGames', 'saveprofile.sav')
        if os.path.exists(file_path):
            mod_time = os.path.getmtime(file_path)
            mod_time_str = time.ctime(mod_time)
            mod_time_dt = datetime.fromtimestamp(mod_time)
            print(f"Current Returnal Checkpoint is from {mod_time_str}.")
            return mod_time_dt
        else:
            print(f"The file {file_path} does not exist.")

    def copy_files(self, source_dir: str, dest_dir: str) -> None:
        """
        Copy the specified files from source directory to destination directory.

        Args:
            source_dir (str): The path to the source directory.
            dest_dir (str): The path to the destination directory.

        Returns:
            None
        """
        files_to_copy = ['SaveProfile.sav',
                         'SaveProfile.susres.sav',
                         'SaveProfile.susresvalid.sav']

        for file in files_to_copy:
            source_path = os.path.join(source_dir, file)
            dest_path = os.path.join(dest_dir, file)
            shutil.copy(source_path, dest_path)
            print(f"File '{file}' copied to '{dest_dir}'")

    def save_current_game(self, current_saved_timestamp: datetime) -> str:
        """
        Save the current Returnal game by backing up the Checkpoint files.

        Args:
            current_saved_timestamp (datetime): The timestamp of the current Checkpoint file.

        Returns:
            str: A message indicating whether the game was successfully saved or not.
        """
        timestamp = current_saved_timestamp.strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = f"save_{timestamp}"
        folder_path = os.path.join(self.backup_folder, folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            message = f"Folder '{folder_name}' created. Checkpoint saved!"

            source_dir = os.path.join(self.returnal_folder, 'SaveGames')
            dest_dir = folder_path
            self.copy_files(source_dir, dest_dir)
        else:
            message = f"Folder '{folder_name}' already exists. Checkpoint not saved."

        return message

    def load_saved_game(self, savegame_folder: str) -> None:
        """
        Load a Checkpoint by copying the Checkpoint files from a specified folder to the Returnal game folder.

        Args:
            savegame_folder (str): The path to the folder containing the Checkpoint files.

        Returns:
            None
        """
        if os.path.exists(savegame_folder):
            dest_dir = os.path.join(self.returnal_folder, 'SaveGames')
            source_dir = savegame_folder
            self.copy_files(source_dir, dest_dir)
        else:
            print('Error loading checkpoint')


class ReturnalApp:
    """
    A class representing a graphical user interface for the Returnal game checkpoint saver.
    Attributes:
    -----------
    returnal_game : ReturnalGame
        A ReturnalGame object to interact with the Checkpoint files.
    window : tkinter.Tk
        The main window of the application.
    save_button : tkinter.Button
        A button to save the current game checkpoint.
    load_button : tkinter.Button
        A button to load a Checkpoint checkpoint.
    exit_button : tkinter.Button
        A button to exit the application.
    backup_listbox : tkinter.Listbox
        A listbox displaying all Checkpoint checkpoints.
    output_text : tkinter.Text
        A text widget to display application output.
    backup_folders : List[str]
        A list of all Checkpoint checkpoints.

    Methods:
    --------
    save_game()
        Saves the current game checkpoint and refreshes the backup listbox.
    load_game()
        Loads a Checkpoint checkpoint and displays a message to the output_text widget.
    exit_app()
        Exits the application.
    refresh_saved_games_list()
        Refreshes the backup listbox with all Checkpoint checkpoints.
    run()
        Runs the graphical user interface.
    """

    def __init__(self, returnal_game: ReturnalGame):
        """
        Constructs a ReturnalApp object.

        Parameters:
        -----------
        returnal_game : ReturnalGame
            A ReturnalGame object to interact with the Checkpoint files.
        """
        self.returnal_game = returnal_game
        self.window = tk.Tk()
        self.window.title("Returnal Checkpoint Saver v0.1")

        self.save_button = tk.Button(
            self.window, text="Save Checkpoint", width=20, height=2, command=self.save_game)
        self.load_button = tk.Button(
            self.window, text="Restore Checkpoint", width=20, height=2, command=self.load_game)
        self.exit_button = tk.Button(
            self.window, text="Exit", command=self.exit_app)

        self.backup_listbox = tk.Listbox(self.window, width=50, height=10)

        self.output_text = tk.Text(self.window, width=50, height=10)

        self.refresh_saved_games_list()

        self.save_button.pack(side="top")
        self.load_button.pack(side="top")
        self.backup_listbox.pack()
        self.output_text.pack()
        self.exit_button.pack()

    def save_game(self):
        """
        Saves the current game checkpoint and refreshes the backup listbox.
        """
        current_saved_time = self.returnal_game.check_current_saved()
        message = self.returnal_game.save_current_game(current_saved_time)
        self.refresh_saved_games_list()
        self.output_text.insert(tk.END, f"{message}\n")

    def load_game(self):
        """
        Loads a Checkpoint checkpoint and displays a message to the output_text widget.
        """
        selection = self.backup_listbox.curselection()
        if selection:
            index = selection[0]
            folder_name = self.backup_listbox.get(index)
            folder_path = os.path.join(
                self.returnal_game.backup_folder, folder_name)
            self.returnal_game.load_saved_game(folder_path)
            self.output_text.insert(
                tk.END, f"Checkpoint loaded from {folder_path}.\n")
        else:
            self.output_text.insert(
                tk.END, "Please select a Checkpoint folder to load.\n")

    def exit_app(self):
        """
        Exits the application.
        """
        self.window.destroy()

    def refresh_saved_games_list(self):
        """Refreshes the backup listbox with all Checkpoint checkpoints."""
        self.backup_listbox.delete(
            0, tk.END)  # delete all current items from the listbox
        # get all folders in the backup folder
        self.backup_folders = os.listdir(self.returnal_game.backup_folder)
        # sort the folders in descending order by date
        self.backup_folders.sort(reverse=True)
        for folder_name in self.backup_folders:
            # insert each folder name into the listbox
            self.backup_listbox.insert(tk.END, folder_name)
            # select the first item in the listbox
            self.backup_listbox.select_set(0)

    def run(self):
        """Runs the GUI application."""
        self.window.mainloop()  # start the main event loop of the GUI application


if __name__ == '__main__':
    returnal_game = ReturnalGame()  # create a new ReturnalGame object
    # create a new ReturnalApp object with the ReturnalGame object as an argument
    returnal_app = ReturnalApp(returnal_game)
    returnal_app.run()  # run the ReturnalApp object
