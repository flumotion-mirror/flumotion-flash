# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
#
# Flumotion - a streaming media server
# Copyright (C) 2008 Fluendo, S.L. (www.fluendo.com).
# All rights reserved.

# Licensees having purchased or holding a valid Flumotion Advanced
# Streaming Server license may use this file in accordance with the
# Flumotion Advanced Streaming Server Commercial License Agreement.
# See "LICENSE.Flumotion" in the source distribution for more information.

# Headers in this file shall remain intact.

import gettext
import os

from flumotion.wizard.basesteps import VideoEncoderStep
from flumotion.wizard.models import VideoEncoder

__version__ = "$Rev$"
_ = gettext.gettext


class VP6VideoEncoder(VideoEncoder):
    component_type = 'vp6-encoder'
    def __init__(self):
        super(VP6VideoEncoder, self).__init__()
        self.has_quality = True
        self.has_bitrate = False

        self.properties.bitrate = 256

    def getProperties(self):
        properties = super(VP6VideoEncoder, self).getProperties()
        #properties['bitrate'] *= 1000
        return properties


class VP6Step(VideoEncoderStep):
    name = 'Windows Media Video Encoder'
    sidebar_name = 'Windows Media Video'
    glade_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'vp6-wizard.glade')
    component_type = 'vp6'

    # WizardStep

    def setup(self):
        self.bitrate.data_type = int

        self.add_proxy(self.model.properties, ['bitrate'])

    def get_next(self):
        return self.wizard.get_step('Encoding').get_audio_page()

    def worker_changed(self):
        self.model.worker = self.worker
        self.wizard.require_elements(self.worker, 'fluvp6enc')


class VP6WizardPlugin(object):
    def __init__(self, wizard):
        self.wizard = wizard
        self.model = VP6VideoEncoder()

    def getConversionStep(self):
        return VP6Step(self.wizard, self.model)
