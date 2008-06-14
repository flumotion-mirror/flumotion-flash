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

from twisted.internet import defer

from flumotion.common import errors
from flumotion.common.i18n import gettexter, ngettext
from flumotion.common.messages import Warning
from flumotion.wizard.basesteps import AudioEncoderStep
from flumotion.wizard.models import AudioEncoder

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
    name = 'AAC encoder'
    sidebarName = 'AAC'
    componentType = 'aac'

    # WizardStep

    def setup(self):
        self.bitrate.set_range(5, 128)
        self.bitrate.set_value(64)

        self.bitrate.data_type = int

        self.add_proxy(self.model.properties, ['bitrate'])

    def workerChanged(self, worker):
        self.model.worker = worker
        def checkElements(elements):
            if elements:
                element_str = "', '".join(elements)
                f = ngettext("Worker '%s' is missing GStreamer element '%s'.",
                    "Worker '%s' is missing GStreamer elements '%s'.",
                    len(elements))
                message = Warning(
                    T_(f, self.worker, element_str), id='flashaac')
                self.wizard.add_msg(message)
                self.wizard.taskFinished(True)
                return defer.fail(errors.FlumotionError('missing %s element(s)' % (
                    element_str,)))

            self.wizard.clear_msg('flashaac')
            self.wizard.taskFinished()

        self.wizard.waitForTask('aac elements check')
        d = self.wizard.requireElements(worker, 'flumcaacenc')
        d.addCallback(checkElements)


class AACWizardPlugin(object):
    def __init__(self, wizard):
        self.wizard = wizard
        self.model = AACAudioEncoder()

    def getConversionStep(self):
        return AACStep(self.wizard, self.model)
