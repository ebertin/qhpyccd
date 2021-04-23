/**
Simplifed include file from the QHYCCD SDK include files (v20210415_16)
refactored for the CFFI-based Python wrapper qhpyccd.
(c) 2021 E.Bertin IAP/CNRS/SorbonneU
*/

typedef uint32_t CONTROL_ID;

typedef void qhyccd_handle;

extern uint32_t SetQHYCCDLogLevel(uint8_t logLevel);

extern uint32_t InitQHYCCDResource(void);
/** \fn uint32_t InitQHYCCDResource()
      \brief initialize QHYCCD SDK resource
      \return
	  on success,return QHYCCD_SUCCESS \n
	  QHYCCD_ERROR_INITRESOURCE if the initialize failed \n
	  another QHYCCD_ERROR code on other failures
  */

extern uint32_t ReleaseQHYCCDResource(void);
/** \fn uint32_t ReleaseQHYCCDResource()
      \brief release QHYCCD SDK resource
      \return
	  on success,return QHYCCD_SUCCESS \n
	  QHYCCD_ERROR_RELEASERESOURCE if the release failed \n
	  another QHYCCD_ERROR code on other failures
  */

extern uint32_t ScanQHYCCD(void);
/** \fn uint32_t ScanQHYCCD()
      \brief scan the connected cameras
	  \return
	  on success,return the number of connected cameras \n
	  QHYCCD_ERROR_NO_DEVICE,if no camera connect to computer
	  another QHYCCD_ERROR code on other failures
  */

extern uint32_t GetQHYCCDId(uint32_t index,char *id);
/** \fn uint32_t GetQHYCCDId(uint32_t index,char *id)
      \brief get the id from camera
	  \param index sequence number of the connected cameras
	  \param id the id for camera,each camera has only id
	  \return
	  on success,return QHYCCD_SUCCESS \n
	  another QHYCCD_ERROR code on other failures
  */

extern qhyccd_handle *OpenQHYCCD(char *id);
/** \fn qhyccd_handle *OpenQHYCCD(char *id)
      \brief open camera by camera id
	  \param id the id for camera,each camera has only id
      \return
	  on success,return QHYCCD_SUCCESS \n
	  another QHYCCD_ERROR code on other failures
  */

extern uint32_t CloseQHYCCD(qhyccd_handle *handle);
/** \fn uint32_t CloseQHYCCD(qhyccd_handle *handle)
      \brief close camera by handle
	  \param handle camera handle
	  \return
	  on success,return QHYCCD_SUCCESS \n
	  another QHYCCD_ERROR code on other failures
  */

extern uint32_t IsQHYCCDControlAvailable(qhyccd_handle *handle,CONTROL_ID controlId);
/** @fn uint32_t IsQHYCCDControlAvailable(qhyccd_handle *handle,CONTROL_ID controlId)
    @brief check the camera has the queried function or not
    @param handle camera control handle
    @param controlId function type
    @return
	  on have,return QHYCCD_SUCCESS \n
	  on do not have,return QHYCCD_ERROR_NOTSUPPORT \n
	  another QHYCCD_ERROR code on other failures
  */

extern uint32_t SetQHYCCDParam(qhyccd_handle *handle,CONTROL_ID controlId, double value);
/** \fn uint32_t SetQHYCCDParam(qhyccd_handle *handle,CONTROL_ID controlId,double value)
      \brief set params to camera
      \param handle camera control handle
      \param controlId function type
	  \param value value to camera
	  \return
	  on success,return QHYCCD_SUCCESS \n
	  QHYCCD_ERROR_NOTSUPPORT,if the camera do not have the function \n
	  QHYCCD_ERROR_SETPARAMS,if set params to camera failed \n
	  another QHYCCD_ERROR code on other failures
  */

