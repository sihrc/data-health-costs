data-health-costs
=================

Data Science Project with athenahealth


Data Use Agreement  (AHRQ-MEPS)
===============================
Individual identifiers have been removed from the micro-data contained in these files. 
Nevertheless, under sections 308 (d) and 903 (c) of the Public Health Service Act (42 U.S.C. 
242m and 42 U.S.C. 299 a-1), data collected by the Agency for Healthcare Research and Quality 
(AHRQ) and/or the National Center for Health Statistics (NCHS) may not be used for any 
purpose other than for the purpose for which they were supplied; any effort to determine the 
identity of any reported cases is prohibited by law. 

Therefore in accordance with the above referenced Federal Statute, it is understood that: 

1. No one is to use the data in this dataset in any way except for statistical reporting and 
analysis; and 

2. If the identity of any person or establishment should be discovered inadvertently, 
then (a) no use will be made of this knowledge, (b) the Director Office of 
Management AHRQ will be advised of this incident, (c) the information that would 
identify any individual or establishment will be safeguarded or destroyed, as 
requested by AHRQ, and (d) no one else will be informed of the discovered identity; 
and 

3. No one will attempt to link this dataset with individually identifiable records from 
any datasets other than the Medical Expenditure Panel Survey or the National Health 
Interview Survey. 

By using these data you signify your agreement to comply with the above stated statutorily based 
requirements with the knowledge that deliberately making a false statement in any matter within 
the jurisdiction of any department or agency of the Federal Government violates Title 18 part 1 
Chapter 47 Section 1001 and is punishable by a fine of up to $10,000 or up to 5 years in prison. 
The Agency for Healthcare Research and Quality requests that users cite AHRQ and the Medical 
Expenditure Panel Survey as the data source in any publications or research based upon these 
data.

===============================
###Code
data.py

  Currently, this contains String processing methods that analyze the differences and frequency of differences of the strings in the first column of the data set. The Strings are in increasing order (they are long numbers). They appear to behave like time-stamps of some sort, or some kind of special identification number. 

stats

  Contains the modules with thinkstats2.py and thinkplot.py provided by Allen Downey through Green Tea Press.

temp.p

  Currently used for pipelining the dataset. 


To-Do

  Refactor the String processing methods into its own class or module. 

