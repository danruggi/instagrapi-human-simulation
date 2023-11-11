import pathlib
import os, sys	
import glob

def initDirs():
	path = sys.path[0];
	dwndir = os.path.join(path, 'downloads')
	baseconfdir = os.path.join(path, "conf")

	if not os.path.exists(dwndir):
		os.mkdir(dwndir)

	if not os.path.exists(baseconfdir):
		os.mkdir(baseconfdir)

def cleanDownloads(conf):
	
	print("Clean 'downloads' dir ", end="")
	files = os.scandir(conf['basedwndir']);

	for f in files:
	    try:
	        os.remove(f.path)
	    except OSError as e:
	        print("Error: %s : %s" % (f.name, e.strerror))
	        
	print("....Done")

def cleanConf(conf):
	linesToKeep=10000;
	confdir = conf["confdir"]
	csv = ["medias.csv", "medias_downloaded.csv", "medias_liked.csv", "medias_seen.csv", "thumbs_downloaded.csv", "followed.csv", "followers.csv"];

	for f in csv:

		with open(os.path.join(confdir, f), 'r+') as fp:
		    # read an store all lines into list
		    lines = fp.readlines()
		    if (len(lines) < linesToKeep):
		    	continue

		    num = len(lines)-linesToKeep;	
		    # move file pointer to the beginning of a file
		    fp.seek(0)
		    # truncate the file
		    fp.truncate()

		    # start writing lines
		    # iterate line and line number
		    for i, line in enumerate(lines):
		        # delete line number 5 and 8
		        # note: list index start from 0
		        if i >= num:
		            fp.write(line)
