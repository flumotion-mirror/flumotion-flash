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

import gst
import gobject


class FluParSetter(gst.Element):
    '''
    I force the pixel aspect ratio to be 1/1 by modifying width and height
    accordingly.
    '''

    __gstdetails__ = ('FluParSetter', 'Generic',
                      'A PAR Setter for Flumotion',
                      'Flumotion Dev Team')

    _sinkpadtemplate = gst.PadTemplate("sink",
                                         gst.PAD_SINK,
                                         gst.PAD_ALWAYS,
                                         gst.caps_from_string("ANY"))

    _srcpadtemplate = gst.PadTemplate("src",
                                         gst.PAD_SRC,
                                         gst.PAD_ALWAYS,
                                         gst.caps_from_string("ANY"))

    def __init__(self):
        gst.Element.__init__(self)

        self.sinkpad = gst.Pad(self._sinkpadtemplate, "sink")
        self.sinkpad.set_chain_function(self.chainfunc)
        self.sinkpad.set_setcaps_function(self.setcaps)
        self.add_pad(self.sinkpad)

        self.srcpad = gst.Pad(self._srcpadtemplate, "src")
        self.add_pad(self.srcpad)

    def chainfunc(self, pad, buffer):
        struc = buffer.get_caps()[0].copy()
        height = struc['height']
        width = struc['width']
        par = struc['pixel-aspect-ratio']

        if par.num >= par.denom:
            height = int(height * par.denom / float(par.num))
        else:
            width = int(width * par.num / float(par.denom))

        struc.set_value("width", width)
        struc.set_value("height", height)
        struc.set_value("pixel-aspect-ratio", gst.Fraction(1, 1))

        caps = gst.Caps()
        caps.append_structure(struc)
        buffer.set_caps(caps)
        self.log("Setting caps to %r" % buffer.get_caps().to_string())

        return self.srcpad.push(buffer)

    def setcaps(self, pad, caps):
        return True

gobject.type_register(FluParSetter)
