# JC_dl
Simple Content downloader for Indian OTT JioCinema (https://www.jiocinema.com/).

*(Currently only supports movies, I haven't looked at TV shows, so if someone wants to open a PR, feel free)*

## Purpose
JioCinema offers many rare and old HQ streams of Indian content which is unfortunately hidden behind DRM and cannot be easily saved for archival purposes. This tool bypasses the DRM restrictions and grabs the **Non-DRM** streams (which are ironically sometimes superior to its DRM counterparts) from JioCinema which can be downloaded directly.

### Prerequisites
An account on JioCinema and the most basic skills.

### WARNING
This tool shall not be abused for purposes which are not archival or educational. Use at your own risk.

## Usage
* Install python and run `pip install -r requirements.txt` in your shell
* Download yt-dlp (from https://github.com/yt-dlp/yt-dlp), aria2c (from https://aria2.github.io/) and the ffmpeg suite (from https://www.ffmpeg.org/download.html) and place the binaries in the root directory
* Add your unique SSOtoken and uniqueID to `config.toml` (check [below](https://github.com/astravaganza/JC_dl#adding-config))
* run `python main.py`
* VideoID can be obtained from the Movie URL (for example: in https://www.jiocinema.com/movies/jaya-ganga?type=0&id=74f26cb06e0111ecb736133f7a349447, `74f26cb06e0111ecb736133f7a349447` is the VideoID). 
* Let yt-dlp and aria2c download the stream (defaults to the most superior stream) and check the `out` folder for the downloaded movie.

### Adding config
* Open JioCinema, ensure you are logged in. 
* Open Devtools (if you're using chrome, Ctrl + Shift + I) 
![DevTools](https://i.ibb.co/rpQhbF7/image.png)
* Play some content (keeping DevTools open)
* Navigate to Network Tab in DevTools and filter by `get`
![get](https://i.ibb.co/gd2pSj5/image.png)
* Iterate through the `get` requests till you find the `SSOtoken` and the `uniqueID` in the request headers section. 

## P. S
I'm really terrible at coding so consider this as the worst code. Please feel free to open PRs.

## Thanks
to yt-dlp for basically solving the m3u8 parsing cause I can't write a parser.

### To-Do
* Add subtitle support
* Simplify the config process
* Add logging
* Add custom quality support
