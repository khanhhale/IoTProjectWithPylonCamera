// Utility_ImageLoadAndSave.cpp
/*
    Note: Before getting started, Basler recommends reading the Programmer's Guide topic
    in the pylon C++ API documentation that gets installed with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the Migration topic in the pylon C++ API documentation.

    This sample illustrates how to load and save images.

    The CImagePersistence class provides static functions for
    loading and saving images. It uses the image
    class related interfaces IImage and IReusableImage of pylon.

    IImage can be used to access image properties and image buffer.
    Therefore, it is used when saving images. In addition to that images can also
    be saved by passing an image buffer and the corresponding properties.

    The IReusableImage interface extends the IImage interface to be able to reuse
    the resources of the image to represent a different image. The IReusableImage
    interface is used when loading images.

    The CPylonImage and CPylonBitmapImage image classes implement the
    IReusableImage interface. These classes can therefore be used as targets
    for loading images.

    The gab result smart pointer classes provide a cast operator to the IImage
    interface. This makes it possible to pass a grab result directly to the
    function that saves images to disk.
*/

// Include files to use the PYLON API.
#include <pylon/PylonIncludes.h>
#include "SampleImageCreator.h"

namespace Utility
{
 class ImageUtilityApp {
   public:
   void LoadandSave();
   void SaveImage(); 
 };
}
