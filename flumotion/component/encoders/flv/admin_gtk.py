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

from flumotion.admin.gtk.basesteps import VideoEncoderStep
from flumotion.admin.gtk.interfaces import IEncoderPlugin
from flumotion.admin.gtk.models import VideoEncoder

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
