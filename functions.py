from dearpygui.core import *
from dearpygui.simple import *
import pytube
import os
from os import path
from moviepy.editor import *

import requests # to get image from the web
import shutil # to save it locally

from sclib import SoundcloudAPI, Track, Playlist

from youtubesearchpython import *
from youtube_search import get_titles, get_links


def download_youtube_mp4_playlist(sender, data):
    with window("File downloader"):
        general_url = get_value("URL")
        playlist = pytube.Playlist(general_url)
        if general_url == "":
            log_warning(logger="logger_general", message="URL is empty")
        else:
            for url in playlist:
                pytube.YouTube(url).streams.first().download('./videos')


def download_youtube_mp3_playlist(sender, data):
    with window("File downloader"):
        general_url = get_value("URL2")
        playlist_mp3 = pytube.Playlist(general_url)
        if general_url == "":
           log_warning(logger="logger_general", message="URL is empty")
        else:
            for url in playlist_mp3:
                download_youtube_mp3 = pytube.YouTube(url)
                stream_mp3 = download_youtube_mp3.streams.first().download('./audios/')
                log_info(logger="logger_general", message="Downloading: "+ download_youtube_mp3.title)
                os.rename(stream_mp3, "./audios/video.mp4") # renaming the file to a more readable format
                file = VideoFileClip("./audios/video.mp4")
                # print(os.path.abspath(video_file))
                audiofile = file.audio
                audiofile.write_audiofile("./audios/video.mp3")
                log_info(logger="logger_general", message="Writing to file")
                audiofile.close()
                file.close()
                os.remove("./audios/video.mp4")
                os.rename("./audios/video.mp3", f'./audios/{download_youtube_mp3.title}.mp3') # renaming it back so its more recognisable
                log_info(logger="logger_general", message="Downloaded: " + download_youtube_mp3.title)


def download_video(sender, data):
    with window("File downloader"):
       if get_value("URL") == "":
           log_warning(logger="logger_general", message="URL is empty")
       else:
        download_youtube = pytube.YouTube(get_value("URL"))
        stream = download_youtube.streams.get_highest_resolution()
        stream.download('./videos')
        log_info(logger="logger_general", message="Downloaded: " + download_youtube.title)

def download_audio(sender, data):
    with window("File downloader"):
       if get_value("URL2") == "":
           log_warning(logger="logger_general", message="URL is empty")
       else:
        download_youtube_mp3 = pytube.YouTube(get_value("URL2"))
        stream_mp3 = download_youtube_mp3.streams.first().download('./audios/')
        os.rename(stream_mp3, "./audios/video.mp4") # renaming the file to a more readable format
        file = VideoFileClip("./audios/video.mp4")
        log_info(logger="logger_general", message="Downloading: "+ download_youtube_mp3.title)
        # print(os.path.abspath(video_file))
        audiofile = file.audio
        audiofile.write_audiofile("./audios/video.mp3")
        log_info(logger="logger_general", message="Writing to file")
        audiofile.close()
        file.close()
        os.remove("./audios/video.mp4")
        os.rename("./audios/video.mp3", f'./audios/{download_youtube_mp3.title}.mp3') # renaming it back so its more recognisable
        log_info(logger="logger_general", message="Downloaded: " + download_youtube_mp3.title)


def download_soundcloud_mp3(sender, data):
    with window("File downloader"):
        api = SoundcloudAPI()
        track =  api.resolve(get_value("URL3"))
        assert type(track) is Track
        image_url = track.artwork_url
        r = requests.get(image_url, stream=True)
        fn = f'./audios/{track.artist} - {track.title}.mp3'
        fn_artwork = f'./artworks/{track.artist} - {track.title}_artwork.jpeg'
        with open(fn, 'wb+') as fp:
            track.write_mp3_to(fp)
            log_info(logger="logger_general", message="Downloaded: " + fn)
            if r.status_code == 200:
                r.raw.decode_content = True
                with open(fn_artwork, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                    log_info(logger="logger_general", message="Artwork downloaded as: " + fn_artwork)
                    draw_image("artwork_image", f'./artworks/{track.artist} - {track.title}_artwork.jpeg', [0, 0], [120, 120])
            else:
                log_error(logger="logger_general", message="Couldn't fetch artwork")


def download_soundcloud_playlist(sender, data):
    with window("File downloader"):

        api = SoundcloudAPI()
        playlist = api.resolve(get_value("URL3"))
        assert type(playlist) is Playlist
        playlist_artwork= playlist.artwork_url
        fn_playlist_artwork = f'./artworks/{playlist.title}_artwork.jpeg'
        r = requests.get(playlist_artwork, stream=True)
        if r.status_code == 200:
            r.raw.decode_content=True
            with open(fn_playlist_artwork, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
                log_info(logger="logger_general", message="Playlist artwork downloaded as: " + fn_playlist_artwork)
        else:
            log_error(logger="logger_general", message="Couldn't fetch playlist artwork")

        for track in playlist.tracks:
            fn = f'./audios/{track.artist} - {track.title}.mp3'
            log_info(logger="logger_general", message="Downloaded: " + fn)
            with open(fn, 'wb+') as fp:
                track.write_mp3_to(fp)


def search_for_videos(sender, data):
    with window("File downloader"):
        list = get_titles(get_value("youtube_search"))
        configure_item("results_listbox", items=list)


def set_links(sender, data):
    with window("File downloader"):
        if get_value("youtube_search") == "":
            log_warning(logger="logger_general", message="Search bar is empty")
        else:
            item = get_value("results_listbox")
            link = get_links(get_value("youtube_search"))
            print(link[item])
            set_value("URL", link[item])
            set_value("URL2", link[item])
