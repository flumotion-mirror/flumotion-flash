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

import os

from flumotion.common.i18n import gettexter, N_
from flumotion.common import errors, messages
from flumotion.component import feedcomponent

T_ = gettexter('flumotion')


class VP6Encoder(feedcomponent.ParseLaunchComponent):
    checkTimestamp = True
    checkOffset = True

    def get_pipeline_string(self, properties):
        return "ffmpegcolorspace ! videoflip method=5 ! fluvp6enc name=encoder"

    def configure_pipeline(self, pipeline, properties):
        element = pipeline.get_by_name('encoder')
        if properties.has_key('encoder-state'):
            element.set_property('encoder-state', properties['encoder-state'])
        if properties.has_key('bitrate'):
            # FIXME: see #2133 to follow up on why all these properties need to get set
            # to get a better bitrate
            element.set_property('bitrate-control', 'cbr')
            element.set_property('drop-frames', 1)
            element.set_property('keyframe-distance', 250)
            element.set_property('spatial-resampling', 1)
            element.set_property('low-resampling-watermark', 30)
            element.set_property('high-resampling-watermark', 40)
            element.set_property('bitrate', int(properties['bitrate'] / 1000))

    def do_setup(self):
        if self.config['properties'].has_key('encoder-state'):
            encoderState = self.config['properties']['encoder-state']

            # validate encoder state file first
            if not os.path.exists(encoderState):
                m = messages.Error(T_(N_(
                  "The configuration property 'encoder-state' should be set to "
                  "an absolute path to an existing MCF configuration file. "
                  "Please fix the configuration, %s does not exist."),
                  encoderState), id='encoder-state')
                self.addMessage(m)
                raise errors.ComponentSetupHandledError()

        return feedcomponent.ParseLaunchComponent.do_setup(self)

