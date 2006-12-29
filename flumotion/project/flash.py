# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
#
# Flumotion - a streaming media server
# Copyright (C) 2004,2005 Fluendo, S.L. (www.fluendo.com). All rights reserved.

# This file may be distributed and/or modified under the terms of
# the GNU General Public License version 2 as published by
# the Free Software Foundation.
# This file is distributed without any warranty; without even the implied
# warranty of merchantability or fitness for a particular purpose.
# See "LICENSE.GPL" in the source distribution for more information.

# Licensees having purchased or holding a valid Flumotion Advanced
# Streaming Server license may use this file in accordance with the
# Flumotion Advanced Streaming Server Commercial License Agreement.
# See "LICENSE.Flumotion" in the source distribution for more information.

# Headers in this file shall remain intact.

import os

# where am I on the disk ?
__thisdir = os.path.dirname(os.path.abspath(__file__))
# toplevel dir
__toplevel = os.path.normpath(os.path.join(__thisdir, '..', '..'))

pythondir = __toplevel
localedatadir = os.path.join(__toplevel)
if not os.path.exists(os.path.join(localedatadir, 'locale')):
    localedatadir = '/usr/local/share'
version = '0.1.0'
