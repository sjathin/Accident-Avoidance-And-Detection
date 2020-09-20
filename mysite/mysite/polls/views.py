from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import Template, Context

import json

#from api.models import reviews
#from api.models import tripInfo
#from api.models import vehicleInfo

import time
import sys
import serial

@csrf_exempt
def index(request):
   mobileno = ['+XXXXXXXXX']
   phone = serial.Serial()
   phone.port="COM5"
   phone.baudrate=9600
   phone.timeout=9
   phone.xonxoff = False
   phone.rtscts = False
   phone.bytesize = serial.EIGHTBITS
   phone.parity = serial.PARITY_NONE
   phone.stopbits = serial.STOPBITS_ONE
   recvSMS(phone)

def get_num(x):
   return str(''.join(ele for ele in x if ele.isdigit()))

def recept(message, recipient):
   time.sleep(0.5)
   phone.write('AT\r\n')
   time.sleep(0.5)
   phone.write('AT+CMGF=1\r\n')
   time.sleep(0.5)
   phone.write('AT+CMGS="'+recipient+'"\r\n')
   out = ''
   time.sleep(1)
   while phone.inWaiting() > 0:
      out += phone.read(1)
   if out != '':
      print (">>" + out)
   phone.write(message)
   phone.write('\x1a')
   out = ''
   time.sleep(1)
   while phone.inWaiting() > 0:
      out += phone.read(1)
   if out != '':
      print (">>" + out)
   number = get_num(out)
   #phone.write('AT+CMSS='+number+'\r\n')
   #out = ''
   #time.sleep(1)
   #while phone.inWaiting() > 0:
   #   out += phone.read(1)
   #if out != '':
   #   print ">>" + out

def sendSMS(message):
  try:
   phone.open()
   phone.flushInput()
   phone.flushOutput()
   for row in mobileno:
    time.sleep(0.5)
    mobile = row
    recept(message, mobile)
   time.sleep(1)
   #phone.write('AT+CMGD=1,4\r\n') DELETS SMS
   phone.close()
  finally:
   phone.close()

def recvSMS(phone):
    phone.open()
    phone.flushInput()
    phone.flushOutput()
    phone.write('AT+CMGF=1\r\n')
    out = ''
    time.sleep(1)
    while phone.inWaiting() > 0:
       out += phone.read(1)
    if out != '':
       print (">>" + out)
    phone.write('AT+CMGL="ALL"\r\n')
    out = ''
    time.sleep(1)
    while phone.inWaiting() > 0:
       out += phone.read(1)
    if out != '':
       print (">>")
    accident = out
    #print "string begin::---" + accident + "----end"
    arr = accident.split("\n")
    data = arr[2]
    data = data.split("|")
    carno = data[1]
    lat = data[3]
    longg = data[5]
    print ("CAR NO: " + str(carno) + "\n")
    print ("LATITIUDE: " + str(lat) + "\n")
    print ("LONGITUDE: " + str(longg) + "\n")
    phone.close()
    
    c = {'carno': carno, 'lat': lat, 'longg': longg}
    return render(request, 'polls/showInfo.html', c)

      
#message = "hi from gsm modem"


