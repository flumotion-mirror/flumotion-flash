# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
#
# Flumotion - a streaming media server
# Copyright (C) 2008 Fluendo, S.L. (www.fluendo.com).
# All rights reserved.

# Licensees having purchased or holding a valid Flumotion Advanced
# Streaming Server license may use this file in accordance with the
# Flumotion Advanced Streaming Server Commercial License Agreement.
# See "LICENSE.Flumotion" in the source distribution for more information.

# Headers in this file shall remain intact.

"""Wizard plugin for the flashhttp plug
"""

from zope.interface import implements

from flumotion.admin.assistant.interfaces import IHTTPConsumerPlugin
from flumotion.admin.assistant.models import HTTPServer, HTTPPlug

__version__ = "$Rev$"

# Copied from posixpath.py
def slashjoin(a, *p):
    """Join two or more pathname components, inserting '/' as needed"""
    path = a
    for b in p:
        if b.startswith('/'):
            path = b
        elif path == '' or path.endswith('/'):
            path +=  b
        else:
            path += '/' + b
    return path


class FlashHTTPPlug(HTTPPlug):
    """I am a model representing the configuration file for a
    Flash HTTP streaming plug.
    """
    plugType = "flash-http-plug"

    # Component

    def getProperties(self):
        p = super(FlashHTTPPlug, self).getProperties()

        p['stream-url'] = self.streamer.getURL()
        p['has-video'] = self.videoProducer is not None
        p['has-audio'] = self.audioProducer is not None

        return p


class FlashHTTPServer(HTTPServer):
    """I am a model representing the configuration file for a
    HTTP server component which will be used to serve a flash file.
    Most of the interesting logic here is actually in a plug.
    """
    componentType = 'http-server'
    def __init__(self, streamer, audioProducer, videoProducer, mountPoint):
        """
        @param streamer: streamer
        @type  streamer: L{HTTPStreamer}
        @param audioProducer: audio producer
        @type  audioProducer: L{flumotion.admin.gtk.models.AudioProducer}
           subclass or None
        @param videoProducer: video producer
        @type  videoProducer: L{flumotion.admin.gtk.models.VideoProducer}
           subclass or None
        @param mountPoint:
        @type  mountPoint:
        """
        self.streamer = streamer

        super(FlashHTTPServer, self).__init__(mountPoint=mountPoint,
                                              worker=streamer.worker)

        porter = streamer.getPorter()
        self.properties.porter_socket_path = porter.getSocketPath()
        self.properties.porter_username = porter.getUsername()
        self.properties.porter_password = porter.getPassword()
        self.properties.port = porter.getPort()
        self.properties.type = 'slave'

        plug = FlashHTTPPlug(self, streamer, audioProducer, videoProducer)
        self.addPlug(plug)

    def getCodebase(self):
        """Returns the base of directory of the applet
        @returns: directory
        """
        return 'http://%s:%d%s' % (self.streamer.hostname,
                                   self.properties.port,
                                   self.properties.mountPoint)

    # Component

    def getProperties(self):
        properties = super(FlashHTTPServer, self).getProperties()
        hostname = self.streamer.getHostname()
        if hostname:
            properties.hostname = hostname
        return properties


class FlashHTTPWizardPlugin(object):
    implements(IHTTPConsumerPlugin)
    def __init__(self, wizard):
        self.wizard = wizard

    def workerChanged(self, worker):
        d = self.wizard.runInWorker(
            worker,
            'flumotion.component.plugs.flashhttp.workercheck',
            'checkFlashPlayer')
        def check(found):
            return bool(found)
        d.addCallback(check)
        return d

    def getConsumer(self, streamer, audioProducer, videoProducer):
        mountPoint = slashjoin(streamer.properties.mount_point,
                                "flash/")
        return FlashHTTPServer(streamer, audioProducer,
                               videoProducer, mountPoint)
