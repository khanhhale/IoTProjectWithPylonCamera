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

import io
import json
import logging
from Utility import *

class DataflowApi(Utility):
  def __init__(self):
    """
    Description: 
       This contructor function initialize super class object
    Args: 
       None
    Returns:
       None
    """
    super(DataflowApi,self).__init__()

  def create_dataflow_job_PubSub_to_GCS(self, client, PROJECT, JOBNAME, BUCKET, topic, table):
    """
    Description: 
       create a dataflow job
    Args: 
       client: client service object
       PROJECT: project id
       JOBNAME: name of dataflow job
       topic: full path to topic name. Ex: projects/cloud-iot-testing-185623/topics/cloud-iot-topic1
       table: full path to a table name. Ex: projectid:datasetid.tableid
    Returns:
       On success: a json object
       On failure: None or an exception will be thrown.
    Raises:
       An exception if the subscription cannot be created.
    """ 
    GCSPATH = "gs://dataflow-templates/latest/Cloud_PubSub_to_GCS_Text"
    BODY = {
        "jobName": "{jobname}".format(jobname=JOBNAME),
        "parameters": {
             "inputTopic": topic,
             "outputDirectory": "gs://{bucket}/camera/".format(bucket=BUCKET),
             "outputFilenamePrefix": "output-",
             "outputFilenameSuffix": ".txt",
         },
         "environment": {
            "tempLocation": "gs://{bucket}/tmp".format(bucket=BUCKET),
            "zone": "us-central1-f"
         }
    }


    try:
        request = client.projects().templates().launch(projectId=PROJECT, gcsPath=GCSPATH, body=BODY)
        response = request.execute()
        return response
    except Exception as e:
        print "Exception: %s, cannot publish message" % e
        raise


