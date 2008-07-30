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

from flumotion.common.i18n import gettexter, N_
from flumotion.common.messages import Warning
from flumotion.component import feedcomponent

from flumotion.common import errors, gstreamer

T_ = gettexter('flumotion-flash')

class MP3Encoder(feedcomponent.ParseLaunchComponent):
    checkTimestamp = True
    checkOffset = True

    def get_pipeline_string(self, properties):
        if not gstreamer.element_factory_exists('lame'):
            raise errors.MissingElementError('lame')

        rate = properties.get('rate', 44100)
        return "audioconvert ! audioresample " \
            "! audio/x-raw-int,rate=%d ! lame name=encoder " \
            "! audio/mpeg,rate=%d ! mp3parse" % (rate, rate)

    def configure_pipeline(self, pipeline, properties):
        self.debug('configure_pipeline')
        element = pipeline.get_by_name('encoder')
        bitrate = properties.get('bitrate')
        if not bitrate:
            self.debug('No bitrate set, using default')
            return

        # the lame element accepts bitrate in kbits/sec, integer
        # Flumotion handles bitrate in bits/sec, but since there are
        # wrong configs, we accept both and convert as needed
        if bitrate < 1000:
            # assume bitrate is specified in kbit/sec
            m = Warning(
                T_(N_("The configuration specifies the bitrate in kbit/sec "
                    "with a value of '%d'. "
                    "Please update the configuration and specify "
                    "bitrate in bit/sec with a value of '%d'."), bitrate,
                    bitrate * 1000))
            self.addMessage(m)
            bitrate *= 1000

        # now we have it in bit/sec, convert to lame's idea
        bitrate = int(bitrate / 1000)

        self.debug('setting bitrate to %d' % bitrate)
        element.set_property('bitrate', bitrate)
