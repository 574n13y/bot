
#from run import getData #gets data from the zigbee(xbee) connected in the raspberry pi

#stikers
Stiker ={"Thinking": "CAADAgADNwADyIsGAAFOgk-EJUfH-gI",
         
  "Albert_Einstein":"CAADAgADIQADyIsGAAHaCFln7THl9QI" ,
         
  "Goodnight":"CAADAgADxgUAAvoLtgjbqjaBr05-YgI",
         
  "Waiting":"CAADAgADxQUAAvoLtgipmNsAAd08atYC",
         
  "Are you still there?":"CAADAgAD2AUAAvoLtgijNBwY2-_7mAI",
         
  "Shocked_skeleton":"CAADAgADuQUAAvoLtgitaO6BWhPrzwI",
         
  "YES_bitcon_guy":"CAADAgADewYAAmMr4gmlCfM1Be9yKAI",

   "Deadpool_laughing":"CAADAgADTQEAAooSqg6mK47oU2XwewI",

   "Thumbs_up_deadpool":"CAADAgADQAEAAooSqg6FLrYwmvbwXwI"      
}
print("here")
#emoji
Emojies={"SMILEY FACE": u'\U0001F600',"LINUX" :u'\U00001427',"MOVIE":"	u'\U0001F3AC"}

#wikiquote api
from wikiquote import quote_of_the_day  #wikiquote module for quotes

print("wikiquote done")
#extensions 
from Extensions.Lms import documents
from Extensions.GoodReads import Gquote  as Good # Goodreads check the extension folder
from Extensions.Quotes import links   
from Extensions.DSE import init as DSE  # dar es salaam stock exchange
import re # regular expressions for searching strings
import subprocess    # for running linux  commands in python
#from serial import SerialException
from Extensions.vAttendence_percentage import attendance

print("Extensions done")
# wikipedia api funtions importation
from wikipedia import summary as ans
from wikipedia import exceptions as ex
from wikipedia import page as Page
print("wikipedia done")

#telegram bot api functions importation
from telegram import Bot
import telegram
from telegram.ext import Updater # checks for updates like new messages etc
from telegram import InlineKeyboardButton, InlineKeyboardMarkup # for the keyboard

print("telegram done")
#useful functions and modules
import schedule # for 
from functools import lru_cache as Cache #for storing data in cache 
import time
from os import remove
print("functions done")

#imdb
import tmdbsimple as tmdb
tmdb.API_KEY = 'e542e5e9c5f014dd493e1a65710bbd18'
search=tmdb.Search()

print("imdb done")
#test the internet connection
def is_connected():
  import socket
  REMOTE_SERVER = "www.google.com"
  try:
    host = socket.gethostbyname(REMOTE_SERVER)
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

#wikipedia fuction
@Cache(maxsize=100) # fuction decorator to store that data received in cache 
def wiki(received,u):
  
                keyWord=re.compile(r'\wiki (.*)')
                try:
                        image=""
                        for img in Page(keyWord.findall(received)).images:
                                if ("jpg" in img or "jpeg" in img or "png" in img):
                                        image=img
                                        break
                        wiki_summary=ans(keyWord.findall(received),sentences=3)
                        if(image==""):
                          image=None
                              
                except ex.PageError:
                        bot.send_message(chat_id=u.message.chat_id, text="Sorry check your spelling")
                except ex.DisambiguationError as e :
                        bot.send_message(chat_id=u.message.chat_id, text="try being more specific \n" +str(e))
                except:
                        pass

                return wiki_summary,image



def Movie(item):
  from google.google import search
  result=search("intitle:index.of? mkv " +item)
  Movies=[]
  for r in result:
    Movies.append(r.link)
  return Movies
	

                
#quote of the day from wikiquote
@Cache(maxsize=100)  # fuction decorator to store that data received in cache
def  Quotes(u):
    quote,person=(quote_of_the_day())
    bot.send_message(chat_id=u.message.chat_id, text=quote)
    bot.send_message(chat_id=u.message.chat_id, text=person)
