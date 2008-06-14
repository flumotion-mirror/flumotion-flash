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

class AACEncoder(feedcomponent.ParseLaunchComponent):
    checkTimestamp = True
    checkOffset = True

    def get_pipeline_string(self, properties):
        rate = properties.get('rate', 44100)
        return "audioconvert ! audioresample " \
            "! audio/x-raw-int,rate=%d " \
            "! flumcaacenc header-type=0 name=encoder " \
            "! audio/mpeg,rate=%d" % (rate, rate)

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
