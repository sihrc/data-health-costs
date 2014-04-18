"""
Config.py contains configuration data like constants
Also contains notes on the data sets

author: chris @ sihrc
"""
import os
import pickle as p
from wrappers import debug


"""
Data sets
"""

codebook = "http://meps.ahrq.gov/mepsweb/data_stats/download_data/pufs/{0}/{0}su.txt"
download = "http://meps.ahrq.gov/data_files/pufs/%sdat.zip"

def path(*path):
    """
    Replacement for os.path.join
    It performs makedirs on paths that don't exists
    Returns the os.path.join() result   
    author:chris
    """
    if len(path) == 0:
        return ""
    targetpath = os.path.join(*path)
    if "." in path[-1]:
        path = path[:-1]
        targetdirs = os.path.join(*path)
        if not os.path.exists(targetdirs):
            os.makedirs(targetdirs) 
    return targetpath

def get(fpath, func, **kwargs):
    print "Checking %s ..." % fpath
    if os.path.exists(fpath):
        return p.load(open(fpath, 'rb'))
    res = func(**kwargs)
    with open(fpath, 'wb') as f:
        print "Saved to %s" % fpath
        p.dump(res, f)
    return res

def load(fpath):
    if os.path.exists(fpath):
        print "Cache Loading from %s" % fpath
        return p.load(open(fpath, 'rb'))
    else:
        return None

def save(fpath, data):
    p.dump(data, open(fpath, 'wb'))

@debug
def clean(args, datafile):
    """
    Config - clean function
    Clean previously cached items
    """
    import os
    import shutil
    delPath = path("..","data",datafile)
    if not os.path.exists(delPath): return
    for arg in args:
        pathD = os.path.join(delPath, arg)
        if os.path.exists(pathD):
            print "Cleaning ... %s" % arg
            shutil.rmtree(pathD)

