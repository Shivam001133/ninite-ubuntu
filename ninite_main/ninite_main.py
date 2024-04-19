from ninite_main import applications
from ninite_main import messages as mess
from urllib.parse import urlparse
from ninite_main import config as conf
import requests
from datetime import datetime
import shutil
import os
from tqdm import tqdm
import logging
import curses

logger = logging.getLogger(__name__)


class NINITE:
    """
    The NINITE class manages software downloads and installations.

    It provides functionalities to download files from URLs, display
    text-based menus for user interaction, prompt for user input, and
    handle DEB package installations.
    """
    def __init__(self) -> None:
        self.DOWNLOAD_DIRECTORY = conf.DOWNLOAD_DIRECTORY
        self.APPLICATION = applications.APPLICATION

    def download_file(self, url):
        """
        Downloads a file from the specified URL and saves it to the
        download directory.

        This function retrieves a file from a given URL and stores it in the
        class's download directory.
        It utilizes a progress bar to display the download progress.

        Args:
            url (str): The URL of the file to download.

        Returns:
            str: The path to the downloaded file.

        Raises:
            Exception: If the download fails or the filename extraction
            encounters issues.
        """
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte

        # Create the download directory if it doesn't exist
        if not os.path.exists(self.DOWNLOAD_DIRECTORY):
            os.makedirs(self.DOWNLOAD_DIRECTORY)

        # Extract filename from URL
        url_path = urlparse(url).path
        filename = os.path.basename(url_path)

        if not filename or filename == '/' or not filename.endswith(".deb"):
            filename = f"{datetime.now()}.deb".replace(" ", "")

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
        print("\n")
        return file_path

    def display_options(self):
        """Displays a text-based menu for the user to select options.

        This function utilizes the curses library to create a user interface
        where the user can navigate through available options and select
        multiple choices.

        Args:
            self: An instance of the class using this function.
                It's assumed to have an `APPLICATION` attribute
                containing a dictionary mapping option names to
                their corresponding functionalities.

        Returns:
            A list of strings representing the option keys selected by the
            user.
        """

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
        # hovering = False

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
                        # hovering = False
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
        """Prompts the user for comma-separated integer choices.

        This function prompts the user to enter a comma-separated list of
        integers. It handles various input formats, including single values,
        spaces around commas, and leading/trailing spaces. It returns a
        unique, sorted list of the integers.

        If an invalid input is encountered (e.g., non-numeric characters, empty
        strings), a clear error message is printed and the user is prompted to
        re-enter their choice.

        Args:
            self (object): The calling object (likely used for logging
            purposes).

        Returns:
            list[int]: A unique, sorted list of the integers provided by the
            user.

        Raises:
            ValueError: If the user enters an empty string or non-numeric
            characters.
        """

        while True:
            choice = input().strip()

            if not choice:  # Check for empty string
                print("Invalid input: Please enter comma-separated integers.")
                continue

            try:
                # Handle various comma and whitespace formats
                input_data = [int(data.strip()) for data in choice.split(',')
                              if data.strip()]
                return sorted(list(set(input_data)))  # Unique and sorted
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter only "
                      "comma-separated integers.")

    def pakage_manager(self) -> None:
        """
        Installs all DEB packages found in the configured download directory.

        This function iterates through all files with the `.deb` extension
        within the download directory specified by `conf.DOWNLOAD_DIRECTORY`.
        For each DEB package, it attempts the following actions:

        1. Installs the package using `sudo dpkg -i <package_name>`.
        2. Removes the installed package file from the download directory.

        If any errors occur during installation, the error message is logged
        using the provided `logger` object. If the download directory does not
        exist, an informative message is logged, indicating that either no DEB
        packages were downloaded or an
        issue might have occurred.

        **Raises:**

        - `OSError`: If an error occurs while interacting with the file system
                    (e.g., issues with directory permissions, file existence).

        **Arguments:**

        - None

        **Returns:**

        - None

        **Pre-conditions:**

        - The `conf` module must be imported and provide a constant
            `conf.DOWNLOAD_DIRECTORY` containing the path to the download
            directory.
        - A logger object (e.g., from the `logging` module) must be available
            for error logging.
        """

        if os.path.exists(conf.DOWNLOAD_DIRECTORY):
            deb_pakages = os.listdir(conf.DOWNLOAD_DIRECTORY)
            for pakage in deb_pakages:
                try:
                    os.system(f"sudo dpkg -i download/{pakage}")
                    os.rmdir(f"download/{pakage}")
                except Exception as e:
                    logger.error(f"Encounter this error: {e}")

            shutil.rmtree(conf.DOWNLOAD_DIRECTORY)
        else:
            logger.info(mess.DOWNLOAD_FOLDER_NOT_FOUND)
