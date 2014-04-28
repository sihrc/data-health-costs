Predicting Medical Expenditures
=================
<b>A data science and machine learning project with athenahealth</b>

<strong>Description:</strong><br>
This project uses data from the Medical Expenditure Panel Surveys by the Agency of Healthcare Research and Quality to predict patients likely to incur high medical costs in attempt to provide pre-emptive care to selected patients.

<i>Please take a look at the Data Use Agreement provided by MEPS, located in this repository for your convenience under DATA_AGREEMENT.</i>

<strong>Documentation:</strong><br>
<i>config.py</i><br>
contains MEPS urls used in data acquition, contains pathing and caching functions used in pipeline
<br><br>

<i>data_helper.py</i><br>
contains the Data object that takes care of parsing and reformatting the data files provided by MEPS into a usable state
<br><br>

<i>feature_lookup.py</i><br>
-- to be continued...


<strong>Tutorial:</strong><br>
Once the code has been downloaded, navigate to the appropriate folder and view the available commands by typing in: <br>
```python run.py -h```
 <br> If everything worked properly you should be greeted by the following screen. 


<i>-f File</i><br>
	The current set up works for all data files found on MEPS database. Available datasets can be found at http://meps.ahrq.gov/mepsweb/data_stats/download_data_files.jsp. If you scroll down to where it says “option 1” and click on one of the categories you will find a long list of data sets that match the description. An example of one of these entries can be seen below.

under the PUF no. tag you will find the number needed for the code to work. More specifically it is the number without the “C-”. For the example seen above, the filename would be “H147”.

<i>-p Print Table</i><br> 
	If you do not know the categories present in the data set this tag can be used. To see all data tables available simply use the -p tag without anything after it. To find what table a specific feature belongs to, type -p followed by the name of the feature. 



<i>-s Select</i><br> 
	By default the code will use all features found in the datafile specified. Since some of these datasets contain a few thousand features, narrowing down this number can be useful. This can be done in a few ways. If you are interested in a specific type of data, such as demographic information, you can use the “-p” tag mentioned above to find the appropriate table letter. If you are only interested in a key set of features they can be added as a list of feature names. 
	Narrowing down the dataset can make it more manageable, accurate and useful, By narrowing it down you do not have to find as much information about the person in question. Many of the features have little to no influence on the outcome so removing them can eliminate whatever small changes they could have caused. 

<i>-i include</i><br>
	For many data sets the cost features are just parts of the total cost. This means that they will have high influence over the target cost feature and can cause there to be a skewed prediction model. In other words, An example of this would be using the cost of a hospital room to predict the price of a night spent at the hospital. To prevent this, none of the cost data are used as features unless they are the target.  to include them all back in, this tag can be used. 
 
<i>-t Trees</i><br>
	The code currently uses Random Forest Regression as a prediction model. The more trees a forest model has the longer it will take to finish but the more accurate it will be. Random Forest Regressors take a random subset of the data and of the features and creates a tree out of it. It continues this process for as many times as specified and then averages the results to predict an outcome. 


<strong>Running the Code:</strong><br>
	
Running the Code
	

