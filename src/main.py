# IG:       wallace.thiago
# GitHub:   WinterSunset95

# This is the api we will be using
# https://consumet-api-six-ochre.vercel.app

# The goal is to write a simple anime downloader cli

# Import dependencies and declare variables
import requests
import json
from pytermgui import Container
baseUrl = "https://consumet-api-six-ochre.vercel.app/anime/gogoanime/"

def toolIsInstalled(tool):
    from shutil import which
    return which(tool) is not None

def downloadFile(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            print("Downloading . . . ")
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    print("Download complete")

def getEpisodeData(episodeId):
    print("Getting episode data . . . ")
    url = baseUrl + "watch/" + episodeId
    res = requests.get(url)
    headers = res.headers
    data = res.json()

    if data['sources']:
        sources = data['sources']
        while True:
            count = 1
            for source in sources:
                print(f"{count}: ")
                print(f"\tURL: {source['url']}")
                print(f"\tQuality: {source['quality']}")
                count = count + 1
            print(f"{count}: Download")
            print("0: Exit")
            choice = int(input("Choose source: "))
            # 0 is for exiting
            if choice == 0:
                print("Exiting")
                break
            # Handle invalid inputs
            if choice > count:
                print("Invalid source number")
                continue
            # The last choice is always 'download'
            if choice == count and data['download']:
                print("Downloading . . . ")
                downloadUrl = data['download']
                downloadFile(downloadUrl)
            else:
                print("Streaming . . . ")
                streamUrl = sources[choice-1]['url']
                print(f"Stream URL: {streamUrl}")
                if toolIsInstalled("mpv"):
                    print("mpv installed")
                    print("Playing . . . ")
                    import subprocess
                    subprocess.run(["mpv", streamUrl])
                elif toolIsInstalled("vlc"):
                    print("vlc installed")
                    print("Playing . . . ")
                    import subprocess
                    subprocess.run(["vlc", streamUrl])
                else:
                    print("Install mpv or vlc to stream")
                    return


def getAnimeData(animeId):
    print("Getting anime data . . . ")
    url = baseUrl + "info/" + animeId
    res = requests.get(url)
    headers = res.headers
    data = res.json()

    if data['episodes']:
        episodes = data['episodes']
        length = len(episodes)
        print(f"{data['title']} has {length} episodes")
        epNo = int(input("Choose episode: "))
        if epNo > length:
            print("Invalid episode number")
            return
        getEpisodeData(episodes[epNo-1]['id'])
    else:
        print("No episodes were returned")
        return

# This is the page the user will see when they first use
def userHome(string, page):
    url = baseUrl + string + "?page=" + str(page)
    res = requests.get(url)
    headers = res.headers
    data = res.json()

    count = 1
    prevPage = 0
    nextPage = 0
    if data['results']:
        searchResults = data['results']
        for result in searchResults:
            print(f"{count}: {result['title']}")
            count = count + 1
    else:
        print("data.results not available")
        return

    if data['currentPage'] != '1':
        print(f"{count}: Prev page")
        prevPage = count
        count = count+1
    if data['hasNextPage']:
        print(f"{count}: Next page")
        nextPage = count
        count = count+1

    print(f"{count}: Exit")
    choice = int(input("Choose: "))
    if choice == count:
        print("Exiting")
        return
    elif choice == prevPage:
        userHome(string, page-1)
    elif choice == nextPage:
        userHome(string, page+1)
    else:
        getAnimeData(searchResults[choice-1]['id'])


    #file1 = open("data.json", "w")
    #data_formatted = json.dumps(data, indent=4)
    #file1.write(data_formatted)
    #file1.close()

def initilize():
    search = input("Search anime: ")
    userHome(search, 1)

initilize()
