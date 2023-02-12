'''
Project Name :Sharda university vattendance
Project by   : Mbonea Mjema
Year         :2017
'''
from requests import Session as Search
from bs4 import BeautifulSoup as bs
import re


def attendance(credentials,u,bot):
    login_url="http://sharda.vattendance.in/"
    pattern=re.compile(r'\wat (\d\d\d\d\d\d\d\d\d) (.*)')
    details=pattern.findall(credentials)
    roll_number=details[0][0]
    password=details[0][1]
    data={"username":roll_number,
          "password":password,
          "submit":"login"}

    with Search() as s:
        
            dash_board=s.post("http://sharda.vattendance.in/",data=data)
            
            html=s.get("http://sharda.vattendance.in/stu_complete_report")
            if(len(html.text)<10000):
                bot.send_message(chat_id=u.message.chat_id, text="check your id and password!")
                return None,None

    attendance=bs(html.text,"html.parser").find("tfoot" )
    name=bs(html.text,"html.parser").find("span",{"class":"username username-hide-on-mobile"})
    percentage=attendance('th')[4].text

    return percentage,name.text
