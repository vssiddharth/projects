# -*- coding: utf-8 -*-
"""Coachability_Score_Siddharth.ipynb
# Objective : To Find Coachability Score for 15 project leads based on a standard set of coachability attributes
"""

import pandas as pd

log=pd.read_csv('/content/log.csv',index_col=0)  # Reading file and storing the table in log dataframe 
deliver_count=log.loc[:,"Deliverable"].value_counts()  # Copying the entire column in to a new columns named deliver_count and then counting values ...this is a series 
coachee_count=log.loc[:,"Coachee"].value_counts()
#print(coachee_count)
attribute=log.loc[:,"Coachability Attribute"]
attribute_count=attribute.value_counts()

# step 1 : Extracting 2 columns from the main table 

newtable=log.loc[:,["Coachee","Coachability Attribute"]]
summary =newtable.describe()
#print(summary)

# step2 : Filtering rows that contain Positive Attitude only 

positive=newtable[newtable['Coachability Attribute'].str.contains("Positive Attitude :")]
negative=newtable[~newtable['Coachability Attribute'].str.contains("Positive Attitude :")]
#print(positive) print(negative)

# step 3 Counting the number of positive and negative attitude by each Coachee 
pos=positive.groupby('Coachee').count()
pos.rename(columns = {'Coachability Attribute':'positive'}, inplace = True)
neg = negative.groupby('Coachee').count()
neg.rename(columns = {'Coachability Attribute':'negative'}, inplace = True)
#print(neg)
#print(pos)    # pos is a DataFrame ( a table with 2 columns) and neg is another table 

# step 4  concatinating 2 tables into 1 table 
result = pd.concat([pos, neg], axis=1, join="inner")
result["percentage"]=result.loc[:,"positive"]/(result.loc[:,"positive"]+result.loc[:,"negative"])
#print(result)

# step 5  calculating mean and std dev for the percentage column
m= result["percentage"].mean()
sd = result["percentage"].std()
#print(m,sd)

# step 6 calculating z score 
result["zscore"]=(result.loc[:,"percentage"]-m)/sd
print(result)

chart=result.plot.bar(y='zscore',color=['blue'],title='Coachability Score')
