#!/usr/bin/env python3
__author__ = 'Philipp Middendorf'
__email__ = "philipp.middendorf@imr.uni-hannover.de"
__status__ = "Development"

import xmlrpc.client


# This function contradicts the usual naming convention - This is necessary to make usage of projector classes
# and servers the same when choosing a class. (Capitalization stays the same)
# TODO: Wrap property functions by expanding the class. Making use of a self.cam_client variable
def Camera(settings_dict):
    """
    Function to mime the camera objects. Makes it possible for the configLoader to simply call this function
    to connect to the server with given parameters.

    Parameters
    ----------
    settings_dict : dict
        Dictionary containing user, password, host and port for the connection

    Returns
    -------
    camera : ServerProxy
        ServerProxy to the server

    """
    try:
        camera = xmlrpc.client.ServerProxy('http://{user}:{password}@{host}:{port}'
                                              ''.format(user=settings_dict['user'],
                                                        password=settings_dict['password'],
                                                        host=settings_dict['host'],
                                                        port=settings_dict['port']))
    except KeyError:
        raise KeyError("Given server settings dictionary not working. "
                       "Content must be <user>, <password>, <host> and <port> ")

    return camera
