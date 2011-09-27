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
        return "ffmpegcolorspace ! flumch264enc name=encoder"

    def configure_pipeline(self, pipeline, properties):
        self.debug('configure_pipeline')
        element = pipeline.get_by_name('encoder')
        props = ('bitrate',)
        for p in props:
            self._set_property(p, properties.get(p), element)

    def _set_property(self, prop, value, element):
        if not value:
            self.debug('No %s set, using default value' % prop)
            return
        if prop == 'bitrate':
            v = int(value)
            self.debug("Setting bitrate to %s" % value)
            element.set_property(prop, value)
            return
        self.debug("Setting %s to %d" %(prop, value))
        element.set_property(prop, value)
