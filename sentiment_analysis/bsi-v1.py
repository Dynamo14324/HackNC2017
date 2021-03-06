# import tweepy library for twitter api access and textblob libary for sentiment analysis
import csv
import tweepy
import numpy as np
import re
import nltk
import pandas as pd
from tweepy.streaming import StreamListener
from sklearn.naive_bayes import BernoulliNB, GaussianNB
from sklearn.linear_model import LogisticRegression
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from collections import Counter
from tweepy import OAuthHandler, Stream
from textblob import TextBlob


def main():
    
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
 
    api = tweepy.API(auth,wait_on_rate_limit=True)

    cpos = 0
    cneg = 0

    # Open/create a file to append data to
    csvFile = open('result1.csv', 'a')

    #Use csv writer
    csvWriter = csv.writer(csvFile)

    for tweet in tweepy.Cursor(api.search,
                           q = "bitcoin price",
                           since = "2017-11-04",
                           until = "2017-11-04",
                           lang = "en").items():
        csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
        #print tweet.created_at, tweet.text
    csvFile.close()
    df = pd.read_csv('result1.csv')

    tweets_list = list(df.iloc[:,1])
    #print len(tweets_list)

    un_labelled = []

    for tweet in tweets_list:
        tweet = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet)
        words = [w.lower() for w in tweet.strip().split() if len(w)>=3]
        un_labelled.append(' '.join(words))

    csvFileP = open('master_positive.csv', 'a')
    csvWriterPositive = csv.writer(csvFileP)

    csvFileN = open('master_negative.csv', 'a')
    csvWriterNegative = csv.writer(csvFileN)

    for sentence in un_labelled:
        analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(sentence)

    # print(str(vs))
        if vs["compound"] < (-0.5057):
            cneg += 1
            csvWriterNegative.writerow([sentence, "Negative"])

        if vs["compound"] > (0.5057):
            cpos += 1
            csvWriterPositive.writerow([sentence, "Positive"])

    csvFileP.close()
    csvFileN.close()
    
   
    bsi = cpos/cneg
    print bsi, cpos, cneg
    
    if bsi > 1:
        print "Current social media trend reflects a positive sentiment towards bitcoin."
    elif bsi < 1:
        print "Current social media trend reflects a negative sentiment towards bitcoin."
    else:
        print "Current social media trend reflects a neutral sentiment towards bitcoin."




if __name__ == '__main__':
    main()
