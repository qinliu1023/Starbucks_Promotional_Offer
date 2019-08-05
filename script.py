#!/usr/bin/env python
# coding: utf-8

# # Starbucks Capstone Challenge
# 
# ### Introduction
# 
# This data set contains simulated data that mimics customer behavior on the Starbucks rewards mobile app. Once every few days, Starbucks sends out an offer to users of the mobile app. An offer can be merely an advertisement for a drink or an actual offer such as a discount or BOGO (buy one get one free). Some users might not receive any offer during certain weeks. 
# 
# Not all users receive the same offer, and that is the challenge to solve with this data set.
# 
# Your task is to combine transaction, demographic and offer data to determine which demographic groups respond best to which offer type. This data set is a simplified version of the real Starbucks app because the underlying simulator only has one product whereas Starbucks actually sells dozens of products.
# 
# Every offer has a validity period before the offer expires. As an example, a BOGO offer might be valid for only 5 days. You'll see in the data set that informational offers have a validity period even though these ads are merely providing information about a product; for example, if an informational offer has 7 days of validity, you can assume the customer is feeling the influence of the offer for 7 days after receiving the advertisement.
# 
# You'll be given transactional data showing user purchases made on the app including the timestamp of purchase and the amount of money spent on a purchase. This transactional data also has a record for each offer that a user receives as well as a record for when a user actually views the offer. There are also records for when a user completes an offer. 
# 
# Keep in mind as well that someone using the app might make a purchase through the app without having received an offer or seen an offer.
# 
# ### Example
# 
# To give an example, a user could receive a discount offer buy 10 dollars get 2 off on Monday. The offer is valid for 10 days from receipt. If the customer accumulates at least 10 dollars in purchases during the validity period, the customer completes the offer.
# 
# However, there are a few things to watch out for in this data set. Customers do not opt into the offers that they receive; in other words, a user can receive an offer, never actually view the offer, and still complete the offer. For example, a user might receive the "buy 10 dollars get 2 dollars off offer", but the user never opens the offer during the 10 day validity period. The customer spends 15 dollars during those ten days. There will be an offer completion record in the data set; however, the customer was not influenced by the offer because the customer never viewed the offer.
# 
# ### Cleaning
# 
# This makes data cleaning especially important and tricky.
# 
# You'll also want to take into account that some demographic groups will make purchases even if they don't receive an offer. From a business perspective, if a customer is going to make a 10 dollar purchase without an offer anyway, you wouldn't want to send a buy 10 dollars get 2 dollars off offer. You'll want to try to assess what a certain demographic group will buy when not receiving any offers.
# 
# ### Final Advice
# 
# Because this is a capstone project, you are free to analyze the data any way you see fit. For example, you could build a machine learning model that predicts how much someone will spend based on demographics and offer type. Or you could build a model that predicts whether or not someone will respond to an offer. Or, you don't need to build a machine learning model at all. You could develop a set of heuristics that determine what offer you should send to each customer (i.e., 75 percent of women customers who were 35 years old responded to offer A vs 40 percent from the same demographic to offer B, so send offer A).

# In[2]:


import pandas as pd
import numpy as np
import math
import json
get_ipython().run_line_magic('matplotlib', 'inline')

# read in the json files
portfolio = pd.read_json('data/portfolio.json', orient='records', lines=True)
profile = pd.read_json('data/profile.json', orient='records', lines=True)
transcript = pd.read_json('data/transcript.json', orient='records', lines=True)


# # Business Understanding
# 
# 
# 
# Offers can be delivered via multiple channels. To better offer offers, following problems will be addressed during the analysis.
# 1. identify which groups of people are most responsive to each type of offer
# 1. figure out how best to present each type of offer.
# 
# 1. Who would make purchase without receiving any offer?

# # Data Understanding
# 
# To answer above questions, transaction, demographic and offer data are needed. 
# 
# Here are tables we have and their briefs:
# * portfolio.json - containing offer ids and meta data about each offer (duration, type, etc.) (10 offers x 6 fields)
# * profile.json - demographic data for each customer (17000 users x 5 felds)
# * transcript.json - records for transactions, offers received, offers viewed, and offers completed (306648 events x 4 fields)
# 
# Here is the schema and explanation of each variable in the files:
# 
# **portfolio.json**
# * id (string) - offer id
# * offer_type (string) - type of offer ie BOGO, discount, informational
# * difficulty (int) - minimum required spend to complete an offer
# * reward (int) - reward given for completing an offer
# * duration (int) - time for offer to be open, in days
# * channels (list of strings)
# 
# **profile.json**
# * age (int) - age of the customer 
# * became_member_on (int) - date when customer created an app account
# * gender (str) - gender of the customer (note some entries contain 'O' for other rather than M or F)
# * id (str) - customer id
# * income (float) - customer's income
# 
# **transcript.json**
# * event (str) - record description (ie transaction, offer received, offer viewed, etc.)
# * person (str) - customer id
# * time (int) - time in hours since start of test. The data begins at time t=0
# * value - (dict of strings) - either an offer id or transaction amount depending on the record
# 

# # Data Preparation
# 
# 

# ## Portfolio

# In[3]:


portfolio


# In[4]:


# Expande channels into multi-columns

channels = ["web", "email", "mobile", "social"]

for col in channels:
    portfolio[col] = portfolio["channels"].apply(lambda x: 1 if col in x else 0)
    
portfolio[["channels", "web", "email", "mobile", "social"]]


# In[ ]:





# ## Profile

# In[5]:


profile.head()


