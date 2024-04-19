from ninite_main import applications
from ninite_main import messages as mess
from urllib.parse import urlparse
import requests
from datetime import datetime
import os
from tqdm import tqdm
import logging
import curses

logger = logging.getLogger(__name__)


class NINITE:
    def __init__(self) -> None:
        self.DOWNLOAD_DIRECTORY = applications.DOWNLOAD_DIRECTORY
        self.APPLICATION = applications.APPLICATION

    def generate_unique_filename(self, url):
        pass



    def download_file(self, url):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte

        # Create the download directory if it doesn't exist
        if not os.path.exists(self.DOWNLOAD_DIRECTORY):
            os.makedirs(self.DOWNLOAD_DIRECTORY)

        # Extract filename from URL
        url_path = urlparse(url).path
        filename = os.path.basename(url_path)

        # If filename is empty or just '/', generate a unique filename
        #if not filename or filename == '/' or not filename.endwith(".deb"):
           # filename = 

        file_path = os.path.join(self.DOWNLOAD_DIRECTORY, filename)

        with open(file_path, 'wb') as f, tqdm(
            desc=filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
            dynamic_ncols=True,
        ) as progress_bar:
            for data in response.iter_content(block_size):
                f.write(data)
                progress_bar.update(len(data))

        return file_path

    def display_options(self):
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)

        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

        max_y, max_x = stdscr.getmaxyx()
        num_cols = 4  # Number of columns for displaying options

        option_keys = list((self.APPLICATION.keys()))
        num_rows = (len(option_keys) + num_cols - 1) // num_cols

        current_selection = set()
        current_idx = 0
        selecting = False
        hovering = False

        while True:
            stdscr.clear()
            stdscr.addstr("\nOptions:\n\n")

            for row in range(num_rows):
                for col in range(num_cols):
                    idx = row * num_cols + col
                    if idx < len(option_keys):
                        key = option_keys[idx]

                        # Adjusted formatting to reduce space and selector size
                        if idx in current_selection:
                            if selecting and idx == current_idx:
                                stdscr.addstr(
                                    f"[*]{key.ljust(14)}",
                                    curses.color_pair(1))
                            else:
                                stdscr.addstr(
                                    f"[*]{key.ljust(14)}",
                                    curses.A_NORMAL)
                        else:
                            if selecting and idx == current_idx:
                                stdscr.addstr(
                                    f"[ ]{key.ljust(14)}",
                                    curses.color_pair(1))
                            else:
                                stdscr.addstr(
                                    f"[ ]{key.ljust(14)}",
                                    curses.A_NORMAL)
                    stdscr.addstr("\t" if col < num_cols - 1 else "")

                stdscr.addstr("\n")

            stdscr.addstr(mess.SELECTING_MESSAGE)

            stdscr.refresh()

            key = stdscr.getch()
            if key == ord('i'):  # Start selecting
                selecting = True
            elif key == ord('q'):  # End selecting
                break
            elif selecting:
                if key == curses.KEY_UP:
                    if current_idx - num_cols >= 0:
                        current_idx -= num_cols
                    else:
                        current_idx = len(option_keys) - 1
                elif key == curses.KEY_DOWN:
                    if current_idx + num_cols < len(option_keys):
                        current_idx += num_cols
                    else:
                        current_idx = 0
                elif key == curses.KEY_LEFT:
                    if current_idx > 0:
                        current_idx -= 1
                elif key == curses.KEY_RIGHT:
                    if current_idx < len(option_keys) - 1:
                        current_idx += 1
                elif key in [curses.KEY_ENTER, 10, 13]:
                    if selecting:
                        if current_idx in current_selection:
                            current_selection.remove(current_idx)
                        else:
                            current_selection.add(current_idx)
                        hovering = False
                    else:
                        selecting = True
                elif key == ord('r'):  # Remove selected option
                    if current_idx in current_selection:
                        current_selection.remove(current_idx)
            else:
                if key == curses.KEY_UP:
                    if current_idx - num_cols >= 0:
                        current_idx -= num_cols
                    else:
                        current_idx = len(option_keys) - 1
                elif key == curses.KEY_DOWN:
                    if current_idx + num_cols < len(option_keys):
                        current_idx += num_cols
                    else:
                        current_idx = 0
                elif key == curses.KEY_LEFT:
                    if current_idx > 0:
                        current_idx -= 1
                elif key == curses.KEY_RIGHT:
                    if current_idx < len(option_keys) - 1:
                        current_idx += 1
                elif key == ord('i'):  # Start selecting
                    selecting = True
                elif key == ord('q'):  # End selecting
                    break
                elif key == curses.KEY_RESIZE:
                    max_y, max_x = stdscr.getmaxyx()

        curses.endwin()
        selected_options = [option_keys[idx] for idx in sorted(
            current_selection)]
        return selected_options

    def get_user_choice(self):
        choice = input("Enter your choice: ").strip()
        if ',' in choice:
            input_data = [data.strip() for data in choice.split(',') if data]
            return [int(data) for data in list(set(input_data)) if data]
        else:
            try:
                input_data = [data.strip() for data in choice.split(
                    ',') if data]
                print("input", input_data)
                input_data = [int(data) for data in list(
                    set(input_data)) if data]
                print("input", input_data)
                return input_data
            except Exception as e:
                logger.error(f"Encounter his error: {e} ")

    def deb_installer(self):
        import subprocess
        BASE_DIE = os.getpwd()

        d_dir = BASE_DIE + "/download"
        files_and_directories = os.listdir(d_dir)
        for file_or_directory in files_and_directories:
            if file_or_directory.endswith(".deb"):
                subprocess.run[f'sudo dpkg -i download/{file_or_directory}']
            else:
                logger.info(f"ihis file `{file_or_directory}` is not deb file")
