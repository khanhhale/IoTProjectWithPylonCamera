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
import random, string, re
import collections
from flask import jsonify

from googleapiclient import discovery
import dateutil.parser
import httplib2
from oauth2client.client import GoogleCredentials
from CloudApis import *
from VisionApi import *
from DataflowApi import *
from StorageApi import *
from ServiceApi import *
from google.protobuf.json_format import MessageToJson
from google.cloud import bigquery


APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 
NUM_RETRIES = 3
BATCH_SIZE = 100


app = Flask(__name__)
app.debug = False
app.config.from_object(__name__)
app.config.from_envvar("FLASKR_SETTINGS", silent=True)
app.static_folder = 'static'
app.template_folder = 'templates'
app.logger.setLevel(logging.INFO)
app.logger.setLevel(logging.DEBUG)


serviceApiObj = ServiceApi()
  
args = serviceApiObj.parse_command_line_args()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=args.credential  
 
credentials = serviceApiObj.get_credentials()
bigqueryClient = serviceApiObj.create_bigquery_client(credentials)
pubsubClient = serviceApiObj.create_pubsub_client(credentials)
cloudiotClient = serviceApiObj.create_cloudiot_client(credentials)
dataflowClient = serviceApiObj.create_dataflowapi_client(credentials)
storageClient = serviceApiObj.create_storageapi_client(credentials)
    
cloudApisObj = CloudApis()
visionApiObj = VisionApi()
dataflowApiObj = DataflowApi()
storageApisObj = StorageApi() 
  
@app.route('/')
def main():
    """
    Description: 
       This function serves the index.html page on the home page 
    Args: 
       None
    Returns:
       An html page
    """	
    return render_template("index.html")

@app.route('/storage/pull_message_from_storage')
def storage_pull_message_from_storage():
   """
    Description: 
       This function accept a request and parse the image file downloaded from the bucket and insert a record containing info on the person if it finds that there is a person in the image file.
    Args: 
       bucket_id : bucket id
       file_name : name of the file from the bucket including the prefix or blob name
       dataset_id : the id of the dataset from bigquery
       prefix : the name of the folder where the image file is stored in the bucket.
    Returns:
       On success: json object
       On failure: json object with error message
    Example: 
       http://0.0.0.0:80/storage/pull_message_from_storage?dataset_id=iot_bigdata_dataset1&table_id=table_image_info&bucket_id=dataflow-cloud-iot-testing-185623&file_name=camera/file.jpg&prefix=camera/
   """
   try:
      bucket_id = urllib.unquote(request.args.get("bucket_id")).decode('utf8')
      blob_name = urllib.unquote(request.args.get("file_name")).decode('utf8')
      dataset_id = urllib.unquote(request.args.get("dataset_id")).decode('utf8')
      table_id = urllib.unquote(request.args.get("table_id")).decode('utf8')
      prefix = urllib.unquote(request.args.get("prefix")).decode('utf8')
       
      blob = storageApisObj.download_blob(bucket_id, blob_name)
      messageJson = []
      if(blob != None):
            print("blob name:", blob.name)
            searchJpegPat = storageApisObj.imageSearchPattern("JPEG")
            searchGifPat = storageApisObj.imageSearchPattern("GIF")          
            jpegCollection = searchJpegPat.findall(blob.download_as_string().encode("utf-8"))
            gifCollection = searchGifPat.findall(blob.download_as_string().encode("utf-8"))
            if(jpegCollection == None and gifCollection == None):
              raise Exception("The file must have jpg or gif image")  
            image_collection = jpegCollection + jpegCollection
            for image in image_collection:
               image_data = image.decode('base64')
               image_buffer = io.BytesIO(image_data)
               image_buffer.seek(0)
               img_data = image_buffer.read().strip()
               response = visionApiObj.detect_faces_str(img_data)
               if(response):
                  faces = response.face_annotations
                  filePath = "gs://{}/{}".format(bucket_id, prefix)
                  fileName = blob.name[len(prefix):]
                  dateCreated = str(datetime.datetime.now())
                  dateDeleted = None
                  personDetected = True
                  row = {"fileName":fileName, "filePath": filePath, "dateCreated": dateCreated, "dateDeleted": dateDeleted, "personDetected": personDetected}
                  messageJson.append(row)
        
      if(messageJson != None and len(messageJson) > 0):
              cloudApisObj.Insert_to_bq(bigqueryClient, args.project_id, dataset_id, table_id, messageJson)

   except Exception as e:
      return jsonify(status ="failed with error", error_message=str(e))
   else:
      return jsonify(status ="success")

if __name__ == '__main__':
   app.run(host = '0.0.0.0', port=80)
