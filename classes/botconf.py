import pathlib
import json
import os, sys


class botConf():
	def __init__(self, conf):
		self.conf=conf;

	def getConf(self):
		return self.conf;

	def writeConf(self):
		tconf=self.conf.copy();
		del(tconf['cl'])		
		with open(tconf["conffile"], 'w') as fp:
			json.dump(tconf, fp, indent=4)

	def resetTodayConf(self, d):
		print("****************************************** ")
		print("********** Reset DAILY counters ********** ");
		print("****************************************** ")
		self.conf["cooldown_day"]["likes"] = 0;
		self.conf["cooldown_day"]["follows"] = 0;
		self.conf["cooldown_day"]["unfollows"] = 0;
		self.conf["cooldown_day"]["curr"] = d;
		self.writeConf();

	def resetHourConf(self, d):
		print("****************************************** ")
		print("********** Reset HOUR counters *********** ");
		print("****************************************** ")
		self.conf["cooldown_hour"]["likes"] = 0;
		self.conf["cooldown_hour"]["follows"] = 0;
		self.conf["cooldown_hour"]["unfollows"] = 0;
		self.conf["cooldown_hour"]["curr"] = d;
		self.writeConf();

	def confAddLike(self):
		self.conf["cooldown_day"]["likes"] += 1;
		self.conf["cooldown_hour"]["likes"] += 1;
		self.writeConf();

	def confAddComment(self):
		self.conf["cooldown_day"]["comments"] += 1;
		self.conf["cooldown_hour"]["comments"] += 1;
		self.writeConf();

	def confAddFollow(self):
		self.conf["cooldown_day"]["follows"] += 1;
		self.conf["cooldown_hour"]["follows"] += 1;
		self.writeConf();

	def confAddUnfollow(self):
		self.conf["cooldown_day"]["unfollows"] += 1;
		self.conf["cooldown_hour"]["unfollows"] += 1;
		self.writeConf();

	def confAddScriptFollower(self):
		self.conf["scripts_followers"] += 1;
		self.writeConf();
