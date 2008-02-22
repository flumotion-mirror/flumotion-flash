# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
#
# Flumotion - a streaming media server
# Copyright (C) 2004,2005,2006,2007,2008 Fluendo, S.L. (www.fluendo.com).
# All rights reserved.

# This file may be distributed and/or modified under the terms of
# the GNU General Public License version 2 as published by
# the Free Software Foundation.
# This file is distributed without any warranty; without even the implied
# warranty of merchantability or fitness for a particular purpose.
# See "LICENSE.GPL" in the source distribution for more information.

# Licensees having purchased or holding a valid Flumotion Advanced
# Streaming Server license may use this file in accordance with the
# Flumotion Advanced Streaming Server Commercial License Agreement.
# See "LICENSE.Flumotion" in the source distribution for more information.

# Headers in this file shall remain intact.

"""XXX
"""

from flumotion.wizard.models import HTTPServer, HTTPPlug

__version__ = "$Rev$"


class FlashHTTPPlug(HTTPPlug):
    """I am a model representing the configuration file for a
    Flash HTTP streaming plug.
    """
    plug_type = "flash-http-plug"
    socket = "flumotion.component.misc.cortado.cortado.FlashPlug"

    # Component

    def getProperties(self):
        p = super(FlashHTTPPlug, self).getProperties()

        p['stream-url'] = self.streamer.getURL()
        p['has-video'] = self.video_producer is not None
        p['has-audio'] = self.audio_producer is not None

        return p


class FlashHTTPServer(HTTPServer):
    """I am a model representing the configuration file for a
    HTTP server component which will be used to serve a flash file.
    Most of the interesting logic here is actually in a plug.
    """
    component_type = 'http-server'
    def __init__(self, streamer, audio_producer, video_producer, mount_point):
        """
        @param streamer: streamer
        @type  streamer: L{HTTPStreamer}
        @param audio_producer: audio producer
        @type  audio_producer: L{flumotion.wizard.models.AudioProducer}
           subclass or None
        @param video_producer: video producer
        @type  video_producer: L{flumotion.wizard.models.VideoProducer}
           subclass or None
        @param mount_point:
        @type  mount_point:
        """
        self.streamer = streamer

        super(FlashHTTPServer, self).__init__(mount_point=mount_point,
                                              worker=streamer.worker)

        self.properties.porter_socket_path = streamer.socket_path
        self.properties.porter_username = streamer.porter_username
        self.properties.porter_password = streamer.porter_password
        self.properties.port = streamer.properties.port
        self.properties.type = 'slave'

        plug = FlashHTTPPlug(self, streamer, audio_producer, video_producer)
        self.addPlug(plug)

    def getCodebase(self):
        """Returns the base of directory of the applet
        @returns: directory
        """
        return 'http://%s:%d%s' % (self.worker,
                                   self.properties.port,
                                   self.properties.mount_point)


class FlashHTTPWizardPlugin(object):
    def __init__(self, wizard):
        self.wizard = wizard

    def getConsumer(self, streamer, audio_producer, video_producer):
        return FlashHTTPServer(streamer, audio_producer,
                               video_producer, "/flash/")
