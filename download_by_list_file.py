import pytube  # library for downloading youtube videos
import time

import sys

directory = '/home/chinv/Videos/middletonhallenglish/'


def main():
    links = load_list()
    for link in links:

        try:
            youtube = pytube.YouTube(link)
            video = youtube.streams.first()
            print(video.title)
            video.download(directory)
            # printing the links downloaded
            print("Downloaded: ", link, "ID: ", link.split('=')[-1])
        except:
            print('Some error in downloading: ', link)
            print('retry link: ', link)

            try:
                youtube = pytube.YouTube(link)
                video = youtube.streams.first()
                print(video.title)
                video.download(directory)
                # printing the links downloaded
                print("Downloaded: ", link, "ID: ", link.split('=')[-1])
            except:
                print('retry failed for link: ', link)

def load_list():
    with open("list.txt", "r") as file:
        return [line.strip() for line in file if line.strip()]
    # for link in links:
    #     print(link)

if __name__ == "__main__":
    main()
    # if sys.argv[1:]:
    #     main(sys.argv[1:])
