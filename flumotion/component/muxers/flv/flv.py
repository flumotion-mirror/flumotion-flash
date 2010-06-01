# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
#
# Flumotion - a streaming media server
# Copyright (C) 2004,2005,2006,2007 Fluendo, S.L. (www.fluendo.com).
# All rights reserved.

# Licensees having purchased or holding a valid Flumotion Advanced
# Streaming Server license may use this file in accordance with the
# Flumotion Advanced Streaming Server Commercial License Agreement.
# See "LICENSE.Flumotion" in the source distribution for more information.

# Headers in this file shall remain intact.

import gst
import gobject
from flumotion.component import feedcomponent
from par_setter import FluParSetter

class FLVMuxer(feedcomponent.MuxerComponent):
    checkOffset = True

    def get_muxer_string(self, properties):
        self.square_pixels = properties.get('square-pixels', False)
        return 'fluflvmux broadcast=true name=muxer'

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
