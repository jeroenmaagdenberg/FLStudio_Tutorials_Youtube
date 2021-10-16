#!/usr/bin/env python
# coding: utf-8

# # FL Studio Tuturials on Youtube

# ## Getting started

# In[1]:


# Run this cell once, this will install the API client.
pip install google-api-python-client


# #### Once installed, restart and clean the kernel and continue from here:

# In[2]:


#### als laatste weg halen ivm quotas

api_key = 'AIzaSyBiBM47drg5csNW-V-wOZjNN-Vl5rfHNPM' #API code Jeroen

api_key = 'AIzaSyA0v2in7KbrgrmjyxTBOrGcLEDn5QJeKio' #API code Tayfun
api_key = 'AIzaSyB770EnyGnPvNtdIgvqVyZIsnBeinWuyzQ' #API code Quinten
api_key = 'AIzaSyAuzxscfTqg5ElsuRhMHQx9zJGZyVzDqpM' #API code Sam


# In[37]:


from googleapiclient.discovery import build
import csv
import time
import os
import json
import pandas as pd


# #### Create an api_key and store this credential as a Environment Variable on your local device
# For information, check [this page](https://tilburgsciencehub.com/building-blocks/store-and-document-your-data/store-data/environment-variables/) or [this instructional video](https://www.youtube.com/watch?v=5iWhQWVXosU).

# In[38]:


api_key = os.environ["YOUTUBE_API"]


# In[39]:


youtube = build('youtube', 'v3', developerKey= api_key)
youtube


# #### Testing the systems
# The cells below will check whether the API functions. 

# In[40]:


# check the default number of results, this should give 5
request = youtube.search().list(
            q='FL tutorial',
            part='snippet',
            type='video')
print(type(request))
response = request.execute()
print('Total items: ' , len(response['items']))


# In[41]:


# use this to increase to max of 50
request = youtube.search().list(q='FL tutorial',part='snippet',type='video',maxResults=50)
print(type(request))
response = request.execute()
print('Total items: ' , len(response['items']))


# If the two cells above gave you the outputs **5** and **50** respectfully, the API works correctly.

# #### Gathering the data

# In[42]:


# print only the titles of the results within the retrieval range of 50.
request = youtube.search().list(q='FL tutorial',part='snippet',type='video',maxResults=50)
response = request.execute()
next_page = response['nextPageToken']
print(next_page) # to get next page token
for item in response['items']:
    print(item['snippet']['title'])


# In[43]:


# counts results within the retrieval range of 50 per page.
# with every page the output provides iteration number and the nextPageToken
no_requests = 0
max_requests = 100

search_res = []

while no_requests <= max_requests:
    try:
        no_requests += 1
        print('iteration number:' + str(no_requests))
        if (no_requests==1): 
            request = youtube.search().list(q='FL tutorial',part='snippet',type='video',maxResults=50)
        else:
            request = youtube.search().list(q='FL tutorial',part='snippet',type='video',maxResults=50, pageToken = next_page)

        response = request.execute()
        next_page = response['nextPageToken']
        print(next_page)
    except:    
        break
    for item in response['items']:
        search_res.append(item['snippet'])
    time.sleep(2)

len(search_res)


# In[44]:


# makes a list of videoIDs

videoIDs = []

for item in search_res:
    videoIDs.append(item['thumbnails']['default']['url'][23:34])

print("Found " + str(len(videoIDs)) + " video IDs!")


# In[45]:


# --- stats --- #
cnt=0
for vid in videoIDs:
    cnt+=1
    if (cnt==5): 
        break   # overview for only 5 results, just to give impression
    stats = youtube.videos().list(part='statistics',id=vid)
    print(stats.execute())


# In[46]:


# response for stats 
response_stats = []

for vid in videoIDs:
    stats = youtube.videos().list(part='statistics',id=vid)
    response_stats.append(stats.execute())
    res_stats = {}
    
    for item in response_stats:
        stats = item['items'][0]['statistics']
        res_stats[item['items'][0]['id']] = stats

