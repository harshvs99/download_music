import requests
import zipfile
import json
import boto3
import os

music_dl_folder = "/home/ec2-user/environment/music_dl/"
dlinks = open("links.json")
download_links = json.load(dlinks)

def download_file_tidal(album):
    url = download_links[album]
    r_payload = requests.get(url)
    print("the payload: ", r_payload)
    file_name = album.replace(" ", "_")
    open(music_dl_folder+file_name+".zip", 'wb').write(r_payload.content)
    print(file_name, " is downloaded")
    with zipfile.ZipFile(music_dl_folder+file_name+".zip", 'r') as zip_ref:
        zip_ref.extractall(music_dl_folder)
    print("Files downloaded to: ", music_dl_folder)

all_albums = ["2014 Forest Hills Drive"]
for album in all_albums:
    download_file_tidal(album)
os.system(f"aws s3 sync {music_dl_folder} s3://harshvs-stream-music")
