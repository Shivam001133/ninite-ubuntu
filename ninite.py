from ninite_main.ninite_main import NINITE
import ninite_main.config as conf

import os
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    ninite = NINITE()
    choices = ninite.display_options()

    for choice in choices:
        if ninite.APPLICATION[choice]["bash"]:
            if ninite.APPLICATION[choice]['method']['apt']:
                if ninite.APPLICATION[choice]['method']['snap']:
                    if not conf.INSTALL_METHOD['snap']:
                        os.system("sudo apt install snap")
                        conf.INSTALL_METHOD['snap'] = True
                    # installing package
                    print("****", ninite.APPLICATION[choice]['bash_code'])
                    os.system(ninite.APPLICATION[choice]['bash_code'])
                elif ninite.APPLICATION[choice]['method']['curl']:
                    if not conf.INSTALL_METHOD['curl']:
                        os.system("sudo apt install curl")
                        conf.INSTALL_METHOD['curl']
                    # installing pakage
                    print("**", ninite.APPLICATION[choice]['bash_code'])
                    os.system(ninite.APPLICATION[choice]['bash_code'])
                else:
                    print("****", ninite.APPLICATION[choice]['bash_code'])
                    os.system(ninite.APPLICATION[choice]['bash_code'])
        else:
            ninite.download_file(
                ninite.APPLICATION[choice]["url"],
                # ninite.APPLICATION[choice]["filename"]
            )
            if not conf.DOWNLOAD_DEB:
                conf.DOWNLOAD_DEB = True
    # fucntion which install deb files
    if conf.DOWNLOAD_DEB:
        ninite.pakage_manager()
