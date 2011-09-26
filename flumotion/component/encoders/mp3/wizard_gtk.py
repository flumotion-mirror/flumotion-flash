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

from zope.interface import implements

from flumotion.common.i18n import gettexter
from flumotion.admin.gtk.basesteps import AudioEncoderStep
from flumotion.admin.assistant.models import AudioEncoder
from flumotion.admin.assistant.interfaces import IEncoderPlugin

__version__ = "$Rev$"
_ = gettext.gettext
T_ = gettexter('flumotion')


class MP3AudioEncoder(AudioEncoder):
    componentType = 'mp3-encoder'

    def __init__(self):
        super(MP3AudioEncoder, self).__init__()

        self.properties.bitrate = 64

    def getProperties(self):
        properties = super(MP3AudioEncoder, self).getProperties()
        properties['bitrate'] *= 1000
        return properties


class MP3Step(AudioEncoderStep):
    name = 'MP3Encoder'
    title = _('MP3 encoder')
    sidebarName = _('MP3')
    componentType = 'mp3'

    # don't complain about our glade magic
    __pychecker__ = '--no-classattr'

    # WizardStep

    def setup(self):
        self.bitrate.set_range(16, 320)
        self.bitrate.set_value(64)

        self.bitrate.data_type = int

        self.add_proxy(self.model.properties, ['bitrate'])

    def workerChanged(self, worker):
        self.model.worker = worker

        def checkDone(elements):
            if not elements:
                return

            self.wizard.clear_msg('elementmp3parse-lame')
            self.wizard.requireElements(worker, 'mp3parse', 'flump3enc')

        d = self.wizard.requireElements(worker, 'mp3parse', 'lame')
        d.addCallback(checkDone)


class MP3WizardPlugin(object):
    implements(IEncoderPlugin)

    def __init__(self, wizard):
        self.wizard = wizard
        self.model = MP3AudioEncoder()

    def getConversionStep(self):
        return MP3Step(self.wizard, self.model)
