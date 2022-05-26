try:
    print('importing modules...')
    from pytube import YouTube
    from datetime import datetime
    import os
    from moviepy.video.io.VideoFileClip import VideoFileClip
    import sys
    import re
    import urllib.request
    import time
except ImportError:
    print("""
    You need to install all the modules
    - pip install pytube
    - pip install datetime
    - pip install os
    - pip install moviepy
    - pip install sys
    - pip install regex
    - pip install urllib3
    """)
    input('Press enter to close this window.')
    sys.exit(1)

class Downloader:
    def __init__(self, link):
        self.link = link
        self.main() # run the program


    # ========================= >
    # Create a new folder for the video
    # < =========================
    def new_video_folder(self, folder):
        """
        This function checks if the path exists if it doesn't then creates the path\n
        folder = the folder name
        """
        path = os.getcwd() + '/downloads/' + folder
        if not os.path.exists(path):
            os.makedirs(path)

        return path


    # ========================= >
    # Print video details
    # < =========================
    def print_video_details(self, yt):
        """
        This function prints details of the video\n
        yt = youtube object
        """
        minutes = yt.length / 60
        print('\n---------------------------------------')
        print(f"Title: {yt.title}")
        print(f'Url: https://www.youtube.com/watch?v={yt.video_id}')
        print(f"Number of views: {yt.views}")
        print(f"Length of video: {round(minutes, 2)} minutes ({yt.length} seconds)")
        print('---------------------------------------\n')


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
        print(f'Downloading "{yt.title}"...')
        print(f"Details: {ys}")

        path = self.new_video_folder(currentTime)
        ys.download(path)


    # ========================= >
    # Converting the video to mp3
    # < =========================
    def convert_to_sound(self, yt, currentTime):
        """
        This function converts the video to mp3\n
        yt = YouTube object\n
        path = path to save the mp3 file\n
        """
        try:
            path = path = self.new_video_folder(currentTime)
            title = yt.title.replace('.', '')
            video = VideoFileClip(os.path.join(path, title + ".mp4"))
            video.audio.write_audiofile(os.path.join(path, title + ".mp3"))
        except Exception as e:
            print(e)
            print("Error: An exception occurred trying to write to mp3.")


    # ========================= >
    # Get the youtube url from title from url
    # < =========================
    def convert_to_url(self, title):
        """
        This function get the youtube title from the link if it wasn't a link but text\n
        title = the title of the video aka the link
        """
        print('looking at youtube...')

        # Send a request with the text
        search_keyword = title.replace(' ', '+')
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
        search_results = re.findall(r'watch\?v=(.{11})', html.read().decode())
        # Return if no results were found

        if len(search_results) == 0:
            return None

        return search_results


    # ========================= >
    # Print the available results
    # < =========================
    def print_results(self, results):
        """
        This function prints 5 results from youtube and returns them in an array\n
        results = the url results from youtube
        """
        # Get the first 5 results
        videos = []
        results_used = []
        i = 0
        for result in results:
            try:
                if (i == 5): break

                if (result not in results_used):
                    yt = YouTube('https://www.youtube.com/watch?v=' + result)

                    minutes = yt.length / 60
                    print(f'---------------------- =({i + 1})= ----------------------')
                    print(f"Title: {yt.title}")
                    print(f'Url: https://www.youtube.com/watch?v={result}')
                    print(f"Length of video: {round(minutes, 2)} minutes ({yt.length} seconds)")
                    print('---------------------------------------------------\n')

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
            if choice == "none" or choice == "exit" or choice == "cancel":
                return None

            try:
                pick = int(choice)

                if (pick > len(videos) or pick <= 0):
                    print('Invalid choice')
                    continue

                users_pick = pick
                break
            except ValueError:
                print('Invalid choice')

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
                print('No results found')
                return
            else:
                print(f'found {len(results)} results...')

            # Get 5 of the most viewed videos
            videos = self.print_results(results)

            # Get users input of which video they want to download
            yt = self.get_user_choice(videos)
            if yt == None:
                return

        # Current time for the directory
        now = datetime.now()
        currentTime = now.strftime("%d-%m-%Y")

        # Download the video
        self.download_video(yt, currentTime)
        time.sleep(1) # Wait for the video to download, so there is no OSError
        self.convert_to_sound(yt, currentTime)

        print("Download completed!")
        print('\n')


if __name__ == "__main__":
    print('Started')

    # Run the main function
    while 1:
        #ask for the link from user
        link = input("Enter the link of YouTube video you want to download (\"cancel\" to cancel): ")
        if link == "none" or link == "exit" or link == "cancel":
            sys.exit(1)

        Downloader(link)