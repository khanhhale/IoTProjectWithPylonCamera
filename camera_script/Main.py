# Copyright 2017, Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse, os, logging, json, glob
import base64
import datetime
import time
import jwt
import requests, urllib
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import uuid
import random, string
import collections
from flask import jsonify
from threading import Event, Thread
from googleapiclient import discovery
import dateutil.parser
import httplib2
from oauth2client.client import GoogleCredentials
from CloudApis import *
from CameraApi import *
from ServiceApi import *
from Utility import *
from google.protobuf.json_format import MessageToJson
from google.cloud import bigquery
import sys, subprocess
reload(sys)
sys.setdefaultencoding('utf8')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

serviceApiObj = ServiceApi() 
args = serviceApiObj.parse_command_line_args()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=args.credential  
 
utilityObj = Utility()   
cloudApisObj = CloudApis()
cameraApiObj = CameraApi()

    
def publish_message():
   '''
    Description: 
       This function take an image and publish to the google cloud Pub/Sub.
    Args: 
       None
    Returns:
       None
    Raise:
       Throw an exception on failure
   '''   
   try:
       img_data = cameraApiObj.CaptureSingleShot("JPEG")
       img_data.seek(0)
       file_data = img_data.read().strip()
       cloudApisObj.publish_message_to_subpub(args.project_id, args.registry_id, args.device_id, args.message_type, args.base_url, args.cloud_region, args.algorithm, args.private_key_file, args.message_data_type, base64.b64encode(file_data))     
   except Exception, e:
       print e
   else:
       print("Image published")
       utilityObj.logData("Image published")

def setInterval(interval, callbackfunc):
   '''
     Description: 
       This function take an image and publish to the google cloud Pub/Sub.
     Args: 
       interval: interval in second between two publishing points
       callbackfunc: callback function
     Returns:
       None
     Raise:
       On Success: print "Image published" and publish image to Pub/Sub
       On failure: Throw an exception
   '''

   event_obj = Event()
   
   def loopFunc():
        while not event_obj.wait(interval):
            callbackfunc()
   Thread(target=loopFunc).start()    
   return event_obj.set

clearTime = setInterval(int(args.send_message_interval), publish_message)
