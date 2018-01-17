from libcpp cimport bool
from libc.stdint cimport uint32_t, uint64_t, int64_t
from libcpp.string cimport string

cdef extern from "Base/GCBase.h":
    cdef cppclass gcstring:
        gcstring()
        gcstring(char*)

cdef extern from "GenApi/GenApi.h" namespace 'GenApi':

    cdef cppclass INode:
        gcstring GetName(bool FullQualified=False)
        gcstring GetNameSpace()
        gcstring GetDescription()
        gcstring GetDisplayName()
        bool IsFeature()
        gcstring GetValue()

    # Types an INode could be
    cdef cppclass IValue:
        gcstring ToString()
        void FromString(gcstring, bool verify=True) except +

    cdef cppclass IBoolean:
        bool GetValue()
        void SetValue(bool) except +

    cdef cppclass IInteger:
        int64_t GetValue()
        void SetValue(int64_t) except +
        int64_t GetMin()
        int64_t GetMax()

    cdef cppclass IString
    cdef cppclass IFloat:
        double GetValue()
        void SetValue(double) except +
        double GetMin()
        double GetMax()

    cdef cppclass NodeList_t:
        cppclass iterator:
            INode* operator*()
            iterator operator++()
            bint operator==(iterator)
            bint operator!=(iterator)
        NodeList_t()
        CDeviceInfo& operator[](int)
        CDeviceInfo& at(int)
        iterator begin()
        iterator end()

    cdef cppclass ICategory

    cdef cppclass INodeMap:
        void GetNodes(NodeList_t&)
        INode* GetNode(gcstring& )
        uint32_t GetNumNodes()

cdef extern from *:
    IValue* dynamic_cast_ivalue_ptr "dynamic_cast<GenApi::IValue*>" (INode*) except +
    IBoolean* dynamic_cast_iboolean_ptr "dynamic_cast<GenApi::IBoolean*>" (INode*) except +
    IInteger* dynamic_cast_iinteger_ptr "dynamic_cast<GenApi::IInteger*>" (INode*) except +
    IFloat* dynamic_cast_ifloat_ptr "dynamic_cast<GenApi::IFloat*>" (INode*) except +
    INodeMap* dynamic_cast_inodemap_ptr "dynamic_cast<GenApi::INodeMap*>" (INode*) except +
    INodeMap* dynamic_cast_inodemap_ptr "dynamic_cast<GenApi::INodeMap*>" (INode*) except +
    ICategory* dynamic_cast_icategory_ptr "dynamic_cast<GenApi::ICategory*>" (INode*) except +

    bool node_is_readable "GenApi::IsReadable" (INode*) except +
    bool node_is_writable "GenApi::IsWritable" (INode*) except +
    bool node_is_implemented "GenApi::IsImplemented" (INode*) except +

