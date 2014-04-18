"""
Main script that the user will run.
Some sad-excuse for a user interface with the code
author: chris @ sihrc
"""

import sys
import model
import config
import format_features
import feature_selection
import data

"""
Scenarios:

I. Client wants to look at what data sets are available
II. Client wants to find out what cost features and important features for each data set are` 
III. Client knows what data set to use and has the features
IV. Client wants to know what features out of inputted are important
V. 
"""

if __name__ == "__main__":
    args = sys.argv
