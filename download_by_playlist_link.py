import pytube
from pytube import request

from typing import Dict, Tuple
from typing import Iterable
from typing import List
from typing import Optional
from pytube.helpers import uniqueify

import re
import json

directory = '/home/chinv/Videos/streamlines/1-departure'
playlist_url = "https://www.youtube.com/playlist?list=PLq9eALo7bUXtGNOeGNg4TmQeooSUhtod8"
_js_regex = re.compile(r"window\[\"ytInitialData\"] = ([^\n]+)")
_video_regex = re.compile(r"href=\"(/watch\?v=[\w-]*)")


def main():
    video_ids = load_video_ids(playlist_url)
    links = [to_video_url(id) for id in video_ids]
    print("Link list:")
    # with open("list.txt", "w") as file:
    #     for link in links:
    #         file.write(link + "\n")

    print(links)
    for link in links:
        # print(link)
        # print(video.title)
        try:
            youtube = pytube.YouTube(link)
            video = youtube.streams.first()
            video.download(directory)
            # printing the links downloaded
            print("Downloaded: ", link)
            # time.sleep(5)
        except:
            print('Some error in downloading: ', link)


def load_video_ids(playlist_url: str):
    html = request.get(playlist_url)
    jsonData = _extract_json(html)
    if len(jsonData) > 1:
        print("Got json")

    videos_urls, continuation = extract_videos(
        # extract the json located inside the window["ytInitialData"] js
        # variable of the playlist html page
        _extract_json(html)
    )

    print(f"Num of videos in this page: {len(videos_urls)}")
    if continuation:
        print(f"Continuation value: {continuation}")

    return videos_urls


def _extract_json(html: str) -> str:
    return _js_regex.search(html).group(1)[0:-1]


def to_video_url(watch_path: str):
    return f"https://www.youtube.com{watch_path}"


def extract_videos(raw_json: str) -> Tuple[List[str], Optional[str]]:
    """Extracts videos from a raw json page
    :param str raw_json: Input json extracted from the page or the last
        server response
    :rtype: Tuple[List[str], Optional[str]]
    :returns: Tuple containing a list of up to 100 video watch ids and
        a continuation token, if more videos are available
    """
    initial_data = json.loads(raw_json)
    try:
        # this is the json tree structure, if the json was extracted from
        # html
        important_content = initial_data["contents"][
            "twoColumnBrowseResultsRenderer"
        ]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"][
            "contents"
        ][
            0
        ][
            "itemSectionRenderer"
        ][
            "contents"
        ][
            0
        ][
            "playlistVideoListRenderer"
        ]
    except (KeyError, IndexError, TypeError):
        try:
            # this is the json tree structure, if the json was directly sent
            # by the server in a continuation response
            important_content = initial_data[1]["response"][
                "continuationContents"
            ]["playlistVideoListContinuation"]
        except (KeyError, IndexError, TypeError) as p:
            print(p)
            return [], None
    videos = important_content["contents"]
    try:
        continuation = important_content["continuations"][0][
            "nextContinuationData"
        ]["continuation"]
    except (KeyError, IndexError):
        # if there is an error, no continuation is available
        continuation = None

    # print(f"videos: {videos}")
    # remove duplicates
    return (
        uniqueify(
            list(
                # only extract the video ids from the video data
                map(
                    lambda x: (
                        f"/watch?v="
                        f"{x['playlistVideoRenderer']['videoId']}"
                    ),
                    videos
                )
            ),
        ),
        continuation,
    )


def load_list():
    with open("list.txt", "r") as file:
        return [line.strip() for line in file if line.strip()]
    # for link in links:
    #     print(link)


if __name__ == "__main__":
    main()
