"""
Main Run File
author:chris
"""

import sys

#Local Modules
import data_helper as dc
import model as m
import config

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



if __name__ == "__main__":
    from optparse import OptionParser

    parse = OptionParser()
    parse.add_option("-f", "--file", dest="datafile",
                      help="name of data set to use. i.e. H144D", metavar="FILE")
    parse.add_option("-s", "--select", dest = "select",
                      help="specify list of data features to use by table name or tag name i.e. [A,B,DUID,PID]", default = "[]")
    parse.add_option("-c", "--costs", dest = "costs", default = "[]",
                        help = "clean cached files of previous runs")
    parse.add_option("-d", "--delete", dest = "clean", default = True, action = "count",
                        help = "removes cached files of previous runs")
    parse.add_option("-p", "--print-tables", dest = "tables", default = "none",
                        help = "looks up a variable and prints the found table, or \"all\" for all tables")
    parse.add_option("-i", "--include", dest = "include", default = True, action = "count",
                        help = "includes other target costs in training data")
    parse.add_option("-t", "--trees", dest = "trees", default = 1,
                        help = "number of trees to use for decision tree algorithms")

    (options, args) = parse.parse_args()

    if options.clean:
        config.clean([\
            "data",\
            "formatted",\
            "features",\
            "models",\
            ], datafile = options.datafile)

    d = config.get(config.path("..","data",options.datafile,"data","dHandler.p"), dc.Data, datafile = options.datafile)     

    if options.tables != "none":
        variable_lookup(options.datafile, options.tables) 
        sys.exit()

    m.main(options.select.strip()[1:-1].split(","), options.costs.strip()[1:-1].split(","), d, include_costs = options.include, trees = int(options.trees))
