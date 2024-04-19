APPLICATION = {
    "VS bash_code": {
        "bash": False,
        'url': 'https://bash_code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64',
    },
    "Sublime Text": {
        "bash": False,
        'url': 'https://download.sublimetext.com/sublime-text_build-3211_amd64.deb',
        'filename': 'sublime_text.deb'
    },
    "Google Chrome": {
        "bash": False,
        'url': 'https://www.google.com/chrome/next-steps.html?brand=CHBD&statcb=0&methoddataindex=empty&defaultbrowser=0#',
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
        "method": {
            "apt": True,
            "snap": False,
            "curl": True
        },
        "bash_code": (
            'sudo apt method curl'
            'sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg'
            'echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main"|sudo tee /etc/apt/sources.list.d/brave-browser-release.list'
            'sudo apt update'
            'sudo apt method brave-browser'
            )
    },
    "Postman": {
        "bash": True,
        "method": {
            "apt": False,
            "snap": True,
            "curl": False
        },
        "bash_code": 'sudo snap method postman'
    },
    "Vlc Media Player": {
        "bash": True,
        "method": {
            "apt": False,
            "snap": True,
            "curl": False
        },
        "bash_code": 'sudo snap method vlc'
    },
}
