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

from flumotion.admin.assistant.models import VideoEncoder
from flumotion.admin.assistant.interfaces import IEncoderPlugin
from flumotion.wizard.basesteps import VideoEncoderStep

__version__ = "$Rev$"
_ = gettext.gettext


class H264VideoEncoder(VideoEncoder):
    componentType = 'h264-encoder'
    def __init__(self):
        super(H264VideoEncoder, self).__init__()
        self.has_quality = True
        self.has_bitrate = False

        self.properties.bitrate = 256

    def getProperties(self):
        properties = super(H264VideoEncoder, self).getProperties()
        #properties['bitrate'] *= 1000
        return properties


class H264Step(VideoEncoderStep):
    name = 'FlashH264VideoEncoder'
    title = _('Flash H264 Video Encoder')
    sidebarName = _('Flash H264 Video')
    gladeFile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'h264-wizard.glade')
    componentType = 'h264'

    # don't complain about our glade magic
    __pychecker__ = '--no-classattr'

    # WizardStep

    def setup(self):
        self.bitrate.data_type = int

        self.add_proxy(self.model.properties, ['bitrate'])

    def workerChanged(self, worker):
        self.model.worker = worker
        self.wizard.requireElements(worker, 'x264enc')


class H264WizardPlugin(object):
    implements(IEncoderPlugin)
    def __init__(self, wizard):
        self.wizard = wizard
        self.model = H264VideoEncoder()

    def getConversionStep(self):
        return H264Step(self.wizard, self.model)