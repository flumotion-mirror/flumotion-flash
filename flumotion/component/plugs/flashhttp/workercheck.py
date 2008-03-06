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

from flumotion.common import log
from flumotion.common.messages import Result

# FIXME: nested import
from flashplayer_location import getFlashFilename

__version__ = "$Rev$"


def checkFlashPlayer():
    """Check for flash player.
    @returns: a result containing the filename to the jar or None if it cannot be found
    @rtype: L{flumotion.common.messages.Result}
    """

    log.debug('flashplayercheck', 'Checking for ...' )
    filename = getFlashFilename('video')
    if not filename:
        msg = 'not found'
    else:
        msg = filename

    log.debug('flashplayercheck', 'filename - %s' % (msg,))
    result = Result()
    result.succeed(filename)
    log.debug('flashplayercheck', 'done, returning')
    return result
