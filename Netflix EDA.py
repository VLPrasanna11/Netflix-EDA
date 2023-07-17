#!/usr/bin/env python
# coding: utf-8

# ## Importing libraries and dataset

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly as px

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


import cufflinks as cf
import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
import statistics as stat


# In[3]:


nd = pd.read_csv("/Users/lakshmiprasanna/Documents/netflix/netflix.csv",encoding='latin-1')


# In[4]:


nd


# ## Data Cleaning and obtaining general idea

# In[5]:


nd['user rating score'].isnull().sum()


# In[6]:


nd = nd.dropna(subset='user rating score')


# In[7]:


nd = nd.reset_index(drop=True)


# In[8]:


nd.columns


# In[9]:


nd['rating'].unique()


# In[10]:


nd['user rating score'].unique()


# In[11]:


nd['user rating score'] = nd['user rating score'].astype('int64')


# In[12]:


nd['user rating size'].unique()


# ##### As user rating size is the same for all the values, we can consider just user rating score for the analysis

# In[13]:


nd.head()


# ##### Ques: Finding which shows the  audience liked

# In[14]:


array_rateDesc = list(nd['ratingDescription'].unique())
array_rateDesc.sort(reverse=True)
array_rateDesc


# In[15]:


array_ratings = []
for i in array_rateDesc:
    array_ratings.append(nd.loc[nd['ratingDescription'] == i, 'rating'].values[0])
print(array_ratings)


# In[16]:


dict = {r:rd for r,rd in zip(array_ratings,array_rateDesc)}
print(dict)


# In[17]:


nd


# In[18]:


rate_count = []
rate_sum = []
avg_rate = []
median_rate = []
most_repeated_rate = []

for i in array_ratings:
    rate_count.append(nd[nd['rating']==i]['user rating score'].count())
    rate_sum.append(nd[nd['rating']==i]['user rating score'].sum())
    avg_rate.append(nd[nd['rating']==i]['user rating score'].mean())
    median_rate.append(nd[nd['rating']==i]['user rating score'].median())
    most_repeated_rate.append(nd[nd['rating']==i]['user rating score'].mode())


# In[19]:


rate_count


# In[20]:


diction = {'Rating genre': array_ratings,'Count' : rate_count, 'Overall ratings sum' : rate_sum, 
           'Average rating' : avg_rate, 'Median rating' : median_rate}
ratings_df = pd.DataFrame(diction)


# In[21]:


ratings_df


# In[22]:


mode=[]
a = []
for i in range(len(most_repeated_rate)):
    for j in range(len(most_repeated_rate[i])):
        a.append(most_repeated_rate[i][j])
    mode.append(stat.mean(a))
    a=[]
mode


# In[23]:


ratings_df['Mode'] = mode
ratings_df


# ##### Ans: Top 3 genres based on count: 
# 1. TV-14 : TV-14 stands for content that may be inappropriate for children younger than 14 years of age.
# 
# 2. PG : PG stands for content that should be watched under parental guidance.
# 
# 3. TV-MA: TV-MA is a rating assigned by the TV Parental Guidelines to a television program that was designed for mature audiences only.

# ##### Ans:  Top 3 genres based on rating: 
# (I'm considering median because it gives the best idea of what people think of the genre)
# 1. NR : NR rating refers to a movie that has not yet been rated. This could mean that the movie has not been submitted for a rating or is an uncut version of a movie that was submitted.
# 
# 2. TV-MA : TV-MA is a rating assigned by the TV Parental Guidelines to a television program that was designed for mature audiences only.
# 
# 3. TV-PG : TV-PG is a rating for the TV shows that are to be watched under parental guidance.

# In[24]:


ratings_df['Weighted average'] = np.random.rand(len(ratings_df))


# In[25]:


for i in range(len(ratings_df)):
    ratings_df['Weighted average'][i] = (ratings_df['Count'][i]+ratings_df['Median rating'][i])/2
ratings_df


# In[26]:


go.Figure(data=go.Box(x=nd['rating'],y=nd['user rating score']))


# ##### Ans: As both count and median are not in sync, weighted average of them can help us in understanding what consumers like from the shows that are on netflix. They are:
# 1. TV-14
# 2. PG
# 3. TV-MA
# 
# ##### Ans: Although it's the same order as that of number of shows on netflix, it can also be said that the audience might like these genres better, considering it is a weighted average. That being said, the creators can also go for top rated shows as it's always the storyline that the audience find appealing.

# ##### Ques: As the rating description values are in decreasing order, does that mean the higher rating type are preferred? or are they just a code numbers? We can decide based on user rating score

# In[27]:


traces = []
for column in ratings_df.columns[3:]:
    trace = go.Scatter(x=ratings_df[column], y=ratings_df['Rating genre'], mode='lines', name=column)
    traces.append(trace)
    
go.Figure(data=traces)


# ##### Ans: As from the graphs, we can say that the rating description values are just random numbers as the order of numbers are random and not in relation with the rating values.

# ##### Ques: Analysis of Movies vs TV Shows

# In[28]:


array_ratings


# In[29]:


TV_shows = []
Movies_and_others = []
Type = ('TV shows', 'Movies and others')

for i in range(len(array_ratings)):
    if (array_ratings[i][0] == 'T' and array_ratings[i][1] == 'V'):
        TV_shows.append(array_ratings[i])
    else:
        Movies_and_others.append(array_ratings[i])


# In[30]:


TV_shows


# In[31]:


Movies_and_others


# In[32]:


nd['type label'] = np.random.rand(len(nd))


# In[33]:


for i in range(len(nd)):
    if nd['rating'][i] in TV_shows:
        nd['type label'][i] = "TV shows"
    else:
        nd['type label'][i] = "Movies and others"


