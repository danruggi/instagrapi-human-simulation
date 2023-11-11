from instagrapi import Client

import random
import time
import os
import json
import sys

from libs.config import *
from classes.botconf import *
def create_user(u, p, t, conf):
	
	conf = loadUserConf(conf, u)
	#### instagrapi file

	if not os.path.exists(conf['confdir']):
		os.mkdir(conf['confdir'])
	else:
		print(f"User Folder {u} already exists")
		return

	print(conf)

	#### bot user config
	conf.update({"username": u, "password": p, "tags": t, "cooldown_day": {"curr": 0, "follows": 0, "likes": 0, "unfollows": 0}, "cooldown_hour": {"curr": 0, "follows": 0, "likes": 0, "unfollows": 0}, "scripts_followers":0, "forced_words":"", "messages": {"active": 1, "texts":{"en": "Hi Thanks for the follow! How are you?", "es": "Gracias por el follow! \nComo estás?", "it": "Piacere, \ngrazie per il follow!"} } })
	localBotConf = botConf(conf);
	localBotConf.writeConf()

	coolconf = {"day_max_follows": 30, "day_max_likes": 80, "day_max_unfollows": 50, "hour_max_follows": 6, "hour_max_likes": 15, "hour_max_unfollows": 10 }
	with open(conf['cooldownfile'], 'w') as fp:
		json.dump(coolconf, fp, indent=4)

	csv = ["medias.csv", "medias_downloaded.csv", "medias_liked.csv", "medias_seen.csv", "thumbs_downloaded.csv", "followed.csv", "followers.csv", "messages.csv"];
	for fn in csv:
		fnp = os.path.join(conf['confdir'], fn)
		if not os.path.exists(fnp):
			open(fnp, 'w').close()

	return

def new_user(conf):
	print()
	print("++ A new directory will be created under ./conf/$(USERNAME)/ with ")
	print("++ all the needed configurations for new user")
	print()
	u = str(input(">> New Username: "))
	p = str(input(">> New Password: "))
	print ()
	print ()
	print ("++ Insert all tags of interest, separated by a ';'. Ie, ")
	print ("++ dog;puppy;puppies;dogs;dogslover;puppylover;puppy35")
	print ("++ Just alfanumeric chars are accepted ")
	t = str(input(">> Tags: "))
	create_user(u, p, t, conf)


