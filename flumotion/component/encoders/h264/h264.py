# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

# Flumotion - a streaming media server
# Copyright (C) 2004,2005,2006,2007,2008,2009 Fluendo, S.L.
# Copyright (C) 2010,2011 Flumotion Services, S.A.
# All rights reserved.
#
# This file may be distributed and/or modified under the terms of
# the GNU Lesser General Public License version 2.1 as published by
# the Free Software Foundation.
# This file is distributed without any warranty; without even the implied
# warranty of merchantability or fitness for a particular purpose.
# See "LICENSE.LGPL" in the source distribution for more information.
#
# Headers in this file shall remain intact.

from flumotion.common import messages
from flumotion.component import feedcomponent

class H264Encoder(feedcomponent.ParseLaunchComponent):
    checkTimestamp = True
    checkOffset = True

    def get_pipeline_string(self, properties):
        self.debug("Blah...")
        return "ffmpegcolorspace ! x264enc me=3 subme=6 name=encoder"

    def configure_pipeline(self, pipeline, properties):
        self.debug('configure_pipeline blah blah')
        element = pipeline.get_by_name('encoder')
        props = ('bitrate', 'speed', 'threads')
        for p in props:
            self._set_property(p, properties.get(p), element)

    def _set_property(self, prop, value, element):
        if not value:
            self.debug('No %s set, using default value' % prop)
            return
        if prop == 'bitrate':
            # GStreamer 0.10 has bitrate in kbps, inconsistent
            # with all other elements, so fix it up
            v = int(value/1000)
            self.debug("Setting bitrate to %s" % value)
            element.set_property(prop, value)
            return
        if prop == 'speed':
            me = 3
            subme = 6
            self.debug("Setting me, subme to %d, %d" %(me, subme))
            element.set_property('me', me)
            element.set_property('subme', subme)
            return
        self.debug("Setting %s to %d" %(prop, value))
        element.set_property(prop, value)
