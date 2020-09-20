import serial
import time
import csv
import threading
from threading import Thread
from twilio.rest import Clients

account_sid = 'haha'
auth_token = 'haha'
client = Client(account_sid, auth_token)

ser = serial.Serial("COM8", 115200, timeout=None)
start=time.time()
start1=time.time()

recent=0

def get_data():
    start=time.time()
    while True:
        row=ser.readline().decode()[:-2].split(',')
        global recent
        recent=int(row[0])
        if time.time()-start>20:
            message = client.messages \
                .create(
                     body="Take a 20 second break and look at something 20 feet away!",
                     from_='+15017122661',
                     to='+18144943971'
                 )
            start=time.time()
        with open('datalog.csv', 'a') as f:
                w = csv.writer(f)
                w.writerow(row)

def analyze_data():
    high_count=0
    total=0
    count=0
    with open('datalog.csv') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            if len(row)!=0:  
                if float(row[0])>530:
                    high_count+=1
                count+=1
                total+=float(row[0])
                recent=float(row[0])
    return high_count,total/count,recent


try:   
    a=threading.Thread(target=get_data,args=())       
    a.start()
    while True:
        if time.time()-start1>60:
            start1=time.time()
            high_count,avg,recent=analyze_data()
            message = client.messages \
                .create(
                     body="Minutes of blue light exposure: "+str(high_count/60"+" "+Avg level of blue light exposure: "+str(+avg),
                     from_='+15017122661',
                     to='+18144943971'
                 )
            print("Minutes of blue light exposure: "+str(high_count/60))
            print("Avg level of blue light exposure: "+str(+avg))
            print("Most recent value: "+str(recent))


except KeyboardInterrupt:
    a.join()
    
