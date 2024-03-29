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

from flumotion.common.i18n import gettexter, N_
from flumotion.common.messages import Warning
from flumotion.component import feedcomponent

from flumotion.common import errors, gstreamer

T_ = gettexter('flumotion-flash')


class MP3Encoder(feedcomponent.EncoderComponent):
    checkTimestamp = True
    checkOffset = True

    def get_pipeline_string(self, properties):
        if gstreamer.element_factory_exists('lame'):
            encoder = 'lame'
        elif gstreamer.element_factory_exists('flump3enc'):
            encoder = 'flump3enc'
        else:
            raise errors.MissingElementError('flump3enc')

        resampler = 'audioresample'
        if gstreamer.element_factory_exists('legacyresample'):
            resampler = 'legacyresample'

        samplerate = properties.get('samplerate', 44100)
        return "audioconvert ! %s " \
            "! audio/x-raw-int,rate=%d ! %s name=encoder " \
            "! audio/mpeg,rate=%d ! mp3parse" % (resampler, samplerate,
                                                 encoder, samplerate)

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
