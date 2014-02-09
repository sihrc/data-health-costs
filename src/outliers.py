import matplotlib.pyplot as plt
from stats import *
import numpy as np
import data as dc
import visuals as vis

d = dc.Data(codebook = dc.HC144D, filename = "h144d.dat")
def reject_outliers(data, m):
        return data[abs(data - np.mean(data)) < m * np.std(data)]
for i in range(44):
        data = d.getColumn("V" + str(i))
        data2 = reject_outliers(data, 1)
        print str(i) + " oldmax " + str(data.max())
        print "newmax " + str(data2.max())
