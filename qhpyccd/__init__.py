from _qhyccd_cffi import ffi, lib
import numpy as np

ERROR_CODE = {
'QHYCCD_SUCCESS' :  		0x00000000,	# Camera works well
'QHYCCD_ERROR'   :  		0xFFFFFFFF,	# Other error
'QHYCCD_ERROR_NO_DEVICE' :	0xFFFFFFFE,	# No camera connected
'QHYCCD_ERROR_UNSUPPORTED':     0xFFFFFFFD,	# Unsupported function
'QHYCCD_ERROR_SETPARAMS':	0xFFFFFFFC,	# Invalid parameter (set)
'QHYCCD_ERROR_GETPARAMS':	0xFFFFFFFB,	# Invalid parameter (get)
'QHYCCD_ERROR_EXPOSING':	0xFFFFFFFA,	# Exposure ongoing
'QHYCCD_ERROR_EXPFAILED':	0xFFFFFFF9,	# Exposure failed
'QHYCCD_ERROR_GETTINGDATA':	0xFFFFFFF8,	# Another instance is transfering data
'QHYCCD_ERROR_GETTINGFAILED':	0xFFFFFFF7,	# Data transfer failure
'QHYCCD_ERROR_INITCAMERA':	0xFFFFFFF6,	# Camera initialization failure
'QHYCCD_ERROR_RELEASERESOURCE':	0xFFFFFFF5,	# Resource release failure
'QHYCCD_ERROR_INITRESOURCE':	0xFFFFFFF4,	# Resource initialization failure
'QHYCCD_ERROR_NO_MATCH':	0xFFFFFFF3,	# No camera matched
'QHYCCD_ERROR_ERROR_OPENCAM':	0xFFFFFFF2,	# Camera opening failure
'QHYCCD_ERROR_INITCLASS':	0xFFFFFFF1,	# Cam class initialization failure
'QHYCCD_ERROR_SETRESOLUTION':	0xFFFFFFF0,	# Invalid resolution
'QHYCCD_ERROR_USBTRAFFIC':	0xFFFFFFEF,	# Invalid USB traffic setting
'QHYCCD_ERROR_USBSPEED':	0xFFFFFFEE,	# Invalid USB speed setting
'QHYCCD_ERROR_SETEXPOSE':	0xFFFFFFED,	# Invalid exposure time
'QHYCCD_ERROR_SETGAIN':		0xFFFFFFEC,	# Invalid detector gain
'QHYCCD_ERROR_SETRED':		0xFFFFFFEB,	# Invalid red color balance
'QHYCCD_ERROR_SETBLUE':		0xFFFFFFEA,	# Invalid blue color balance
'QHYCCD_ERROR_EVTCMOS':		0xFFFFFFE9,	# CMOS EVT failure
'QHYCCD_ERROR_EVTUSB':		0xFFFFFFE8,	# USB EVT failure
'QHYCCD_ERROR_UNKNOWN':		0xFFFFFFE7	# Unknown
}

ERROR_STRING = {
'QHYCCD_SUCCESS' :  		'Camera works well',
'QHYCCD_ERROR'   :  		'Other error',
'QHYCCD_ERROR_NO_DEVICE' :	'No camera connected',
'QHYCCD_ERROR_UNSUPPORTED':     'Unsupported function',
'QHYCCD_ERROR_SETPARAMS':	'Invalid parameter (set)',
'QHYCCD_ERROR_GETPARAMS':	'Invalid parameter (get)',
'QHYCCD_ERROR_EXPOSING':	'Exposure ongoing',
'QHYCCD_ERROR_EXPFAILED':	'Exposure failed',
'QHYCCD_ERROR_GETTINGDATA':	'Another instance is transfering data',
'QHYCCD_ERROR_GETTINGFAILED':	'Data transfer failure',
'QHYCCD_ERROR_INITCAMERA':	'Camera initialization failure',
'QHYCCD_ERROR_RELEASERESOURCE':	'Resource release failure',
'QHYCCD_ERROR_INITRESOURCE':	'Resource initialization failure',
'QHYCCD_ERROR_NO_MATCH':	'No camera matched',
'QHYCCD_ERROR_ERROR_OPENCAM':	'Camera opening failure',
'QHYCCD_ERROR_INITCLASS':	'Cam class initialization failure',
'QHYCCD_ERROR_SETRESOLUTION':	'Invalid resolution',
'QHYCCD_ERROR_USBTRAFFIC':	'Invalid USB traffic setting',
'QHYCCD_ERROR_USBSPEED':	'Invalid USB speed setting',
'QHYCCD_ERROR_SETEXPOSE':	'Invalid exposure time',
'QHYCCD_ERROR_SETGAIN':		'Invalid detector gain',
'QHYCCD_ERROR_SETRED':		'Invalid red color balance',
'QHYCCD_ERROR_SETBLUE':		'Invalid blue color balance',
'QHYCCD_ERROR_EVTCMOS':		'CMOS EVT failure',
'QHYCCD_ERROR_EVTUSB':		'USB EVT failure',
'QHYCCD_ERROR_UNKNOWN':		'Unknown error'
}

ERROR_DEFINE = dict([(ERROR_CODE[key], key) for key in ERROR_CODE])

def check_call(status):
    if status != ERROR_CODE['QHYCCD_SUCCESS']:
        raise RuntimeError(f'{ERROR_STRING[ERROR_DEFINE[status]]}')
    return status

class qhyccd(object):
    """Very minimalistic wrapper to the QHYCCD camera
    """
                   
    def __init__(self):
        lib.SetQHYCCDLogLevel(0)
        print(self.SDKVersion())
        check_call(lib.InitQHYCCDResource())

    def SDKVersion(self):
       ymds = ffi.new("uint32_t[4]")
       check_call(lib.GetQHYCCDSDKVersion(ymds, ymds+1, ymds+2, ymds+3))
       version = f'V20{ymds[0]:02d}{ymds[1]:02d}{ymds[2]:02d}_{ymds[3]}'
       return version
    
    def __del__(self):
       return

if __name__=='__main__':
    a = qhyccd()

