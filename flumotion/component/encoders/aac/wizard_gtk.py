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

from flumotion.admin.assistant.models import AudioEncoder
from flumotion.admin.assistant.interfaces import IEncoderPlugin
from flumotion.admin.gtk.basesteps import AudioEncoderStep
from flumotion.common import errors, messages
from flumotion.common.i18n import gettexter, N_

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

        if self.wizard.getStep('Encoding').getMuxerFormat() == 'aac':
            self.model.properties.headers = True

    def workerChanged(self, worker):
        self.model.worker = worker
        self._runChecks(worker)

    def _runChecks(self, worker):
        self.wizard.waitForTask('aac checks')
        msg = messages.Info(T_(N_('Checking for libstdc++5 library...')),
            mid='aac-check')
        self.wizard.add_msg(msg)

        def libraryFound(result):
            self.wizard.taskFinished(blockNext=not result)
            self.wizard.clear_msg('aac-check')
            if result:
                self.wizard.requireElements(worker, 'flumcaacenc')
            else:
                msg = messages.Error(
                    T_(N_('libstdc++5 is required by the aac encoder but does '
                          'not seem to be installed on the worker.\n'
                          'Please install it in order to go forward.')),
                    mid='aac-check')
                self.wizard.add_msg(msg)

        d = self.wizard.runInWorker(worker, 'flumotion.worker.checks.check',
                                    'checkFile', '/usr/lib/libstdc++.so.5')
        d.addCallback(libraryFound)

        return d


class AACWizardPlugin(object):
    implements(IEncoderPlugin)

    def __init__(self, wizard):
        self.wizard = wizard
        self.model = AACAudioEncoder()

    def getConversionStep(self):
        return AACStep(self.wizard, self.model)
