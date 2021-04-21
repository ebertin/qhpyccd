from _qhyccd_cffi import ffi, lib
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
('QHYCCD_ERROR', 0xFFFFFFFF, 'Other error'),
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

def check_status(status_code):
    """Examine return status code of function call
    and raise RunTimeError if appropriate

    Parameters
    ----------
    status_code: integer
        status code

    Returns
    -------
    status: integer
        propagated function result

    """

    if status_code > ERROR_MIN:
        raise RuntimeError(f'{ERROR_DESC_DICT[status_code]}')

    return status_code

def raise_error(status_string):
    """Raise RunTimeError using a given status string

    Parameters
    ----------
    status_string: string
        status string
    """

    raise RuntimeError(f'{ERROR_DESC_DICT[ERROR_CODE_DICT[status_string]]}')

class qhyccd(object):
    """Minimalistic wrapper object around the QHYCCD camera driver
    """
                   
    def __init__(self, cam_no=0):
        lib.SetQHYCCDLogLevel(0)
        print(f"Driver version: {self.get_sdkversion()}")
        self.init_resource()
        if self.scan_cams() == 0:
            raise_error('QHYCCD_ERROR_NO_DEVICE')
        self.set_camno(cam_no)
        print(f"QHYCCD camera found: {self.get_camname()}")
        self.open_cam()
        print(f"Firmware version: {self.get_fwversion()}")
        if self.has_control('CAM_SINGLEFRAMEMODE') == False:
            print("Error: Single-Frame mode not supported")
            raise_error('QHYCCD_ERROR_UNSUPPORTED')

    def init_resource(self):
        """Initialize QHYCCD SDK resource

        Initialize the QHYCCD SDK resource
        Raises RunTimeError in case of error
        """
        check_status(lib.InitQHYCCDResource())
        return

    def release_resource(self):
        """Release QHYCCD SDK resource

        Release the QHYCCD SDK resource
        Raises RunTimeError in case of error
        """
        check_status(lib.ReleaseQHYCCDResource())
        return self

    def scan_cams(self):
        """Scan for connected QHYCCD cameras

        Update the number of connected QHYCCD cameras,
        Raises RunTimeError in case of error

        Returns
        -------
        ncam: integer
            number of connected cameras
        """
        self.ncam = check_status(lib.ScanQHYCCD())
        return self.ncam

    def set_camno(self, cam_no):
        """Set the camera index

        Set the camera index
        Raises RunTimeError in case of error
        """
        if cam_no >= self.ncam:
          check_status(ERROR_CODE_DICT['QHYCCD_ERROR_NO_MATCH'])
        self.cam_no = cam_no
        self.cam_id = ffi.new("char[32]")
        check_status(lib.GetQHYCCDId(self.cam_no, self.cam_id))
        self.cam_idstr = ffi.string(self.cam_id).decode()
        return self

    def get_camname(self):
        """Get the name of the current QHYCCD camera
        
        Returns the name of the current QHYCCD camera

        Returns
        -------
        version: string
            camera name
        """
        return self.cam_idstr

    def open_cam(self):
        """Open the current camera
        
        Gets the handle of the current QHYCCD camera

        Raises RunTimeError in case of error
        """
        self.cam_handle = lib.OpenQHYCCD(self.cam_id)
        if ffi.cast("uintptr_t", self.cam_handle) == 0:
            check_status(ERROR_CODE_DICT['QHYCCD_ERROR_ERROR_OPENCAM'])
        return self

    def close_cam(self):
        """Close the current camera
        
        Remove the handle of the current QHYCCD camera

        Raises RunTimeError in case of error
        """
        check_status(lib.CloseQHYCCD(self.cam_handle))
        del self.cam_handle
        return self

    def has_control(self, control):
        """Check if the current camera has a given control
        
        Remove the handle of the current QHYCCD camera

        Parameters
        ----------
        control: string
            control code string

        Returns
        -------
        flag: boolean
            whether the control exists for the current camera
        """
        ret = lib.IsQHYCCDControlAvailable(self.cam_handle,
        	CONTROL_CODE_DICT[control])
        flag = (ret == ERROR_CODE_DICT['QHYCCD_SUCCESS'])
        return flag

    def set_control(self, control):
        """set a given control in the current camera
        
        Set a control in the current QHYCCD camera
        Raises RunTimeError in case of error
        
        Parameters
        ----------
        control: string
            control code string

        Returns
        -------
        flag: boolean
            whether the control exists for the current camera

        Raises RunTimeError in case of error
        """
        return

    def get_sdkversion(self):
        """Get the version of the QHYCCD driver
        
        Returns the version of the QHYCCD driver
        Raises RunTimeError in case of error

        Returns
        -------
        version: string
            driver version
        """
        ymds = ffi.new("uint32_t[4]")
        check_status(lib.GetQHYCCDSDKVersion(ymds, ymds+1, ymds+2, ymds+3))
        version = f'20{ymds[0]:02d}{ymds[1]:02d}{ymds[2]:02d}_{ymds[3]}'
        return version
    
    def get_fwversion(self):
        """Get the version of the camera firmware
 
        Gets the firmware version of the current QHYCCD camera
        Raises RunTimeError in case of error

        Returns
        -------
        version: string
            driver version
        """

        fwv = ffi.new("uint8_t[32]")
        check_status(lib.GetQHYCCDFWVersion(self.cam_handle, fwv))

        yr1 = fwv[0] >> 4
        if yr1 < 10:
          yr1 += 0x10
        yr2 = fwv[0] & ~0xf0

        version = f'20{yr1:02d}_{yr2:02d}_{fwv[1]:02d}'
        return version

    def __del__(self):
        if hasattr(self, 'cam_handle'):
            self.close_cam()
        self.release_resource()
        return

if __name__=='__main__':
    a = qhyccd()

