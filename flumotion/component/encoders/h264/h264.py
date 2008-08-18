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

from flumotion.common import messages
from flumotion.common.i18n import N_, gettexter
from flumotion.component import feedcomponent

T_ = gettexter()

class H264Encoder(feedcomponent.ParseLaunchComponent):
    checkTimestamp = True
    checkOffset = True

    def get_pipeline_string(self, properties):
        return "ffmpegcolorspace ! x264enc me=3 subme=6 name=encoder"

    def configure_pipeline(self, pipeline, properties):
        self.debug('configure_pipeline')
        element = pipeline.get_by_name('encoder')
        bitrate = properties.get('bitrate')
        if not bitrate:
            self.debug('No bitrate set, using default')
            return

        if bitrate < 10000:
            self.addMessage(
                messages.Warning(T_(N_(
                    "Your configuration uses 'bitrate' expressed in "
                    "kbit/sec.  Please convert it to a value in bit/sec by"
                    " multiplying the value by 1000.")), mid='bitrate'))
            bitrate *= 1000

        # FIXME: GStreamer 0.10 has bitrate in kbps, inconsistent
        # with all other elements, so fix it up
        value = int(bitrate/1000)

        self.debug('setting bitrate to %d' % value)
        element.set_property('bitrate', value)
