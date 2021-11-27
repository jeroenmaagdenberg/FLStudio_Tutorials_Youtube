#!/usr/bin/env python
# coding: utf-8

# # FL Studio Tuturials on Youtube

# ## Getting started

# To run this code, the pip package "google-api-python-client" is required
# If not installed, please uncomment and run the following line by removing the '#':

# In[ ]:


# pip install google-api-python-client


# #### Once installed, restart and clean the kernel and continue from here:

# In[ ]:


from googleapiclient.discovery import build
import csv
import time
import os
import json
import pandas as pd


# #### Create an api_key and store this credential as a Environment Variable on your local device
# In this project, the variable is defined in Terminal as  "YOUTUBE_API". For more information, check [this page](https://tilburgsciencehub.com/building-blocks/store-and-document-your-data/store-data/environment-variables/) or [this instructional video](https://www.youtube.com/watch?v=5iWhQWVXosU).

# In[ ]:


api_key = os.environ["YOUTUBE_API"]


# In[ ]:


youtube = build('youtube', 'v3', developerKey= api_key)


# #### Testing the systems
# The cells below will check whether the API functions. 
# 
# Within this document, each definition of a parameter, operation or function is explained within the cells. These definitions should be considered as the same throughout the project unless mentioned otherwise.

# In[ ]:


# check the default number of results, this should give 5

# .search = executes the search method 
# .list = retrieves a list of zero or more resources
# q = query term
# part = identifies group of properties that should be returned
# type = type of resource
# snippet = provides overview with information about the video such as titles, description, thumbnails and tags
# .execute = executes the request

request = youtube.search().list(
            q='FL tutorial',
            part='snippet',
            type='video')
response = request.execute()
print('Total items: ' , len(response['items']))


# In[ ]:


# check the maximum number of results, this should give 50

# maxResults = specifies the number of items that should be returned with a maximum of 50

request = youtube.search().list(q='FL tutorial',part='snippet',type='video',maxResults=50)
response = request.execute()
print('Total items: ' , len(response['items']))


# If the two cells above gave you the outputs **5** and **50** respectfully, the API works correctly.

# #### Gathering the data

# In[ ]:


# create function for data collection

# search_res = list with search results
# no_requests = number of requests to the API
# max_requests = maximum number of requests
# next_page = every page contains a nextPageToken and this is used to iterate over multiple pages


def retrieve_data(no_requests, max_requests):
    search_res = []
    
    while no_requests <= max_requests:
        try:
            no_requests += 1
            # if no results have been gathered, then go find the first result
            # else get the result from the next page
            if (no_requests==1): 
                request = youtube.search().list(q='FL tutorial',part='snippet',type='video',maxResults=50)
            else:
                request = youtube.search().list(q='FL tutorial',part='snippet',type='video',maxResults=50, pageToken = next_page)

            # capture response and set next page
            response = request.execute()
            next_page = response['nextPageToken']
        except:    
            # if no next page is found, then stop the script
            break

        # add an item to the search_res list and wait 2 seconds before continuing with next page
        for item in response['items']:
            search_res.append(item['snippet'])
        time.sleep(2)
        
    return search_res


# In[ ]:


# make a list of videoIDs

# videoIDs = list of all video ids
videoIDs = []
search_res = retrieve_data(no_requests=0, max_requests=100)

# gather only the id of a video, the id is part of the url
for item in search_res:
    videoIDs.append(item['thumbnails']['default']['url'][23:34])


# In[ ]:


# --- start of gathering statistics --- #

# response_stats = response of API for the statistics 
# res_stats = result of statistics
response_stats = []

for vid in videoIDs:
    stats = youtube.videos().list(part='statistics',id=vid)
    response_stats.append(stats.execute())
    res_stats = {}
    
    for item in response_stats:
        stats = item['items'][0]['statistics']
        res_stats[item['items'][0]['id']] = stats


# In[ ]:


# write statistics to a json file
converted_to_string = json.dumps(res_stats)
f = open('stats_output.json', 'w', encoding='utf-8')
f.write(converted_to_string + '\n')
f.close()


# In[ ]:


# read the statistics json file 
f = open('stats_output.json', 'r', encoding='utf-8')
content = f.readlines()
for item in content:
    jsonobj = json.loads(item)
    f.close()


