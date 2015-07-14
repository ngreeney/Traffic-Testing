# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 13:42:36 2015

@author: ngreeney
"""
import numpy as np

import simplejson as json
import urllib2 as url
import mysql.connector
from datetime import datetime
import time

#Google API key
apiKey = "AIzaSyCDdvTmvvbRjnlycDcgQ-TVgW_lIad7Qbk"
#Locations
origin = "Dinosaur+Parking+Lots,+U.S.+40,+Golden,+CO"
destinations = np.array(["Breckenridge,+CO","Vail,+CO","Beaver+Creek,+CO",
                         "12121+Grant+St,+Thornton,+CO+80241",
                         "Rocky+Mountain+MS+Center"])
#MySQL connection
sql = mysql.connector.connect(user="admin",password="admin01",
                              host="sv-oryx",database="driving")
cursor = sql.cursor()


temp = "0"
while (4 <= datetime.now().hour < 10) or (14 <= datetime.now().hour < 17) :
    if temp == "0": temp = origin
    #Loop for pulling and logging data
    timeNow = datetime.now()
    
    for dest in destinations:
        if timeNow.hour > 14:
            origin = dest
            dest = temp
        dirURL = "https://maps.googleapis.com/maps/api/directions/json?key=" + \
                    apiKey + \
                    "&origin=" + origin + \
                    "&destination=" + dest
        jURL = url.urlopen(dirURL)
        data = json.load(jURL)
        #pull only duration
        duration = data['routes'][0]['legs'][0]['duration']['value']
        print "Duration of ",duration/60/60.," hours at ",timeNow
        timeData = {
            "startLoc": origin.replace("+"," "),
            "endLoc":dest.replace("+"," "),
            "duration":duration,
            "startTime":timeNow
        }
        #add to database
        add_times = ("INSERT INTO times "
                "(startLoc,endLoc,duration,startTime) "
                "VALUES (%(startLoc)s, %(endLoc)s, %(duration)s, %(startTime)s)")
        cursor.execute(add_times,timeData)
        
    sql.commit()
    
    time.sleep(60.*5)#wait 5 min before next check



#close connection
cursor.close()
sql.close()