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

import gettext
import os

from zope.interface import implements

from flumotion.admin.assistant.models import VideoEncoder
from flumotion.admin.assistant.interfaces import IEncoderPlugin
from flumotion.admin.gtk.basesteps import VideoEncoderStep

__version__ = "$Rev$"
_ = gettext.gettext


class H264VideoEncoder(VideoEncoder):
    componentType = 'h264-encoder'

    def init(self):
        self.has_bitrate = False

        self.properties.bitrate = 256

    def getProperties(self):
        properties = super(H264VideoEncoder, self).getProperties()
        properties.bitrate *= 1000
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
        self.wizard.requireElements(worker, 'flumch264enc')


class H264WizardPlugin(object):
    implements(IEncoderPlugin)

    def __init__(self, wizard):
        self.wizard = wizard
        self.model = H264VideoEncoder()

    def getConversionStep(self):
        return H264Step(self.wizard, self.model)