# In[34]:


nd


# In[35]:


sns.set(style="darkgrid")
sns.countplot(x="type label", data=nd, palette="Set2")


# In[36]:


labels = ['TV shows', 'Movies and others']

count = []

count.append(nd[nd['type label']=='TV shows']['type label'].count())
count.append(nd[nd['type label']=='Movies and others']['type label'].count())

lay = go.Layout(title='count')
go.Figure(data=go.Bar(x=labels,y=count),layout=lay)


# ##### Ans: From the interactive plot and data, we can say that, there are 405 TV shows and 200 Movies and other types of shows on netflix. 

# ##### Ques: Highest rated movies/TV shows

# In[37]:


top_5_max_values = nd['user rating score'].nlargest(5)
print(top_5_max_values)


# ##### As the rating value is 99, let's see which all programs have the score of 99

# In[38]:


nd[nd['user rating score']==99]


# ##### Ans: Above mentioned 8 shows have the highest rating. Observe that all are TV shows and of the genre TV-MA. Hence audience are liking this genre and hence the creators should focus more on it.

# #### Que: In genre other than TV shows, highest rated movies?

# In[39]:


top_5_movies = nd[nd['type label']=='Movies and others']['user rating score'].nlargest(5)
print(top_5_movies)


# ##### As the rating value is 98, let's see which all programs have the score of 98

# In[40]:


nd[(nd['type label']=='Movies and others') & (nd['user rating score']==98)]


# ##### Ans: Above mentioned 5 shows have the highest rating. Observe that all are of the genre PG. Hence audience are liking this genre and hence the creators should focus more on it.

# In[41]:


#dict


# ##### Que: Finding the distribution of genre and the number of programs on netflix 

# In[42]:


sns.countplot(nd['rating'])


# In[43]:


sns.barplot(data=nd,x='user rating score',y='rating')


# In[44]:


go.Figure(data=go.Bar(x=ratings_df['Rating genre'],y=ratings_df['Count']))


# ##### Ans: We see that the count of a few types are really less, like that of NR, R, PG-13 etc, whereas of a few they are incredibly large, like TV-14 and TV-Y7-FV. What can be the reason? We can know by grilling years data.

# ##### Ques: YEAR ON YEAR ANALYSIS 

# In[45]:


nd.head()


# In[46]:


year = list(nd['release year'].unique())
year.sort()


# In[47]:


count_year = []
for i in year:
    count_year.append(nd[nd['release year']==i]['title'].count())


# In[48]:


go.Figure(data=go.Bar(x=year,y=count_year))


# ##### Ans: We see a non uniform increase and decrease in the content released on netflix based on the year of release. 

# ##### Ques: Year on year released based on their genre 

# In[49]:


grouped = nd.groupby('type label')

traces = []
for category, group in grouped:
    trace = go.Histogram(x=group['release year'], name=category)
    traces.append(trace)

fig = go.Figure(data=traces)

fig.show()


# ##### Ans: Based on their type, we can see that earlier we observed a domination of movies, whereas this decade has been a bloom for TV shows

# In[50]:


grouped = nd.groupby('rating')

traces = []
for category, group in grouped:
    trace = go.Histogram(x=group['release year'], name=category)
    traces.append(trace)

fig = go.Figure(data=traces)

fig.show()


# ##### Ans: As there are a lot of genres involved, it's better to see the growth in individual graphs

# In[51]:


for i in array_ratings:
    
    selected_values = nd['release year'].loc[nd['rating']==i]

    histogram = go.Histogram(x=selected_values)

    layout = go.Layout(title=f'Histogram for {i}')

    fig = go.Figure(data=[histogram], layout=layout)

    fig.show()


# ##### Ans: We can see the trend of each genre over the years in the above graphs. The peculiar growth or decline is found in TV-14: There has been a tremendous increase in the year 2016, from 23 to 88 shows, but then even drastic decrease from 2016, 2017, from 88 to 10. Reason can be based on user ratings

# In[52]:


nd.head()


# In[53]:


nd_tv14 = nd[nd['rating']=='TV-14'].reset_index(drop=True)


# In[54]:


nd_tv14


# In[55]:


count_16 = nd_tv14[nd_tv14['release year']==2016]['user rating score'].count()
median_16 = nd_tv14[nd_tv14['release year']==2016]['user rating score'].median()

count_17 = nd_tv14[nd_tv14['release year']==2017]['user rating score'].count()
median_17 = nd_tv14[nd_tv14['release year']==2017]['user rating score'].median()

count_15 = nd_tv14[nd_tv14['release year']==2015]['user rating score'].count()
median_15 = nd_tv14[nd_tv14['release year']==2015]['user rating score'].median()


# In[56]:


count = []
count.append([count_15,count_16,count_17])
count = [obj for sublist in count for obj in sublist]
median = []
median.append([median_15,median_16,median_17])
median = [obj for sublist in median for obj in sublist]


temp_dict = {'year': [2015,2016,2017],'count': count, 'median': median}
temp = pd.DataFrame(temp_dict)
temp = temp.set_index('year')

print(temp)


# ##### Ans: Couldn't find an answer because the rating median still remained the same, it can be other production related issues or an issue outside the scope of the data.

# ##### Que: Ratings based on genre

# In[57]:


for i in array_ratings:
    
    selected_values = nd['user rating score'].loc[nd['rating']==i]

    histogram = go.Histogram(x=selected_values)

    layout = go.Layout(title=f'Histogram for {i}')

    fig = go.Figure(data=[histogram], layout=layout)

    fig.show()


# ##### We can see that most shows and movies have their rating on the higher side, although there are a few genres like TV-Y7 and TV-G. Considering their weighted average is on the lower end too, the producers and story writers should invest more in the betterment of these genres and experiment.
