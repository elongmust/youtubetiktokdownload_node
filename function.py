import random
import string
from datetime import date
from pytube import YouTube
import os
import re
from pathlib import Path
import requests
import json
import youtube_key
from tiktok_module import downloader


def genera_date_folder_with_rnd_string3():
    rd = ''
    for i in range(3):
        rd += random.choice(string.ascii_letters)
    today = date.today()
    rs = today.strftime("%Y%m%d")
    rs = rs + "_" + rd
    return rs


def download_youtube_item_from_video_id(id, new_path, download_type, res_type='max'):
    base_url = 'https://www.youtube.com/watch?v='
    url = f'{base_url}{id}'
    yt = YouTube(url)
    status = yt.vid_info['playabilityStatus']['status']
    if status == "UNPLAYABLE":
        print(f"video_id {id} is not playable, cannot download.")
        return

    try:
        isinstance(yt.length, int)
    except:
        print(f"Could not get video length for {id}. Skipping download.")
        return

    # create condition - if the yt.length > 600 (10 mins), then don't download it
    # if yt.length > 600:
    #     print(f"video_id {id} is longer than 10 minutes, will not download.")
    #     return

    if (download_type == 'mp3'):
        # download mp3 files
        videos = yt.streams.filter(only_audio=True, mime_type='audio/mp4')
        # print(videos[0].abr)
        itag_min = videos[0].itag
        itag_max = videos[0].itag
        s = videos[0].abr
        max_abr = int(''.join(i for i in s if i.isdigit()))
        min_abr = max_abr
        for item in videos:
            # print(item.itag)
            tmp = item.abr
            if (type(tmp) is str):
                abr = int(''.join(i for i in tmp if i.isdigit()))
                if abr >= max_abr:
                    max_abr = abr
                    itag_max = item.itag
                if abr <= min_abr:
                    min_abr = abr
                    itag_min = item.itag
        if (res_type == 'min'):
            video = yt.streams.get_by_itag(itag_min)
        else:
            video = yt.streams.get_by_itag(itag_max)
        # video = yt.streams.filter(only_audio=True).first()

        try:
            song_title_raw = yt.title
        except:
            print(f'Unable to get title for id {id}. Skipping download.')
            return
        song_title = re.sub('\W+', ' ', song_title_raw).lower().strip()
        song_path = f"{song_title}"

        download_path = f"{new_path}/{song_path}"
        out_file = video.download(download_path)

        # save the file (which will be mp4 format)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

        # move the mp3 to the root dir
        p = Path(new_file).absolute()
        parent_dir = p.parents[1]
        p.rename(parent_dir / p.name)

        # delete the child dir
        os.rmdir(download_path)

        # rename the mp3 to remove the bad chars
        source_name = f"{new_path}/{song_title_raw}.mp3"
        dest_name = f"{new_path}/{song_path}.mp3"
        try:
            os.rename(source_name, dest_name)
        except:
            print(f"Failed to rename the file: {song_title_raw}")

        # result of success
        print(f"{song_path} has been successfully downloaded. Video id: {id}")
    else:
        video_lists = yt.streams.filter(file_extension='mp4', progressive=True)
        itag_min = video_lists[0].itag
        itag_max = video_lists[0].itag
        # print(itag_max)
        s = video_lists[0].resolution
        max_res = int(''.join(i for i in s if i.isdigit()))
        min_res = max_res
        for item in video_lists:
            # print(item.itag)
            tmp = item.resolution
            if (type(tmp) is str):
                res = int(''.join(i for i in tmp if i.isdigit()))
                if res >= max_res:
                    max_res = res
                    itag_max = item.itag
                if res <= min_res:
                    min_res = res
                    itag_min = item.itag

        # video = yt.streams.filter(file_extension = 'mp4').first()
        if (res_type == 'min'):
            video = yt.streams.get_by_itag(itag_min)
        else:
            video = yt.streams.get_by_itag(itag_max)

        # video = yt.streams.filter(file_extension = 'mp4').first()
        try:
            video_title_raw = yt.title
        except:
            print(f'Unable to get title for id {id}. Skipping download.')
            return
        video_title = re.sub('\W+', ' ', video_title_raw).lower().strip()
        video_path = f"{video_title}"

        download_path = f"{new_path}/{video_path}"
        out_file = video.download(download_path)

        # save the file (which will be mp4 format)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp4'
        os.rename(out_file, new_file)

        # move the mp3 to the root dir
        p = Path(new_file).absolute()
        parent_dir = p.parents[1]
        p.rename(parent_dir / p.name)

        # delete the child dir
        os.rmdir(download_path)

        # result of success
        print(f"{video_path} has been successfully downloaded. Video id: {id}")


def manage_download_of_ids(video_ids, path, download_type, res_type='max'):
    for id in video_ids:
        try:
            download_youtube_item_from_video_id(
                id, path, download_type, res_type)
        # except: print(f'Failed to download video id: {id}')
        except:
            a = 1


