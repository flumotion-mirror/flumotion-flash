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
from flumotion.component import feedcomponent
from par_setter import FluParSetter


class FLVMuxer(feedcomponent.MuxerComponent):
    checkOffset = True

    def get_muxer_string(self, properties):
        self.square_pixels = properties.get('square-pixels', False)
        flu_muxer = properties.get('fluendo-muxer', True)
        if flu_muxer == True:
            return 'fluflvmux broadcast=true name=muxer'
        else:
            return 'flvmux streamable=true name=muxer'

    def get_link_pad(self, muxer, srcpad, caps):
        linkpad = muxer.get_compatible_pad(srcpad, caps)
        if not self.square_pixels:
            return linkpad
        if caps.to_string().startswith("video"):
            setter = FluParSetter()
            self.pipeline.add(setter)
            setter.get_pad("src").link(linkpad)
            setter.set_state(gst.STATE_PLAYING)
            return setter.get_pad("sink")
        return linkpad
