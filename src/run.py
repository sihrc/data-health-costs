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

def variable_lookup(datafile, tables):
    import get_features as gf
    with open(config.path("..","data",datafile,"data", "variables.txt"), 'rb') as f:
        all_tables = f.read()
        if tables.lower() == "all":
            print all_tables
            return
        index = all_tables.find(tables.strip())
        if index == -1:
            print all_tables
            print "Could not find specified variable."
            return
        end = all_tables[:index].rfind("===")
        start = all_tables[:end].rfind("===")
        rest = end + all_tables[end + 3:].find("===")
        if rest == end - 1:
            rest = -1
        print
        print all_tables[start:end].replace("=","").strip()
        print all_tables[end + 3:rest]

    return

@debug
def extract_model(path, datafile, cost, d):
    """
    Given the target cost name and data set. Extracts the model to ..\models\model_name\ for use in future
    """
    import shutil
    contTags, catTags = config.load(path)
    path = config.path("..","models", cost)
    shutil.copy(config.path("..", "data", datafile, "models", "%s.p" % cost), config.path(path, "%s.p" % cost))
    data = [d.tags[tag] for tag in contTags] + [d.tags[tag] for tag in catTags]

    config.save(config.path(path, "config.p"), len(contTags))

    with open(config.path(path, "input.csv"), 'wb') as f:
        f.write(",".join(data))

    with open(config.path(path, "features.txt"), 'wb') as f:
        f.write("\n".join([tag + "\t" + d.features[tag][1] + "\n\t" + "\n\t".join(["\t==========\t".join(line) for line in d.features[tag][2]]) + "\n" for tag in data]))

    sys.exit()

@debug
def use_model(path, cost, d):
    path = config.path("..","models", cost)
    model = config.load(config.path(path,"%s.p" % costs))
    limit = config.load(config.path(path, "config.p"))
    

    model.predict()
    pass

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
                        help = "target cost argument to extract a model for future use")

    (options, args) = parse.parse_args()

    output = sys.stdout

    if options.tables != "none":
        sys.stdout = open("runOutput.txt", 'wb')
        d = config.get(config.path("..","data",options.datafile,"data","dHandler.p"), dc.Data, datafile = options.datafile)     
        sys.stdout = output
        variable_lookup(options.datafile, options.tables) 
        sys.exit()

    if options.lookup != "":
        import feature_lookup as fl
        sys.stdout = open("runOutput.txt", 'wb')
        d = config.get(config.path("..","data",options.datafile,"data","dHandler.p"), dc.Data, datafile = options.datafile)     
        sys.stdout = output
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
        d = config.get(config.path("..","data",options.datafile,"data","dHandler.p"), dc.Data, datafile = options.datafile)     
        path = config.path("..","data", options.datafile, "models", "config_%s.p" % options.extract)
        if not os.path.exists(path):
            print "The %s model was not found under %s" % (options.extract.upper(), options.datafile)
            print "Please run \npython run.py -f [data set] -s [features] -c [cost-features] -d -t [number of trees]"
            sys.exit()
        extract_model(path, options.datafile, options.extract, d)

    if options.model != "":
        d = config.get(config.path("..","data",options.datafile,"data","dHandler.p"), dc.Data, datafile = options.datafile)     



    d = config.get(config.path("..","data",options.datafile,"data","dHandler.p"), dc.Data, datafile = options.datafile)     
    m.main(options.select.strip()[1:-1].split(","), options.costs.strip()[1:-1].split(","), d, include_costs = options.include, trees = int(options.trees))
