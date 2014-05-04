"""
Feature Selection using sci-kit learn
author:chris
"""

# Python Modules
# from sklearn.ensemble import GradientBoostingRegressor as Model
# from sklearn.linear_model import Ridge as Model
from sklearn.ensemble import RandomForestRegressor as Model
from sklearn.cross_validation import train_test_split
# from sklearn.metrics import mean_squared_error as score
from sklearn.metrics import explained_variance_score as score
import numpy as np

#Local Modules
from wrappers import debug
import features as ff
import data_helper as dc
import config


@debug
def load_data(d):
    """
    Loads numpy array from CSV file
    """
    return np.genfromtxt(config.path("..","data",d.datafile, "data", d.datafile.lower() + ".csv"), delimiter=",")

@debug
def create_model(x_train, y_train, trees):
    """
    Creates and fits the model based on x_train and y_train
    Returns model as specified in import
    """
    model =  Model(trees)
    model.fit(x_train, y_train)
    return model


@debug
def model_score(model, train, test):
    """
    The coefficient R^2 is defined as (1 - u/v), 
     where u is the regression sum of squares ((y_true - y_pred) ** 2).sum()
     and v is the residual sum of squares ((y_true - y_true.mean()) ** 2).sum().
    Best possible score is 1.0, lower values are worse.
    """
    return model.score(train,test)

# @debug
# def extract_model(path, datafile, cost, d):
#     """
#     Given the target cost name and data set. Extracts the model to ..\models\model_name\ for use in future
#     """
#     import shutil
#     catTags, contTags = config.load(path)
#     path = config.path("..","models", cost)

#     shutil.copy(config.path("..", "data", datafile, "models", "%s_example_data.csv" % cost), config.path(path, "training_data_%s.csv" % cost))

#     data = [d.tags[tag] for tag in catTags] + [d.tags[tag] for tag in contTags]

#     config.save(config.path(path, "config.p"), len(contTags))

#     with open(config.path(path, "input.csv"), 'wb') as f:
#         f.write(",".join(data))

#     with open(config.path(path, "features.txt"), 'wb') as f:
#         f.write("\n".join([tag + "\t" + d.features[tag][1] + "\n\t" + "\n\t".join(["\t==========\t".join(line) for line in d.features[tag][2]]) + "\n" for tag in data]))

#     sys.exit()

# @debug
# def use_model(cost, d):
#     """
#     Uses extracted model from ../models
#     Predicts based on inputs saved in csv
#     """
#     path = config.path("..","models", cost)
#     model = config.load(path,"%s.p" % cost))
#     limit = config.load(path, "config.p"))

#     with open(config.path(path, "input.csv"), 'rb') as f:
#         read = f.readlines()
#         if len(read) == 1:
#             print "Please input data to feed the model in ..\models\%s\input.csv" % cost
#             return

#     tags = read[0].strip().split(",")
#     cont = []
#     cat = []
#     for line in read[1:]:
#         data = line.strip().split(",")
#         cat.append(data[limit-1:])
#         try:
#             cont.append([float(num) for num in data[:limit-1]])   
#         except:
#             print "%s is not a valid value" % num

#     cont = np.array(cont)
#     cat = np.array(cat)

#     for x,row in enumerate(cat):
#         for y,col in enumerate(row):
#             if col in d.catMapper:
#                 cat[x][y] = int(d.catMapper[col])
#             else:
#                 print "Category: %s not found in %s at row %d" % (col, tags[y], x)

#     encoder = config.load("..","data", d.datafile,"encoder.p"))
#     cat = encoder.transform(np.hstack((cat.astype("float").astype("int"))))

#     train_ = np.hstack((cont[:-1,], cat[:-1,]))
#     prediction = model.predict(train_)
#     print "Predictions for %s with the data given:" % (cost)
#     print list(enumerate(prediction))
#     return

@debug
def extract_model(datafile, cost, d):
    import shutil
    dataPath = config.path("..","data",datafile,"models",cost)
    modelPath = config.path("..","models", cost)

    #Copy the model
    shutil.copy(config.path(dataPath, "model.p"), config.path(modelPath, "model.p"))
    
    #Create csv for feature input
    cont, cat = config.load(dataPath, "features.p"))
    shutil.copy(config.path(dataPath, "features.p"), config.path(modelPath, "features.p"))
    with open(config.path(modelPath, "input.csv")) as f:
        f.write(",".join([d.tags[tag] for tag in cont + cat]))


@debug
def use_model(datafile, cost, d):
    path = config.path("..","models", cost)
    model = config.load(path,"model.p"))

    data = np.genfromtxt(config.path(path, "input.csv"), delimiter = ",", dtype = str)
    cont, cat = config.load(modelPath, "features.p")

    cont = data[1:,:len(cont)]
    cat = data[1:,:len(cat)]




@debug
def main(featureTags, costTags, d, include_costs = False, trees = 10, test = True):
    """
    Performs feature selection given datafile
    """
    #Get Data Handler
    path = config.path("..","data",d.datafile)
    
    #Parsing features
    cat_tags, cont_tags, cost_tags = ff.extract_features(d, featureTags, costTags)

    #Get feature and target data
    data = load_data(d)
    cont, newCats = ff.formatContinuous(data = data[:,cont_tags], d = d)
    cat = ff.one_hot(data = np.hstack((data[:,cat_tags].astype("int"), newCats)), datafile = d.datafile)

    #Set up Training Data
    x_train = np.hstack((cont,cat))
    y_train = data[:,cost_tags]

    results = []
    #Loops through every cost found in datafile
    for target, costIndex in enumerate(cost_tags):
        if include_costs:
            x_train_ = np.hstack((x_train, y_train[:,:target], y_train[:,target + 1:]))
        else:
            x_train_ = x_train

        #Creating Model and Testing
        model = create_model(x_train = x_train_, y_train = y_train[:,target], trees = trees)
        accuracy = model_score(model, x_train_, y_train[:,target])
        results.append("Model accuracy for cost:%s%saccuracy:%.2f\n" % (costTag, (30 - len(costTag)) * " ", accuracy))
        
        #Sorting and Writing Important Features
        ff.writeFeatures(costFeature = costIndex, importance = model.feature_importances_, d = d)        
        
        #Splitting to testing and training datasets
        costTag =  d.tags[costIndex]
        config.save(config.path(path, "models", costTag,"features.p"), (cont_tags, cat_tags))
        config.save(config.path(path, "models", costTag,"model.p"), (model))
    print "\n".join(results)
