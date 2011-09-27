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

from flumotion.common import messages, errors
from flumotion.component import feedcomponent
from flumotion.common.i18n import N_, gettexter

T_ = gettexter()

class H264Encoder(feedcomponent.ParseLaunchComponent):
    checkTimestamp = True
    checkOffset = True

    profiles = {
            'base' : 0, 'cif' : 1, 'main' : 2, 'svcd' : 3, 'd1' : 4,
            'high' : 5, 'dvd' : 6, 'hddvd' : 7, 'bd' : 8, 'bdmain' : 9,
            'psp' : 10, '720p' : 11, '1080i' : 12, 'ipod' : 13, 'avchd' : 14,
            'iphone' : 15, '1seg' : 16, 'psp_480_270' : 20, 'psp_640_480': 21,
            'divx' : 22, 'flash_low' : 23, 'flash_high' : 24}

    def get_pipeline_string(self, properties):
        return "ffmpegcolorspace ! flumch264enc name=encoder"

    def configure_pipeline(self, pipeline, properties):
        self.debug('configure_pipeline')
        element = pipeline.get_by_name('encoder')
        props = ('bitrate', 'keyframe-distance', 'profile')
        for p in props:
            self._set_property(p, properties.get(p), element)

    def _set_property(self, prop, value, element):
        if value is None:
            self.debug('No %s set, using default value', prop)
            return
        if prop in ['bitrate', 'keyframe-distance']:
            self.debug("Setting %s to %s", prop, value)
        if prop == 'profile':
            if value not in self.profiles:
                m = messages.Error(T_(N_(
                    "The profile '%s' does not match any of the encoder's "
                    "available profiles"), value), mid='profile')
                self.addMessage(m)
                raise errors.ComponentSetupHandledError()
            self.debug("Setting h264 '%s' profile", value)
            value = self.profiles[value]
        element.set_property(prop, value)
