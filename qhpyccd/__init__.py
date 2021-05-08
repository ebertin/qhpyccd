"""
Simplified Python wrapper for the QHYCCD cameras.
(c) 2021 E.Bertin IAP/CNRS/SorbonneU
"""
from _qhpyccd_cffi import ffi, lib
import numpy as np
import sys

CONTROL_CODES = (
('CONTROL_BRIGHTNESS', 0, 'Image brightness'),
('CONTROL_CONTRAST', 1, 'Image contrast'),
('CONTROL_WBR', 2, 'Red of white balance'),
('CONTROL_WBB', 3, 'Blue of white balance'),
('CONTROL_WBG', 4, 'Green of white balance'),
('CONTROL_GAMMA', 5, 'Screen gamma'),
('CONTROL_GAIN',  6, 'Detector gain'),
('CONTROL_OFFSET', 7, 'Detector offset'),
('CONTROL_EXPOSURE', 8, 'Exposure time (us)'),
('CONTROL_SPEED', 9, 'Transfer speed'),
('CONTROL_TRANSFERBIT', 10, 'Image bit depth'),
('CONTROL_CHANNELS', 11, 'Number of image channels'),
('CONTROL_USBTRAFFIC', 12, 'USB traffic parameter'),
('CONTROL_ROWNOISERE', 13, 'Row noise reduction'),
('CONTROL_CURTEMP', 14, 'Current detector temprature'),
('CONTROL_CURPWM', 15, 'Current cooling power'),
('CONTROL_MANULPWM', 16, 'Cooling power adjustment'),
('CONTROL_CFWPORT', 17,  'Color filter wheel port'),
('CONTROL_COOLER', 18, 'Cooler'),
('CONTROL_ST4PORT', 19, 'ST4 port'),
('CAM_COLOR', 20, 'Color feature'),
('CAM_BIN1X1MODE', 21, '1x1 binning mode'),
('CAM_BIN2X2MODE', 22, '2x2 binning mode'),
('CAM_BIN3X3MODE', 23, '3x3 binning mode'),
('CAM_BIN4X4MODE', 24, '4x4 binning mode'),
('CAM_MECHANICALSHUTTER', 25, 'Mechanical shutter'),
('CAM_TRIGER_INTERFACE', 26, 'Trigger interface'),
('CAM_TECOVERPROTECT_INTERFACE', 27, 'TEC overprotection'),
('CAM_SINGNALCLAMP_INTERFACE', 28, 'Signal clamp'),
('CAM_FINETONE_INTERFACE', 29, 'Fine tone'),
('CAM_SHUTTERMOTORHEATING_INTERFACE', 30, 'Shutter motor heating'),
('CAM_CALIBRATEFPN_INTERFACE', 31, 'Calibrated frame'),
('CAM_CHIPTEMPERATURESENSOR_INTERFACE', 32, 'Chip temperature sensor'),
('CAM_USBREADOUTSLOWEST_INTERFACE', 33, 'USB readout slowest'),
('CAM_8BITS', 34, '8-bit depth'),
('CAM_16BITS', 35, '16-bit depth'),
('CAM_GPS', 36, 'GPS'),
('CAM_IGNOREOVERSCAN_INTERFACE', 37, 'Ignore overscan area'),
('QHYCCD_3A_AUTOBALANCE', 38, 'Auto white balance'),
('QHYCCD_3A_AUTOEXPOSURE', 39, 'Auto exposure time'),
('QHYCCD_3A_AUTOFOCUS', 40, 'Autofocus'),
('CONTROL_AMPV', 41, 'Detector ampv'),
('CONTROL_VCAM', 42, 'Virtual Camera switch'),
('CAM_VIEW_MODE', 43, 'View mode'),
('CONTROL_CFWSLOTSNUM', 44, 'CFW slots number'),
('IS_EXPOSING_DONE', 45, 'Exposure complete flag'),
('ScreenStretchB', 46, 'Screen stretch B'),
('ScreenStretchW', 47, 'Screen stretch W'),
('CONTROL_DDR', 48, 'DDR'),
('CAM_LIGHT_PERFORMANCE_MODE', 49, 'Light performance mode'),
('CAM_QHY5II_GUIDE_MODE', 50, 'QHY5II guide mode'),
('DDR_BUFFER_CAPACITY', 51, 'DDR buffer capacity'),
('DDR_BUFFER_READ_THRESHOLD', 52, 'DDR read threshold'),
('DefaultGain', 53, 'Default detector gain'),
('DefaultOffset', 54, 'Default detector offset'),
('OutputDataActualBits', 55, 'Actual number of bits in output data'),
('OutputDataAlignment', 56, 'Output data alignment'),
('CAM_SINGLEFRAMEMODE', 57, 'Single frame mode'),
('CAM_LIVEVIDEOMODE', 58, 'Live video mode'),
('CAM_IS_COLOR', 59, 'Color mode'),
('hasHardwareFrameCounter', 60, 'Hardware frame counter'),
('CONTROL_MAX_ID_Error', 61, 'Max Error ID'),
('CAM_HUMIDITY', 62, 'Humidity sensor'),
('CAM_PRESSURE', 63, 'Pressure sensor'),
('CONTROL_VACUUM_PUMP', 64, 'Vacuum pump'),
('CONTROL_SensorChamberCycle_PUMP', 65, 'Chamber Cycle pump sensor')
)

