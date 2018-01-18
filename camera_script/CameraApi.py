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

from __future__ import absolute_import, print_function, division

import pypylon
import matplotlib.pyplot as plt
import numpy as np
import random, string, os, time, base64, io, logging, cStringIO
from Utility import *
from PIL import Image

APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 

class CameraApi(Utility):
  def __init__(self):
    """
    Description: 
       This contructor function initialize its parent class object
    Args: 
       None
    Returns:
       None
    """ 
    super(CameraApi,self).__init__()
  def image_resize(self, new_width, pilImage):
    """
    Description: 
       This function resize image with a new width passed in and a new height calculated from the new width.
    Args: 
       new_width: resize image to the new width
       pilImage: pil Image object
    Returns:
       pil Image object with new width and height
    """
    new_height = 300

    width,height = pilImage.size

    new_height = int(new_width * (height/width))

    pilImage = pilImage.resize((new_width,new_height), Image.ANTIALIAS)

    return pilImage

  def CaptureSingleShot(self, imageFormat="JPG"):
    """
    Description: 
       This function capture image, resize the image, and then save the image to memory buffer. The message sending through IoT devices must be less
       than 256 KB due to size limit being placed on IoT devices.
    Args: 
       None
    Returns:
       New image data in byte string
    """
    available_cameras = pypylon.factory.find_devices()

    cam = pypylon.factory.create_device(available_cameras[-1])

    cam.open()
    image_data = io.BytesIO()
    for image in cam.grab_images(1):
       image = self.image_resize(700, image)
       image.save(image_data, format=imageFormat, optimize=True, quality=85)
       next(cam.grab_images(1))
    return image_data

