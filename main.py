try:
    print('importing modules...')
    from pytube import YouTube
    from datetime import datetime
    import os
    from moviepy.video.io.VideoFileClip import VideoFileClip
    import sys
    import time
    from pypresence import Presence
    import random
    import json
    import re
    import urllib.request
    import time
    import string
except (ImportError or ModuleNotFoundError) as importError:
    print("""
    You need to install all the modules
    - pip install pytube
    - pip install datetime
    - pip install os
    - pip install moviepy
    - pip install sys
    - pip install regex
    - pip install pypresence
    - pip install urllib3
    """)
    input('Press enter to close this window.')
    sys.exit(1)

AUTHOR = "https://github.com/6fy"
DOWNLOAD_PATH = "downloads/"
MAX_RESULTS = 5

QUIT_CHARS = ["quit", "q", "cancel", "none", "exit", "close"]
VALID_CHARS = list(string.ascii_lowercase + " " + string.digits)

class Downloader:
    def __init__(self):
        self.link = ''

    # ========================= >
    # Sets the link and runs main
    # < =========================
    def set_program(self, link):
        self.link = link
        self.main()


    # ========================= >
    # Returns the link for the Discord presence
    # < =========================
    def get_link(self):
        return self.link


    # ========================= >
    # Sets the Discord presence
    # < =========================
    def set_presence(self, presence):
        game = ""
        
        data = read_json_file()
        if data and data.get('game'):
            games = data.get('game')
            game = random.choice(games) if type(games) == list else games

        RPC.update(
            large_image = "original",
            large_text = "This is a cat",
            details = presence,
            state = game,
            start = start,
        )


    # ========================= >
    # Create a new folder for the video
    # < =========================
    def new_video_folder(self, folder):
        """
        This function checks if the path exists if it doesn't then creates the path\n
        folder = the folder name
        """
        path = os.getcwd() + "/" + DOWNLOAD_PATH + folder
        if not os.path.exists(path):
            os.makedirs(path)

        return path


    # ========================= >
    # log video details
    # < =========================
    def log_video_details(self, yt):
        """
        This function logs details of the video\n
        yt = youtube object
        """
        minutes = yt.length / 60
        log('\n---------------------------------------')
        log(f"Title: {yt.title}")
        log(f'Url: https://www.youtube.com/watch?v={yt.video_id}')
        log(f"Number of views: {yt.views}")
        log(f"Length of video: {round(minutes, 2)} minutes ({yt.length} seconds)")
        log('---------------------------------------\n')


    # ========================= >
    # Download the video
    # < =========================
    def download_video(self, yt, currentTime):
        """
        This function downloads the video\n
        yt = youtube object
        currentTime = current time, to create a folder with that day
        """
        ys = yt.streams.get_highest_resolution()

        #Starting download
        log(f'Downloading "{yt.title}"...')
        log(f"Details: {ys}")

        path = self.new_video_folder(currentTime)
        file_name = ys.download(path)

        return file_name


    # ========================= >
    # Converting the video to mp3
    # < =========================
    def convert_to_sound(self, currentTime, title):
        """
        This function converts the video to mp3\n
        yt = YouTube object\n
        path = path to save the mp3 file\n
        """
        try:
            path = self.new_video_folder(currentTime)

            video = VideoFileClip(os.path.join(path, title))
            video.audio.write_audiofile(os.path.join(path, title + ".mp3"))
        except Exception as e:
            log(e)
            log("Error: An exception occurred trying to write to mp3.")
            return False
        return True


    # ========================= >
    # Get the youtube url from title from url
    # < =========================
    def convert_to_url(self, title):
        """
        This function get the youtube title from the link if it wasn't a link but text\n
        title = the title of the video aka the link
        """
        log('looking at youtube...')

        # Send a request with the text
        search_keyword = title.replace(' ', '+')
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
        search_results = re.findall(r'watch\?v=(.{11})', html.read().decode())
        # Return if no results were found

        if len(search_results) == 0:
            return None

        return search_results


    # ========================= >
    # log the available results
    # < =========================
    def log_results(self, results):
        f"""
        This function logs {MAX_RESULTS} results from youtube and returns them in an array\n
        results = the url results from youtube
        """
        # Get the first MAX_RESULTS (default is 5) results
        videos = []
        results_used = []
        i = 0
        for result in results:
            try:
                if (i == MAX_RESULTS): break

                if (result not in results_used):
                    yt = YouTube('https://www.youtube.com/watch?v=' + result)

                    minutes = yt.length / 60
                    log(f'---------------------- =({i + 1})= ----------------------')
                    log(f"Title: {yt.title}")
                    log(f"Number of views: {yt.views}")
                    log(f'Url: https://www.youtube.com/watch?v={result}')
                    log(f"Length of video: {round(minutes, 2)} minutes ({yt.length} seconds)")
                    log('---------------------------------------------------\n')

                    results_used.append(result)
                    videos.append(yt)
                    i += 1

            except:
                pass

        return videos


    # ========================= >
    # Get the user to choose a video
    # < =========================
    def get_user_choice(self, videos):
        """
        This function gets the user to choose a video from the list of videos\n
        videos = youtube objects in an array
        """
        users_pick = 0
        # Ask user to choose a video
        while 1:
            choice = input('Enter the number of the video you want to download ("cancel" to cancel): ')
            if any(word in QUIT_CHARS for word in choice.split(" ")):
                return None

            try:
                pick = int(choice)

                if (pick > len(videos) or pick <= 0):
                    log('Invalid choice')
                    continue

                users_pick = pick
                break
            except ValueError:
                log('Invalid choice')

        return videos[users_pick - 1]


    # ========================= >
    # Main function
    # < =========================
    def main(self):
        """
        This function runs the programs and enters all the steps\n
        to complete the download process
        """
        try:
            # Get youtube video from link
            yt = YouTube(self.link)
        except:
            # Get results from the link as youtube title
            results = self.convert_to_url(self.link)
            if (results == None):
                log('No results found')
                return
            else:
                log(f'found {len(results)} results...')

            # Get 5 of the most viewed videos
            videos = self.log_results(results)

            # Get users input of which video they want to download
            yt = self.get_user_choice(videos)
            if yt == None:
                return

        # Current time for the directory
        now = datetime.now()
        currentTime = now.strftime("%d-%m-%Y")

        # Download the video and return the file name to convert it to mp3 later
        title = self.download_video(yt, currentTime)
        time.sleep(0.5) # Wait for the video to download, so there is no OSError
        succeeded = self.convert_to_sound(currentTime, title)

        log("Download completed!" if succeeded else "The download is incomplete, because of an error.")
        print('\n')

