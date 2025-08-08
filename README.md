
<img width="709" height="319" alt="Screenshot 2025-08-07 at 8 48 17 PM" src="https://github.com/user-attachments/assets/6bbe4e3b-9cac-4376-83f0-353a5915cb7e" />

###############################
# Setup Instructions 5 minutes:
###############################

> `Step 1 Setup Python`:
- Download python at this link by clicking on the yellow button: https://www.python.org/downloads/
- IMPORTANT: When you run the installer make sure to check the 2 squares that say `add Python to Path` and `Install launcher for all users`

> `Step 2 Download Packages`:
- Now open terminal or command prompt on your computer and run these commands one by one:
- pip install colorama
- pip install nodriver
- pip install -U camoufox[geoip]
- python3 -m camoufox fetch

> `Step 3 Download Chromium Browser`:
- For MacOS Follow these steps
    - Go to this link: https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Mac_Arm/1000282/
    - Download the file “chrome-mac.zip”
    - Once downloaded go to the downloads folder and drag the blue Chromium app to the applications folder
    - Open terminal and run these commands on at a time:
        - chmod +x /Applications/Chromium.app/Contents/MacOS/Chromium
        - xattr -cr /Applications/Chromium.app
- For Windows Follow these steps
    - Go to this link: https://chromium.woolyss.com/download/en/
    - Click on the blue button that says "Chromium 64-bit (.exe)"
    - Run the downloaded installer

#######################
# Running Instructions:
#######################

- Open Terminal or Command Prompt
- Run these commands one by one:
    - cd Downloads
    - cd sentry
    - python main.py

#######################
# Tips:
#######################

- It is recommended to include proxies inside the `proxies.txt` file. If you dont want to use proxies keep that file empty, otherwise input your own proxies into that file. Keep the `proxies.txt` file right next to the sentry app
- The chromium option is tested and guarenteed to work on websites such as Target that have Shape security
- You can play around between both browsers and see what works better for you
- The "cd" command means change directory and you can techincally put the sentry folder wherever you want, but then your gonna have to change up the cd commands above to actually cd into the new spot