CONTROL_CODE_DICT = dict([(code[0], code[1]) for code in CONTROL_CODES])
CONTROL_DESC_DICT = dict([(code[1], code[2]) for code in CONTROL_CODES])

ERROR_CODES = (
('QHYCCD_SUCCESS', 0x00000000, 'Camera works well'),
('QHYCCD_ERROR', 0xFFFFFFFF, 'Error'),
('QHYCCD_ERROR_NO_DEVICE', 0xFFFFFFFE, 'No camera connected'),
('QHYCCD_ERROR_UNSUPPORTED', 0xFFFFFFFD, 'Unsupported function'),
('QHYCCD_ERROR_SETPARAMS', 0xFFFFFFFC, 'Invalid parameter (set)'),
('QHYCCD_ERROR_GETPARAMS', 0xFFFFFFFB, 'Invalid parameter (get)'),
('QHYCCD_ERROR_EXPOSING', 0xFFFFFFFA, 'Exposure ongoing'),
('QHYCCD_ERROR_EXPFAILED', 0xFFFFFFF9, 'Exposure failed'),
('QHYCCD_ERROR_GETTINGDATA', 0xFFFFFFF8, 'Another instance is transferring data'),
('QHYCCD_ERROR_GETTINGFAILED', 0xFFFFFFF7, 'Data transfer failure'),
('QHYCCD_ERROR_INITCAMERA', 0xFFFFFFF6,	'Camera initialization failure'),
('QHYCCD_ERROR_RELEASERESOURCE', 0xFFFFFFF5, 'Resource release failure'),
('QHYCCD_ERROR_INITRESOURCE', 0xFFFFFFF4, 'Resource initialization failure'),
('QHYCCD_ERROR_NO_MATCH', 0xFFFFFFF3, 'No camera matched'),
('QHYCCD_ERROR_ERROR_OPENCAM', 0xFFFFFFF2, 'Camera opening failure'),
('QHYCCD_ERROR_INITCLASS', 0xFFFFFFF1, 'Cam class initialization failure'),
('QHYCCD_ERROR_SETRESOLUTION', 0xFFFFFFF0, 'Invalid resolution'),
('QHYCCD_ERROR_USBTRAFFIC', 0xFFFFFFEF, 'Invalid USB traffic setting'),
('QHYCCD_ERROR_USBSPEED', 0xFFFFFFEE, 'Invalid USB speed setting'),
('QHYCCD_ERROR_SETEXPOSE', 0xFFFFFFED, 'Invalid exposure time'),
('QHYCCD_ERROR_SETGAIN', 0xFFFFFFEC, 'Invalid detector gain'),
('QHYCCD_ERROR_SETRED', 0xFFFFFFEB, 'Invalid red color balance'),
('QHYCCD_ERROR_SETBLUE', 0xFFFFFFEA, 'Invalid blue color balance'),
('QHYCCD_ERROR_EVTCMOS', 0xFFFFFFE9, 'CMOS EVT failure'),
('QHYCCD_ERROR_EVTUSB', 0xFFFFFFE8, 'USB EVT failure'),
('QHYCCD_ERROR_UNKNOWN', 0xFFFFFFE7, 'Unknown')
)