extern double GetQHYCCDParam(qhyccd_handle *handle,CONTROL_ID controlId);
/** \fn double GetQHYCCDParam(qhyccd_handle *handle,CONTROL_ID controlId)
      \brief get the params value from camera
      \param handle camera control handle
      \param controlId function type
	  \return
	  on success,return the value\n
	  QHYCCD_ERROR_NOTSUPPORT,if the camera do not have the function \n
	  QHYCCD_ERROR_GETPARAMS,if get camera params'value failed \n
	  another QHYCCD_ERROR code on other failures
  */

extern uint32_t SetQHYCCDResolution(qhyccd_handle *handle,uint32_t x,uint32_t y,uint32_t xsize,uint32_t ysize);
/** @fn uint32_t SetQHYCCDResolution(qhyccd_handle *handle,uint32_t x,uint32_t y,uint32_t xsize,uint32_t ysize)
    @brief set camera ouput resolution
    @param handle camera control handle
    @param x the top left position x
    @param y the top left position y
    @param xsize the image width
    @param ysize the image height
    @return
        on success,return QHYCCD_SUCCESS\n
        another QHYCCD_ERROR code on other failures
  */

extern uint32_t SetQHYCCDBinMode(qhyccd_handle *handle, uint32_t wbin,uint32_t hbin);
/** \
  @fn uint32_t SetQHYCCDBinMode(qhyccd_handle *handle,uint32_t wbin,uint32_t hbin)
  @brief set camera's bin mode for ouput image data
  @param handle camera control handle
  @param wbin width bin mode
  @param hbin height bin mode
  @return
  on success,return QHYCCD_SUCCESS \n
  another QHYCCD_ERROR code on other failures
*/

extern uint32_t SetQHYCCDBitsMode(qhyccd_handle *handle,uint32_t bits);
/**
   @fn uint32_t SetQHYCCDBitsMode(qhyccd_handle *handle,uint32_t bits)
   @brief set camera's depth bits for ouput image data
   @param handle camera control handle
   @param bits image depth
   @return
   on success,return QHYCCD_SUCCESS \n
   another QHYCCD_ERROR code on other failures
  */

extern uint32_t GetQHYCCDChipInfo(qhyccd_handle *h,double *chipw,double *chiph,uint32_t *imagew,uint32_t *imageh,double *pixelw,double *pixelh,uint32_t *bpp);
/** @fn uint32_t GetQHYCCDChipInfo(qhyccd_handle *h,double *chipw,double *chiph,uint32_t *imagew,uint32_t *imageh,double *pixelw,double *pixelh,uint32_t *bpp)
      @brief get the camera's ccd/cmos chip info
      @param h camera control handle
      @param chipw chip size width
      @param chiph chip size height
      @param imagew chip output image width
      @param imageh chip output image height
      @param pixelw chip pixel size width
      @param pixelh chip pixel size height
      @param bpp chip pixel depth
  */

extern uint32_t GetQHYCCDOverScanArea(qhyccd_handle *h,uint32_t *startX, uint32_t *startY, uint32_t *sizeX, uint32_t *sizeY);
/** @fn uint32_t GetQHYCCDOverScanArea(qhyccd_handle *h,uint32_t *startX, uint32_t *startY, uint32_t *sizeX, uint32_t *sizeY)
      @brief get the camera's ccd/cmos chip info
      @param h camera control handle
      @param startX the OverScan area x position
      @param startY the OverScan area y position
      @param sizeX the OverScan area x size
      @param sizeY the OverScan area y size
	  @return
	  on success,return QHYCCD_SUCCESS \n
	  another QHYCCD_ERROR code on other failures
  */

extern uint32_t GetQHYCCDEffectiveArea(qhyccd_handle *h,uint32_t *startX, uint32_t *startY, uint32_t *sizeX, uint32_t *sizeY);
/** @fn uint32_t GetQHYCCDEffectiveArea(qhyccd_handle *h,uint32_t *startX, uint32_t *startY, uint32_t *sizeX, uint32_t *sizeY)
      @brief get the camera's ccd/cmos chip info
      @param h camera control handle
      @param startX the Effective area x position
      @param startY the Effective area y position
      @param sizeX the Effective area x size
      @param sizeY the Effective area y size
	  @return
	  on success,return QHYCCD_SUCCESS \n
	  another QHYCCD_ERROR code on other failures
  */

