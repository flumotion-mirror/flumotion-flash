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

from flumotion.common import gstreamer, messages, errors
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
        #FIXME: Default profile should be 'base' but we use 'flash_high'
        profile = properties.get('profile')
        if profile is None:
            m = messages.Warning(
                T_(N_("Encoding profile not specified. Using 'flash_high' "
                    "as default.\n")))
            self.addMessage(m)
            profile = 'flash_high'
        self._set_property('profile', profile, element)
        props = ('bitrate', 'byte-stream', 'max-keyframe-distance',
                'min-keyframe-distance')
        for p in props:
            self._set_property(p, properties.get(p), element)

    def _set_property(self, prop, value, element):
        if value is None:
            self.debug('No %s set, using default value', prop)
            return
        if prop == 'bitrate':
            self.debug("Setting bitrate to %s", value)
            element.set_property(prop, value)
        if prop == 'byte-stream':
            if value == True:
                self.debug("Setting byte-stream format")
                element.set_property('es', 1)
        if prop in ('max-keyframe-distance', 'min-keyframe-distance'):
            if gstreamer.get_plugin_version('flumch264enc') <= (0, 10, 5, 0):
                m = messages.Warning(
                    T_(N_("Versions up to and including %s of the '%s' "
                        "cannot set this property.\n"),
                        '0.10.5', 'flumch264enc'))
                self.addMessage(m)
                return
            self.debug("Setting %s to %s", prop, value)
            element.set_property(prop, value)
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
            # Adobe recommends using a keyframe distance equivalent to 10
            # seconds and the GStreamer component doesn't set it. For live
            # we want to have at least on keyframe each 3 seconds
            # See priv#7131
            if value in [23, 24]:
                #FIXME: Supposing we have a PAL input with 25fps
                element.set_property('max-keyframe-distance', 75)
