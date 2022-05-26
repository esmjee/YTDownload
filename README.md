# YouTube downloader

Download YouTube videos quickly and without any hussle

Downloading videos from YouTubes website is against their Terms Of Service, use this program on your own risk.

## Motivation

I dislike the online converters, because they are slow and sometimes download corrupt files. I can run this program easily whenever I want to download a youtube video or song, without having to also convert the video to mp3 myself.

## Run it yourself

### Presequence

1. Make sure you have [Python](https://www.python.org/downloads/) 3.9.4 or higher

2. Make sure you have [Git](https://git-scm.com/downloads) installed

3. Make sure you have the python packages
- pip install pytube
- pip install datetime
- pip install os
- pip install moviepy
- pip install sys
- pip install regex
- pip install urllib3

### Running the application

1. Open a terminal (cmd, powershell, terminal..)

2. Type `git clone https://github.com/6fy/YTDownloader.git`
- This will clone all the files onto your pc

3. Type `cd YTDownloader`
- This will make YTDownloader your *current directory* which will allow you to run the program

4. Type `python main.py`
- This will run the script

### Make the file an executable

1. Download [pyinstaller](https://pypi.org/project/pyinstaller/) by typing `pip install pyinstaller` in a terminal

2. Make sure your current directory includes the main.py script
- If it doesn't type `cd *folder*/` until it is

3. Type `pyinstaller --onefile main.py`

4. Wait until it is finished converting

5. Open `dist/`

6. Run the executable