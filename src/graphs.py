import matplotlib.pyplot as plt
from stats import *
import numpy as np
import data as dc

d = dc.Data(codebook = dc.HC144D, filename = "h144d.dat")
for i in range(5):
        data = d.getColumn("V" + str(i))
        print data.std()
