# Tesla_Stock_Sentiment_Analyzer

Requirement Text
Web scraping cnbc.com to fetch entities related to tesla and do sentiment analysis based on positive
and negative news that will tell If one should buy or sell stocks of tesla.
High Level Requirements
1.) Fetch tesla articles from cnbc.com
a. Title and description
2.) Process the content
a. Parse and clean the content which is not relevant for sentiment analysis
3.) Perform Sentiment Analysis
4.) Predict the impact on tesla stock based on sentiment analysis results
Modules and Approach Used for Implementing High Level Requirements
1.) Fetch tesla articles from cnbc.com
Python Module: webscrapper.py
Python Internal Modules used
import requests
from bs4 import BeautifulSoup
import pandas_read_xml as pdx
import pandas as pd
Method to fetch cnbc urls recursively from baseurl –
'https://www.cnbc.com/sitemapAll.xml'
For POC purpose – in order to keep the Data-set short… Fetching only tesla urls from latest years
CNBCsitemapAll10.xml (2019, 2020 and 2021)
It fetches the urls which have tesla in it and saves them in xml format on disc.

2.) Process the content
Python Module: preprocessdata.py
Python Internal Modules used
import re
import pandas as pd
Method is used to do pre-processing on the content returned from previous module. It basically
removes links, urls, hashtags, mentions, punctuations, multiple spaces, numbers which are not relevant
to sentiment analysis. Finally, it produces the cleaned data frame as output.

3.) Perform Sentiment Analysis
4.) Predict the impact on tesla stock based on sentiment analysis results
Python Module: sentimentanalysis.py
Python Internal Modules used
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import pandas as pd
Method is used to perform sentiment analysis of the processed content. It uses NLTK Vader
SentimentIntensityAnalyzer tool. It calculates the polarity score of each individual article (which includes
title and description) and prepares list of results by computing the compound results.
After that, it computes the count of positive, negative and neutral sentiments and their individual
percentages.
Finally, tells the prediction based on the sentiment analysis percentage.
"


# Conclude Results
if positive_sentiments_percentage > negative_sentiments_percentage:
print (
'Positive sentiments percentage is more than Negative sentiments
percentage based on the content analysed '
'on cnbc, so one should buy (i.e. invest) stocks of Tesla' )
else :
print (
'Negative sentiments percentage is more than Positive sentiments
percentage based on the content analysed '
'on cnbc, so one should sell (i.e. not invest) stocks of Tesla' )
Challenges
● Normal Web scrapping using BeautifulSoup does not work here as the articles on cnbc website
are loaded dynamically, so finding the div/anchor/span tags was not appropriate.
● Also, I tried using selenium web driver to control the operations of cnbc web page. But the
design approach was really complicated and not much useful.
● So, I explored the option to query the data using ‘https://www.cnbc.com/robots.txt’ url and
recursively parse all tesla urls from baseurl ‘https://www.cnbc.com/sitemapAll.xml’
● Another, problem was the number of web pages that needs to be parsed and scanned for
fetching the tesla content. So, considering the tesla stock will get impacted based on data of
recent most years. I have used tesla new articles from
‘https://www.cnbc.com/CNBCsitemapAll10.xml’ for years 2019, 2020 and 2021 only.
