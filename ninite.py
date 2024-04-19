from ninite_main.ninite_main import NINITE
import shutil

import logging

logger = logging.getLogger(__name__)


def pakage_manager():
    import os

    deb_pakages = os.listdir("download/")
    for pakage in deb_pakages:
        try:
            os.system(f"sudo dpkg -i download/{pakage}")
            os.rmdir(f"download/{pakage}")
        except Exception as e:
            logger.error(f"Encounter this error: {e}")

    shutil.rmtree('download/')


if __name__ == "__main__":
    ninite = NINITE()
    choices = ninite.display_options()
    for choice in choices:
        if ninite.APPLICATION[choice]["bash"]:
            pass
        else:
            ninite.download_file(
                ninite.APPLICATION[choice]["url"],
                # ninite.APPLICATION[choice]["filename"]
            )
    pakage_manager()
