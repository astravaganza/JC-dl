import requests, json
import os, sys
import base64

# define paths
currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)
ytdl_path = dirPath + "\yt-dlp.exe"

# define 
def load_config():
    global accesstoken, devid
    with open ("creds.txt", "r") as f:
        try:
            Creds = json.load(f)
            accesstoken = Creds['accesstoken']
            devid = Creds['deviceid']
        except json.JSONDecodeError:
            accesstoken = ''
            devid = ''    

Request_URL = "https://apis-jiovoot.voot.com/playbackjv/v4/"
Meta_URL = "https://prod.media.jio.com/apis/common/v3/metamore/get/"
OTPSendURL = "https://auth-jiocinema.voot.com/userservice/apis/v4/loginotp/send"
OTPVerifyURL = "https://auth-jiocinema.voot.com/userservice/apis/v4/loginotp/verify"
IdURL = "https://cs-jv.voot.com/clickstream/v1/get-id"
GuestURL = "https://auth-jiocinema.voot.com/tokenservice/apis/v4/guest"

def get_accesstoken():
    id = requests.get(url=IdURL).json()['id']

    token = requests.post(url=GuestURL, json={
            'adId': id,
            "appName": "RJIL_JioCinema",
            "appVersion": "23.10.13.0-841c2bc7",
            "deviceId": id,
            "deviceType": "phone",
            "freshLaunch": True,
            "os": "ios"
        }, headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }).json()

    return token["authToken"], id

def login(mobile_number):
    accesstoken, id = get_accesstoken()
    
    send = requests.post(url=OTPSendURL, json={
            "number": base64.b64encode(f"+91{mobile_number}".encode()).decode(),
            "appVersion": "23.10.13.0-841c2bc7"
        }, headers = {
            'accesstoken': accesstoken,
            'appname': 'RJIL_JioCinema',
            'cache-control': 'no-cache',
            'devicetype': 'phone',
            'os': 'ios',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
})
    print(send.content)
    if 'karix' in str(send.content):
        OTP = input ('Enter OTP Received: ')
        verify = requests.post(url = OTPVerifyURL, headers = {
            'accesstoken': accesstoken,
            'appname': 'RJIL_JioCinema',
            'cache-control': 'no-cache',
            'devicetype': 'phone',
            'os': 'ios',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        }, json={
            "appVersion": "23.10.13.0-841c2bc7",
            "deviceInfo": {
                "consumptionDeviceName": "iPhone",
                "info": {
                    "androidId": id,
                    "platform": {
                        "name": "iPhone OS"
                    },
                    "type": "iOS"
                }
            },
            "number": base64.b64encode(f"+91{mobile_number}".encode()).decode(),
            "otp": OTP
        })
        creds = json.loads(verify.content)
        load_creds(creds)
    else:
        print ("Wrong/Unregistered Mobile Number (ensure there's no +91 or 0 in the beginning)")
        sys.exit()

def load_creds(creds):
    try:
        accesstoken = creds['authToken']
        devid = creds['deviceId']
    except KeyError:
        print ("Wrong OTP, Try again!")
        sys.exit()
    Creds = {
        "accesstoken" : accesstoken,
        "deviceid" : devid
    }
    with open("creds.txt", "w") as f:
        f.write(json.dumps(Creds))

def get_manifest(VideoID):
    headers = {
    "Accesstoken": accesstoken,
    "Appname": "RJIL_JioCinema",
    "Versioncode": "2310130",
    "Deviceid": devid,
    "x-apisignatures": "o668nxgzwff",
    "X-Platform": "androidweb",
    "X-Platform-Token": "web",
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }
    response = requests.post(url=Request_URL + VideoID, headers=headers, json={
            "4k": False,
            "ageGroup": "18+",
            "appVersion": "3.4.0",
            "bitrateProfile": "xhdpi",
            "capability": {
                "drmCapability": {
                    "aesSupport": "yes",
                    "fairPlayDrmSupport": "none",
                    "playreadyDrmSupport": "none",
                    "widevineDRMSupport": "none"
                },
                "frameRateCapability": [
                    {
                    "frameRateSupport": "60fps",
                    "videoQuality": "2160p"
                    }
                ]
            },
            "continueWatchingRequired": True,
            "dolby": True,
            "downloadRequest": False,
            "hevc": False, # adjust accordingly
            "kidsSafe": False,
            "manufacturer": "Windows",
            "model": "Windows",
            "multiAudioRequired": True,
            "osVersion": "10",
            "parentalPinValid": True,
            "x-apisignatures": "o668nxgzwff"
        })
    return json.loads(response.text)

def get_m3u8(manifest):
    m3u8 = manifest['data']['playbackUrls'][1]['url']
    return m3u8

def mod_m3u8(url):
    mod = url.replace("jiovod.cdn.jio.com", "jiobeats.cdn.jio.com")
    lst = mod.split("/")
    lst[-1] = "chunklist.m3u8"
    mod = "/".join(lst)
    return mod

print ('JioCinema Content Downloading Tool')
load_config()
if accesstoken == "" and devid == "":
    M_No = input ('Enter Mobile Number: ')
    login (M_No)
    load_config()
VideoID = input ('Enter VideoID: ')
manifest = get_manifest(VideoID)

try:
    content_name = manifest['data']['name']
except KeyError:
    print ("Incorrect/Malformed VideoID")
    sys.exit()
print (f'Downloading: {content_name} |  {manifest["data"]["defaultLanguage"]}')
# print (f'Subtitles available: {metadata["subtitle"]}')    
fileName = f'{content_name}.mp4'

def get_streams(m3u8):
    print ("Downloading A/V")
    os.system(f'{ytdl_path} {m3u8} --allow-unplayable-formats --downloader aria2c --user-agent "JioOnDemand/1.5.2.1 (Linux;Android 4.4.2) Jio" -q --no-warnings') # + -P TEMP:{cachePath} -P HOME:{outPath}
    os.rename(f'{dirPath}\chunklist [chunklist].mp4', fileName)
    print ("\nSuccessfully downloaded the stream!")


m3u8_url = get_m3u8(manifest)
nonDRM_m3u8_url = mod_m3u8(m3u8_url)
get_streams(nonDRM_m3u8_url)

