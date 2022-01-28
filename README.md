# JC_dl
Simple Content downloader for Indian OTT JioCinema (https://www.jiocinema.com/)

## Purpose
JioCinema offers many rare and old HQ streams of Indian content which is unfortuantely hidden behind DRM and cannot be easily saved for archival purposes. This tool bypasses the DRM restrictions and grabs the **Non-DRM** streams (which are ironically sometimes superior to its DRM counterparts) from JioCinema which can be downloaded directly.

### Prerequisites
An account on JioCinema and the most basic skills

### WARNING
This tool shall not be abused for purposes which are not archival or educational. Use at your own risk.

## Usage
* Install python and run `pip install -r requirements.txt` in your shell
* Download aria2c (from https://aria2.github.io/) and the ffmpeg suite (from https://www.ffmpeg.org/download.html) and place the binaries in the root directory
* Add your unique SSOtoken and uniqueID to `config.toml` 
