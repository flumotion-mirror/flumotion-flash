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
from flumotion.common.messages import ngettext, gettexter, Warning
from flumotion.wizard.basesteps import AudioEncoderStep
from flumotion.wizard.models import AudioEncoder

__version__ = "$Rev$"
_ = gettext.gettext
T_ = gettexter('flumotion')


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

    def worker_changed(self, worker):
        self.model.worker = worker
        def checkElements(elements):
            if elements:
                element_str = "', '".join(elements)
                f = ngettext("Worker '%s' is missing GStreamer element '%s'.",
                    "Worker '%s' is missing GStreamer elements '%s'.",
                    len(elements))
                message = Warning(
                    T_(f, self.worker, element_str), id='flashmp3')
                self.wizard.add_msg(message)
                self.wizard.taskFinished(True)
                return defer.fail(errors.FlumotionError('missing %s element(s)' % (
                    element_str,)))

            self.wizard.clear_msg('flashmp3')
            self.wizard.taskFinished()

        self.wizard.waitForTask('mp3 elements check')
        d = self.wizard.require_elements(worker, 'mp3parse', 'lame')
        d.addCallback(checkElements)


class MP3WizardPlugin(object):
    def __init__(self, wizard):
        self.wizard = wizard
        self.model = MP3AudioEncoder()

    def getConversionStep(self):
        return MP3Step(self.wizard, self.model)
