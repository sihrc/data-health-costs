"""
Data Acquisition 
author:chris @ sihrc
"""

#Python Modules
import string
from re import search

#Local Modules
import config
from wrappers import debug
import get_features as gf

class Data():
    """
    in data.py
    Data Handler object that has methods for handling references 
    for our variables, such as looking up variables,
    getting data for features as well as loading data, 
    saving and loading temporary sessions
    """
    def __init__ (self, datafile = ""):
        self.datafile = datafile
        self.features = {}
        self.tags = []
        self.costs = []
        self.categorical = []
        self.continuous = []

        self.parseCodebook()
        self.writeDataCSV()
        self.getCostFeatures()
        self.varTables = config.get(config.path("..","data",datafile,"data","varTables.p"), gf.read_tables, datafile = datafile)
        self.writeTables()

    @debug
    def writeDataCSV(self):
        """
        Download data
        """
        def download(self):
            import zipfile
            import urllib
            dfile = config.path("..","data",self.datafile.upper(), self.datafile.upper() + ".zip")
            urllib.urlretrieve(config.download % self.datafile.lower(), dfile)
            with zipfile.ZipFile(dfile) as zf:
                zf.extractall(config.path("..","data",self.datafile.upper(),"data"))

        path = config.path("..","data",self.datafile, "data", self.datafile.lower())

        if not config.os.path.exists(path + ".dat"):    download(self)
        if config.os.path.exists(path + ".csv"): return

        indices = [self.features[tag][0] for tag in self.tags]
        printFormat = "".join(["%s" * (high - low) + "," for low,high in zip(indices, indices[1:])])
        with open(path+".csv", 'wb') as g:
            with open(path + ".dat", 'rb') as f:
                format_ = printFormat + "%s" * (len(f.readline().strip()) - indices[-1] + 1)
                for line in f:
                    g.write(format_ % tuple(line.strip()) + "\n")
        return

    @debug
    def getCostFeatures(self):
        """
        Get target cost features from data set
        author: chris
        """
        self.costs = []
        for feature, details in self.features.items():
            if "$" in details[-1][-1][1]:
                if sum([type(search("\W+%s[\WS]+" % x, details[1])) != type(None) for x in ["PAYMENT", "COST", "CHG", "CHARGE", "FEE", "EXP", "EXPENSE", "PD","PAID"]]) > 0:       
                    index = self.tags.index(feature)
                    if index in self.categorical:
                        self.categorical.remove(index)
                    if index in self.continuous:
                        self.continuous.remove(index)
                    self.costs.append(index)
        if len(self.costs) == 0:
            print "WARNING: THIS DATASET HAS NO COST DATA"
        

    @debug
    def parseCodebook(self):
        """
        Given the datafile name, returns the codebook needed
        author: chris
        """
        import urllib2, unicodedata
        def download(path):
            page = urllib2.urlopen(config.codebook.format(self.datafile.lower())).read()
            with open(path, 'wb') as f:
                f.write(page)
            return page
        path = config.path("..","data",self.datafile,"data","codebook.txt")

        if not config.os.path.exists(path):
            page = download(path)
        else:
            with open(path, 'rb') as f:
                page = f.read()

        _input  = page.find("* INPUT STATEMENTS;")
        _format = page.find("* FORMAT STATEMENTS;")
        _label  = page.find("* LABEL STATEMENTS;")
        _value  = page.find("* VALUE STATEMENTS;")

        indices = page[_input:_format]
        mapping = page[_format:_label]
        desc = page[_label: _value]
        values = page[_value:]

        for line in indices.split("\n")[3:]:
            if line.strip() == ";":
                break
            split = line.split()
            self.tags.append(split[-2].strip())
            self.features[split[-2].strip()] = [int(split[-3].strip()[1:])]
        for line in desc.split("\n")[1:]:
            if line.strip() == ";":
                break
            split = line.split("=")
            self.features[split[0].strip().split()[-1]].append(split[1].strip())
        
        mapper = {}
        for line in mapping.split("\n")[1:]:
            if line.strip() == ";":
                break
            split = line.split()
            mapper[split[-1].strip()[:-1]] = split[-2].strip()


        tag = ""
        value_list = []
        count = 0
        cost_tags = [self.tags[cost] for cost in self.costs]
        for line in values.split("\n")[1:]:
            if line.strip() == "":
                continue
            if "VALUE" in line[:6]:
                tag = mapper[line.split()[1].strip()]
                continue
            if "=" in line:
                split = line.split("=")
                value_list.append((split[0].strip(), split[1].strip()))
            if ";" == line.strip()[0]:
                check = value_list[-1][-1]
                if "-" in check and check.split("-")[-1].strip()[0] not in string.letters:
                    self.continuous.append(self.tags.index(tag))
                else:
                    self.categorical.append(self.tags.index(tag))
                self.features[tag].append(value_list)
                value_list = []
                continue
        return

    @debug
    def writeTables(self):
        """
        In data.py
        Writing tables to file for user to reference
        """
        path = config.path("..","data",self.datafile,"data", "variables.txt")
        if config.os.path.exists(path):
            return
        with open(path, 'wb') as f:
            f.write("Variables found for data set %s\n" % self.datafile)
            for title, tables in self.varTables.items():
                f.write("\n\n=== %s ===\n" % title)
                f.write("\n".join(["\t%s\t%s" % (tag, self.features[tag][1]) for tag in tables if tag in self.features]))

    def getTagIndices(self,tagNames):
        return [self.tags.index[tag] for tag in tagNames]
    
    def printTargetTags(self):
        print "\n".join([self.tags[tag] + "\t" + self.features[self.tags[tag]][1] for tag in self.costs])
    """
    Class native methods
    """
    def __repr__(self):
        return "Data Handler Object"

    def __str__(self):
        return "Attributes: \ndata\t\t - contains dataset as a numpy array\nindicies\t - contains variables:indicies dictionary\nfeatures\t - contains variables:feature descriptions as dictionary\n\npandas data file at [].csv"

if __name__ == "__main__":
    import sys
    data = Data(sys.argv[1])

