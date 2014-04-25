"""
Config.py contains configuration data like constants
Also contains notes on the data sets

author: chris @ sihrc
"""
import os
import pickle as p
import numpy as np
from wrappers import debug


"""
Data sets
"""

codebook = "http://meps.ahrq.gov/mepsweb/data_stats/download_data/pufs/{0}/{0}su.txt"
download = "http://meps.ahrq.gov/data_files/pufs/%sdat.zip"
tables = "http://meps.ahrq.gov/mepsweb/data_stats/download_data/pufs/{0}/{0}doc.shtml"

def path(*path):
    """
    in config.py
    It performs makedirs on paths that don't exists
    Returns the path   
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


def getNP(fpath, func, **kwargs):
    """
    in config.py
    Caching function for sparse matrices
    """
    print "Checking %s ..." % fpath
    if os.path.exists(fpath):
        return np.load(fpath)
    res = func(**kwargs)
    print "Saved to %s" % fpath
    res.dump(fpath)
    return res

def get(fpath, func, **kwargs):
    """
    in config.py
    Caching function
    """
    print "Checking %s ..." % fpath
    if os.path.exists(fpath):
        return p.load(open(fpath, 'rb'))
    res = func(**kwargs)
    with open(fpath, 'wb') as f:
        print "Saved to %s" % fpath
        p.dump(res, f)
    return res

def load(fpath):
    """
    in config.py
    Pickle load that checks for path
    """
    if os.path.exists(fpath):
        print "Cache Loading from %s" % fpath
        return p.load(open(fpath, 'rb'))
    else:
        return None

def save(fpath, data):
    """
    in config.py
    Pickle save
    """
    p.dump(data, open(fpath, 'wb'))

def write(fpath, data):
    with open(fpath, 'wb') as f:
        f.write("{0}".format(data))

@debug
def clean(args, datafile):
    """
    in config.py
    Config - clean function
    Clean previously cached items
    """
    import os
    import shutil
    delPath = path("..","data",datafile)
    if not os.path.exists(delPath): return
    always = False
    for arg in args:
        pathD = os.path.join(delPath, arg)
        if os.path.exists(pathD):
            if always:
                shutil.rmtree(pathD)
                print "Cleaning ... %s" % arg
            else:
                response = raw_input("Clean %s?(y/n/a)" % arg)
                response = "a"
                if response.lower() == "a": 
                    always = True
                    response = "y"
                if response.lower() == "y":
                    shutil.rmtree(pathD)
                    print "Cleaning ... %s" % arg
                else:
                    print "Did not clean %s" % arg
                    continue

