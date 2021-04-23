#!/usr/bin/python
import numpy as np
from qhpyccd import qhyccd
from astropy.io import fits

cam = qhyccd(gain=200, offset=20)
print("Acquisition start!")
cam.get_image()
print("Acquisition end!")
print(f"Image mean:   {np.mean(cam.image):.2f}")
print(f"Image stddev: {np.std(cam.image):.2f}")
hdu = fits.PrimaryHDU(cam.image)
hdu.writeto('qhyccd.fits', overwrite=True)

