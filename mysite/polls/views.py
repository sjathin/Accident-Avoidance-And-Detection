from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import Template, Context

import sys, traceback
import json, urllib2
from math import radians, cos, sin, asin, sqrt

import time
import sys
import serial

#traffic = {}
#tra = 0

hospitals = {}
hos = 0
message = ''

hospitals[0]=["RDFSDFSFSDFDSFDSFDSFDFSDF",99.9999, 99.9999,"+XXXXX"]
hospitals[1]=["SFSDDFSDDSFDSDSFDS",99.999999, 77.99999,"+XX"]
hospitals[2]=["SDFSDFDSFSDFSDFDSFSF",9999.99999, 999.999999,"+XXX"]
hospitals[3]=["SFSDFSDFDSFDSFSD",99.934850, 99.584247,"+XXXX"]
hospitals[4]=["ASDFSDFDSFDSFDSFSDFS",99.9999, 9999.9999,"+XXXX"]
hospitals[21]=["SDFDSFDSFDSFDSFS",99.9999, 999.9999,"+XXXXXX"]
hospitals[6]=["SDFSDFSDSDFSDFSDFDSFDS",99.9999, 99.9999,"+XXX"]
hospitals[7]=["SDFSDFDSFSDFDSFSDF",99.9999, 99.9999,"+XXXXXXX"]
hospitals[8]=["SDFSDFDSFFSDSFDSF",99.9999, 9999.9999,'+XXXXXX']


@csrf_exempt

def index(request):
   '''phone = serial.Serial()
   phone.port="COM8"
   phone.baudrate=9600
   phone.timeout=9
   phone.xonxoff = False
   phone.rtscts = False
   phone.bytesize = serial.EIGHTBITS
   phone.parity = serial.PARITY_NONE
   phone.stopbits = serial.STOPBITS_ONE'''
   c = recvSMS()
   t = loader.get_template('polls/showInfo.html')
   return render(request, 'polls/showInfo.html', c)


def get_num(x):
   return str(''.join(ele for ele in x if ele.isdigit()))


def sendSMS(message,hos):
    recipient = hospitals[hos][3]
    sphone = serial.Serial()
    sphone.port="COM8"
    sphone.baudrate=9600
    sphone.timeout=9
    sphone.xonxoff = False
    sphone.rtscts = False
    sphone.bytesize = serial.EIGHTBITS
    sphone.parity = serial.PARITY_NONE
    sphone.stopbits = serial.STOPBITS_ONE
    sphone.open()
    sphone.flushInput()
    sphone.flushOutput()
    try:
        time.sleep(0.5)
        sphone.write('ATZ\r')
        time.sleep(0.5)
        sphone.write('AT+CMGF=1\r')
        time.sleep(0.5)
        sphone.write('''AT+CMGS="''' + recipient + '''"\r''')
        time.sleep(0.5)
        sphone.write(message + "\x1A")
        time.sleep(0.5)
        sphone.write(chr(26))
        time.sleep(0.5)
    finally:
        sphone.close()



