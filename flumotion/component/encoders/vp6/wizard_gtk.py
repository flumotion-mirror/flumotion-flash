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


class VP6VideoEncoder(VideoEncoder):
    componentType = 'vp6-encoder'

    def __init__(self):
        super(VP6VideoEncoder, self).__init__()
        self.has_quality = True
        self.has_bitrate = False

        self.properties.bitrate = 256

    def getProperties(self):
        properties = super(VP6VideoEncoder, self).getProperties()
        properties['bitrate'] *= 1000
        return properties


class VP6Step(VideoEncoderStep):
    name = 'FlashVP6VideoEncoder'
    title = _('Flash VP6 Video Encoder')
    sidebarName = _('Flash VP6 Video')
    gladeFile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'vp6-wizard.glade')
    componentType = 'vp6'

    # don't complain about our glade magic
    __pychecker__ = '--no-classattr'

    # WizardStep

    def setup(self):
        self.bitrate.data_type = int

        self.add_proxy(self.model.properties, ['bitrate'])

    def workerChanged(self, worker):
        self.model.worker = worker
        self.wizard.requireElements(worker, 'fluvp6enc')


class VP6WizardPlugin(object):
    implements(IEncoderPlugin)

    def __init__(self, wizard):
        self.wizard = wizard
        self.model = VP6VideoEncoder()

    def getConversionStep(self):
        return VP6Step(self.wizard, self.model)
