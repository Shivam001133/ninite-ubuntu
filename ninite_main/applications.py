SNAP = 'sudo apt install snapd'

DOWNLOAD_DIRECTORY = '.download'

APPLICATION = {
    "VS Code": {
        "bash": False,
        'url': 'https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64',
        
    },
    "Sublime Text": {
        "bash": False,
        'url': 'https://download.sublimetext.com/sublime-text_build-3211_amd64.deb',
        'filename': 'sublime_text.deb'
    },
    "Google Chrome": {
        "bash": False,
        'url': 'https://www.google.com/chrome/next-steps.html?brand=CHBD&statcb=0&installdataindex=empty&defaultbrowser=0#',
        'filename': 'google_chrome.deb'
    },
    "Microsoft Edge": {
        "bash": False,
        'url': 'https://go.microsoft.com/fwlink?linkid=2149051&brand=M102',
        'filename': 'microsoft_edge.deb'
    },
    "Opera": {
        "bash": False,
        'url': 'https://download.opera.com/download/get/?partner=www&opsys=Linux&utm_campaign=%2307+-+IN+-+Search+-+EN+-+Branded+-+2017&utm_content=40191622276',
        'filename': 'opera.deb'
    },
    "Brave": {
        "bash": True,
        "install": {
            "apt": True,
            "snap": False,
            "curl": True
        },
        "code": [
            'sudo apt install curl',
            'sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg',
            'echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main"|sudo tee /etc/apt/sources.list.d/brave-browser-release.list',
            'sudo apt update',
            'sudo apt install brave-browser'
        ]
    },
    "Postman": {
        "bash": True,
        "install": {
            "apt": False,
            "snap": True,
            "curl": False
        },
        "code": 'sudo snap install postman'
    },
    "Vlc Media Player": {
        "bash": True,
        "install": {
            "apt": False,
            "snap": True,
            "curl": False
        },
        "code": 'sudo snap install vlc'
    },
}
