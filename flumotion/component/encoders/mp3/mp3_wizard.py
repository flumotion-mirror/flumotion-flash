# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
#
# Flumotion - a streaming media server
# Copyright (C) 2008 Fluendo, S.L. (www.fluendo.com).
# All rights reserved.

# This file may be distributed and/or modified under the terms of
# the GNU General Public License version 2 as published by
# the Free Software Foundation.
# This file is distributed without any warranty; without even the implied
# warranty of merchantability or fitness for a particular purpose.
# See "LICENSE.GPL" in the source distribution for more information.

# Licensees having purchased or holding a valid Flumotion Advanced
# Streaming Server license may use this file in accordance with the
# Flumotion Advanced Streaming Server Commercial License Agreement.
# See "LICENSE.Flumotion" in the source distribution for more information.

# Headers in this file shall remain intact.

from flumotion.wizard.basesteps import AudioEncoderStep
from flumotion.wizard.models import AudioEncoder

__version__ = "$Rev$"


class MP3AudioEncoder(AudioEncoder):
    component_type = 'mp3-encoder'

    def __init__(self):
        super(MP3AudioEncoder, self).__init__()

        self.properties.bitrate = 64

    def getProperties(self):
        properties = super(MP3AudioEncoder, self).getProperties()
        properties['bitrate'] *= 1000
        return properties


class MP3Step(AudioEncoderStep):
    name = 'MP3 encoder'
    sidebar_name = 'MP3'
    component_type = 'mp3'

    # WizardStep

    def setup(self):
        self.bitrate.set_range(5, 128)
        self.bitrate.set_value(64)

        self.bitrate.data_type = int

        self.add_proxy(self.model.properties, ['bitrate'])

    def worker_changed(self):
        self.model.worker = self.worker
        self.wizard.require_elements(self.worker, 'mp3parse')


class MP3WizardPlugin(object):
    def __init__(self, wizard):
        self.wizard = wizard
        self.model = MP3AudioEncoder()

    def getConversionStep(self):
        return MP3Step(self.wizard, self.model)
