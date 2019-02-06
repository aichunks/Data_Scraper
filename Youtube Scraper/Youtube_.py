from apiclient.discovery import build
from tkinter import messagebox
import pafy
import re
import importlib
import sys
import os
import pandas as pd
import shutil
import glob
importlib.reload(sys)
import tkinter as tk
from tkinter import ttk
import threading
from googleapiclient.errors import HttpError


DEVELOPER_KEY = "###################"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
pafy.set_api_key("########")
class MyFirstGUI:
    def __init__(self, master,top):
        self.top=top
        self.master = master



        try:
            self.youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY
                                 ,cache_discovery=False)
        except HttpError:
            self.master.destroy()
            self.top.withdraw()
            messagebox.showerror("error", "HTTp Error, enter your credentials ")
            exit()
        self.result_list=[]
        self.fn="scraper.csv"
    def mainWindow(self):
#        self.master.geometry("400x200")    
#        self.master.title("Process  ")
        self.master.resizable(0,0)
        self.master.overrideredirect(1)
        self.processbar = ttk.Progressbar(self.top, orient="horizontal",
                                        length=250, mode="indeterminate")
        self.processbar.grid(row=7, column=1,columnspan=2,sticky='W')
        self.processbar.start(10)
        
    def login(self):
        self.top.geometry("750x550")

        self.top.resizable(0, 0)
        # self.top.configure(background='#fe2956')

        background_image = tk.PhotoImage(file="F:/DB/DATA Scrper/youtubeback.gif")
        background_label = tk.Label(self.top, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image


        
        tk.Label(self.top, text="Term you want to Search :",width=27,height=2).grid(row=0,column=0,padx=100,pady=40,columnspan=2)
        self.a=tk.Entry(self.top,font=('Calibri',18))
        self.a.grid(row=0, column=2,columnspan=2)
        tk.Label(self.top, text="Do you want to download videos?",width=27,height=2).grid(row=1,padx=100,pady=40,columnspan=2)
        self.v = tk.IntVar()
        self.v.set(1)
        tk.Radiobutton(self.top, text="YES", variable=self.v, value=0,width=8,height=2).grid(row=1,column=2,sticky='W')
        tk.Radiobutton(self.top, text="NO", variable=self.v, value=1,width=8,height=2).grid(row=1,column=3,sticky='E')
        
        tk.Label(self.top, text="Select limit",width=27,height=2).grid(row=3,padx=100,pady=40,columnspan=2)
        
        variable = tk.StringVar(self.top)
        variable.set(1) # default value
        
        self.b=tk.Spinbox(self.top,from_=1, to=50,width=15,font=('Calibri', 17))
        self.b.grid(row=3,column=2,sticky='E')
        tk.Button(self.top, text='Search',command=lambda:self._login_btn_clicked(),width=12,height=2).grid(row=5,column=0,padx=20,pady=40,columnspan=2,sticky='E')

        self.output_variable = tk.StringVar(self.top)
        
    def search(self):
        self.searchTerm = self.a.get()
        self.c=self.v.get()
        self.limit=self.b.get()
        if len(self.searchTerm)==0:
            self.processbar.stop()
            messagebox.showerror("error", "Please Enter your Search Item ")

        elif int(self.limit)>50:
            self.processbar.stop()
            messagebox.showerror("error", "select lmit 0-50")

        else:
            
            self.fetch_data()
            
            
            
 
    def get_videodata(self,videoId):
        
        
        url = "https://www.youtube.com/watch?v=" + videoId
        	#Request fro Metadata of the Video
        v = pafy.new(url)
        title = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+://\S+)", " ", v.title).split())
        print(title.encode('utf-8'))
        self.result_list.append((title,v.duration,v.rating,v.author,v.length,v.thumb,v.videoid,v.viewcount,v.likes,v.dislikes,v.published,v.keywords))
        	#print(len(result_list))
        column_names=['title','duration','rating','author','length','thumb','videoid','viewcount','likes','dislikes','published','keywords','description','category','username']
        if os.path.exists(self.fn):
            data = pd.read_csv('scraper.csv',names=column_names)
            data1=pd.DataFrame(self.result_list)
			  #print(data1[6])
            res=data[['videoid']]
			#print(res)
            result = data1[~(data1[6].isin(data['videoid']))]
			#print(result)
            if len(result)!=0:
                s = v.getbest(preftype="mp4")
                filename = s.download(quiet=False)
                source_dir = '/Users/lenovo/Desktop/scrap_data' #Path where your files are at the moment
                dst = '/Users/lenovo/Desktop/scrap_data/videos' #Path you want to move your files to
                files = glob.iglob(os.path.join(source_dir, "*.mp4"))
                for file in files:
                    if os.path.isfile(file):
                        shutil.move(file, dst)
        else:
            column_names=['title','duration','rating','author','length','thumb','videoid','viewcount','likes','dislikes','published','keywords']
            csv_file = open(self.fn,'a')
            data = pd.read_csv('scraper.csv',names=column_names)
            #column_names=['title','duration','rating','author','length','thumb','videoid','viewcount','likes','dislikes','published','keywords']
            data1=pd.DataFrame(self.result_list)
            res=data[['videoid']]
            #print(res)
            result = data1[~(data1[6].isin(data['videoid']))]
            #print(result)
            if len(result)!=0:
                s = v.getbest(preftype="mp4")
                filename = s.download(quiet=False)
                source_dir = '/Users/lenovo/Desktop/scrap_data' #Path where your files are at the moment
                dst = '/Users/lenovo/Desktop/scrap_data/videos' #Path you want to move your files to
                files = glob.iglob(os.path.join(source_dir, "*.mp4"))
                for file in files:
                    if os.path.isfile(file):
                        shutil.move(file, dst)
        return self.result_list
    def get_data(self,videoId):
        	
        	
        	url = "https://www.youtube.com/watch?v=" + videoId
        	#Request fro Metadata of the Video
        	v = pafy.new(url)
        	title = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+://\S+)", " ", v.title).split())
        	print("llllll",title.encode('utf-8'))
        	
        	self.result_list.append((title,v.duration,v.rating,v.author,v.length,v.thumb,v.videoid,v.viewcount,v.likes,v.dislikes,v.published,v.keywords))
        	
        	return self.result_list
        
    def fetch_data(self):
        if self.c==0:
        	
        	search_response = self.youtube.search().list(
        		  q=self.searchTerm,
        		  part="id,snippet",
        		  maxResults=self.limit
        		).execute()
        	
        	count = 0
        	for search_result in search_response.get("items", []):
        		if search_result["id"]["kind"] == "youtube#video":
        			if count <100:
        				
        				
        				vID = search_result["id"]["videoId"]
        				self.get_videodata(vID)
        				count += 1
        				
        			else:
        				break
        		else:
        			continue
        elif self.c==1:
        
        	search_response = self.youtube.search().list(
        		  q=self.searchTerm,
        		  part="id,snippet",
        		  maxResults=self.limit
        		).execute()
        	count = 0
        	for search_result in search_response.get("items", []):
        		if search_result["id"]["kind"] == "youtube#video":
        			if count <100:
        				
        				
        				vID = search_result["id"]["videoId"]
        				self.get_data(vID)
        				count += 1
        				
        			else:
        				break
        		else:
        			continue
        	
        
        
        self.unique_list=[]
        if os.path.exists(self.fn):
        	column_names=['title','duration','rating','author','length','thumb','videoid','viewcount','likes','dislikes','published','keywords']
        	data = pd.read_csv(self.fn,names=column_names)
        	#column_names=['title','duration','rating','author','length','thumb','videoid','viewcount','likes','dislikes','published','keywords']
        	data1=pd.DataFrame(self.result_list)
        
        
        	self.res=data[['videoid']]
        	#print(data1[[6]])
        	self.result = data1[~(data1[6].isin(data['videoid']))]
        
        	
        	#unique_list.append(result)
        	self.result.to_csv(self.fn, encoding='utf-8', index=False,mode='a',header=False)
        	self.processbar.stop()
        	messagebox.showinfo("Sucess","Sucesssfully saved")
        	
        	
	
        else:
        	column_names=['title','duration','rating','author','length','thumb','videoid','viewcount','likes','dislikes','published','keywords']
        	data1=pd.DataFrame(self.result_list)
        	data1.to_csv(self.fn, encoding='utf-8', index=False,mode='a',header=False)
        	self.processbar.stop()
        	messagebox.showinfo("Sucess","Sucesssfully saved")
        	        	      	       	
 
    def _login_btn_clicked(self):
        
        _thread = threading.Thread(target=self.search, daemon=True)
        _thread.start()
        self.mainWindow()
        self.top.deiconify()
    



if __name__=="__main__":
    top = tk.Tk()
    root = tk.Toplevel()
    menu =MyFirstGUI(root,top)
    menu.login()
    root.withdraw()

    root.mainloop()