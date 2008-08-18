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

from zope.interface import implements

from flumotion.wizard.basesteps import VideoEncoderStep
from flumotion.wizard.interfaces import IEncoderPlugin
from flumotion.wizard.models import VideoEncoder

__version__ = "$Rev$"
_ = gettext.gettext


class FLVVideoEncoder(VideoEncoder):
    componentType = 'flv-encoder'
    def __init__(self):
        super(FLVVideoEncoder, self).__init__()
        self.has_quality = True
        self.has_bitrate = False

        self.properties.bitrate = 300

    def getProperties(self):
        properties = super(FLVVideoEncoder, self).getProperties()
        properties['bitrate'] *= 1000
        return properties


class FLVStep(VideoEncoderStep):
    name = 'FLVEncoder'
    title = _('FLV Encoder')
    sidebarName = _('FLV')
    gladeFile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'flv-wizard.glade')
    componentType = 'flv'

    # don't complain about our glade magic
    __pychecker__ = '--no-classattr'

    # WizardStep

    def setup(self):
        self.bitrate.data_type = int

        self.add_proxy(self.model.properties, ['bitrate'])

    def workerChanged(self, worker):
        self.model.worker = worker
        self.wizard.requireElements(worker, 'ffenc_flv')


class FLVWizardPlugin(object):
    implements(IEncoderPlugin)
    def __init__(self, wizard):
        self.wizard = wizard
        self.model = FLVVideoEncoder()

    def getConversionStep(self):
        return FLVStep(self.wizard, self.model)