# In[6]:


# Not all demographic data are reasonable
# do describe 
profile.describe()


# In[8]:


profile["became_member_on"].apply(lambda x: str(x)[:4]).value_counts()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ## Transcript

# In[5]:


transcript.head()


# In[8]:


# Check Keys in column value
transcript.value.apply(lambda x: x.keys()).value_counts()


# In[9]:


transcript["transcript_offer_id"] = transcript["value"].apply(lambda x: x.get("offer id") if "offer id" in x.keys() else
                                                             x.get("offer_id") if "offer_id" in x.keys() else 
                                                             np.nan)
transcript["transcript_amount"] = transcript["value"].apply(lambda x: x.get("amount"))
transcript["transcript_reward"] = transcript["value"].apply(lambda x: x.get("reward"))


# In[10]:


transcript.info()


# In[9]:


transcript.head()


# In[91]:


transcript.query('event == "offer received"').groupby(["transcript_offer_id", "person"])["person"].count().sort_values(ascending = False).value_counts()


# In[ ]:





# In[ ]:





# In[6]:


# Check event types
transcript.event.unique()


# In[34]:


received = transcript[transcript["event"] == "offer received"][["person", "transcript_offer_id"]].drop_duplicates(keep = "first")
viewed = transcript[transcript["event"] == "offer viewed"][["person", "transcript_offer_id"]].drop_duplicates(keep = "first")
completed = transcript[transcript["event"] == "offer completed"][["person", "transcript_offer_id"]].drop_duplicates(keep = "first")
offers = received.merge(viewed, how = "outer", on = ["person", "transcript_offer_id"], indicator = True).rename(columns = {"_merge": "is_viewed"}).merge(completed, how = "outer", on = ["person", "transcript_offer_id"], indicator = True).rename(columns = {"_merge": "is_completed"})


# In[35]:


offers.head()


# In[36]:


offers[["is_viewed", "is_completed"]].drop_duplicates(keep = "first")


# In[37]:


offers["is_completed"] = offers.apply(lambda row: 
"viewed_completed" if (row["is_viewed"] == "both") & (row["is_completed"] == "both") else
"viewed_not_completed" if (row["is_viewed"] == "both") & (row["is_completed"] == "left_only") else
"not_viewed_completed" if (row["is_viewed"] == "left_only") & (row["is_completed"] == "both") else
"not_viewed_not_completed" if (row["is_viewed"] == "left_only") & (row["is_completed"] == "left_only") else
np.nan, axis = 1)


# In[38]:


offers["is_viewed"] = offers["is_viewed"].apply(lambda x: "viewed" if x == "both" else
                                                          "not_viewed" if x == "left_only" else 
                                                          np.nan)


# In[39]:


offers["is_viewed"].value_counts()


# In[40]:


offers["is_completed"].value_counts()


# In[41]:


offers[["is_viewed", "is_completed"]].drop_duplicates(keep = "first")


# In[ ]:





# ## Combine All 3 DataFrames

# In[66]:


df = transcript.drop("value", axis = 1).merge(portfolio.drop("channels", axis = 1), 
       how = "left", left_on = "transcript_offer_id", right_on = "id").drop("id", axis = 1)\
.merge(profile, how = "left", left_on = "person", right_on = "id").drop("id", axis = 1)


# In[67]:


df.info()


# In[68]:


df.head(3)


# In[76]:


portfolio.columns


# In[80]:


offer_funnel = df.groupby(["transcript_offer_id", "difficulty", "duration", "offer_type", "reward",
       "web", "email", "mobile", "social", "event"])["person"].count().unstack().reset_index()

offer_funnel["view2received"] = 1.0 * offer_funnel["offer viewed"]/offer_funnel["offer received"]
offer_funnel["completed2received"] = 1.0 * offer_funnel["offer completed"]/offer_funnel["offer received"]
offer_funnel["completed2view"] = 1.0 * offer_funnel["offer completed"]/offer_funnel["offer viewed"]

offer_funnel.sort_values(["completed2view", "completed2received", "view2received"], ascending = [False, False, False])


# In[100]:


# Separate (Person, Offer) for which offer is not Viewed but is completed

offer_viewed = df[df["event"] == "offer viewed"][["person", "transcript_offer_id"]].drop_duplicates(keep = "first")
offer_completed = df[df["event"] == "offer completed"][["person", "transcript_offer_id"]].drop_duplicates(keep = "first")

offer_details = offer_viewed.merge(offer_completed
                                   , how = "outer", on = ["person", "transcript_offer_id"]
                                   , indicator = True)


# In[102]:


offer_details["details"] = offer_details["_merge"].apply(lambda x: "viewed_and_completed" if x == "both" else
                                        "viewed_not_completed" if x == "left_only" else 
                                        "not_viewed_but_completed")


# In[101]:


offer_details["_merge"].value_counts()


# In[103]:


offer_details


# In[83]:


offer_viewed.shape


# In[85]:


df[df["event"] == "offer viewed"][["person", "transcript_offer_id", "event"]].groupby(["person", "transcript_offer_id"])["event"].count().sort_values(ascending = False).head()


# In[86]:


df.query('person == "6d2db3aad94648259e539920fc2cf2a6"').query('transcript_offer_id == "f19421c1d4aa40978ebb69ca19b0e20d"')


# In[ ]:


one offer will be sent for multiple times


# In[ ]:





# # Modeling
# 
# 
# 

# # Evaluation
# 
# 
# 
# 

# # Deployment
# 
# 
# 
# 

# In[ ]:




