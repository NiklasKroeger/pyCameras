#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Philipp Middendorf'
__email__ = "philipp.middendorf@imr.uni-hannover.de"
__status__ = "Development"

# with pip install future
try:
    from xmlrpc.server import DocXMLRPCServer, DocXMLRPCRequestHandler
except ImportError:
    pass
    # from DocXMLRPCServer import DocXMLRPCServer, DocXMLRPCRequestHandler
    # TODO: check this error

# requires pip install configparser
from configparser import ConfigParser
import base64
import threading
import os


class AuthorizationRequestHandler(DocXMLRPCRequestHandler):
    def do_POST(self):
        """ Extends the do_POST function by checking the authorization """
        if 'Authorization' in self.headers or 'authorization' in self.headers:
            config = ConfigParser()
            config.read('serv.cfg')

            header = self.headers['Authorization']
            t, user_pwd = header.split()
            username, password = base64.decodebytes(bytes(user_pwd, 'utf-8')).decode('utf-8').split(':')
            # print "Given: " , username, password
            if True or username == config.get('xmlrpc', 'user') and password == config.get('xmlrpc', 'password'):
                super(AuthorizationRequestHandler, self).do_POST()
            else:
                self.send_error(403)
        else:
            self.send_error(401)


class ServerThread(threading.Thread):
    def __init__(self):
        """ Creates a server thread. Used for projector servers. """
        super(ServerThread, self).__init__()
        print('Server init')

        # Read serv.cfg file
        config = ConfigParser()
        fpath, fname = os.path.split(os.path.realpath(__file__))
        config_fname = fpath + '/serv.cfg'
        config.read(config_fname)
        # 0.0.0.0 allows all IPs
        hostname = '0.0.0.0'    # Old hostname: socket.gethostbyname(socket.gethostname())
        port = config.getint('xmlrpc', 'port')

        print('Setting up server at %s port %i' % (hostname, port))
        self.server = DocXMLRPCServer((hostname, port), AuthorizationRequestHandler, allow_none=True)
        self.server.register_introspection_functions()
        self.server.set_server_name('pyCamera')
        self.server.set_server_title('Camera Signal Provider')

    def __del__(self):
        print('Server destructor')

    def getServer(self):
        return self.server

    def startServer(self):
        """
        start server and beforehand register some instances to operate with
        """
        self.start()

    def run(self):
        print('Starting server thread')
        self.server.serve_forever()
        print('Finished server thread')
