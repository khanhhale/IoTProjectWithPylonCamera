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

from PIL import Image
import random, string, os, re

import logging
from logging.handlers import RotatingFileHandler

APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 

class Utility(object):
  def __init__(self):
    pass
  def generate_image_file(self, num, length, fileType="jpg"):
    """
    Description: 
       This function returns a random image file name.
    Args: 
       num: any number converted to string and added to the filename
       length: how long a file name is depends on the length and num arguments
       fileType: the file extension
    Returns:
       file name of an image
    """
    letters = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return 'image-' + ''.join( (random.choice(letters) + str(7 >> 1)) for i in range(length)) + str(num) + '.' + fileType
  def crop(self, imageData, coords, saved_location):
    """
    Description: 
       This function crop an image based on coordinates.
    Args: 
       imageData: image data in byte string
       coords: A tuple of x/y coordinates (x1, y1, x2, y2)
       saved_location: Path to save the cropped image
    Returns:
       None
    """
    image_obj = Image.open(imageData)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)
     
  def imageSearchPattern(self, imageFormat):
      """
      Description: 
       This function returns regular expression object based on image in four formats JPG, PNG and GIF.
      Args: 
       blobName: name of the blob
      Returns:
       On success: Search pattern object
       On failure: None
      """
      imageFormat = imageFormat.upper() 
      if(imageFormat.endswith("JPG")):
         return re.compile('^\/9j\/.+\/9k=$', re.M)
      elif(imageFormat.endswith("JPEG")):
         return re.compile('^\/9j\/.+\/9k=$', re.M)
      elif(imageFormat.endswith("GIF")):
         return re.compile('^R0lGODlh|R0lGODdh.+ADs=$', re.M)
      else:
         return None
     
  def logData(self, data):   
    """
      Description: 
       This function log information to the logfile within the log folder.
      Args: 
       data: data write to logfile
      Returns:
       None
    """
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
    logFile = os.path.join(APP_ROOT, "log", "logfile")
    fileHandler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=2, encoding=None, delay=0)
    fileHandler.setFormatter(log_formatter)
    fileHandler.setLevel(logging.INFO)

    app_log = logging.getLogger('applogger')
    app_log.setLevel(logging.INFO)

    app_log.addHandler(fileHandler)
    app_log.info(data)  
