import os
import time
import shutil
import tkinter as tk
from datetime import datetime


class ReturnalGame:
    def __init__(self):
        self.returnal_folder = os.path.join(
            os.environ['USERPROFILE'], 'AppData\Local\Returnal\Steam\Saved\\')
        self.backup_folder = self.returnal_folder+'Backup'

    def check_current_saved(self):
        file_path = os.path.join(self.returnal_folder,
                                 'SaveGames', 'saveprofile.sav')
        if os.path.exists(file_path):
            mod_time = os.path.getmtime(file_path)
            mod_time_str = time.ctime(mod_time)
            mod_time_dt = datetime.fromtimestamp(mod_time)
            print(f"Current Returnal Saved Game is from {mod_time_str}.")
            return mod_time_dt
        else:
            print(f"The file {file_path} does not exist.")

    def copy_files(self, source_dir, dest_dir):
        files_to_copy = ['SaveProfile.sav',
                         'SaveProfile.susres.sav', 'SaveProfile.susresvalid.sav']

        for file in files_to_copy:
            source_path = os.path.join(source_dir, file)
            dest_path = os.path.join(dest_dir, file)
            shutil.copy(source_path, dest_path)
            print(f"File '{file}' copied to '{dest_dir}'")

    def save_current_game(self, current_saved_timestamp):
        timestamp = current_saved_timestamp.strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = f"save_{timestamp}"
        folder_path = os.path.join(self.backup_folder, folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            message = f"Folder '{folder_name}' created. Game saved!"

            source_dir = os.path.join(self.returnal_folder, 'SaveGames')
            dest_dir = folder_path
            self.copy_files(source_dir, dest_dir)
        else:
            message = f"Folder '{folder_name}' already exists. Game not saved."

        return message

    def load_saved_game(self, savegame_folder):
        if os.path.exists(savegame_folder):
            dest_dir = os.path.join(self.returnal_folder, 'SaveGames')
            source_dir = savegame_folder
            self.copy_files(source_dir, dest_dir)
        else:
            print('error, no se pudo loadear')


class ReturnalApp:
    def __init__(self, returnal_game):
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

        backup_folders = os.listdir(self.returnal_game.backup_folder)
        for folder_name in backup_folders:
            self.backup_listbox.insert(tk.END, folder_name)

        self.save_button.pack(side="top")
        self.load_button.pack(side="top")
        self.backup_listbox.pack()
        self.output_text.pack()
        self.exit_button.pack()

    def save_game(self):
        current_saved_time = self.returnal_game.check_current_saved()
        message = self.returnal_game.save_current_game(current_saved_time)
        self.refresh_saved_games_list()
        self.output_text.insert(tk.END, f"{message}\n")

    def load_game(self):
        selection = self.backup_listbox.curselection()
        if selection:
            index = selection[0]
            folder_name = self.backup_listbox.get(index)
            folder_path = os.path.join(
                self.returnal_game.backup_folder, folder_name)
            self.returnal_game.load_saved_game(folder_path)
            self.output_text.insert(
                tk.END, f"Game loaded from {folder_path}.\n")
        else:
            self.output_text.insert(
                tk.END, "Please select a backup folder to load.\n")

    def exit_app(self):
        self.window.destroy()

    def refresh_saved_games_list(self):
        self.backup_listbox.delete(0, tk.END)
        self.backup_folders = os.listdir(self.returnal_game.backup_folder)
        self.backup_folders.sort(reverse=True)
        for folder_name in self.backup_folders:
            self.backup_listbox.insert(tk.END, folder_name)
        self.backup_listbox.select_set(0)

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    returnal_game = ReturnalGame()
    returnal_app = ReturnalApp(returnal_game)
    returnal_app.run()
