from time import sleep
import RPi.GPIO as GPIO
from gpiozero import Button
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import pymssql


"""
server = "10"
#di=10.239.9.45 , machine=.128
user = "b"
password = "sunday.12"
DB = "OTGAZ"
"""

"""
server = 
#d=10.23
password = "78"
DB = "OTGAZ"
"""

#conn = pymssql.connect('10','','','')
conn = pymssql.connect('1','phytest','789456','OTGAZ')
#conn = pyodbc.connect('10','phytest','789456','OTGAZ')
print("open conn after")
cursor = conn.cursor()
cursor.execute('Select * From NaturalGasCounterDatas')
for row in cursor:
    #print(row['id'])
    print(row[0])
conn.close

smtp_server="smtp.gmail.com"
port=587
sender_email="@gmail.com"
receiver_email=["@gmail.com"]
password="zffff"

message=MIMEMultipart()
message["From"]="@gmail.com"
message["To"]=",".join(receiver_email)
message["Subject"]="Doğalgaz Sensörü"

text="Alarm,Gaz iletimi Yok!!!!!"
body_text=MIMEText(text,"plain")
message.attach(body_text)
delayTime=0
GPIO.setwarnings (False)
GPIO.setmode (GPIO.BOARD)
Button=12
GPIO.setup(Button,GPIO.IN,pull_up_down=GPIO.PUD_UP)
count=0
time_diff=0
downtime=time.time()
butt_press=0
LastSqlTime=0
file=open("Counter.txt","w+")
Input_Stop=True
while True:
    #print(GPIO.input(Button))
    #5 dakikada bir sqle data at
    
    #end of 5 dakikada bir sqle data at

    #15 dakika gaz gelmezse mail at
    if(GPIO.input(Button)==GPIO.LOW and (time.time()-butt_press)>1):
        count=count+1
        file.write(str(count)+"\n")
        file.flush()
        print("MetreKüp:",count)
        downtime=time.time()
        butt_press=time.time()
        Input_Stop=True
    else:
        time_diff=time.time()-downtime
        if (time_diff>(60*15) and Input_Stop):
            #MAIL AT
            print("hop burdayım")
            try:
                server=smtplib.SMTP(smtp_server,port)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(sender_email,password)
                server.sendmail("@gmail.com",receiver_email,message.as_string())
                print("Sistemin durduğu bilgisi gönderildi!!")
                Input_Stop=False
                downtime=time.time()
            
            
              
            
            except:
                print("Mail gönderilemiyor")
                downtime=time.time()
                #end of 15 dakika gaz gelmezse mail at
                

            
            #do something
    #sleep(0.5)
    #print(time_diff)
            
        
        
        
   
   
   
       
        


