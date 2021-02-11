from youtubesearchpython import *



def get_titles(query):
    titles = []
    fetcher = StreamURLFetcher()
    vs = VideosSearch(query)
    for video in vs.result()['result']:
        titles.append(video['title'])
    return titles


def get_links(query):
    links = []
    fetcher = StreamURLFetcher()
    vs = VideosSearch(query)
    for video in vs.result()['result']:
        links.append(video['link'])
    return links
