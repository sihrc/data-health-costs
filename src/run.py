"""
Main Run File
author:chris
"""

import sys, os

#Local Modules
import data_helper as dc
import model as m
import config
from wrappers import debug

def variable_lookup(d, tables):
    import get_features as gf
    if tables == "all":
        for title, tags in sorted(d.titleMap.items()):
            print "\n\n=== %s :: %s ===\n" % (title, tags[0])
            print "\n".join(["\t%s%s%s" % (tag, (18 - len(tag))*" ",d.features[tag][1]) for tag in tags[1] if tag in d.features])            
        return

    for title,tags in d.titleMap.items():
        if tables in tags[1]:
            print "\n\n=== %s :: %s ===\n" % (title, tags[0])
            print "\n".join(["\t%s%s%s" % (tag, (18 - len(tag))*" ",d.features[tag][1]) for tag in tags[1] if tag in d.features])
    return


if __name__ == "__main__":
    from optparse import OptionParser

    parse = OptionParser()
    parse.add_option("-f", "--file", dest="datafile",
                      help="name of data set to use. i.e. H144D", metavar="FILE")
    parse.add_option("-s", "--select", dest = "select",
                      help="specify list of data features to use by table name or tag name i.e. [A,B,DUID,PID]", default = "[]")
    parse.add_option("-c", "--costs", dest = "costs", default = "[]",
                        help = "clean cached files of previous runs")
    parse.add_option("-d", "--delete", dest = "clean", default = False, action = "count",
                        help = "removes cached files of previous runs")
    parse.add_option("-p", "--print-tables", dest = "tables", default = "none",
                        help = "looks up a variable and prints the found table, or \"all\" for all tables")
    parse.add_option("-i", "--include", dest = "include", default = False, action = "count",
                        help = "includes other target costs in training data")
    parse.add_option("-t", "--trees", dest = "trees", default = 1,
                        help = "number of trees to use for decision tree algorithms")
    parse.add_option("-l", "--lookup", dest = "lookup", default = "",
                        help = "looks up specific variable and prints descriptions and values")
    parse.add_option("-u", "--use", dest = "model", default = "",
                        help = "use an extracted model to predict costs")
    parse.add_option("-e", "--extract", dest = "extract", default = "",
                        help = "target cost argument to create a model for future use")

    (options, args) = parse.parse_args()

    output = sys.stdout

    if options.tables != "none":
        print "Looking up tables, please wait..."
        # sys.stdout = open("runOutput.txt", 'wb')
        d = config.get(config.path("..","data",options.datafile,"data","dHandler.p"), dc.Data, datafile = options.datafile)     
        # sys.stdout = output
        variable_lookup(d, options.tables) 
        sys.exit()

    if options.lookup != "":
        import feature_lookup as fl
        print "Looking up feature, please wait..."
        # sys.stdout = open("runOutput.txt", 'wb')
        d = config.get(config.path("..","data",options.datafile,"data","dHandler.p"), dc.Data, datafile = options.datafile)     
        # sys.stdout = output
        print "======================================="
        print  fl.getDetails(options.datafile, options.lookup)["Description"]
        print
        print  fl.getDetails(options.datafile, options.lookup)["Values"]
        print "======================================="
        sys.exit()

    if options.clean:
        config.clean([\
            "data",\
            "features",\
            "models",\
            ], datafile = options.datafile)

    if options.extract != "":
        options.extract = options.extract.strip()
        d = config.get(config.path("..","data",options.datafile,"data","dHandler.p"), dc.Data, datafile = options.datafile)     
        if options.extract not in d.tags:
            print "%s is not a feature in %s" % (options.extract, options.datafile)
            sys.exit()
        path = config.path("..","data", options.datafile, "models", "config_%s.p" % options.extract)
        if not os.path.exists(path):
            m.main(options.select.strip()[1:-1].split(","), [options.extract], d, include_costs = options.include, trees = int(options.trees), test = False)
        m.extract_model(options.datafile, options.extract, d)
        sys.exit()

    if options.model != "":
        m.use_model(options.model.strip().upper())
        sys.exit()



    d = config.get(config.path("..","data",options.datafile,"data","dHandler.p"), dc.Data, datafile = options.datafile)     
    
    #Jazmin's looping things
    featuredTags = []
    d = config.get(config.path("..","data",options.datafile,"data","dHandler.p"), dc.Data, datafile = options.datafile) 
    tags = ["IPCCC3X" ,"IPCCC4X" ,"IPDOF11X","IPPRO2X" ,"DLVRTYPE","FFIPTYPE","IPPRO1X" ,"NUMNIGHT","ANYOPER" ,"IPICD4X" ,"IPCCC2X" ,"IPICD1X" ,"SPECCOND","VARPSU"  ,"IPBEGMM" ,"IPCCC1X" ,"IPICD3X" ,"IPBEGYR" ,"VARSTR"  ,"RSNINHOS","IPBEGDD" ,"NUMNIGHX","IPENDMM" ,"PERWT11F","IPICD2X" ,"EMERROOM","IPENDYR" ,"IPENDDD" ,"EPIDURAL","IMPFLAG" ]
    for tag in tags:
        featuredTags.append(tag)    
        m.main(featuredTags, options.costs.strip()[1:-1].split(","), d, include_costs = options.include, trees = int(options.trees))