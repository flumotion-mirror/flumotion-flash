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

from flumotion.component import feedcomponent
from flumotion.common import gstreamer


class AACEncoder(feedcomponent.EncoderComponent):
    checkTimestamp = True
    checkOffset = True

    def get_pipeline_string(self, properties):
        # v2 supports only 16000, 22050, 24000, 32000, 44100, 48000 KHz
        samplerate = properties.get('samplerate', 44100)
        
        ht = properties.get('headers', False) and 1 or 0

        he = properties.get('high-efficiency-version', 2)

        channels = properties.get('channels', 2)

        resampler = 'audioresample'
        if gstreamer.element_factory_exists('legacyresample'):
            resampler = 'legacyresample'

        return "audioconvert ! %s " \
            "! audio/x-raw-int,rate=%d,channels=%d " \
            "! flumcaacenc header-type=%d name=encoder he=%d " \
            "! audio/mpeg,rate=%d" % (resampler, samplerate, channels, ht, he, samplerate)

    def configure_pipeline(self, pipeline, properties):
        self.debug('configure_pipeline')
        element = pipeline.get_by_name('encoder')
        bitrate = properties.get('bitrate')
        if not bitrate:
            self.debug('No bitrate set, using default')
            return

        # the flumcaacenc element accepts bitrate in bits/sec
        self.debug('setting bitrate to %d' % bitrate)
        element.set_property('bitrate', bitrate)
