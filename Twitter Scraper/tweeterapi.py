from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
#import tweepy
from textblob import TextBlob
import tkinter as tk
#import json
import csv
#import time
#import sys
import re
import wget
import threading
from tkinter import ttk




access_token = "##################################################"
access_token_secret = "#########################################"
consumer_key = "#####################"
consumer_secret = "##########################################"


#This is a basic listener that just prints received tweets to stdout.
result_list=[]
media_files = []
ouput_dir = 'output_media'


class StdOutListener(StreamListener):
    
    
    def on_status(self, status):
        if status.retweeted:
            return

        description = status.user.description
        loc = status.user.location
        print(loc)
        text = status.text
        #tidy_tweet = text.strip().encode('ascii', 'ignore')
        cleaned_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+://\S+)", " ", text).split())
        print(cleaned_tweet.encode('utf-8'))
#print(tidy_tweet)
        coords = status.coordinates
        geo = status.geo
        print(geo)
        name = status.user.screen_name
        print(name)
        user_created = status.user.created_at
        print(user_created)
        followers = status.user.followers_count
        print(followers)
        friends=status.user.friends_count
        print(friends)
        favorites=status.user.favourites_count
        print(favorites)
        id=status.id
        print(id)
        id_str = status.id_str
        created = status.created_at
        print(created)
        retweets = status.retweet_count
        print(retweets)
        url=status.entities["urls"]
        
        print(url)
        hashtags=status.entities["hashtags"]
        print(hashtags)
        blob = TextBlob(text)
        sent = blob.sentiment
        polarity=sent.polarity
        
        if polarity < 0:
            sentiment = "negative"
            
        elif polarity == 0:
            
            sentiment = "neutral"
            
        else:
            sentiment = "positive"
            

        # output sentiment
        print(sentiment)
        if 'media' in status.entities:
#            print("Media is there")
            medias=status.entities['media']
            for k in medias:
                l=k["media_url"]
                wget.download(l, ouput_dir)
                #print("done")
        else:
            print("No Media")
        bg_color = status.user.profile_background_color
        result_list.append((id,name,loc,cleaned_tweet,geo,followers,created,retweets,url,favorites,friends,followers,sentiment,hashtags))
		
        csv_file = open('tweeet.csv', 'a')
        csv_writer = csv.writer(csv_file)
        #csv_writer.writerow("\n\n")
        csv_writer.writerow([id,name,loc,cleaned_tweet,geo,followers,created,retweets,url,favorites,friends,followers,sentiment,hashtags])
        csv_file.close()
    # def on_error(self, status):
        # print (status)
    def on_error(self, status_code):
        if status_code == 420:
#returning False in on_error disconnects the stream
           return False	
class StddOutListener(StreamListener):

    def on_status(self, status):
    
        if status.retweeted:
            return

        description = status.user.description
        loc = status.user.location
        print(loc)
        text = status.text
        #tidy_tweet = text.strip().encode('ascii', 'ignore')
        cleaned_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+://\S+)", " ", text).split())
        print(cleaned_tweet.encode('utf-8'))
#print(tidy_tweet)
        coords = status.coordinates
        geo = status.geo
        print(geo)
        name = status.user.screen_name
        print(name)
        user_created = status.user.created_at
        print(user_created)
        followers = status.user.followers_count
        print(followers)
        friends=status.user.friends_count
        print(friends)
        favorites=status.user.favourites_count
        print(favorites)
        id=status.id
        print(id)
        id_str = status.id_str
        created = status.created_at
        print(created)
        retweets = status.retweet_count
        print(retweets)
        url=status.entities["urls"]
        
        print(url)
        hashtags=status.entities["hashtags"]
        print(hashtags)
        blob = TextBlob(text)
        sent = blob.sentiment
        polarity=sent.polarity
        
        if polarity < 0:
            sentiment = "negative"
            
        elif polarity == 0:
            sentiment = "neutral"
            
        else:
            sentiment = "positive"
            

        # output sentiment
        print(sentiment)
        if 'media' in status.entities:
            print("Media is there")
            medias=status.entities['media']
            for k in medias:
                l=k["media_url"]
                print(l)
                # wget.download(l, ouput_dir)
                # #print("done")
        else:
            print("No Media")
        bg_color = status.user.profile_background_color
        result_list.append((id,name,loc,cleaned_tweet,geo,followers,created,retweets,url,favorites,friends,followers,sentiment,hashtags))
		
        csv_file = open('tweeet.csv', 'a')
        csv_writer = csv.writer(csv_file)
        #csv_writer.writerow("\n\n")
        csv_writer.writerow([id,name,loc,cleaned_tweet,geo,followers,created,retweets,url,favorites,friends,followers,sentiment,hashtags])
        csv_file.close()
    # def on_error(self, status):
        # print (status)
    def on_error(self, status_code):
        if status_code == 420:
#returning False in on_error disconnects the stream
           return False	

if __name__ == '__main__':
#    a=input(str("enter the keywords you want to search"))
#    c=int(input("enter"))
    root=tk.Tk()
    root.geometry("1000x600")
    root.title("Twitter Scraper")
    root.configure(background='#0271aa')
    tk.Label(root, text="Term you want to Search :").grid(row=0,padx=100,pady=40)
    inp=tk.Entry(root)
    inp.grid(row=0, column=1)
    
    
    v = tk.IntVar()
    v.set(1)
    tk.Radiobutton(root, text="YES", variable=v, value=0).grid(row=1,column=1)
    tk.Radiobutton(root, text="NO", variable=v, value=1).grid(row=1,column=2)
    tk.Label(root, text="Do you want to download Media?:").grid(row=1)
    vv = ttk.Progressbar(root, orient="horizontal",
                                        length=300, mode="indeterminate")
    vv.grid(row=7, column=1)
    
    
    
    def t1():
        a=inp.get()
        c=v.get()
        if c==0:
        #This handles Twitter authetification and the connection to Twitter Streaming API
            l = StdOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            stream = Stream(auth, l)
            
           
        elif c==1:
            l = StddOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            stream = Stream(auth, l)
        while True:
            try:
                stream.filter(track=[a])
            except Exception as e:
                continue
#    t2 = threading.Thread(target=t1) 
    def thread2():
        vv.stop()
        messagebox.showinfo("Sucess","Sucessfully Saved")
        root.destroy()
        exit()
  
    def getValues():
        vv.start(10)
        t2 = threading.Thread(target=t1) 
        t2.daemon = True
        t2.start()
    
    tk.Button(root, text='Search',command=lambda:getValues()).grid(row=5,column=1,padx=20,pady=40)
    tk.Button(root, text='Stop',command=lambda:thread2()).grid(row=6,column=1,padx=20,pady=40)
    root.mainloop()
        
    