def get_video_id_from_playlist(playlist_id):
    # https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=200&playlistId=PLf7xdKcE1Xl8UgrduPU9JwtR7rs7bPufO&key=AIzaSyAfJcO-0I9iq9U_m4XntWRj6HxR8bo3qpY
    URL = 'https://youtube.googleapis.com/youtube/v3/playlistItems'
    PARAMS = {'part': 'contentDetails', 'maxResults': 200,
              'playlistId': playlist_id, 'key': youtube_key.YOUTUBE_API_KEY}
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    id_list = []
    for i in data['items']:
        id = i['contentDetails']['videoId']
        id_list.append(id)
    return id_list


def download_single(link, download_type='mp3', res_type='max'):
    yt = YouTube(link)
    if (download_type == 'mp3'):
        videos = yt.streams.filter(only_audio=True, mime_type='audio/mp4')
        # print(videos[0].mime_type)
        itag_min = videos[0].itag
        itag_max = videos[0].itag
        s = videos[0].abr
        max_abr = int(''.join(i for i in s if i.isdigit()))
        min_abr = max_abr
        for item in videos:
            # print(item.itag)
            tmp = item.abr
            if (type(tmp) is str):
                abr = int(''.join(i for i in tmp if i.isdigit()))
                if abr >= max_abr:
                    max_abr = abr
                    itag_max = item.itag
                if abr <= min_abr:
                    min_abr = abr
                    itag_min = item.itag
        if (res_type == 'min'):
            video = yt.streams.get_by_itag(itag_min)
        else:
            video = yt.streams.get_by_itag(itag_max)
        # print(itag_min)
        # print(itag_max)

        # video = yt.streams.filter(only_audio=True).first()
        try:
            song_title_raw = yt.title
        except:
            print(f'Unable to get title for id {id}. Skipping download.')
        download_path = f"ui_mp3s/"
        out_file = video.download(download_path)

        # save the file (which will be mp4 format)
        base, ext = os.path.splitext(out_file)
        k = f'r"{base}'
        a = k.split('/')
        song_title = a[1]
        if (res_type == 'min'):
            new_file = base + '_' + str(min_abr) + 'kbps.mp3'
        else:
            new_file = base + '_' + str(max_abr) + 'kbps.mp3'
        os.rename(out_file, new_file)

        # move the mp3 to the root dir
        # p = Path(new_file).absolute()
        # parent_dir = p.parents[1]
        # p.rename(parent_dir / p.name)

        # # delete the child dir
        # os.rmdir(download_path)
        # # return download_path
        # source_name = f"saved_mp3s/{song_title_raw}.mp3"
        # dest_name = f"saved_mp3s/{song_path}.mp3"
        # try: os.rename(source_name,dest_name)
        # except: print(f"Failed to rename the file: {song_title_raw}")
        if (res_type == 'min'):
            s = song_title + '_' + str(min_abr) + 'kbps.mp3'
        else:
            s = song_title + '_' + str(max_abr) + 'kbps.mp3'
        # return mp3 file path
        print(json.dumps(s))
    else:
        video_lists = yt.streams.filter(file_extension='mp4', progressive=True)
        itag_min = video_lists[0].itag
        itag_max = video_lists[0].itag
        # print(itag_max)
        s = video_lists[0].resolution
        max_res = int(''.join(i for i in s if i.isdigit()))
        min_res = max_res
        for item in video_lists:
            # print(item.itag)
            tmp = item.resolution
            if (type(tmp) is str):
                res = int(''.join(i for i in tmp if i.isdigit()))
                if res >= max_res:
                    max_res = res
                    itag_max = item.itag
                if res <= min_res:
                    min_res = res
                    itag_min = item.itag

        # video = yt.streams.filter(file_extension = 'mp4').first()
        if (res_type == 'min'):
            video = yt.streams.get_by_itag(itag_min)
        else:
            video = yt.streams.get_by_itag(itag_max)
        try:
            song_title_raw = yt.title
        except:
            print(f'Unable to get title for id {id}. Skipping download.')
        download_path = f"ui_mp4s/"
        out_file = video.download(download_path)
        base, ext = os.path.splitext(out_file)
        k = f'r"{base}'
        a = k.split('/')
        video_title = a[1]
        s = video_title + '.mp4'

        print(json.dumps(s))


def download_multiple(playlist_id, download_type='mp3', res_type='max'):
    output_dir = 'ui_mp3s/'
    if (download_type == 'mp4'):
        output_dir = 'ui_mp4s/'
    # sub_dir = generate_random_string10()
    sub_dir = genera_date_folder_with_rnd_string3()
    path = os.path.join(output_dir, sub_dir)
    os.makedirs(path)
    video_ids = get_video_id_from_playlist(playlist_id)
    manage_download_of_ids(video_ids, path, download_type, res_type)
    # print(path)
    print(json.dumps(path))


def tiktokDownload(link):
    # https://www.tiktok.com/@hungbavuatiente/video/7195768642385005851
    data = link.split("/")
    video_id_data = data[5].split('?')
    video_id = video_id_data[0]
    output_name = "tiktok_files/"+data[3].replace("@", "")+"_"+video_id+".mp4"
    dl = downloader.tiktok_downloader()
    result = dl.musicaldown(url=link, output_name=output_name)
    if (result):
        return output_name
    else:
        return -1