#this fuction is scheduled to run every morning
def morning(t):
  documents()
  keyWord=re.compile(r'\wrainy (.*)')
  images=links(keyWord.findall("brainy jim rohn"))
  for img in images:
    bot.send_photo(chat_id=431226183, photo=img)

#checks if connected to the internet 
while not is_connected():
    print("status: offline")

#bot initializations
updater = Updater(token="399340337:AAG-yD4Xpfo1cCOfoLJLI9lDSE7_fbEtqiA") #put the token you got from "THE BOT FATHER"
print("updater done")
bot=Bot(token="399340337:AAG-yD4Xpfo1cCOfoLJLI9lDSE7_fbEtqiA")#put the token you got from "THE BOT FATHER"
print("bot done")
#print(bot.get_me()) #prints the bots details
updater.start_polling(timeout=10)#starts the updater

print("status: online")
# this will run a certain task at a particular time everyday
schedule.every().day.at("03:00").do(morning,"ok") #you can 


while True:
    schedule.run_pending()
    try :
            
            for u in bot.get_updates():  #u stands for update
                #do something
                user=u.message.from_user
                received=u.message.text
                print(str(user["first_name"])+" texted : " + received)
                if "ip" in received.lower():
                    inet=str(subprocess.check_output(["ifconfig | grep inet"], shell=True)).split("          ")
                    ip=inet[4].split("  ")
                    text=ip[0]
                    bot.send_message(chat_id=u.message.chat_id, text=text)

                   #for brainy quotes (images) text brainy (name of the person)
                elif "brainy" in received.lower():
                  keyWord=re.compile(r'\wrainy (.*)')
                  print(keyWord.findall(received.lower()))
                  images=links(keyWord.findall(received.lower()))
                  for img in images:
                    bot.sendPhoto(chat_id=u.message.chat_id, photo=img)

                  #for goodreads quotes text good (person) (number of quotes you want)
                elif "movie" in received.lower():
                  keyWord=re.compile(r'\wvie (.*)')
                  item=(keyWord.findall(received.lower())[0])
                  imdb_result=search.movie(query=item)
      
                  
                  if(len(imdb_result["results"])!=0):
                    data=imdb_result["results"][0]
                    title=data["title"]
                    poster="https://image.tmdb.org/t/p/w300_and_h450_bestv2"+data["poster_path"]
                    print("done imdb")

                  
                    Movies=Movie(title)
                    keyboard=[]
                    row=[]
                    for link in Movies:
                      if(Movies.index(link)!= 3):
                        print("creating links")
                        row.append([telegram.InlineKeyboardButton(text=" link :"+ str(Movies.index(link)+1),url=str(link))])
                        print("link")
                      else:
                        print("links created...")
                        break

                

                    reply_markup = telegram.InlineKeyboardMarkup(row)
                    bot.sendPhoto(chat_id=u.message.chat_id,photo=poster,caption=title)
                    bot.send_message(chat_id=u.message.chat_id, text= "overview : \n" +data["overview"] ,reply_markup=reply_markup)
                  else:
                    bot.send_message(chat_id=u.message.chat_id, text="Nothing found")
                  print("sent movie details")
                                 

                elif "lms" in received.lower():
                  keyWord=re.compile(r'\wms (.*)')
                  import os
                  lms_files='/app/LMS'
                  Lms=os.listdir(lms_files)
                  Files={}
                  for dir in Lms:
                    files_list=[]
                    directory=lms_files+'/'+dir
                    course_name=dir
                    if os.path.isdir(directory):
                      for file in os.listdir(directory):
                        files_list.append(directory+"/"+file)
                      Files[course_name]=files_list

                  if keyWord.findall(received) == []:
                    keyboard=[]
                    available_files=list(Files.keys())
                    for file in available_files:
                      keyboard.append(["lms "+str(file)])
                    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
                    bot.send_message(chat_id=u.message.chat_id, text='choose '+Emojies["SMILEY FACE"] ,reply_markup=reply_markup)
                  else:
                    course=str(keyWord.findall(received)[0])
                    print(course)
                    import os
                    lms_files='/app/LMS'
                    Lms=os.listdir(lms_files)
                    Files={}
                    for dir in Lms:
                      files_list=[]
                      directory=lms_files+'/'+dir
                      course_name=dir
                      if os.path.isdir(directory):
                        for file in os.listdir(directory):
                          files_list.append(directory+"/"+file)
                        Files[course_name]=files_list    
                    for file in Files[course]:
                      bot.send_document(chat_id=u.message.chat_id, document=open(file,"rb"))
                    print("sent files")
                    
                elif "refresh" in received.lower():
                  documents()
                  bot.send_message(chat_id=u.message.chat_id, text="Refreshed")

                elif "good" in received.lower():
                  keyWord=re.compile(r'\wod(.*) (\d?\d)?')
                  qoute , number=keyWord.findall(received.lower())[0]
                  if number != None:
                    number=int(number)
                  Gq=Good(qoute , number)
                  for quote in Gq :
                    bot.send_message(chat_id=u.message.chat_id, text=quote[0])
                    bot.send_message(chat_id=u.message.chat_id, text=quote[1])

                 #dar es salaam stock exchange text "dse"
                elif "dse" in received.lower():
                    stock_data,Market_report=DSE()
                    bot.send_message(chat_id=u.message.chat_id, text=stock_data)
                    bot.send_document(chat_id=u.message.chat_id, document=Market_report)

                 #get music from the music folder text "Music (song name)"   
                elif "Music" in received:
                    keyWord=re.compile(r'\wusic (.*)')
                    word=str(keyWord.findall(received)[0])
                    audio=str(subprocess.check_output(["ls /home/pi/Music/"+word], shell=True).decode()).strip()
                    bot.send_audio(chat_id=u.message.chat_id, audio=open(audio,"rb"))
                    bot.send_chat_action(chat_id=u.message.chat_id,action=telegram.ChatAction.UPLOAD_AUDIO)
                elif "Vat" in received:
                  text,name=attendance(received,u,bot)
                  if text!=None:
                    bot.send_message(chat_id=u.message.chat_id, text=name + "your attendance is "+text)
                    if float(text.replace("%","")) > 75:
                      bot.send_sticker(chat_id=u.message.chat_id,sticker=Stiker['YES_bitcon_guy'])
                    else:
                      bot.send_sticker(chat_id=u.message.chat_id,sticker=Stiker['Shock_skeleton'])
                #get wikiquote of the day text "quote" 
                elif "quote" in received.lower():
                    Quotes(u)

                #search wikipedia text "wiki (something)" example "wiki University of Dar es salaam"    
                elif "wiki" in received.lower():
                    bot.send_message(chat_id=u.message.chat_id, text="ok")
                    text,image = wiki(received,u)
                    print(image)
                    print("sending photo")
                    bot.sendPhoto(chat_id=u.message.chat_id, photo=image)
                    bot.send_message(chat_id=u.message.chat_id, text=text)
                
                                
            

                #the bot will send your first name    
                elif("name" in received.lower() ):
                    text="Your name is "+user["first_name"]
                    bot.send_message(chat_id=u.message.chat_id, text=text)

                #The bot will send you a document
                elif("document" in received.lower()):           
                    bot.send_document(chat_id=u.message.chat_id, document=open("/home/ubuntu/workspace/UdPject/Records.xlsx","rb"))
                else:
                  import random
                  #default message
                  bot.send_message(chat_id=u.message.chat_id, text="Hi "+user["first_name"]+" "+user["last_name"]+" "+Emojies["SMILEY FACE"] +''' 
Try 
(1)dse 
(2)quotes
(3) wiki obama or wiki 'something'
(4) lms (for sharda EEE 3rd Year students)
(5) Vat roll_number password (Attendance percentage for Sharda Students)
(6)Movie eg movie avengers
(7)Name (to see your UserName)''')
                  time.sleep(1)
                  bot.send_sticker(chat_id=u.message.chat_id,sticker=random.choice(list(Stiker.values())))
    except Exception as e:
        print("status: offline")
        while not is_connected():
          pass
        updater.start_polling()
        print("status: online")
        #for debugging purposes it will text you the exception that occured 
        text=str(e)
        bot.send_message(chat_id=u.message.chat_id, text=text)







        
