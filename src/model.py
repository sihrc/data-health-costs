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



@debug
def extract_model(datafile, cost, d):
    """
    Given the target cost name and data set. Extracts the model to ..\models\model_name\ for use in future
    """
    import shutil
    dataPath = config.path("..","data",datafile,"models",cost)
    modelPath = config.path("..","models", cost)

    #Copy the model
    shutil.copy(config.path(dataPath, "model.p"), config.path(modelPath, "model.p"))
    shutil.copy(config.path(dataPath, "features.p"), config.path(modelPath, "features.p"))
    shutil.copy(config.path(dataPath, "cont_mean.p"), config.path(modelPath, "cont_mean.p"))
    shutil.copy(config.path(dataPath, "encoder.p"), config.path(modelPath, "encoder.p"))

    train_data = config.load(dataPath, "used_to_train.p")
    np.savetxt(config.path(modelPath, "used_to_train.csv"), train_data, fmt = "%g", delimiter = ",")
    
    #Create csv for feature input
    cont, cat = config.load(dataPath, "features.p")
    with open(config.path(modelPath, "input.csv"), 'wb') as f:
        f.write(",".join([d.tags[tag] for tag in cont + cat]) + "\n")
        f.write(",".join(list(train_data[1,:].astype('str'))))

@debug
def use_model(cost, d):
    """
    Uses extracted model from ../models
    Predicts based on inputs saved in csv
    """
    path = config.path("..","models", cost)
    model = config.load(path,"model.p")
    cont_mean = config.load(path,"cont_mean.p")
    encoder = config.load(path, "encoder.p")
    
    data = np.atleast_2d(np.genfromtxt(config.path(path, "input.csv"), delimiter = ",", dtype = str))
    cont, cat = config.load(path, "features.p") 
    cont = data[1:,:len(cont)].astype('float')
    cat = data[1:,:len(cat)]
    if len(cont) == 0:
        print "Please input data to feed the model in ..\models\%s\input.csv" % cost
        return
    # print cont_mean
    cont, newCats, cont_mean = ff.formatContinuous(data = cont, d = d, mean = cont_mean)
    for x in xrange(cat.shape[0]):
        for y in xrange(cat.shape[1]):
            str_val = str(cat[x,y])
            if str_val not in d.catMapper:
                cat[x,y] = d.catMapper["NAN"]
            else:
                cat[x,y] = d.catMapper[str_val]
    cat = np.hstack((cat.astype("int"), newCats.astype("int")))
    cat = encoder.transform(cat).toarray()
    prediction = model.predict(np.hstack((cont,cat))).astype(str)
    print "Predicted costs of:\n%s" % "$" + "\n$".join(list(prediction))

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
    cont, newCats, mean = ff.formatContinuous(data = data[:,cont_tags], d = d)
    encoder, cat = ff.one_hot(data = np.hstack((data[:,cat_tags].astype("int"), newCats)), d = d)

    #Set up Training Data
    x_train = np.hstack((cont,cat))
    y_train = data[:,cost_tags]

    results = []
    #Loops through every cost found in datafile
    for target, costIndex in enumerate(cost_tags):
        if include_costs:
            x_train_ = np.hstack((x_train, y_train[:,:target], y_train[:,target + 1:]))
            cont_tags_ = cont_tags + cost_tags[:target] + cost_tags[target + 1:]
        else:
            x_train_ = x_train
            cont_tags_ = cont_tags

        #Creating Model and Testing
        model = create_model(x_train = x_train_, y_train = y_train[:,target], trees = trees)
        accuracy = model_score(model, x_train_, y_train[:,target])
        
        #Sorting and Writing Important Features
        ff.writeFeatures(costFeature = costIndex, importance = model.feature_importances_, d = d)        
        
        #Splitting to testing and training datasets
        costTag =  d.tags[costIndex]
        results.append("Model accuracy for cost:%s%saccuracy:%.2f\n" % (costTag, (30 - len(costTag)) * " ", accuracy))
        modelPath = config.path(path, "models", costTag)
        config.save(config.path(modelPath, "features.p"), (cont_tags_, cat_tags))
        config.save(config.path(modelPath,"model.p"), (model))
        config.save(config.path(modelPath, "used_to_train.p"), data[:5,cont_tags_ + cat_tags])
        config.save(config.path(modelPath, "cont_mean.p"), mean)
        config.save(config.path(modelPath, "encoder.p"), encoder)
    print "\n".join(results)
