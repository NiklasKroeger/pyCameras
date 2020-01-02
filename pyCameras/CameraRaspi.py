#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Tim Betker"
__copyright__ = "Copyright 2018, LUH: IMR"
# __credits__ = [""]
__license__ = "closed-source"
__version__ = "0.2"
__maintainer__ = "Tim Betker"
__email__ = "tim.betker@imr.uni-hannover.de"
__status__ = "alpha"
__package_name__ = "pyProjectors"
__developer__ = __author__

from pyCameras.cameraTemplate import CameraTemplate
from pyCameras.cameraTemplate import ControllerTemplate
import pyCameras.serverFunctions as serverThread
import time
import Picamera
import smbus

LOGGING_LEVEL = None


class Controller(ControllerTemplate):
    """
    Implementation of a generic usb camera controller
    """
    def __init__(self, num_of_cams=1):
        """
        Controller to handle device detection and interaction before actually
        opening the camera

        Parameters
        ----------
        num_of_cams : int
            Expected number of cameras currently connected. Default = 4
        """
        super(Controller, self).__init__()
        self.logger = logging.getLogger(__name__)
        if LOGGING_LEVEL is not None:
            self.logger.setLevel(LOGGING_LEVEL)
        self.logger.debug('Starting usb Camera Controller')
        self.num_of_cams = num_of_cams
        self.device_handles = []


    def updateDeviceHandles(self):
        """
        Update the list of available device handles by trying to open the first
        self.num_of_cams and stopping at the first error
        """
        self.logger.debug('Searching for usb camera devices')
        self.device_handles = []
        for i in range(self.num_of_cams):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                self.device_handles.append(i)
                cap.release()
            else:
                break
        self.logger.debug('Found {num} usb camera devices: {devices}'
                          ''.format(num=len(self.device_handles),
                                    devices=self.device_handles))

    def getDevice(self, device_handle):
        """
        Open the actual capture device to grab images

        Parameters
        ----------
        device_handle
            One entry of the device list returned by self.listDevices()

        Returns
        -------
        The capture device of type usbCamera
        """
        self.logger.debug('Opening device {device_handle}'
                          ''.format(device_handle=device_handle))
        return Camera(device_handle=device_handle)

    def closeController(self):
        """Delete all detected devices"""
        for cap in self.device_handles:
            del cap

    def __repr__(self):
        return "<Raspi Camera Controller>"


class Camera(CameraTemplate):
    """
    Implements the LCR4500 projector.
    """
    def __init__(self, device_handle):
        """
        Initializes projector interface to communicate with LCR4500.

        This class may be used as interface for the server or as a standalone projector object which supports the same
        functionality as the server.
        """
        super(Camera, self).__init__(device_handle)

        if LOGGING_LEVEL is not None:
            self.logger.setLevel(LOGGING_LEVEL)

        self.openDevice()
        self.framerate = 30

        self.rawCap = PiRGBArray(self.device)

        self.device.raw_format = "bgr"

        self.device.image_denoise = True

        self.device.flash_mode ='off'

        self.device.framerate = self.framerate

        self.device.awb_mode = 'auto'

        self.device.exposure_mode ='auto'

        self.device.awb_mode = 'off'

        self.device.awb_gains = (1.7, 1.8)

        self.device.iso = 100

    def openDevice(self):
        """
        Open the device by using self.device_handle and store the device in
        self.device
        """
        try:
            self.logger.debug('Opening camera device')
            self.device = Picamera()
        except Exception as e:
            self.logger.exception('Failed to open the camera device: '
                                  '{e}'.format(e=e))


    def closeDevice(self):
        """
        Closes camera device
        """
        try:
            self.logger.debug('Closing camera device')
            self.device.closeCamera()
        except Exception as e:
            self.logger.exception('Failed to close the camera device: '
                                  '{e}'.format(e=e))


    def captureSequence(self, numstr):
        try:
            print("Capture Sequence of ", numstr, "Images")
            img = []
            rawCaplist = [PiRGBArray(self.device) for i in range(int(numstr))]

            self.device.capture_sequence(rawCaplist, format="raw", use_video_port=True)

            return rawCaplist

        except Exception:

            print("Capture Sequence not succesfull")

            self.closeDevice()




    def setResolution(self, numstr):
        print(len(numstr))

        if len(numstr) > 6:

            width = int(numstr[0:4])

            height = int(numstr[4:8])

            print("Setting Resolution to ", width, "x", height)

            self.cam.resolution = (width, height)

        else:

            width = int(numstr[0:3])

            height = int(numstr[3:len(numstr)])

            print("Setting Resolution to ", width, "x", height)

            self.cam.resolution = (width, height)

        return


    def setExposure(self, numstr):
        print("Setting Exposure to", numstr)

        self.device.shutter_speed = int(numstr)

        return


    # def captureStream(self):
    #     numstr = 5
    #
    #     start_time = time.time()
    #
    #     self.start_recording('my_video.h264')
    #
    #     self.wait_recording(5)
    #
    #     self.stop_recording()
    #
    #     capture_time = time.time() - start_time
    #
    #     print("capture time is", capture_time)
    #
    #     print("fps is", int(numstr) / capture_time)


def setTriggermode(self, numstr):
    try:
        Dataset = bus.write_byte(address, int(numstr))
        print("Raspberry Schickt folgende Zahlen: ", numstr)
        time.sleep(0.1)
        received = bus.read_byte(address)
        print("Arduino received Frametime of: ", received)

    except Exception:
        print("Setting Triggermode not succesfull")
        if self.device is not None:
            self.closeDevice()


# def getTestSequence():
#     return [{'type': 'sinusoidal',
#              'frequency': 1,
#              'phase': 0,
#              'direction': 'x'},
#             {'type': 'sinusoidal',
#              'frequency': 6,
#              'phase': 0,
#              'direction': 'x'},
#             {'type': 'sinusoidal',
#              'frequency': 36,
#              'phase': 0,
#              'direction': 'x'},
#             {'type': 'sinusoidal',
#              'frequency': 1,
#              'phase': 0,
#              'direction': 'y'},
#             {'type': 'sinusoidal',
#              'frequency': 6,
#              'phase': 0,
#              'direction': 'y'},
#             {'type': 'sinusoidal',
#              'frequency': 36,
#              'phase': 0,
#              'direction': 'y'}
#             ]


# def develop():
#     """
#     Helper function to allow simple switching between developing and regular
#     use case
#     """
#     pro = Projector(None)
#     pro.setFeature('exposure', 300000)
#     pro.setFeature('interval', 500000)
#     pro.setFeature('brightness', 0.3)
#     pro.setSequence(getTestSequence())
#     pro.playSequence()


def xmlServe():
    """
    Serve the Picamera as xmlrpc server
    """
    cam = Camera(None)
    serverThread.startCameraServer(cam)


if __name__ == "__main__":
    """
    Uncomment or comment desired use case:
        develop : Used to develop the projector implementation, debugging and so on...
        xmlServe : Starts up a xmlrpc server using this projector class 
    """
    import logging

    logging.basicConfig(level=logging.DEBUG)

    # develop()
    xmlServe()
