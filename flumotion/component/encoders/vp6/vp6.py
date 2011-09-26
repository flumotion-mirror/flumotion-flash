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

import os

from flumotion.common.i18n import gettexter, N_
from flumotion.common import errors, messages
from flumotion.component import feedcomponent

T_ = gettexter('flumotion')


class VP6Encoder(feedcomponent.EncoderComponent):
    checkTimestamp = True
    checkOffset = True

    def get_pipeline_string(self, properties):
        return "ffmpegcolorspace ! videoflip method=5 ! fluvp6enc name=encoder"

    def configure_pipeline(self, pipeline, properties):
        element = pipeline.get_by_name('encoder')
        if 'encoder-state' in properties:
            element.set_property('encoder-state', properties['encoder-state'])
        if 'bitrate' in properties:
            element.set_property('bitrate', int(properties['bitrate'] / 1000))

    def do_setup(self):
        if 'encoder-state' in self.config['properties']:
            encoderState = self.config['properties']['encoder-state']

            # validate encoder state file first
            if not os.path.exists(encoderState):
                m = messages.Error(T_(N_(
                  "The configuration property 'encoder-state' should be set to"
                  " an absolute path to an existing MCF configuration file. "
                  "Please fix the configuration, %s does not exist."),
                  encoderState), id='encoder-state')
                self.addMessage(m)
                raise errors.ComponentSetupHandledError()

        return feedcomponent.ParseLaunchComponent.do_setup(self)
