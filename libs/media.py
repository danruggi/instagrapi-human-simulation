import pathlib
import os
import random
import traceback
import urllib
import urllib.request

import emoji

from classes.botconf import botConf

from libs.config import loadCoolDownValues


def downloadThumb(conf, pk, thumbnail_url):
    confdir = conf["confdir"]

    with open(os.path.join(confdir, "thumbs_downloaded.csv")) as f:
        if str(pk) in f.read():
            print("x", end='')
            return

    if thumbnail_url is not None:
        urllib.request.urlretrieve(str(thumbnail_url), os.path.join(conf["basedwndir"], "temp_thumb"))

    print("o", end='');
    # media checked
    with open(os.path.join(confdir, "thumbs_downloaded.csv"), "a") as f:
        f.write(str(pk) + "\n")


def downloadMedia(conf, pk, item_type, product_type):
    cl = conf["cl"]
    confdir = conf["confdir"]

    with open(os.path.join(confdir, 'medias_downloaded.csv')) as f:
        if str(pk) in f.read():
            print("[likeMedia] next")
            return

    # media checked
    with open(os.path.join(confdir, 'medias_downloaded.csv'), "a") as f:
        f.write(str(pk) + "\n")

    print("[downloadMedia] Downloading media " + str(pk))
    try:
        if item_type == 1:
            cl.photo_download(pk, folder=conf["basedwndir"])
        elif item_type == 8:
            if product_type == "album":
                cl.album_download(pk, folder=conf["basedwndir"])
        elif item_type == 2:
            if product_type == "igtv":
                cl.igtv_download(pk, folder=conf["basedwndir"])
            elif product_type == "video":
                cl.video_download(pk, folder=conf["basedwndir"])
    except Exception as e:
        print("\n[downloadMedia] Some error in feed downloads vvvv ")
        print(e)


def likeMedia(conf, pk, product_type):
    cl = conf["cl"]
    confdir = conf["confdir"]
    localBotConf = botConf(conf)
    coolDownMaxValues = loadCoolDownValues(conf)

    a = bool(conf["cooldown_day"]["likes"] >= coolDownMaxValues["day_max_likes"]);
    b = bool(conf["cooldown_hour"]["likes"] >= coolDownMaxValues["hour_max_likes"]);
    if a or b:
        print("[likeMedia] Max cooldown reached, can't like ")
        print("[likeMedia] Day: " + str(a))
        print("[likeMedia] Hour: " + str(b))
        return;

    if product_type == 'ad':
        print("[likeMedia] Skipping ad")
        return

    with open(os.path.join(confdir, 'medias_liked.csv')) as f:
        if str(pk) in f.read():
            print("[likeMedia] next")
            return

    # media checked
    with open(os.path.join(confdir, 'medias_liked.csv'), 'a') as f:
        f.write(str(pk) + "\n")

    print("[likeMedia] Liking media " + str(pk))
    localBotConf.confAddLike()

    try:
        cl.media_like(pk)
    except:
        if conf['DEBUG']:
            traceback.print_exc()
        print("[likeMedia] Some error liking the media")


def commentMedia(conf, pk, username, product_type):
    cl = conf["cl"]
    confdir = conf["confdir"]
    localBotConf = botConf(conf)
    coolDownMaxValues = loadCoolDownValues(conf)

    a = bool(conf["cooldown_day"]["comments"] >= coolDownMaxValues["day_max_comments"])
    b = bool(conf["cooldown_hour"]["comments"] >= coolDownMaxValues["hour_max_comments"])
    if a or b:
        print("[commentMedia] Max cooldown reached, can't comment ")
        print("[commentMedia] Day: " + str(a))
        print("[commentMedia] Hour: " + str(b))
        return

    if product_type == 'ad':
        print("[commentMedia] Skipping ad")
        return

    with open(os.path.join(confdir, 'medias_commented.csv')) as f:
        if str(pk) in f.read():
            print("[commentMedia] next")
            return

    # media checked
    with open(os.path.join(confdir, 'medias_commented.csv'), 'a') as f:
        f.write(str(pk) + "\n")

    print("[commentMedia] Commenting media " + str(pk))
    localBotConf.confAddComment()

    try:
        possible_comments = conf["comments"]
        chosen_comment = random.choice(possible_comments)
        if '@' in chosen_comment:
            chosen_comment = chosen_comment.format(username)
        cl.media_comment(pk, text=emoji.emojize(chosen_comment))
    except:
        if conf['DEBUG']:
            traceback.print_exc()
        print("[commentMedia] Some error commenting the media")