# In[ ]:


# drop favoriteCount column, this is an old feature that does not longer exist on YouTube

# dfstats = dataframe for statistics

dfstats = pd.read_json(r'stats_output.json', orient = 'index')
dfstats.drop(dfstats.columns[3],axis=1,inplace=True)


# In[ ]:


# clean statistics by removing NaNs and converting datatype to integer

# cols_stats = columns in statistics output

cols_stats = ['viewCount', 'likeCount', 'dislikeCount', 'commentCount']

dfstats[cols_stats] = dfstats[cols_stats].fillna(0)
dfstats[cols_stats] = dfstats[cols_stats].astype(int)


# In[ ]:


# create ratio for likes vs dislikes and comments vs views in percentages and adjust decimals for more readability

dfstats['likeRatio %'] = (dfstats['likeCount']/(dfstats['likeCount'] + dfstats['dislikeCount']))*100
dfstats['likeRatio %'] = dfstats['likeRatio %'].apply(lambda x: '%.2f' % x)

dfstats['commentRatio %'] = (dfstats['commentCount']/dfstats['viewCount'])*100
dfstats['commentRatio %'] = dfstats['commentRatio %'].apply(lambda x: '%.2f' % x)


# In[ ]:


# write dataframe of video statistics to csv file

dfstats.to_csv('video_statistics.csv', index_label ='id')


# In[ ]:


# --- start of gathering snippets --- #

# response_snippets = response of API for the snippets of videos 
# res_snippets = result of snippets

response_snippets = []

for item in videoIDs:
    snippets = youtube.videos().list(part='snippet',id=item)
    response_snippets.append(snippets.execute())
    res_snippets = {}
    
    for item in response_snippets:
        snippets = item['items'][0]['snippet'] 
        res_snippets[item['items'][0]['id']] = snippets


# In[ ]:


# write snippets to a json file

converted_to_string = json.dumps(res_snippets)
f = open('snippet_output.json', 'w', encoding='utf-8')
f.write(converted_to_string + '\n')
f.close()


# In[ ]:


# read the snippets json file 

f = open('snippet_output.json', 'r', encoding='utf-8')
content = f.readlines()
for item in content:
    jsonobj = json.loads(item)
    f.close()


# In[ ]:


# drop column liveBroadcastContent which contains only the value "none"

# dfsnip = dataframe for snippets

dfsnip = pd.read_json(r'snippet_output.json', orient = 'index')
dfsnip.drop(dfsnip.columns[8],axis=1,inplace=True)


# In[ ]:


# write dataframe of video snippets to csv file

dfsnip.to_csv('video_snippets.csv', index_label ='id')


# In[ ]:


# create Channel ID list

# ChannelIDs = list of all channel ids

ChannelIDs = []

for item in search_res:
    ChannelIDs.append(item['channelId'])


# In[ ]:


# --- start of gathering channel statistics --- #

# response_channel = response of API for the channel statistics 
# res_channels = result of channel statistics

response_channel = []
res_channels = {}
for chn in ChannelIDs:
    channel = youtube.channels().list(part='statistics',id=chn)
    response_channel.append(channel.execute())
    
    for chn in response_channel:
        channelstat = chn['items'][0]['statistics']
        res_channels[chn['items'][0]['id']] = channelstat


# In[ ]:


# write channel statistics to a json file

converted_to_string = json.dumps(res_channels)
f = open('channels_output.json', 'w', encoding='utf-8')
f.write(converted_to_string + '\n')
f.close()


# In[ ]:


# read the channel statistics json file 

f = open('channels_output.json', 'r', encoding='utf-8')
content = f.readlines()
for item in content:
    jsonobj = json.loads(item)
    f.close()


# In[ ]:


# write dataframe of channel statistics to csv file

# dfchn = dataframe for channel statistics

dfchn = pd.read_json(r'channels_output.json', orient = 'index')
dfchn.to_csv('video_channels.csv', index_label ='channelId')


# In[ ]:


#--- merging the video snippets and video statistics --- #

# dfmerged = dataframe for merged video data

dfsnip = pd.read_csv('video_snippets.csv')
dfstats = pd.read_csv('video_statistics.csv')

dfmerged = dfsnip.merge(dfstats, on='id')
dfmerged.to_csv('video_output.csv')

