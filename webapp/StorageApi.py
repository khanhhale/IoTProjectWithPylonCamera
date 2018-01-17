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

from google.cloud import storage
import base64, io, os, random
from PIL import Image
import logging
from Utility import *

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

class StorageApi(Utility):
  def __init__(self):
    """
    Description: 
       This contructor function initialize super class object and client service object for storage
    Args: 
       None
    Returns:
       None
    """
    super(StorageApi,self).__init__()
    self.clientService = storage.Client()

  def getBlobList(self, bucket_id, prefix=None):
    """
    Description: 
       Returns a list of blobs
    Args: 
       bucket_id: bucket id
       prefix: prefix of a blob
    Returns:
       A list of blobs
    """ 
    bucket = self.clientService.get_bucket(bucket_id)
    blob_iter = bucket.list_blobs(delimiter='/', prefix=prefix)
    return blob_iter 

  def create_bucket(self,bucket_name):
    """
    Description: 
       This function create bucket
    Args: 
       bucket_name: bucket id
    Returns:
       created bucket
    """
    
    bucket = self.clientService.create_bucket(bucket_name)
    return bucket


  def delete_bucket(self,bucket_name):
    """
    Description: 
       This function delete bucket
    Args: 
       bucket_name: bucket id
    Returns:
       None
    """
    
    bucket = self.clientService.get_bucket(bucket_name)
    bucket.delete()

  def get_bucket_labels(self,bucket_name):
    """
    Description: 
       This function delete bucket
    Args: 
       bucket_name: bucket id
    Returns:
       None
    """
    
    bucket = self.clientService.get_bucket(bucket_name)
    labels = bucket.labels
    pprint.pprint(labels)


  def add_bucket_label(self,bucket_name):
    """
    Description: 
       Add a label to a bucket.
    Args: 
       bucket_name: bucket id
    Returns:
       None
    """
    bucket = self.clientService.get_bucket(bucket_name)

    labels = bucket.labels
    labels['example'] = 'label'
    bucket.labels = labels
    bucket.patch()

  def remove_bucket_label(self,bucket_name):
    """
    Description: 
       Remove a label from a bucket.
    Args: 
       bucket_name: bucket id
    Returns:
       None
    """
    bucket = self.clientService.get_bucket(bucket_name)

    labels = bucket.labels

    if 'example' in labels:
        del labels['example']

    bucket.labels = labels
    bucket.patch()

  def list_blobs(self,bucket_name):
    """
    Description: 
       Lists all the blobs in a bucket.
    Args: 
       bucket_name: bucket id
    Returns:
       A list of all the blobs in a bucket
    """
    bucket = self.clientService.get_bucket(bucket_name)

    blobs = bucket.list_blobs()

    for blob in blobs:
        print(blob.name)

    return blobs

  def list_blobs_with_prefix(self,bucket_name, prefix, delimiter=None):
    """
    Description: 
       Lists all the blobs in a bucket that begin with the prefix.
    Args: 
       bucket_name: bucket id
    Returns:
       A list of all the blobs in a bucket that begin with the prefix
    """
    bucket = self.clientService.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)

    print('Blobs:')
    for blob in blobs:
        print(blob.name)

    if delimiter:
        print('Prefixes:')
        for prefix in blobs.prefixes:
            print(prefix)

    return blobs

  def upload_blob(self,bucket_name, source_file_name, destination_blob_name):
    """
    Description: 
       Uploads a file to the bucket.
    Args: 
       bucket_name: bucket id
       source_file_name: file name to upload
       destination_blob_name: file name to be saved in the bucket
    Returns:
       None
    """
    bucket = self.clientService.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

  def download_blob(self,bucket_name, source_blob_name):
    """
    Description: 
       Downloads a blob from the bucket.
    Args: 
       bucket_name: bucket id
       source_file_name: file name to upload
    Returns:
       blob
    """
    bucket = self.clientService.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    return blob

  def download_blob_to_file(self,bucket_name, source_blob_name, destination_file_name):
    """
    Description: 
       Downloads a blob from the bucket and save to a local file.
    Args: 
       bucket_name: bucket id
       source_blob_name: name of blob in the bucket
       destination_file_name: path to local file
    Returns:
       none
    """
    bucket = self.clientService.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)


  def delete_blob(self,bucket_name, blob_name):
    """
    Description: 
       Deletes a blob from the bucket.
    Args: 
       bucket_name: bucket id
       blob_name: name of blob in the bucket
    Returns:
       none
    """
    bucket = self.clientService.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()


  def make_blob_public(self,bucket_name, blob_name):
    """
    Description: 
       Makes a blob publicly accessible
    Args: 
       bucket_name: bucket id
       blob_name: name of blob in the bucket
    Returns:
       none
    """
    bucket = self.clientService.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.make_public()

    print('Blob {} is publicly accessible at {}'.format(
        blob.name, blob.public_url))




