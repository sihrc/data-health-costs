#Python Modules
# from sklearn.ensemble import GradientBoostingRegressor as Model
# from sklearn.linear_model import Ridge as Model
from sklearn.ensemble import RandomForestRegressor as Model
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error as score



#Local Modules
import config
from wrappers import debug
import data as dc
import feature_selection as fs


def loadData(datafile, cost, d):
    path = config.path("..","data",datafile,"features","features%s.p" % cost)
    if not config.os.path.exists(path):
        fs.select([d.tags.index(cost)], datafile, d)
    return config.load(path)

def main(cost, datafile, importance):
    #Get Data Handler
    d = config.get(config.path("..","data",datafile,"data","dHandler.p"), dc.Data, datafile = datafile, include_costs = False)
    #Get Data
    features, target = loadData(datafile, cost, d)
    #Splitting to testing and training datasets
    x_train, x_test, y_train, y_test = train_test_split(features[:,:importance], target,test_size=0.15, random_state=42)

    model = Model()
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = score(predictions, y_test)
    print accuracy ** .5


if __name__ == "__main__":
    datafile = "H144D"

    # Clean Past Data
    config.clean([\
        # "data",\
        "features",\
        # "formatted",\
        # "models",\
        ], datafile = datafile)

    main("IPDMD11X",datafile, 15)