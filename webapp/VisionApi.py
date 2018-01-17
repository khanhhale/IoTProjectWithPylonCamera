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

import argparse
import io
import json
import logging
from google.cloud import vision
from google.cloud.vision import types
from flask import jsonify
from Utility import *

class VisionApi(Utility):
  def __init__(self):
    """
    Description: 
       This contructor function initialize super class object and client service object for vision api
    Args: 
       None
    Returns:
       None
    """
    super(VisionApi,self).__init__()
    self.client = vision.ImageAnnotatorClient()

  def detect_faces(self,path):
    """
    Description: 
       Detects faces in an image.
    Args: 
       path: Path to local image file
    Returns:
       face dection json object
    """ 

    

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = self.client.face_detection(image=image)

    return response
   
  def detect_faces_str(self, content):
    """
    Description: 
       Detects faces in an image.
    Args: 
       content: content of file in byte string
    Returns:
       face dection json object
    """ 
    

    image = types.Image(content=content)

    response = self.client.face_detection(image=image)

    return response

  def detect_faces_uri(self,uri):
    """
    Description: 
       Detects faces in an image.
    Args: 
       uri: url to the image on the web
    Returns:
       face dection json object
    """ 
    
    image = types.Image()
    image.source.image_uri = uri

    response = self.client.face_detection(image=image)

    return response

  def detect_labels(self,path):
    """
    Description: 
       Detects labels in an image.
    Args: 
       path: path to local image
    Returns:
       label dection json object
    """ 
    

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = self.client.label_detection(image=image)

    return response

  def detect_labels_uri(self,uri):
    """
    Description: 
       Detects labels in an image.
    Args: 
       uri: url to an image on the Internet
    Returns:
       label dection json object
    """ 
    
    image = types.Image()
    image.source.image_uri = uri

    response = self.client.label_detection(image=image)
    return response

  def detect_landmarks(self,path):
    """
    Description: 
       Detects labels in an image.
    Args: 
       path: path to local image
    Returns:
       label dection json object
    """ 
    

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = self.client.landmark_detection(image=image)

    return response

  def detect_landmarks_uri(self,uri):
    """
    Description: 
       Detects landmarks in an image.
    Args: 
       uri: url to an image on the Internet
    Returns:
       landmarks dection json object
    """ 
    
    image = types.Image()
    image.source.image_uri = uri

    response = self.client.landmark_detection(image=image)

    return response

  def detect_logos(self,path):
    """
    Description: 
       Detects logos in an image.
    Args: 
       path: path to a local image
    Returns:
       logos dection json object
    """ 
    

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = self.client.logo_detection(image=image)

    return response

  def detect_logos_uri(self,uri):
    """
    Description: 
       Detects logos in an image.
    Args: 
       uri: url to an image on the Internet
    Returns:
       logos dection json object
    """ 
    
    image = types.Image()
    image.source.image_uri = uri

    response = self.client.logo_detection(image=image)

    return response

  def detect_safe_search(self,path):
    """
    Description: 
       Detects unsafe contents in an image.
    Args: 
       path: path to a local image
    Returns:
       unsafe search json object
    """ 
    

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = self.client.safe_search_detection(image=image)

    return response

  def detect_safe_search_uri(self,uri):
    """
    Description: 
       Detects unsafe contents in an image.
    Args: 
       uri: url to an image on the Internet
    Returns:
       unsafe search json object
    """
    
    image = types.Image()
    image.source.image_uri = uri

    response = self.client.safe_search_detection(image=image)

    return response

  def detect_text(self,path):
    """
    Description: 
       Detects and extracts text in an image.
    Args: 
       path: path to a local image
    Returns:
       text dection json object
    """ 
    

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = self.client.text_detection(image=image)
    return response

  def detect_text_uri(self,uri):
    """
    Description: 
       Detects and extracts text in an image.
    Args: 
       uri: url to an image on the Internet
    Returns:
       text dection json object
    """ 
    
    image = types.Image()
    image.source.image_uri = uri

    response = self.client.text_detection(image=image)

    return response

  def detect_properties(self,path):
    """
    Description: 
       Detects properties in an image.
    Args: 
       path: path to a local image
    Returns:
       detect properties json object
    """ 
    

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = self.client.image_properties(image=image)

    return response

  def detect_properties_uri(self,uri):
    """
    Description: 
       Detects properties in an image.
    Args: 
       uri: url to an image on the Internet
    Returns:
       detect properties json object
    """ 
    
    image = types.Image()
    image.source.image_uri = uri

    response = self.client.image_properties(image=image)

    return response

  def detect_web(self,path):
    """
    Description: 
       Detects web urls that are using the matching image in the request
    Args: 
       path: path to a local image
    Returns:
       web detection json object 
    """ 
    

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = self.client.web_detection(image=image)

    return response

  def detect_web_uri(self,uri):
    """
    Description: 
       Detects web urls that are using the matching image in the request
    Args: 
       uri: url to an image on the Internet
    Returns:
       web detection json object 
    """ 
    
    image = types.Image()
    image.source.image_uri = uri

    response = self.client.web_detection(image=image)

    return response

  def detect_crop_hints(self,path):
    """
    Description: 
       Detects crop hints in an image.
    Args: 
       path: path to a local image
    Returns:
       crop hints json object
    """
    

    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)

    crop_hints_params = types.CropHintsParams(aspect_ratios=[1.77])
    image_context = types.ImageContext(crop_hints_params=crop_hints_params)

    response = self.client.crop_hints(image=image, image_context=image_context)

    return response

  # [START   def_detect_crop_hints_uri]
  def detect_crop_hints_uri(self,uri):
    """
    Description: 
       Detects crop hints in an image.
    Args: 
       uri: url to an image on the Internet
    Returns:
       crop hints json object
    """
    
    image = types.Image()
    image.source.image_uri = uri

    crop_hints_params = types.CropHintsParams(aspect_ratios=[1.77])
    image_context = types.ImageContext(crop_hints_params=crop_hints_params)

    response = self.client.crop_hints(image=image, image_context=image_context)

    return response

  def detect_document(self,path):
    """
    Description: 
       Detects and extracts text in an image, but the text returned is optimized for dense text and documents.
       The response includes page, block, paragraph, word, and break information.
    Args: 
       path: path to a local image
    Returns:
       document text dection json object
    """ 
    

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = self.client.document_text_detection(image=image)
    
    return response

  def detect_document_uri(self,uri):
    """
    Description: 
       Detects and extracts text in an image, but the text returned is optimized for dense text and documents.
       The response includes page, block, paragraph, word, and break information.
    Args: 
       uri: url to an image on the Internet
    Returns:
       document text dection json object
    """ 
    
    image = types.Image()
    image.source.image_uri = uri

    response = self.client.document_text_detection(image=image)

    return response

