#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Philipp Middendorf'
__email__ = "philipp.middendorf@imr.uni-hannover.de"
__status__ = "Development"

from pyCameras import serverSettings


def ping():
    """ Test server connection """
    return "pong"


def startCameraServer(camera):
    """
    Starts up a xmlrpc server to control a camera of passed camera type.
    Registers different base functions to control settings,
    function definitions can be found in "cameraTemplate.py".

    Parameters
    ----------
    camera : camera object
        This object may be any implemented camera which follows
        the camera template defined in "cameraTemplate.py"
    """

    serverThread = serverSettings.ServerThread()
    server = serverThread.getServer()


    # TODO: edit for camera Server?
    # Setting sequence and fire
    # server.register_function(camera.projectSequence, "projectSequence")
    # # Setting a sequence
    # server.register_function(camera.setSequence, "setSequence")
    # # Fire
    # server.register_function(camera.playSequence, "playSequence")
    # server.register_function(camera.stopSequence, "stopSequence")
    # # Some settings
    # server.register_function(camera.setFeature, "setFeature")
    # server.register_function(camera.getFeature, "getFeature")
    # server.register_function(camera.getFeatures, "getFeatures")
    #
    # server.register_function(camera.setExposure, "setExposure")
    # server.register_function(camera.setInterval, "setInterval")
    # server.register_function(camera.setResolution, "setResolution")
    # server.register_function(camera.setColor, "setColor")
    # server.register_function(camera.setBrightness, "setBrightness")
    # server.register_function(camera.setTriggerMode, "setTriggerMode")
    # Test connection
    server.register_function(ping, "ping")

    serverThread.startServer()
