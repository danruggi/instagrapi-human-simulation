from libs.config import *
from libs.media import downloadThumb;

from classes.botconf import botConf

import random
import time
from datetime import datetime, tzinfo, date, timezone
#import calendar

from langdetect import detect

def getNewFollowers(conf, cursor=None):
	cl=conf["cl"]
	confdir = conf["confdir"]
	username = conf["username"]
	localBotConf = botConf(conf);

	my_pk = cl.user_id_from_username(username)
	my_user_id_infos = cl.user_info(my_pk);
	# followers = cl.user_followers(my_pk);
	followers, cursor = cl.user_followers_v1_chunk(my_pk, 100, cursor)

	for x in followers:
		if x.pk not in open(os.path.join(confdir, "followers.csv")).read():
			print("[GetNewFollowers] Registering follower "+x.username);
			with open(os.path.join(confdir, "followers.csv"), "a") as f:
				f.write(x.pk+"\n")

			if x.pk in open(os.path.join(confdir, "followed.csv")).read():
				#get when followed
				with open(os.path.join(confdir, "followed.csv"), 'rt') as f:
					data = f.readlines()
				
				diffInDays=None
				for line in data:
					if (x.pk in line):
						t = line.split(":")[0]
						diffInDays = int((time.mktime(time.strptime(str(datetime.now(timezone.utc)).split(".")[0], "%Y-%m-%d %H:%M:%S")) - float(t))/14400);

				localBotConf.confAddScriptFollower()

				print("[GetNewFollowers] User "+x.username+" is a NEW follower, followed "+str(diffInDays)+" days ago");
				if diffInDays <= 3:
					sendMessage(conf, x.pk)
					time.sleep(10)

	return


def sendMessage(conf, pk):
	cl=conf["cl"]
	confdir = conf["confdir"]
	username = conf["username"]

	#### Send Message part
	if conf["messages"]["active"] == 0:
		return

	with open(os.path.join(confdir, 'messages.csv'), 'r') as f:
		if pk in f.read():
			return
	
	user_info = cl.user_info(pk);
	bio = user_info.biography;
	try:
		lan = detect(bio);
	except:
		lan = 'en'
	if lan not in conf["messages"].keys():
		lan = "en"
	m = conf["messages"]["texts"][lan];

	print("[SendMessage] Sending Message in "+lan);
	with open(os.path.join(confdir, 'messages.csv'), 'a') as f:
		f.write(pk+"\n")

	# cl.direct_send(m, [9518783079]);
	cl.direct_send(m, [pk]);