/**
 * @brief CONTROL_ID enum define
 *
 * List of the function could be control
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

