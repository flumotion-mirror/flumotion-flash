# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
#
# Flumotion - a streaming media server
# Copyright (C) 2004,2005,2006,2008 Fluendo, S.L. (www.fluendo.com).
# All rights reserved.

# Licensees having purchased or holding a valid Flumotion Advanced
# Streaming Server license may use this file in accordance with the
# Flumotion Advanced Streaming Server Commercial License Agreement.
# See "LICENSE.Flumotion" in the source distribution for more information.

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