ERROR_MIN = 0xFFFF0000
ERROR_CODE_DICT = dict([(code[0], code[1]) for code in ERROR_CODES])
ERROR_DESC_DICT = dict([(code[1], code[2]) for code in ERROR_CODES])

# Stream modes
QHYCCD_STREAM_SINGLE = 0x00
QHYCCD_STREAM_LIVE = 0x01

def check_status(status_code):
    """Examine return status code of function call
    and raise RunTimeError if appropriate

    Parameters
    ----------
    status_code : integer
        status code

    Returns
    -------
    status : integer
        propagated function result

    """

    if status_code > ERROR_MIN:
        raise RuntimeError(f'{ERROR_DESC_DICT[status_code]}')

    return status_code

def error(status_string):
    """Return the error description that matches a status string

    Parameters
    ----------
    status_string : string
        status string
    Returns
    -------
    description : string
        error description

    """
    return f'{ERROR_DESC_DICT[ERROR_CODE_DICT[status_string]]}'
   
class qhyccd(object):
    """Minimalistic wrapper object around the QHYCCD camera driver
    """
                   
    def __init__(self,
                 cam_no=0,
                 usbtraffic=0,
                 gain=100,
                 offset=100,
                 exptime=0.1,
                 region_start=[0,0],
                 region_size=[0,0],
                 bin_size=[1,1],
                 bit_depth=16):

        lib.SetQHYCCDLogLevel(0)
        print(f"Driver version: {self.get_sdk_version()}")
        self.init_resource()
        if self.scan_cameras() == 0:
            raise RuntimeError(error('QHYCCD_ERROR_NO_DEVICE'))
        self.set_camera(cam_no)
        print(f"QHYCCD camera found: {self.get_camera_name()}")
        self.open_camera()
        print(f"Firmware version: {self.get_firmware_version()}")
        if self.has_control('CAM_SINGLEFRAMEMODE') == False:
            print("Error: Single-Frame mode not supported")
            raise KeyError(error('QHYCCD_ERROR_UNSUPPORTED'))
        self.set_stream_mode(mode='single')
        print(f"Acquisition mode set to {self.get_stream_mode()}")
        print("Initializing...", end='\r', flush=True)
        self.init_camera()
        print(f"{self.get_camera_name()} initialized")
        print("Color sensor" if self.has_control('CAM_COLOR') else "B/W sensor")
        print(f"Max resolution: {self.get_image_size()[0]:d} x {self.get_image_size()[1]:d}")
        print(f"Chip size: {self.get_chip_size()[0]:.2f}mm x {self.get_chip_size()[1]:.2f}mm")
        print(f"Pixel size: {self.get_pixel_size()[0]:.2f}um x {self.get_pixel_size()[1]:.2f}um")
        self.set_usbtraffic(usbtraffic)
        print(f"USBtraffic parameter: {self.get_usbtraffic()}")
        self.set_gain(gain)
        print(f"Gain: {self.get_gain()} cB")
        self.set_offset(offset)
        print(f"Offset: {self.get_offset()}")
        self.set_exptime(exptime)
        print(f"Exposure time: {self.get_exptime():.6f} s")
        self.set_region(region_start,region_size)
        print(f"Acquisition region: {self.get_region()[0][0]}-" + \
              f"{self.get_region()[0][0] + self.get_region()[1][0]} x " + \
              f"{self.get_region()[0][1]}-" + \
              f"{self.get_region()[0][1] + self.get_region()[1][1]}")
        self.set_binsize(bin_size)
        print(f"Binsize: {self.get_binsize()[0]} x {self.get_binsize()[1]}")
        self.set_bitdepth(bit_depth)
        print(f"Bitdepth: {self.get_bitdepth()}")

    def init_resource(self):
        """Initialize QHYCCD SDK resource

        Initialize the QHYCCD SDK resource
        Raises RunTimeError in case of error
        """
        check_status(lib.InitQHYCCDResource())
        return self

    def release_resource(self):
        """Release QHYCCD SDK resource

        Release the QHYCCD SDK resource
        Raises RunTimeError in case of error
        """
        check_status(lib.ReleaseQHYCCDResource())
        return self

    ################################# Camera ##################################

    def scan_cameras(self):
        """Scan for connected QHYCCD cameras

        Update the number of connected QHYCCD cameras.
        Raises RunTimeError in case of error.

        Returns
        -------
        ncam : integer
            number of connected cameras
        """
        self._ncam = check_status(lib.ScanQHYCCD())
        return self._ncam

    def set_camera(self, cam_no):
        """Set the camera index

        Set the camera index.
        Raises RunTimeError in case of error.
        """
        if cam_no >= self._ncam:
          raise RuntimeError(error('QHYCCD_ERROR_NO_MATCH'))
        self._cam_no = cam_no
        self._cam_id = ffi.new('char[32]')
        check_status(lib.GetQHYCCDId(self._cam_no, self._cam_id))
        self._cam_idstr = ffi.string(self._cam_id).decode()
        return self

    def get_camera_name(self):
        """Return the name of the current QHYCCD camera
        
        Return the name of the current QHYCCD camera.
        Raises RunTimeError if the camera is not set.

        Returns
        -------
        version : string
            camera name
        """
        if not hasattr(self, '_cam_idstr'):
            print("Error: camera is not set")
            raise RuntimeError(error('QHYCCD_ERROR'))

        return self._cam_idstr

    def open_camera(self):
        """Open the current camera
        
        Gets the handle of the current QHYCCD camera.
        Raises RunTimeError in case of error or if the camera is not set.
        """
        if not hasattr(self, '_cam_id'):
            print("Error: camera is not set")
            raise RuntimeError(error('QHYCCD_ERROR'))

        self._cam_handle = lib.OpenQHYCCD(self._cam_id)
        if ffi.cast('uintptr_t', self._cam_handle) == 0:
            raise RuntimeError(error('QHYCCD_ERROR_ERROR_OPENCAM'))
        return self

    def close_camera(self):
        """Close the current camera
        
        Remove the handle of the current QHYCCD camera.
        Raises RunTimeError in case of error.
        """
        if hasattr(self, '_cam_handle'):
            check_status(lib.CloseQHYCCD(self._cam_handle))
            del self._cam_handle
        return self

    def init_camera(self):
        """Initialize the current camera

        Initialize the current QHYCCD camera.
        Raises RunTimeError in case of error or if the camera is not open.
        """
        if not hasattr(self, '_cam_handle'):
            print("Error: camera is not open")
            raise RuntimeError(error('QHYCCD_ERROR'))

        check_status(lib.InitQHYCCD(self._cam_handle))
        return self

    ############################## Acquisition ################################
    def get_image(self):
        """Acquire an image with the current QHYCCD camera
        
        Acquire an image with the current QHYCCD camera.
        Raises RunTimeError in case of error or if the camera is not open.
        """
        if not hasattr(self, '_cam_handle'):
            print("Error: camera is not open")
            raise RuntimeError(error('QHYCCD_ERROR'))

        if not hasattr(self, 'image'):
            print("Error: Acquisition region has not been set")
            raise RuntimeError(error('QHYCCD_ERROR'))

        check_status(lib.ExpQHYCCDSingleFrame(self._cam_handle))
        #memsize = lib.GetQHYCCDMemLength(self._cam_handle)
        roi_size = ffi.new('uint32_t[2]')
        bpp = ffi.new('uint32_t *')
        channels = ffi.new('uint32_t *')
        self.imageData = ffi.cast("uint8_t *", self.image.ctypes.data)
        check_status(lib.GetQHYCCDSingleFrame(self._cam_handle, \
                                              roi_size, roi_size + 1, \
                                              bpp, \
                                              channels, \
                                              self.imageData))

        return self


    ########################## Control parameters #############################

    def has_control(self, control):
        """Check if the current camera has a given control parameter
        
        Check if the current camera has a given control parameter.

        Parameters
        ----------
        control: string
            control parameter code string

        Returns
        -------
        flag : boolean
            whether the control exists for the current camera
        """
        ret = lib.IsQHYCCDControlAvailable(self._cam_handle,
        	CONTROL_CODE_DICT[control])
        flag = (ret == ERROR_CODE_DICT['QHYCCD_SUCCESS'])
        return flag

    def set_control(self, control, value):
        """Set a given control parameter in the current camera
        
        Set a control parameter in the current QHYCCD camera.
        Raises RunTimeError in case of error.

        Parameters
        ----------
        control : string
            control parameter code string
        value: float
            control parameter value
        """
        check_status(lib.SetQHYCCDParam(self._cam_handle, \
                     CONTROL_CODE_DICT[control], float(value)))
        return self

    def query_control(self, control):
        """Query a given control parameter from the current camera
        
        Query a given control parameter from the current QHYCCD camera.

        Parameters
        ----------
        control : string
            control parameter code string

        Returns
        -------
        value: float
            control parameter value
        """
        value = lib.GetQHYCCDParam(self._cam_handle, CONTROL_CODE_DICT[control])
        
        return float(value)

    ################################ USB speed ################################

    def set_usbtraffic(self, usbtraffic):
        """Set the USB speed (USBTRAFFIC) parameter of the current camera
        
        Set the USB speed (USBTRAFFIC) parameter of the current QHYCCD camera.
        Raises KeyError in case of error.

        Parameters
        ----------
        usbtraffic: integer
            USB speed factor between 0 (fastest) and 100 (slowest)

        Sets attributes
        ---------------
        _usbtraffic : integer
            USB speed factor between 0 (fastest) and 100 (slowest)
        """
        if self.has_control('CONTROL_USBTRAFFIC'):
            self.set_control('CONTROL_USBTRAFFIC', usbtraffic)
        else:
            print("Error: USB traffic parameter not supported")
            raise KeyError(error('QHYCCD_ERROR_UNSUPPORTED'))

        self._usbtraffic = int(usbtraffic)

        return self

    def get_usbtraffic(self):
        """Return the USB speed (USBTRAFFIC) parameter of the current camera
        
        Return the USB speed (USBTRAFFIC) parameter of the current camera.

        Returns
        -------
        usbtraffic: integer
            USB speed factor between 0 (fastest) and 100 (slowest)
        """
        if not hasattr(self, '_usbtraffic'):
            if self.has_control('CONTROL_USBTRAFFIC'):
                self._usbtraffic = int(self.query_control('CONTROL_USBTRAFFIC'))
            else:
                print("Error: USB traffic parameter not supported")
                raise KeyError(error('QHYCCD_ERROR_UNSUPPORTED'))

        return self._usbtraffic

    ################################## Gain ###################################

    def set_gain(self, gain):
        """Set the detector gain of the current camera
        
        Set the detector gain of the current QHYCCD camera.
        Raises KeyError in case of error.

        Parameters
        ----------
        gain: float
            detector gain (in cB)

        Sets attributes
        ---------------
        _gain : float
            detector gain (in cB)
        """
        if self.has_control('CONTROL_GAIN'):
            self.set_control('CONTROL_GAIN', gain)
        else:
            print("Error: gain parameter not supported")
            raise KeyError(error('QHYCCD_ERROR_UNSUPPORTED'))

        self._gain = gain

        return self

    def get_gain(self):
        """Return the detector gain of the current camera
        
        Return the detector gain of the current QHYCCD camera.

        Returns
        -------
        gain: float
            detector gain (in cB)
        """
        if not hasattr(self, '_gain'):
            if self.has_control('CONTROL_GAIN'):
                self._gain = int(self.query_control('CONTROL_GAIN'))
            else:
                print("Error: gain not supported")
                raise KeyError(error('QHYCCD_ERROR_UNSUPPORTED'))

        return self._gain

    ################################# Offset ##################################

    def set_offset(self, offset):
        """Set the detector offset of the current camera
        
        Set the detector offset of the current QHYCCD camera.
        Raises KeyError in case of error.

        Parameters
        ----------
        offset: integer
            detector offset

        Sets attributes
        ---------------
        _offset : integer
            detector offset
        """
        if self.has_control('CONTROL_OFFSET'):
            self.set_control('CONTROL_OFFSET', offset)
        else:
            print("Error: offset parameter not supported")
            raise KeyError(error('QHYCCD_ERROR_UNSUPPORTED'))

        self._offset = offset

        return self

    def get_offset(self):
        """Return the detector offset parameter of the current camera
        
        Return the detector offset of the current QHYCCD camera.

        Returns
        -------
        offset: float
            detector offset
        """
        if not hasattr(self, '_offset'):
            if self.has_control('CONTROL_OFFSET'):
                self._offset = int(self.query_control('CONTROL_OFFSET'))
            else:
                print("Error: offset not supported")
                raise KeyError(error('QHYCCD_ERROR_UNSUPPORTED'))

        return self._offset

    ############################## Exposure time ##############################

    def set_exptime(self, exptime):
        """Set the exposure time of the current camera
        
        Set the exposure time of the current QHYCCD camera.
        Raises KeyError in case of error.

        Parameters
        ----------
        exptime: float
            exposure time (in seconds)

        Sets attributes
        ---------------
        _exptime : float
            exposure time (in seconds)
        """
        if self.has_control('CONTROL_EXPOSURE'):
            self.set_control('CONTROL_EXPOSURE', int(exptime * 1.0e6))
        else:
            print("Error: exposure time parameter not supported")
            raise KeyError(error('QHYCCD_ERROR_UNSUPPORTED'))

        self._exptime = int(exptime * 1.0e6) * 1.0e-6

        return self

    def get_exptime(self):
        """Return the exposure time of the current camera
        
        Return the exposure time of the current QHYCCD camera.

        Returns
        -------
        exptime: float
            exposure time (in seconds)
        """
        if not hasattr(self, '_exptime'):
            if self.has_control('CONTROL_EXPOSURE'):
                self._exptime = float(self.query_control('CONTROL_EXPOSURE')) * 1.0e-6
            else:
                print("Error: exposure time not supported")
                raise KeyError(error('QHYCCD_ERROR_UNSUPPORTED'))

        return self._exptime

    ################################ Bitdepth #################################

    def set_bitdepth(self, bitdepth):
        """Set the bit depth
        
        Set the camera bit depth.
        Raises RuntimeError in case of error.
        
        Parameters
        ----------
        bitdepth : int
            Bit depth in bits

        Sets attributes
        ---------------
        _bitdepth : int
            Bit depth in bits
        """
        check_status(lib.SetQHYCCDBitsMode(self._cam_handle, int(bitdepth)))

        self._bitdepth = bitdepth

        return self

    def get_bitdepth(self):
        """Get the bit depth
        
        Get the camera bit depth.
        
        Returns
        ---------------
        bitdepth: int
            Bit depth in bits
        """
        if not hasattr(self, '_bitdepth'):
            print("Error: camera bit depth not set")
            raise RuntimeError(error('QHYCCD_ERROR'))

        return self._bitdepth

    ############################### Streaming #################################

    def set_stream_mode(self, mode='single'):
        """Set the camera read out mode
        
        Set the camera streaming mode.
        Raises KeyError or RunTimeError in case of error.
        
        Parameters
        ----------
        mode : string
            'single': single exposure (default)
            'live': video mode
        """
        if mode == 'single':
            imode = 0x00
        elif mode == 'live':
            imode = 0x01
        else:
            raise KeyError(error('QHYCCD_ERROR_UNSUPPORTED'))
        check_status(lib.SetQHYCCDStreamMode(self._cam_handle, imode))

        self._stream_mode = mode
        return self

    def get_stream_mode(self):
        """Return the camera stream mode
        
        Return the camera stream mode.
        Raises RunTimeError if stream mode is not set.
        
        Returns
        -------
        mode : string
            'single': single exposure (default)
            'live': video mode
        """
        if not hasattr(self, '_stream_mode'):
            print("Error: camera stream mode not set")
            raise RuntimeError(error('QHYCCD_ERROR'))

        return  self._stream_mode

    ############################ Detector geometry ############################

    def set_region(self, start, size):
        """Set the camera acquisition region
        
        Set the camera acquisition region
        Raises RunTimeError in case of error.
        
        Parameters
        ----------
        start : int[2]
            [startX, startY]
        size : int[2]
            [sizeX, sizeY]

        Sets attributes
        ---------------
        _region_start : int[2]
            [startX, startY]
        _region_size : int[2]
            [sizeX, sizeY]
        """
        if size[0]*size[1] == 0:
            size = self.get_image_size()

        # Need this if region updated
        if hasattr(self, '_region_set'):
            check_status(lib.CancelQHYCCDExposingAndReadout(self._cam_handle))

        check_status(lib.SetQHYCCDResolution(self._cam_handle, \
                     start[0], start[1], size[0], size[1]))

        self._region_start = start.copy()
        self._region_size = size.copy()
        self._region_set = True
        
        self.image = np.zeros([self._region_size[1], self._region_size[0]], dtype=np.uint16)

        return self

    def get_region(self):
        """Get the camera acquisition region
        
        Get the camera acquisition region
        Raises KeyError or RunTimeError in case of error.
        
        Sets attributes
        ---------------
        _region_start : int[2]
            [startX, startY]
        _region_size : int[2]
            [sizeX, sizeY]

        Returns
        ---------------
        region_start : int[2]
            [startX, startY]
        region_size : int[2]
            [sizeX, sizeY]

        """
        if not hasattr(self, '_region_size'):
            self._region_start = [0, 0]
            self._region_size = self.get_image_size().copy()

        return self._region_start, self._region_size

    def set_binsize(self, binsize):
        """Set the pixel binsize
        
        Set the camera pixel binsize.
        Raises RuntimeError in case of error.
        
        Parameters
        ----------
        binsize : int[2]
            [sizeX, sizeY]

        Sets attributes
        ---------------
        _binsize : int[2]
            [sizeX, sizeY]
        """
        check_status(lib.SetQHYCCDBinMode(self._cam_handle, \
                     binsize[0], binsize[1]))

        self._binsize = binsize.copy()

        return self

    def get_binsize(self):
        """Get the pixel binsize
        
        Get the camera pixel binsize.
        
        Returns
        ---------------
        binsize : int[2]
            [sizeX, sizeY]
        """
        if not hasattr(self, '_binsize'):
            self._binsize = [1, 1]

        return self._binsize.copy()

    def query_chip_info(self):
        """Query information from the current camera
        
        Query information from the current camera.
        Raises RunTimeError in case of error.

        Sets attributes
        ---------------
        _chip_size : float[2]
            physical chip size (W,H in mm), 
        _image_size : uint32[2]
            maximum raster size (W,H in pixels),
        _pixel_size : float[2]
            physical pixel size (W,H in um),
        _bpp : uint8
            bit depth
        """
        chip_size = ffi.new('double[2]')
        image_size = ffi.new('uint32_t[2]')
        pixel_size = ffi.new('double[2]')
        bpp = ffi.new('uint32_t *')
        
        check_status(lib.GetQHYCCDChipInfo(self._cam_handle, \
                     chip_size, chip_size + 1, \
                     image_size, image_size + 1, \
                     pixel_size, pixel_size + 1, \
                     bpp))

        self._chip_size = list(chip_size)
        self._image_size = list(image_size)
        self._pixel_size = list(pixel_size)
        self._bpp = int(bpp[0])
        return self

    def get_chip_size(self):
        """Return the physical chip size of the current camera
        
        Return the physical chip size of the current QHYCCD camera.

        Returns
        -------
        chip_size : float[2]
            physical chip size (W,H in mm), 
        """
        if not hasattr(self, '_chip_size'):
            self.query_chip_info()
        return self._chip_size.copy()

    def get_image_size(self):
        """Return the maximum image size of the current camera
        
        Return the maximum image (raster) size of the current QHYCCD camera.

        Returns
        -------
        image_size : uint32[2]
            maximum raster size (W, H in pixels)
        """
        if not hasattr(self, '_image_size'):
            self.query_chip_info()
        return self._image_size.copy()

    def get_pixel_size(self):
        """Return the physical pixel size of the current camera
        
        Return the physical pixel size of the current QHYCCD camera.

        Returns
        -------
        pixel_size :float[2]
            physical pixel size (W,H in um), 
        """
        if not hasattr(self, '_pixel_size'):
            self.query_chip_info()
        return self._pixel_size.copy()

    def query_overscan_area(self):
        """Query the overscan limits from the current camera
        
        Query the overscan limits from the current QHYCCD camera.
        Raises RunTimeError in case of error

        Sets attributes
        ---------------
        _overscan_limits : int[4]
            [startX, startY, sizeX, sizeY]
        """
        limits = ffi.new('uint32_t[4]')
        check_status(lib.GetQHYCCDOverScanArea(self._cam_handle, \
                     limits, limits + 1, limits + 2, limits + 3))
        self._overscan_limits = list(limits)
        return self

    def get_overscan_area(self):
        """Return the overscan limits of the current camera
        
        Return the overscan limits from the current QHYCCD camera.

        Returns
        -------
        overscan_limits : int[4]
            [startX, startY, sizeX, sizeY]
        """
        if not hasattr(self, '_overscan_limits'):
            self.query_oversan_area()
        return self._overscan_limits.copy()

    def query_effective_area(self):
        """Query the effective limits from the current camera
        
        Query the effective limits from the current QHYCCD camera.
        Raises RunTimeError in case of error.

        Sets attributes
        ---------------
        _effective_limits : int[4]
            [startX, startY, sizeX, sizeY]
        """
        limits = ffi.new('uint32_t[4]')
        check_status(lib.GetQHYCCDOverScanArea(self._cam_handle, \
                     limits, limits + 1, limits + 2, limits + 3))
        self._effective_limits = list(limits)
        return self

    def get_effective_area(self):
        """Return the effective limits of the current camera
        
        Return the effective limits from the current QHYCCD camera.

        Returns
        -------
        effective_limits : int[4]
            [startX, startY, sizeX, sizeY]
        """
        if not hasattr(self, '_effective_limits'):
            self.query_effective_area()
        return self._effective_limits.copy()

    ########################## Cooling and temperature ########################
    def get_temperature(self):
        """Return the temperature of the sensor
        
        Return the detector temperature of the current QHYCCD camera.

        Returns
        -------
        temp: float
            detector temperature (in °C)
        """
        if self.has_control('CONTROL_CURTEMP'):
            return float(self.query_control('CONTROL_CURTEMP'))
        else:
            print("Error: curtemp not supported")
            raise KeyError(error('QHYCCD_ERROR_UNSUPPORTED'))

    def get_target_temperature(self):
        """Return the target temperature of the cooling system
        
        Parameters
        ----------
        temp: float
              target temperature (in °C)
        """
        if self.has_control('CONTROL_COOLER'):
            return float(self.query_control('CONTROL_COOLER'))
        else:
            print("Error: cooling not supported")
            raise KeyError(error('QHYCCD_ERROR_UNSUPPORTED'))


    def set_target_temperature(self, temp, wait=False):
        """Set the target temperature of the cooling system
        
        Parameters
        ----------
        temp: float
              target temperature (in °C)
        """
        if self.has_control('CONTROL_COOLER'):
            self.set_control('CONTROL_COOLER', temp)
        else:
            print("Error: cooling not supported")
            raise KeyError(error('QHYCCD_ERROR_UNSUPPORTED'))


    ############################ Software versions ############################
    def query_sdk_version(self):
        """Query the version of the QHYCCD driver
        
        Query the version of the QHYCCD driver.
        Raises RunTimeError in case of error.

        Sets attributes
        ---------------
        _sdk_version : string
            driver version
        """
        ymds = ffi.new('uint32_t[4]')
        check_status(lib.GetQHYCCDSDKVersion(ymds, ymds+1, ymds+2, ymds+3))
        self._sdk_version = f'20{ymds[0]:02d}{ymds[1]:02d}{ymds[2]:02d}_{ymds[3]}'
        return self
    
    def get_sdk_version(self):
        """Return the version of the QHYCCD driver
        
        Return the version of the QHYCCD driver.

        Returns
        -------
        version : string
            driver version
        """
        if not hasattr(self, '_sdk_version'):
            self.query_sdk_version()
        return self._sdk_version
        
    def query_firmware_version(self):
        """Query the version of the firmware from the camera
 
        Query the version of the firmware from the current QHYCCD camera.
        Raises RunTimeError in case of error.

        Sets attributes
        ---------------
        _firmware_version : string
            firmware version
        """
        fwv = ffi.new('uint8_t[32]')
        check_status(lib.GetQHYCCDFWVersion(self._cam_handle, fwv))

        yr1 = fwv[0] >> 4
        if yr1 < 10:
          yr1 += 0x10
        yr2 = fwv[0] & ~0xf0

        self._firmware_version = f'20{yr1:02d}_{yr2:02d}_{fwv[1]:02d}'
        return self

    def get_firmware_version(self):
        """Return the version of the firmware from the camera
        
        Return the version of the firmware from the current QHYCCD camera.

        Returns
        -------
        version : string
            firmware version
        """
        if not hasattr(self, '_firmware_version'):
            self.query_firmware_version()
        return self._firmware_version
        
    def __del__(self):
        if hasattr(self, '_region_set'):
            check_status(lib.CancelQHYCCDExposingAndReadout(self._cam_handle))
        self.close_camera()
        self.release_resource()

if __name__=='__main__':
    a = qhyccd()

