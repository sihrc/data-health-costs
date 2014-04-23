"""
Model Script
Creates models based on selected features from feature_selection or user input
author: chris @ sihrc
"""
#Python Modules
# from sklearn.ensemble import GradientBoostingRegressor as Model
from sklearn.linear_model import Ridge as Model
# from sklearn.ensemble import RandomForestRegressor as Model
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error as score

#Local Modules
import config
from wrappers import debug
import data_helper as dc
import feature_selection as fs

@debug
def loadData(cost, d, include_costs):
    """
    Loads the feature pickle file from feature_selection.py
    """
    path = config.path("..","data",d.datafile,"features","features%s.p" % cost)
    if not config.os.path.exists(path):
        fs.select([d.tags.index(cost)], d, include_costs = include_costs, predict = True)
    return config.load(path)

@debug
def main(cost, importance ,d, include_costs = False):
    """
    Runs main model and predicts for an accuracy score
    """
    #Get Data Handler
    tags, features, target = loadData(cost, d, include_costs)
    #Splitting to testing and training datasets
    x_train, x_test, y_train, y_test = train_test_split(features[:,:importance], target,test_size=0.15, random_state=42)

    model = Model(100)
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = score(predictions, y_test)
    print "Model accuracy after feature selection of:\n{0}\nfor cost: {1}\t accuracy:{2}"\
    .format("\n".join(tags[:importance]),cost, accuracy ** .5)


if __name__ == "__main__":
    import sys
    datafile = sys.argv[1]
    # Clean Past Data
    config.clean([\
        # "data",\
        # "features",\
        # "formatted",\
        # "models",\
        ], datafile = datafile)
        
    d = config.get(config.path("..","data",datafile,"data","dHandler.p"), dc.Data, datafile = datafile)  
    main(d.costInput(), 15, d, False)