cdef extern from "pylon/PylonIncludes.h" namespace 'Pylon':

    # ctypedef gcstring String_t

    # Common special data types
    cdef cppclass String_t
    cdef cppclass StringList_t

    # Top level init functions
    void PylonInitialize() except +
    void PylonTerminate() except +

    cpdef enum EPixelType:
        PixelType_Mono1packed,
        PixelType_Mono2packed,
        PixelType_Mono4packed,
        PixelType_Mono8,
        PixelType_Mono8signed,
        PixelType_Mono10,       
        PixelType_Mono10packed,
        PixelType_Mono10p,  
        PixelType_Mono12,
        PixelType_Mono12packed,
        PixelType_Mono12p,
        PixelType_Mono16,
        PixelType_BayerGR8,
        PixelType_BayerRG8,
        PixelType_BayerGB8,
        PixelType_BayerBG8,
        PixelType_BayerGR10,
        PixelType_BayerRG10,
        PixelType_BayerGB10,
        PixelType_BayerBG10,
        PixelType_BayerGR12,
        PixelType_BayerRG12,
        PixelType_BayerGB12,
        PixelType_BayerBG12,
        PixelType_RGB8packed,
        PixelType_BGR8packed,
        PixelType_RGBA8packed,
        PixelType_BGRA8packed,
        PixelType_RGB10packed,
        PixelType_BGR10packed,
        PixelType_RGB12packed,
        PixelType_BGR12packed,
        PixelType_RGB16packed,
        PixelType_BGR10V1packed,
        PixelType_BGR10V2packed,
        PixelType_YUV411packed,
        PixelType_YUV422packed,
        PixelType_YUV444packed,
        PixelType_RGB8planar,
        PixelType_RGB10planar,
        PixelType_RGB12planar,
        PixelType_RGB16planar,
        PixelType_YUV422_YUYV_Packed,
        PixelType_BayerGR12Packed,
        PixelType_BayerRG12Packed,
        PixelType_BayerGB12Packed,
        PixelType_BayerBG12Packed,
        PixelType_BayerGR10p,
        PixelType_BayerRG10p,
        PixelType_BayerGB10p,
        PixelType_BayerBG10p,
        PixelType_BayerGR12p,
        PixelType_BayerRG12p,
        PixelType_BayerGB12p,
        PixelType_BayerBG12p,
        PixelType_BayerGR16,  
        PixelType_BayerRG16,   
        PixelType_BayerGB16,  
        PixelType_BayerBG16,  
        PixelType_RGB12V1packed
    
    cpdef enum EImageOrientation:
        ImageOrientation_TopDown,
        ImageOrientation_BottomUp

    cpdef enum EImageFileFormat:
        ImageFileFormat_Bmp = 0,
        ImageFileFormat_Tiff = 1,
        ImageFileFormat_Jpeg = 2,
        ImageFileFormat_Png = 3,
        ImageFileFormat_Raw = 4
         
    cdef cppclass CImagePersistenceOptions:
        CImagePersistenceOptions()
        void SetQuality(int quality)

    cpdef cppclass CImagePersistence:
        @staticmethod 
        void Save(EImageFileFormat imageFileFormat, String_t& filename, const IImage& image, CImagePersistenceOptions* pOptions = NULL)  except +
        @staticmethod
        void Load(const String_t& filename, IReusableImage& image)  except +

    cdef cppclass IImage:
        uint32_t GetWidth()
        uint32_t GetHeight()
        size_t GetPaddingX()
        size_t GetImageSize()
        void* GetBuffer()
        bool IsValid()
        EPixelType GetPixelType()

    cdef cppclass CGrabResultData:
        bool GrabSucceeded()

    cdef cppclass CGrabResultPtr:
        IImage& operator()
        #CGrabResultData* operator->()


    cdef cppclass IPylonDevice:
        pass

    cdef cppclass CDeviceInfo:
        String_t GetSerialNumber() except +
        String_t GetUserDefinedName() except +
        String_t GetModelName() except +
        String_t GetDeviceVersion() except +
        String_t GetFriendlyName() except +
        String_t GetVendorName() except +
        String_t GetDeviceClass() except +

    cdef cppclass CInstantCamera:
        CInstantCamera()
        void Attach(IPylonDevice*)
        CDeviceInfo& GetDeviceInfo() except +
        void IsCameraDeviceRemoved()
        void Open() except +
        void Close() except +
        bool IsOpen() except +
        IPylonDevice* DetachDevice() except +
        void StartGrabbing(size_t maxImages) except +    #FIXME: implement different strategies
        bool IsGrabbing()
        # RetrieveResult() is blocking call into C++ native SDK, allow it to be called without GIL
        bool RetrieveResult(unsigned int timeout_ms, CGrabResultPtr& grab_result) nogil except + # FIXME: Timout handling
        INodeMap& GetNodeMap()

    cdef cppclass DeviceInfoList_t:
        cppclass iterator:
            CDeviceInfo operator*()
            iterator operator++()
            bint operator==(iterator)
            bint operator!=(iterator)
        DeviceInfoList_t()
        CDeviceInfo& operator[](int)
        CDeviceInfo& at(int)
        iterator begin()
        iterator end()

    cdef cppclass CTlFactory:
        int EnumerateDevices(DeviceInfoList_t&, bool add_to_list=False)
        IPylonDevice* CreateDevice(CDeviceInfo&)

# Hack to define a static member function
cdef extern from "pylon/PylonIncludes.h"  namespace 'Pylon::CTlFactory':
    CTlFactory& GetInstance()

# HACK: We cannot dereference officially with the -> operator. So we use ugly macros...
cdef extern from 'hacks.h':
    bool ACCESS_CGrabResultPtr_GrabSucceeded(CGrabResultPtr ptr)
    String_t ACCESS_CGrabResultPtr_GetErrorDescription(CGrabResultPtr ptr)
    uint32_t ACCESS_CGrabResultPtr_GetErrorCode(CGrabResultPtr ptr)

cdef extern from "pylon/_ImageFormatConverterParams.h" namespace 'Basler_ImageFormatConverterParams':
    cppclass CImageFormatConverterParams_Params:
        pass
	
cdef extern from "pylon/ImageFormatConverter.h" namespace 'Pylon':
    cdef cppclass IReusableImage(IImage):
        IReusableImage()
        void Reset(EPixelType pixelType, uint32_t width, uint32_t height, EImageOrientation orientation = ImageOrientation_TopDown)

    cdef cppclass CPylonImageBase(IReusableImage):
        void Save(EImageFileFormat imageFileFormat, String_t& filename, CImagePersistenceOptions* pOptions = NULL)

    cdef cppclass CImageFormatConverter(CImageFormatConverterParams_Params):
        CImageFormatConverter() except+
        void Save(EImageFileFormat imageFileFormat, string filename, CImagePersistenceOptions* pOptions = NULL)
        void Initialize(EPixelType sourcePixelType) except+
        void Convert(IReusableImage& destinationImage, IImage& sourceImage) except+
        cppclass IOutputPixelFormatEnum:
             void SetValue( EPixelType outputPixelType)  except+
        IOutputPixelFormatEnum& OutputPixelFormat;   

cdef extern from "pylon/PylonImage.h" namespace "Pylon":
    cdef cppclass CPylonImage(CPylonImageBase):
        CPylonImage()
        void *GetBuffer() except+
        size_t GetImageSize() except+
        uint32_t GetWidth() except+
        uint32_t GetHeight() except+
        EPixelType GetPixelType() except+
        void CopyImage(const IImage& image)

cdef extern from "ImageUtilityApp.h" namespace "Utility":
    cdef cppclass ImageUtilityApp:
        void LoadandSave()
        void SaveImage()

