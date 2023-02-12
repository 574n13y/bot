from bs4 import BeautifulSoup as bs 
from requests import Session as Search
'''
PROJECT NAME:SHARDA LMS
BY          :MBONEA MJEMA
     2017
'''

def documents():
    Documents={}
    #login url
    url="http://sulms.sharda.ac.in/login/index.php"

    #user input
    print("##########_______SHARDA UNIVERSITY  LMS LOGIN_________########## ")
    #user=input("Enter username ")
    #password=input("Enter the password ")

    #user_data
    data={
    "username":'150104025',    
    "password":'Student@666'
    }
    
    #opening request object
    with Search() as s:
        #posting user infomation in the login page
        dashboard=s.post(url,data=data)
        print("signed in...")

        #creating course link list
        print("creating a course list")
        #Scrapping the course links from the dashboard
        course_links=[course('a')[0].attrs["href"] for course in bs(dashboard.text,"html.parser").findAll("div",{"class":"box coursebox"})]
        #Scrapping the course names from the dashboard
        course_name=[course('a')[0].attrs["title"].split("_")[0] for course in bs(dashboard.text,"html.parser").findAll("div",{"class":"box coursebox"})]
        print("opening course links and running mega loop")

        import sys
        for directory in course_links:
            percentage=str(int(course_links.index(directory)/len(course_links)*100))
            sys.stderr.write("{}%".format(percentage))
            sys.stderr.write("\n")
            #opening the course links
            data = s.get(directory)

            #list of assignment_paths of a given subject "Newsfeed"
            Newsfeed=[link('a')[0].attrs['href'] for link in bs(data.text,"html.parser").findAll("div",{"class":"activityinstance"})]

            #moving up the directory
            Tuitorials=s.get(Newsfeed[0])

            #assignment path
            
            
            path=[link('a')[0].attrs['href'] for link in bs(Tuitorials.text,"html.parser").findAll('td',{'class':"topic starter"}) if bs(Tuitorials.text,"html.parser").findAll('td',{'class':"topic starter"})!=[] ]
            if(path!=[]):
                assignment_links=[]
                for link in path:
                    file=s.get(link)
                    if(bs(file.text,"html.parser").findAll("div",{"class":"attachments"})!= []):
                        #creating a link to the documents 
                        assignment_links.append(bs(file.text,"html.parser").findAll("div",{"class":"attachments"})[0]("a")[0].attrs["href"])
                    if(bs(file.text,"html.parser").findAll("div",{"class":"attachedimages"})[0]("img")!= []):
                        assignment_links.append(bs(file.text,"html.parser").findAll("div",{"class":"attachedimages"})[0]("img")[0].attrs["src"])
                Documents[course_name[course_links.index(directory)]]=assignment_links               

            else:
                Documents[course_name[course_links.index(directory)]]=[]
                        
                   
                
        print("downloading files...")

        #downloading and creating files
        done=0
        for key in Documents:
            done+=1
            percentage=str(int(done/len(Documents)*100))
            sys.stderr.write("{}%".format(percentage))
            sys.stderr.write("\n")
            if Documents[key]!=[]:
                lms="/app/LMS/"
                folder=lms+key
                import os
                if not os.path.exists(folder):
                    os.makedirs(folder)
                for link in Documents[key]:
                    file_name = folder+"/"+link.split('/')[-1].replace("%20"," ").replace("%28"," ").replace("%29"," ").replace("%2C","")
                    r = s.get(link, stream=True)
                    if not os.path.exists(file_name):
                        with open(file_name, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=102400): 
                                if chunk: # filter out keep-alive new chunks
                                    f.write(chunk)
                                    #f.flush() commented by recommendation from J.F.Sebastian
        print("done!!!!")
        return (Documents)

        
