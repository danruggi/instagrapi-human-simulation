import os, sys
import json

def loadMainConf(conf):
	path = sys.path[0];
	
	conf["basedwndir"]=os.path.join(path, 'downloads')
	conf["baseconfdir"] = os.path.join(path, "conf")

	return conf;

def loadUserConf(conf, user):

	confdir = os.path.join(conf["baseconfdir"], user)
	conffile = os.path.join(confdir, "conf.json")

	if os.path.isfile(conffile):
		with open(conffile, 'r') as f:
			conf.update(json.load(f))
	
	conf['confdir']=confdir	
	conf["conffile"]=conffile
	conf["loginfile"] = os.path.join(confdir, "login.json")
	conf["cooldownfile"] = os.path.join(confdir, "cool_down_conf.json")

	return conf

def loadCoolDownValues(conf):
	confdir=conf["confdir"];

	with open(conf['cooldownfile']) as f:
		coolDownMaxValues = json.load(f)

	return coolDownMaxValues;