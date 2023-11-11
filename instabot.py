from instagrapi import Client
from instagrapi.exceptions import (
    BadPassword, ReloginAttemptExceeded, ChallengeRequired,
    SelectContactPointRecoveryForm, RecaptchaChallengeForm,
    FeedbackRequired, PleaseWaitFewMinutes, LoginRequired
)
from datetime import datetime, tzinfo, date, timezone
#import calendar
import pytz

import time
import random
import os, sys
import pathlib
import urllib
import urllib.request

import json

### my classes
# import classes.errors
# from classes.botconf import *

import argparse

from libs.stats import printStats
from libs.feed import gefFromFeed
from libs.getfromhashtag import getFromHashtag
from libs.newfollowers import getNewFollowers
from libs.unfollowusers import unfollowUsers
from libs.cooldown import *
from libs.intro import intro
from libs.config import *
from libs.init import *

from modules.new_user import *

def parseArgs():
	# Arguments and help
	parser = argparse.ArgumentParser(description="Human Being simulator using Instagram, to get follows back")
	subparsers = parser.add_subparsers(dest='command')
	createUser = subparsers.add_parser('new', help="Create new user dir and config files")
	noInput = subparsers.add_parser('user', help="To run application without the need of providing input. Provide direcly the username",)
	noInput.add_argument("user", help="provide the desired username", type=str)
	noInput.add_argument("-max_exec", default=0, help="Set how many execution to run, before to exit", type=int)
	args = parser.parse_args()

	conf = {'METHOD': args.command}
	if args.command == 'user':
		conf['USER'] = args.user
		conf['MAX_EXEC'] = args.max_exec

	return conf	

def main():
	conf = parseArgs()
	cl = Client() 
	print(cl)

	conf['cl'] = cl

	## Create folders if missing
	initDirs()
	conf = loadMainConf(conf)

	method = conf['METHOD']
	del(conf['METHOD'])
	if method == 'new':
		new_user(conf)
		cl.dump_settings(conf['loginfile'])
		quit()

	intro()

	if 'USER' not in conf:

		users=next(os.walk(conf['baseconfdir']))[1] 
		i=1
		for user in users:
			print (str(i)+" > "+user)
			i+=1

		position = -1
		while position<=0 or position>len(users):
			position = int(input("Chose user: "))

		### GLOBAL VARS
		conf['USER'] = users[position-1]	
		conf['MAX_EXEC'] = 0

	
	conf = loadUserConf(conf, conf['USER'])
	coolDownMaxValues = loadCoolDownValues(conf)

	# Init botConf with actual conf
	localBotConf = botConf(conf);

	username = conf["username"]
	password = conf["password"]
	tags = conf["tags"].split(";")
	confdir = conf["confdir"]

	#### INIT
	cleanDownloads(conf)
	cleanConf(conf)

	print(conf)

	### check instagrapi conf file 
	if not os.path.isfile(conf["loginfile"]):
		print("File login not found")
		quit()

	# LOGIN
	cl.load_settings(conf["loginfile"])

	print (" >>>>>> Login <<<<<< ")
	cl.login(username, password)

	print(" Logged in.. saving settings");
	cl.dump_settings(conf["loginfile"])

	print(" >>>>>> Begin <<<<<< ")
	execution_counter=1

	printStats(conf)
	
	while 1:
		# Today in UTC
		cooldown_day_ts=conf["cooldown_day"]["curr"]
		today_ts=time.mktime(time.strptime(str(datetime.now(timezone.utc)).split(" ")[0], '%Y-%m-%d'))
		if (today_ts > cooldown_day_ts):
			## Reset daily counters
			localBotConf.resetTodayConf(today_ts)

		### This hour in UTC
		hour_ts=time.mktime(time.strptime(str(datetime.now(timezone.utc)).split(":")[0], '%Y-%m-%d %H'))
		cooldown_hour_ts=conf["cooldown_hour"]["curr"]
		if (hour_ts > cooldown_hour_ts):
			localBotConf.resetHourConf(hour_ts)

		print("****************************************** ")
		print("#### Execution # "+str(execution_counter))
		
		if not coolDownCheckDay(conf, coolDownMaxValues):
			print("Cool Down Values Reached for the day, no go, sleep 4 hours")
			time.sleep(7200)
			continue

		if not coolDownCheckHour(conf, coolDownMaxValues):
			print("Cool Down Values Reached for the Hour, no go, sleep 10 minutes")
			time.sleep(600)
			continue


		getNewFollowers(conf)

		#########
		# FEED
		# print(" Getting my feed")

		r1=random.randint(0,10)
		# if r1<6:
		# 	print(" ++ Getting my feed")
		# 	gefFromFeed(conf)
		# 	s=random.uniform(.5,5)
		# 	time.sleep(s)

		if r1<3:
			unfollowUsers(conf)

		#########
		# HASTAGS
		getFromHashtag(conf)

		printStats(conf)
		
		#########
		# SLEEP
		r1=random.randint(0,100)
		if r1<10:
			r=random.randint(3600,14400) #night every ~10 exec
		elif r1<20:
			r=random.randint(600, 3600)
		elif r1<50:
			r=random.randint(60,360)
		else:
			r=random.randint(10,60)

		print("#### End Execution # "+str(execution_counter))
		execution_counter += 1

		if conf['MAX_EXEC'] > 0 and execution_counter > conf['MAX_EXEC']:
			break

		print("Sleeping "+str(r)+" seconds")
		print("****************************************** ")
		time.sleep(r)

main()










print("#### FINISH ")