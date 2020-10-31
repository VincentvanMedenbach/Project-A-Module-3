from tkinter import *
import tkinter as tk
from tkinter import ttk
from cfg import Config
import tweepy
import threading
import requests, json

statusId = 0


root = Tk()


root.geometry('450x200')

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

frame_container = Frame(root)
frame_container.pack()
canvas_container = Canvas(frame_container, height=100)
frame2 = Frame(canvas_container)
canvas_container.create_window((0, 0), window=frame2, anchor='nw')

contentLabel = Label(canvas_container, text="Bericht van reiziger", font=('Helvetica', 30))
contentLabel.pack()

frame2.pack()


canvas_container.pack(side=LEFT)

frame_container.pack()

# Enter your API key here
api_key = Config.openWeatherApiKey

# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Give city name
city_name = "Utrecht"

# complete_url variable to store
# complete url address
complete_url = base_url + "q=" + city_name + "&appid=" + api_key


def getTweets():

    global statusId
    global frame2
    global contentLabel

    threading.Timer(5, getTweets).start()

    auth = tweepy.OAuthHandler(Config.consumer_key, Config.consumer_secret)
    auth.set_access_token(Config.access_token, Config.access_token_secret)
    api = tweepy.API(auth)
    if not statusId:
        status = api.user_timeline()[-1]
    else:
        try:
            status = api.user_timeline(since_id=statusId)[-1]
        except:
            print("No status to be found!")
    print("test")
    # print(status)
    if 'status' in locals():
        contentLabel['text'] = "Bericht van reiziger"

        statusId = status.id
        print(status.text)
        frame2.destroy()
        frame2 = Frame(canvas_container)
        frame2.pack()
        tweet = Label(frame2, text=status.text,  font=('Comic Sans MS', 20))
        tweet.pack()
    else:
        response = requests.get(complete_url)
        contentLabel['text'] = "Weer"
        # json method of response object
        # convert json format data into
        # python format data
        x = response.json()
        print(x)
        frame2.destroy()
        frame2 = Frame(canvas_container)
        frame2.pack()
        weer1 = Label(frame2, text=x['weather'][0]['main'] , font=('Comic Sans MS', 20))
        weer1.pack()
        weer2 = Label(frame2, text=x['weather'][0]['description'], font=('Comic Sans MS', 20))
        weer2.pack()



getTweets()

app = Window(root)
root.mainloop()


