#!/usr/bin/python

import tweepy
import textwrap

consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

pad = '-' * 35

w = "\033[0m"
b = "\033[1m"
d = "\033[2m"
bb = "\033[34m"
bc = "\033[36m"
blb = "\033[94m"
blc = "\033[96m"

def is_reply(tweet):
   if (tweet.in_reply_to_status_id or 
      tweet.in_reply_to_status_id_str or 
      tweet.in_reply_to_user_id or 
      tweet.in_reply_to_user_id_str or
      tweet.in_reply_to_screen_name):
      return True

def is_retweet(tweet):
   if (tweet.retweeted or
      "RT @" in tweet.text):
      return True


def color(word):
   if word.startswith("#"):
      word = blc+word+"\033[0m"
      return word
   elif word.startswith("@"):
      word = blb+word+"\033[0m"
      return word
   elif word.startswith("https"):
      word = d+word+"\033[0m"
      return word
   else:
      return word


class MyStreamListener(tweepy.StreamListener):
   def on_status(self, status):
      if (not is_retweet(status)) and (not is_reply(status)):
         print("\n"+blb+b+status.user.name+w+" - "+blb+"@"+status.user.screen_name+w)
         if status.truncated:
            text = status.extended_tweet["full_text"]
         else:
            text = status.text

         l = text.split()
         l[:] = [color(word) for word in l]
         text = " ".join(l)
         print("\n"+textwrap.fill(text, 35)+"\n\n"+bb+b+pad+w)


def main():
   print(bc+b+"{: ^35s}".format("Python Twitter API Feed")+"\n"+bb+b+pad+w)
   myStreamListener = MyStreamListener()
   myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener, tweet_mode="extended")

   myStream.filter(follow=["34743251", "44196397"], track=["#spacex"])


if __name__ == "__main__":
   main()
