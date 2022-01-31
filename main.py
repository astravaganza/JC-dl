import requests, json
import os, sys

# define paths
currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)
ytdl_path = dirPath + "\yt-dlp.exe"

# define 
def load_config():
    global ssotoken, uniqueID
    with open ("creds.txt", "r") as f:
        try:
            Creds = json.load(f)
            ssotoken = Creds['ssotoken']
            uniqueID = Creds['uniqueID']
        except json.JSONDecodeError:
            ssotoken = ''
            uniqueID = ''    

Request_URL = "https://prod.media.jio.com/apis/common/v3/playbackrights/get/"
Meta_URL = "https://prod.media.jio.com/apis/common/v3/metamore/get/"
#cachePath = 
#outPath = 
OTPSendURL = "https://prod.media.jio.com/apis/common/v3/login/sendotp"
OTPVerifyURL = "https://prod.media.jio.com/apis/common/v3/login/verifyotp"

def login(mobile_number):
    send = requests.post(url = OTPSendURL, headers = {
    'authority': 'prod.media.jio.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'origin': 'https://www.jiocinema.com',
    'referer': 'https://www.jiocinema.com/',
    },
     data = '{"number":"+91' + mobile_number +'"}'
    )
    if 'success' in str(send.content):
        OTP = input ('Enter OTP Received: ')
        verify = requests.post(url = OTPVerifyURL, headers = {
        'authority': 'prod.media.jio.com',
        'pragma': 'no-cache',
        'origin': 'https://www.jiocinema.com',
        'referer': 'https://www.jiocinema.com/',
        'deviceid': '1727391720'
        },
        data = '{"number":"+91' + mobile_number + '","otp":"' + OTP + '"}')
        creds = json.loads(verify.content)
        print (creds)
        load_creds(creds)
    else:
        print ("Wrong/Unregistered Mobile Number (ensure there's no +91 or 0 in the beginning)")
        sys.exit()

def load_creds(creds):
    try:
        ssotoken = creds['ssoToken']
        uniqueID = creds['uniqueId']
    except KeyError:
        print ("Wrong OTP, Try again!")
        sys.exit()
    Creds = {
        "ssotoken" : ssotoken,
        "uniqueID" : uniqueID
    }
    with open("creds.txt", "w") as f:
        f.write(json.dumps(Creds))

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
load_config()
if ssotoken == "" and uniqueID == "":
    M_No = input ('Enter Mobile Number: ')
    login (M_No)
    load_config()
VideoID = input ('Enter VideoID: ')
manifest = get_manifest(VideoID)
metadata = get_metadata(VideoID)
try:
    content_name = metadata['name']
except KeyError:
    print ("Incorrect/Malformed VideoID")
    sys.exit()
print (f'Downloading: {content_name} | {metadata["year"]} | {metadata["language"]}')
# print (f'Subtitles available: {metadata["subtitle"]}')    
fileName = f'{content_name}.{metadata["year"]}.mp4'

def get_streams(m3u8):
    print ("Downloading A/V")
    os.system(f'{ytdl_path} {m3u8} --allow-unplayable-formats --downloader aria2c --user-agent "JioOnDemand/1.5.2.1 (Linux;Android 4.4.2) Jio" -q --no-warnings') # + -P TEMP:{cachePath} -P HOME:{outPath}
    os.rename(f'{dirPath}\chunklist [chunklist].mp4', fileName)
    print ("\nSuccessfully downloaded the stream!")


m3u8_url = get_m3u8(manifest)
nonDRM_m3u8_url = mod_m3u8(m3u8_url)
get_streams(nonDRM_m3u8_url)

