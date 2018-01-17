request = require("request");

// This is a request option
// Please change the url, prefix, bucket_id, dataset_id and table_id to yours.
var options = {
  url: 'http://ip_or_hostname/storage/pull_message_from_storage',
  headers: {
    'User-Agent': 'request'
  },
  qs: {'file_name':'na', 'prefix':'camera/', 'bucket_id':'dataflow-cloud-iot-testing-185623', 'dataset_id':'iot_bigdata_dataset1', 'table_id':'table_image_info'}
};

//
//    Description: 
//       This function that receives a response and use this response to check for for communication status or parse response data.
//   Args: 
//       response: response object
//       body: contains data returns
//       error: error object that comes back from the request if there is an error.
//    Returns:
//       None
 
function callback(error, response, body) {
  if (!error && response.statusCode == 200) {
    var info = JSON.parse(body);
    console.log(info);
  }
}
//
//    Description: 
//       This function capture image, resize the image, and then save the image to memory buffer.
//   Args: 
//       event: an event object
//       callback: a callback function
//    Returns:
//      New image data in byte string
 
exports.pullImagesFromPubsub = function (event, callback) {
  const file = event.data;

  if (file.resourceState === 'not_exists') {
    console.log('File ${file.name} deleted.');
  } else if (file.metageneration === '1') {
    options.qs['file_name'] = file.name;
    request(options, callback);
    // metageneration attribute is updated on metadata changes.
    // on create value is 1
    console.log('File ${file.name} uploaded.');
  } else {
    console.log('File ${file.name} metadata updated.');
  }

};
