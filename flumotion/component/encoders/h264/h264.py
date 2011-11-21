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


class H264Encoder(feedcomponent.EncoderComponent):
    checkTimestamp = True
    checkOffset = True

    profiles = [
            'base', 'cif', 'main', 'svcd', 'd1', 'high', 'dvd', 'hddvd', 'bd',
            'bdmain', 'psp', '720p', '1080i', 'ipod', 'avchd', 'iphone',
            '1seg', 'psp_480_270', 'psp_640_480', 'divx', 'flash_low',
            'flash_high']

    bitrate_mode = ['cbr', 'cqt', 'vbr']
    sync_on_offset= False

    def get_pipeline_string(self, properties):
        return ("ffmpegcolorspace ! flumch264enc max-keyframe-distance=125"
                " name=encoder")

    def configure_pipeline(self, pipeline, properties):
        self.debug('configure_pipeline')
        element = pipeline.get_by_name('encoder')

        profile = properties.get('profile')
        if profile is None:
            m = messages.Warning(
                T_(N_("Encoding profile not specified. Using 'main' "
                    "as default.\n")))
            self.addMessage(m)
            profile = 'main'
        self._set_property('profile', profile, element)

        maxKFDistance = properties.get('max-keyframe-distance')
        minKFDistance = properties.get('min-keyframe-distance')
        self._kfDistance = 0
        if maxKFDistance == minKFDistance:
            self._kfDistance = maxKFDistance

        props = ('bitrate', 'bitrate-mode', 'byte-stream',
                'max-keyframe-distance', 'min-keyframe-distance')

        for p in props:
            self._set_property(p, properties.get(p), element)
        # Default to a maximum of 4 threads
        self._set_property('threads', properties.get('threads', 4), element)
        # for max-bitrate use in this order: 'max-bitrate', 'bitrate' or None
        self._set_property('max-bitrate',
            properties.get('max-bitrate', properties.get('bitrate', None)),
            element)

    def _set_property(self, prop, value, element):
        if value is None:
            self.debug('No %s set, using default value', prop)
            return

        if prop == 'bitrate':
            self.debug("Setting bitrate to %s", value)
            element.set_property(prop, value)
        if prop == 'max-bitrate':
            self.debug("Setting max bitrate to %s", value)
            element.set_property(prop, value)
        if prop == 'bitrate-mode':
            if value not in self.bitrate_mode:
                m = messages.Error(T_(N_(
                    "The bitrate mode '%s' does not match any "
                    "of the encoder's "
                    "available modes"), value), mid='profile')
                self.addMessage(m)
                raise errors.ComponentSetupHandledError()
            self.debug("Setting bitrate mode to %s", value)
            element.set_property(prop, value)
        if prop == 'byte-stream':
            if value is True:
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
            element.set_property(prop, value)
            # Adobe recommends using a keyframe distance equivalent to 10
            # seconds and the GStreamer component doesn't set it. For live
            # we want to have at least on keyframe each 3 seconds
            # See priv#7131
            if value in ['flash_high', 'flash_low']:
                #FIXME: Supposing we have a PAL input with 25fps
                element.set_property('max-keyframe-distance', 75)

    def modify_property_Bitrate(self, value):
        if not self.checkPropertyType('bitrate', value, int):
            return False
        self.modify_element_property('encoder', 'bitrate', value)
        return True