res_stats


# In[50]:


# output stats to json file
import json
converted_to_string = json.dumps(res_stats)
f = open('stats_output.json', 'a', encoding='utf-8')
f.write(converted_to_string + '\n')
f.close()


# In[51]:


# read json file for stats
f = open('stats_output.json', 'r', encoding='utf-8')
content = f.readlines()
for item in content:
    jsonobj = json.loads(item)
    print(jsonobj)
    f.close()


# In[52]:


# read json df for stats

import pandas as pd
dfstats = pd.read_json(r'stats_output.json', orient = 'index')
dfstats


# In[53]:


# write df for stats to csv
dfstats.to_csv('video_statistics.csv', index_label ='id')


# END OF STATS

# In[54]:


# --- snippets ---#
cnt=0
for vid in videoIDs:
    cnt+=1
    if (cnt==5): break
    snippets = youtube.videos().list(part='snippet',id=vid)
    print(snippets.execute())


# In[55]:


# response for snippet
response_snippets = []

for item in videoIDs:
    snippets = youtube.videos().list(part='snippet',id=item)
    response_snippets.append(snippets.execute())
    res_snippets = {}
    
    for item in response_snippets:
        snippets = item['items'][0]['snippet'] 
        res_snippets[item['items'][0]['id']] = snippets

res_snippets


# In[56]:


# output snippets to json file

converted_to_string = json.dumps(res_snippets)
f = open('snippet_output.json', 'a', encoding='utf-8')
f.write(converted_to_string + '\n')
f.close()


# In[57]:


# read json file for snippet
f = open('snippet_output.json', 'r', encoding='utf-8')
content = f.readlines()
for item in content:
    jsonobj = json.loads(item)
    print(jsonobj)
    f.close()


# In[58]:


# read json df for snippet

dfsnip = pd.read_json(r'snippet_output.json', orient = 'index')
dfsnip


# In[59]:


# write df for snippet to csv
dfsnip.to_csv('video_snippets.csv', index_label ='id')


# END OF SNIPPETS

# In[60]:


#--- creation of Channel ID list ---#
ChannelIDs = []

for item in search_res:
    ChannelIDs.append(item['channelId'])

ChannelIDs


# In[61]:


# channel output
cnt=0
for chn in ChannelIDs:
    cnt+=1
    if (cnt==3): 
        break
    channel = youtube.channels().list(part='statistics',id=chn)
    print(channel.execute())
    
channel.execute().keys()


# In[62]:


# Response channel

response_channel = []
res_channel = []
res_channels = {}
for chn in ChannelIDs:
    channel = youtube.channels().list(part='statistics',id=chn)
    response_channel.append(channel.execute())
    
    for chn in response_channel:
        channelstat = chn['items'][0]['statistics']
        res_channels[chn['items'][0]['id']] = channelstat
               
res_channels


# In[63]:


# output channel to json file

converted_to_string = json.dumps(res_channels)
f = open('channel_output.json', 'a', encoding='utf-8')
f.write(converted_to_string + '\n')
f.close()


# In[64]:


# read json file for channel
f = open('channel_output.json', 'r', encoding='utf-8')
content = f.readlines()
for item in content:
    jsonobj = json.loads(item)
    print(jsonobj)
    f.close()


# In[65]:


# read json df for channel
dfchn = pd.read_json(r'channel_output.json', orient = 'index')
dfchn


# In[66]:


# write df for channel to csv
dfchn.to_csv('video_channel.csv', index_label ='ChannelId')


# END OF CHANNEL

# In[67]:


#--- merging the video snippets and statistics --- #
dfsnip = pd.read_csv('video_snippets.csv')
dfstats = pd.read_csv('video_statistics.csv')

dfmerged = dfsnip.merge(dfstats, on='id')
dfmerged


# In[68]:


dfmerged.to_csv('video_output.csv')


# THE END
