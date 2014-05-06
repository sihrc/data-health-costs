"""
Feature Selection using sci-kit learn
author:chris
"""

# Python Modules
# from sklearn.ensemble import GradientBoostingRegressor as Model
# from sklearn.linear_model import Ridge as Model
from sklearn.ensemble import RandomForestRegressor as Model
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error as score
# from sklearn.metrics import explained_variance_score as score
# from sklearn.metrics import r2_score as score
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
    # model =  Model(trees, oob_score = True)
    model =  Model()
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
    shutil.copy(config.path(dataPath, "dHandler.p"), config.path(modelPath, "dHandler.p"))

    #Sample Data
    train_data = config.load(dataPath, "used_to_train.p")
    np.savetxt(config.path(modelPath, "used_to_train.csv"), train_data, fmt = "%g", delimiter = ",")
        
    #Create csv for feature input
    cont, cat = config.load(dataPath, "features.p")
    print train_data.shape
    with open(config.path(modelPath, "input.csv"), 'wb') as f:
        f.write(",".join([d.tags[tag] for tag in cont + cat]) + "," + cost + "\n")
        f.write(",".join(list(train_data[0].astype('str'))))


def manual_error_score(real, prediction):
    diff = (prediction - real)
    bigger = prediction > real
    scale = np.zeros(prediction.shape)
    scale[bigger] = prediction[bigger]
    scale[np.invert(bigger)] = real[np.invert(bigger)]
    scale[diff == 0] = 1
    
    return 1 - np.mean(np.abs(diff)/scale)


@debug
def use_model(cost):
    """
    Uses extracted model from ../models
    Predicts based on inputs saved in csv (contains sample data)
    """
    path = config.path("..","models", cost)
    model = config.load(path,"model.p")
    cont_mean = config.load(path,"cont_mean.p")
    encoder = config.load(path, "encoder.p")
    d = config.load(path, "dHandler.p")

    data = np.atleast_2d(np.genfromtxt(config.path(path, "input.csv"), delimiter = ",", dtype = str))
    cont, cat = config.load(path, "features.p") 
    cont = data[1:,:len(cont)].astype('float')
    cat = data[1:,-len(cat)-1:-1]
    cost = data[1:,-1]

    if len(cont) == 0:
        print "Please input data to feed the model in ..\models\%s\input.csv" % cost
        return

    cont, newCats, cont_mean = ff.formatContinuous(data = cont, d = d, mean = cont_mean)
    cat = np.hstack((cat, newCats))
    for x in xrange(cat.shape[0]):
        for y in xrange(cat.shape[1]):
            str_val = str(cat[x,y])
            if str_val not in d.catMapper:
                cat[x,y] = d.catMapper["NAN"]
            else:
                cat[x,y] = d.catMapper[str_val]
    cat = encoder.transform(cat.astype("int")).toarray()
    prediction = model.predict(np.hstack((cont,cat))).astype(str)
    print "Predicted costs of:\n%s" % "$" + "\n$".join(list(prediction))
    # print "Test cost of:\n%s" % "$" + "\n$".join(list(cost)) # for testing purposes

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
    encoder, cat = ff.one_hot(data = np.hstack((data[:,cat_tags], newCats)), d = d)

    #Set up Training Data
    x_train = np.hstack((cont,cat)) 
    y_train = data[:,cost_tags]
    if test:    x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size = .1, random_state = 42)

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
        if test:
            x_test_ = np.hstack((x_test, y_test[:,:target], y_test[:,target + 1:])) if include_costs else x_test
            prediction = model.predict(x_test_)
            accuracy = manual_error_score(y_test[:,target], prediction)

            # prediction = model.predict(np.zeros(x_test_.shape))
            # config.save(config.path("results", d.tags[costIndex], "prediction.p"), prediction)
            # config.save(config.path("results", d.tags[costIndex], "real.p"), y_test[:,target])
            # accuracy = score(y_test[:,target], prediction) ** .5 / np.mean(y_test[:,target])
            # accuracy = model.oob_score_
        else:
            prediction = model.predict(np.zeros(x_train.shape))
            accuracy = 1 - manual_error_score(y_train[:,target], prediction)
        
        #Sorting and Writing Important Features
        all_tags = [d.tags[tag] for tag in d.continuous +d.categorical + cost_tags[:target] + cost_tags[target+1:]] if include_costs else [d.tags[tag] for tag in d.continuous + d.categorical]
        print all_tags
        ff.writeFeatures(costFeature = d.tags[costIndex], datafile = d.datafile, importance = model.feature_importances_, tags = all_tags)        
        
        #Splitting to testing and training datasets
        costTag =  d.tags[costIndex]
        results.append("Model accuracy for cost:%s%saccuracy:%.4f\n" % (costTag, (30 - len(costTag)) * " ", accuracy))
        modelPath = config.path(path, "models", costTag)
        config.save(config.path(modelPath, "features.p"), (cont_tags_, cat_tags))
        config.save(config.path(modelPath, "model.p"), (model))
        config.save(config.path(modelPath, "used_to_train.p"), data[:5,cont_tags_ + cat_tags + [costIndex]])
        config.save(config.path(modelPath, "cont_mean.p"), mean)
        config.save(config.path(modelPath, "encoder.p"), encoder)
        config.save(config.path(modelPath, "dHandler.p"), d)
        if test:
            with open(config.path(modelPath, "results.txt"), 'a') as f:
                f.write(",".join([d.tags[tag] for tag in cont_tags_ + cat_tags]))
                f.write("\t" + results[-1] + "\n")
    print "\n".join(results)
    return accuracy

if __name__ == "__main__":
    import sys

    datafile = sys.argv[1]
    cost = sys.argv[2]

    importance_path = config.path("..","data",datafile,"features","importances")
   
    d = config.get(config.path("..","data",datafile,"data","dHandler.p"), dc.Data, datafile = datafile)     
    main([], [cost], d, include_costs = True, trees = 50)
    
    import shutil
    shutil.copy(config.path(importance_path, cost + ".txt"), config.path(importance_path, cost + "_test.txt"))

    with open(config.path(importance_path, cost + "_test.txt"), 'rb') as f:
        features = [line.strip().split() for line in f.readlines()][::-1]

    with open(config.path(importance_path, "%s_results.txt" % cost), 'wb') as f:
        for i,feature in enumerate(features):
            remaining_features = [feat[0] for feat in features[i:]]
            f.write("Round %d\n" % i)
            f.write("Eliminated feature :%s,%s \n" % (feature[0], feature[1]))
            f.write("Remaining Features:\n %s\n" % [feat[0] for feat in features[i:]])
            scores = 0
            for iteration in xrange(10):
                score_var = main(remaining_features, [cost], d, include_costs = True, trees = 30)
                f.write("Model Score: %.04f\n" % score_var)
                scores += score_var
