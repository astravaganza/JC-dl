import requests, toml, json
import os, sys

# define paths
currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)
cachePath = dirPath + "\cache"
outputPath = dirPath + "\out"
ytdl_path = dirPath + "\yt-dlp.exe"

# load config
config = toml.load("config.toml")

# define 
ssotoken = config ["ssotoken"]
uniqueID = config ["uniqueID"]
Request_URL = config ["Request_URL"]
Meta_URL = config ["MetaURL"]

def get_manifest(VideoID):
    headers = {
    'authority': 'prod.media.jio.com',
    'pragma': 'no-cache',
    'ssotoken': ssotoken,
    'bitrates': 'true',
    'os': 'Android',
    'user-agent': 'JioOnDemand/1.5.2.1 (Linux;Android 4.4.2) Jio',
    'content-type': 'application/json',
    'accept': 'application/json, text/plain, */*',
    'devicetype': 'tv',
    }
    response = requests.post(url = Request_URL + VideoID , data = '{"uniqueId":"' + uniqueID + '"}' , headers = headers)
    return json.loads(response.text)

def get_mpd(manifest):
    MPD_High = manifest['mpd']['high']
    return MPD_High

def get_m3u8(manifest):
    m3u8 = manifest['m3u8']['high']
    return m3u8

def mod_m3u8(url):
    mod = url.replace("jiovod.cdn.jio.com", "jiobeats.cdn.jio.com")
    lst = mod.split("/")
    lst[-1] = "chunklist.m3u8"
    mod = "/".join(lst)
    return mod


def get_metadata(VideoID):
    response = requests.get (url= Meta_URL + VideoID)
    return json.loads(response.text)

print ('JioCinema Content Downloading Tool')
VideoID = input ("Enter VideoID: ")
manifest = get_manifest(VideoID)
metadata = get_metadata(VideoID)
try:
    content_name = metadata['name']
except KeyError:
    print ("Incorrect/Malformed VideoID")
    sys.exit()
print (f'Downloading: {content_name} | {metadata["year"]} | {metadata["language"]}')
print (f'Subtitles available: {metadata["subtitle"]}')    
fileName = f'{content_name}.{metadata["year"]}.mp4'

def get_streams(mpd):
    print ("Downloading A/V")
    os.system(ytdl_path + ' ' + mpd + ' --allow-unplayable-formats' + ' --downloader aria2c' + ' --user-agent "JioOnDemand/1.5.2.1 (Linux;Android 4.4.2) Jio" -q --no-warnings -P TEMP:' + cachePath + ' -P HOME:' + outputPath)
    os.rename(f'{outputPath}\chunklist [chunklist].mp4', fileName)
    print ("Successfully downloaded the stream!")

m3u8_url = get_m3u8(manifest)
mpd_url = get_mpd(manifest)
nonDRM_m3u8_url = mod_m3u8(m3u8_url)
get_streams(nonDRM_m3u8_url)