def read_json_file():
    """
    This function reads the json file and returns the data
    """
    try:
        f = open(DOWNLOAD_PATH + 'config.json', 'r')
        data = json.load(f)
        return data
    except Exception as ignored:
        log(f'Error: No {DOWNLOAD_PATH}config.json file found')
        return None

def log(message):
    print(f"[YTDownloader] {message}")

def main():
    log(f"""
    
    _____.___._______  ____ ________                      .__                    .___            
\__  |   |\__    ___/   \______ \   ______  _  ______ |  |   _________     __| _/___________ 
 /   |   |  |    |       |    |  \ /  _ \ \/ \/ /    \|  |  /  _ \__  \   / __ |/ __ \_  __ 
 \____   |  |    |       |    `   (  <_> )     /   |  \  |_(  <_> ) __ \_/ /_/ \  ___/|  | \/
 / ______|  |____|      /_______  /\____/ \/\_/|___|  /____/\____(____  /\____ |\___  >__|   
 \/                           \/                  \/                \/      \/    \/     
    
    Created by: {AUTHOR}
    Quit keys: {QUIT_CHARS}
    Download path: {DOWNLOAD_PATH}
    Max results for video titles: {MAX_RESULTS}

    """)

    dwnl = Downloader()

    view_presence = False

    data = read_json_file()
    view_presence = True if data != None and data.get('presence') else False

    if view_presence:
        try:
            start = int(time.time())
            client_id = "979507386832273449"
            RPC = Presence(client_id)
            RPC.connect()
        except Exception as ignored:
            log('Error: Could not connect to discord, please make sure you have discord running.')

    # Run the main function
    while 1:
        if view_presence:
            dwnl.set_presence('Stand by...')

        #ask for the link from user
        link = input("Enter the title or link of the YouTube video you want to download (\"cancel\" to quit): ")
        if any(word in QUIT_CHARS for word in link.split(" ")):
            sys.exit(1)

        if view_presence:
            dwnl.set_presence(f"Downloading {link}...")
        
        #(?:v=|\/)([0-9A-Za-z_-]{11}).*
        try:
            dwnl.set_program(link)
        except Exception as regex:
            log('There seems to be an invalid character! A link may contain these characters:')
            log(VALID_CHARS)
    
if __name__ == "__main__":
    main()
