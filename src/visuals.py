#To-DO Create a Visuals module that holds all the visualization TASKS
import matplotlib.pyplot as plt
class Graphs():

	def __init__ (self, data):
		self.data = data
		self.costId = data.lookUp(desc = "CHG")[0][0] # V49
		self.cost = data.getColumn(self.costId)

	def FeatureVsCost(self, var):
			try:
				data = self.data.getColumn(var)
		 		plt.scatter(data, self.cost)
		 		print "Plotting " + var + " vs cost plot"
		 		plt.xlabel(self.data.lookUp(var = var)[0])
		 		plt.ylabel("Cost in dollars")
		 		plt.savefig("../visuals/feature_v_cost/" + self.data.lookUp(var = var)[0].replace(" ", "_") + ".png")
			except:
			 	print "Plotting " + str(i) + " failed"

	def AllFeatureVsCost(self):
		for i in range (len(self.data.features)):
			try:
				self.FeatureVsCost("V" + str(i))
			except:
				print "Plotting " + str(i) + " failed"