def recvSMS():
   #phone.open()
   #phone.flushInput()
   #phone.flushOutput()
   #phone.write('AT+CNMI=2,1,0,0,0\r\n')
   #phone.write('AT+CMGF=1\r\n')
   #out = ''
   #time.sleep(1)
   #while phone.inWaiting() > 0:
   #   out += phone.read(1)
   #if out != '':
   #   print (">>" + out)
   #phone.write('AT+CMGL="ALL"\r\n')
   #out = ''
   #time.sleep(1)
   #while phone.inWaiting() > 0:
   #   out += phone.read(1)
   #if out != '':
   #   print (">>")
   #accident = out
   #chck = out
   #chck = chck.split("\n")
   #print len(chck);
   #phone.write('AT+CMGD=1\r\n')
   #time.sleep(2);
   #if len(chck) <= 4:
    #  return {'carno': "NO ACCIDENT", 'lat': "0", 'longg': "0",'hospital_name':"NA",'addr':"NA"}
   #else:
      #arr = accident.split("\n")
      #data = arr[3] # SIM900A
      #data = arr[2] SIM 808
      #data = data.split("!") # SIM900A
      #data = data.split("|") SIM808
      carno = "XXXXXXXX"
      #carno = carno[1:14]
      # lat = float(data[3]) SIM808
      # longg = float(data[5]) SIM808
      lat = "XXXXXXXX" #SIM900A
      #lat = lat[1:10] # SIM900A
      #lat = float(lat) #SIM900A
      longg = "XXXXXXX" #SIM900A
      #longg = longg[1:10] #SIM 900A
      #longg = float(longg) #SIM900A
      # ta = data[6]
      # if(ta == 'A')
      #
      print ("CAR NO: " + str(carno) + "\n")
      print ("LATITIUDE: " + str(lat) + "\n")
      print ("LONGITUDE: " + str(longg) + "\n")
      #phone.close()
      print "Distance of hospitals from accident location:\n"
      min_dist = drivingDistance(lat,longg,hospitals[0][1],hospitals[0][2])
      hos = 0
      #print "check" + str(min_dist)
      for i in range(22):
         if min_dist > (drivingDistance(lat,longg,hospitals[i][1],hospitals[i][2])):
            min_dist = drivingDistance(lat,longg,hospitals[i][1],hospitals[i][2])
            hos = i
         print str(hospitals[i][0]) + ":" + str(drivingDistance(lat,longg,hospitals[i][1],hospitals[i][2]))
      print "\n"
      print "Send the ambulance from:"
      print hospitals[hos][0]
      message = "Send an ambulance to this location:" + str(latlng_to_addr(lat,longg)) + "\n" + str("CAR NO:") + carno + str(" ")
      #sendSMS(message,hos)
      return {'carno': carno, 'lat': lat, 'longg': longg,'hospital_name':hospitals[hos][0],'addr':latlng_to_addr(lat,longg)}
      #end
      #else
      #print ("CAR NO: " + str(carno) + "\n")
      #print ("LATITIUDE: " + str(lat) + "\n")
      #print ("LONGITUDE: " + str(longg) + "\n")
      #phone.close()
      #print "Distance of hospitals from accident location:\n"
      #tramin_dist = drivingDistance(lat,longg,traffic[0][1],traffic[0][2])
      #tra = 0
      #print "check" + str(tramin_dist)
      #for i in range(22):
      #   if min_dist > (drivingDistance(lat,longg,traffic[i][1],traffic[i][2])):
      #      min_dist = drivingDistance(lat,longg,traffic[i][1],traffic[i][2])
      #      tra = i
      #   print str(traffic[i][0]) + ":" + str(drivingDistance(lat,longg,traffic[i][1],traffic[i][2]))
      #print "\n"
      #print "Send the police from:"
      #print traffic[tra][0]
      #message = "Send an policeman to this location:" + str(latlng_to_addr(lat,longg)) + "\n" + str("CAR NO:") + carno + str(" ")
      #sendSMS(message,tra)
      #return {'carno': carno, 'lat': lat, 'longg': longg,'hospital_name':trafic[tra][0],'addr':latlng_to_addr(lat,longg)}
   






#Calculate the great circle distance between two points 
#on the earth (specified in decimal degrees)    
def haversine(lon1, lat1, lon2, lat2):
   # convert decimal degrees to radians 
   lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
   # haversine formula 
   dlon = lon2 - lon1 
   dlat = lat2 - lat1 
   a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
   c = 2 * asin(sqrt(a)) 
   km = 6367 * c
   return km


def drivingDistance(lat1,lng1,lat2,lng2):
  url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s,%s&destinations=%s,%s&mode=driving&language=en-EL' % (lat1,lng1,lat2,lng2)
  res_json = json.loads(urllib2.urlopen(url).read())
  #print "origin address:" + str(res_json["origin_addresses"][0])
  #print "dest address:" + str(res_json["destination_addresses"][0])
  #print "Distance:" + str(res_json["rows"][0]["elements"][0]["distance"]["text"])
  #print "ETA:" + str(res_json["rows"][0]["elements"][0]["duration"]["text"])
  dis = res_json["rows"][0]["elements"][0]["distance"]["text"]
  dis = dis.split(" ")
  return float(dis[0])


'''convert given latitude & longitude to formatted address with Google Maps API
ref: http://techslides.com/convert-latitude-and-longitude-to-a-street-address/ '''
def latlng_to_addr (lat, lng):
   maps_api_url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=false' % (lat, lng)
   try:
      resp_json = json.loads(urllib2.urlopen(maps_api_url).read())
      fmt_addr = resp_json["results"][0]["formatted_address"]
      return fmt_addr
   except:
      traceback.print_exc(file=sys.stderr)
