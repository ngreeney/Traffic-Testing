# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 12:50:09 2015

@author: ngreeney
"""

import numpy as np
import matplotlib.pyplot as plt

import mysql.connector
from datetime import datetime
import time

#connect to database
sql = mysql.connector.connect(user="admin",password="admin01",
                              host="sv-oryx",database="driving")
cursor = sql.cursor()
#locations
origin = "Dinosaur+Parking+Lots,+U.S.+40,+Golden,+CO"
destinations = np.array(["Breckenridge,+CO","Vail,+CO","Beaver+Creek,+CO"])

for dest in destinations:
#    for day in xrange(0,7):
        locVars = (
            dest.replace("+"," "),
#            day
        )
        #pull from database
#        selectLine = ("SELECT round(time_to_sec(startTime)/(10*60)) as timekey, "
#                    "avg(duration) from times "
#                    "where hour(startTime) between 5 and 12 "
#                    "and endLoc = %s "
#                    "and weekday(startTime) = %s "
#                    "group by timekey")
        selectLine = ("select startTime, avg(duration) from times "
                     "where hour(startTime) between 4 and 12 "
                     "and endLoc = %s "
#                     "and weekday(startTime) = %s "
                     "group by startTime;")
        cursor.execute(selectLine,locVars)
        data = np.array(cursor.fetchall())
        data = data.transpose()
        
        try:
            print "day ",day
            plt.plot(data[0],data[1]/60-60,label=dest[:-4])#+" "+np.str(day))
        except Exception,e:
            print np.str(e)

plt.legend()
print cursor.column_names
cursor.close()
sql.close()