extern uint32_t SetQHYCCDStreamMode(qhyccd_handle *handle,uint8_t mode);
/**
 @fn uint32_t SetQHYCCDStreamMode(qhyccd_handle *handle,uint8_t mode)
 @brief Set the camera's mode to chose the way reading data from camera
 @param handle camera control handle
 @param mode the stream mode \n
 0x00:default mode,single frame mode \n
 0x01:live mode \n
 @return
 on success,return QHYCCD_SUCCESS \n
 another QHYCCD_ERROR code on other failures
 */

extern uint32_t InitQHYCCD(qhyccd_handle *handle);
/** \fn uint32_t InitQHYCCD(qhyccd_handle *handle)
      \brief initialization specified camera by camera handle
	  \param handle camera control handle
      \return
	  on success,return QHYCCD_SUCCESS \n
	  on failed,return QHYCCD_ERROR_INITCAMERA \n
	  another QHYCCD_ERROR code on other failures
  */

extern uint32_t GetQHYCCDSDKVersion(uint32_t *year,uint32_t *month,uint32_t *day,uint32_t *subday);

extern uint32_t GetQHYCCDFWVersion(qhyccd_handle *h,uint8_t *buf);
/** @fn uint32_t GetQHYCCDFWVersion(qhyccd_handle *h,uint8_t *buf)
      @brief Get the QHYCCD's firmware version
      @param h camera control handle
	  @param buf buffer for version info
      @return
	  on success,return QHYCCD_SUCCESS \n
 
	  another QHYCCD_ERROR code on other failures
 */

extern uint32_t ExpQHYCCDSingleFrame(qhyccd_handle *handle);
/** \fn uint32_t ExpQHYCCDSingleFrame(qhyccd_handle *handle)
      \brief start to expose one frame
      \param handle camera control handle
      \return
	  on success,return QHYCCD_SUCCESS \n
	  QHYCCD_ERROR_EXPOSING,if the camera is exposing \n
	  QHYCCD_ERROR_EXPFAILED,if start failed \n
	  another QHYCCD_ERROR code on other failures
  */

extern uint32_t GetQHYCCDMemLength(qhyccd_handle *handle);
/** \fn uint32_t GetQHYCCDMemLength(qhyccd_handle *handle)
      \brief get the minimum memory space for image data to save(byte)
      \param handle camera control handle
      \return
	  on success,return the total memory space for image data(byte) \n
	  another QHYCCD_ERROR code on other failures
  */

extern uint32_t GetQHYCCDSingleFrame(qhyccd_handle *handle,uint32_t *w,uint32_t *h,uint32_t *bpp,uint32_t *channels,uint8_t *imgdata);
/**
   @fn uint32_t GetQHYCCDSingleFrame(qhyccd_handle *handle,uint32_t *w,uint32_t *h,uint32_t *bpp,uint32_t *channels,uint8_t *imgdata)
   @brief get live frame data from camera
   @param handle camera control handle
   @param *w pointer to width of ouput image
   @param *h pointer to height of ouput image
   @param *bpp pointer to depth of ouput image
   @param *channels pointer to channels of ouput image
   @param *imgdata image data buffer
   @return
   on success,return QHYCCD_SUCCESS \n
   QHYCCD_ERROR_GETTINGFAILED,if get data failed \n
   another QHYCCD_ERROR code on other failures
 */

extern uint32_t CancelQHYCCDExposingAndReadout(qhyccd_handle *handle);
/**
  @fn uint32_t CancelQHYCCDExposingAndReadout(qhyccd_handle *handle)
  @brief force stop the camera long exposure. And also camera does not send back the image data. Host software must not readout the data. All camera support this mode. 
  @param handle camera control handle
  @return
  on success,return QHYCCD_SUCCESS \n
  another QHYCCD_ERROR code on other failures
  */

