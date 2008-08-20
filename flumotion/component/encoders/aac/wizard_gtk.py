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

from zope.interface import implements

from flumotion.common.i18n import gettexter
from flumotion.admin.gtk.basesteps import AudioEncoderStep
from flumotion.admin.assistant.models import AudioEncoder
from flumotion.admin.assistant.interfaces import IEncoderPlugin

__version__ = "$Rev$"
_ = gettext.gettext
T_ = gettexter('flumotion')


class AACAudioEncoder(AudioEncoder):
    componentType = 'aac-encoder'

    def __init__(self):
        super(AACAudioEncoder, self).__init__()

        self.properties.bitrate = 64

    def getProperties(self):
        properties = super(AACAudioEncoder, self).getProperties()
        properties['bitrate'] *= 1000
        return properties


class AACStep(AudioEncoderStep):
    name = 'AACEncoder'
    title = _('AAC encoder')
    sidebarName = _('AAC')
    componentType = 'aac'

    # don't complain about our glade magic
    __pychecker__ = '--no-classattr'

    # WizardStep

    def setup(self):
        self.bitrate.set_range(5, 128)
        self.bitrate.set_value(64)

        self.bitrate.data_type = int

        self.add_proxy(self.model.properties, ['bitrate'])

    def workerChanged(self, worker):
        self.model.worker = worker
        self.wizard.requireElements(worker, 'flumcaacenc')


class AACWizardPlugin(object):
    implements(IEncoderPlugin)
    def __init__(self, wizard):
        self.wizard = wizard
        self.model = AACAudioEncoder()

    def getConversionStep(self):
        return AACStep(self.wizard, self.model)
