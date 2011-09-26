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

import os

from twisted.web.resource import Resource
from twisted.web.static import Data, File

from flumotion.common import log
from flumotion.common.errors import ComponentStartError
from flumotion.component.misc.httpserver.httpserver import HTTPFileStreamer
from flumotion.component.plugs.base import ComponentPlug

# FIXME: nested import
from flashplayer_location import getFlashFilename

__version__ = "$Rev$"


class FlashDirectoryResource(Resource):
    """I generate the directory used to serve a cortado applet
    It contains::
    - a html file, usually called index.html.
    - cortado.jar - cortado java applet
    """

    def __init__(self, mount_point, properties):
        Resource.__init__(self)

        index_name = properties.get('index', 'index.html')

        root = mount_point
        if not root.endswith("/"):
            root += "/"
        if index_name != 'index.html':
            root = None
        self._mount_point_root = root
        self._properties = properties
        self._index_name = index_name

        self._index_content = self._getHTMLResource()
        self._addChildren()

    def _addChildren(self):
        self.putChild(self._index_name, self._index_content)
        self.putChild('', self._index_content)
        self.putChild("fluflashplayer.swf", self._getSWFResource())
        self.putChild("fluflashembed.js", self._getJSResource())
        self.putChild("flustream.flv.m3u", self._getM3UResource())

    def _getHTMLResource(self):
        html_template = self._getLocalFile('flashplayer.html.template')
        ns = {}
        # FIXME: put in the whole url or?
        ns['m3u-url'] = 'flustream.flv.m3u'
        data = open(html_template, 'r').read()
        content = data % ns
        return Data(content, 'text/html')

    def _getJSResource(self):
        filename = self._getLocalFile('fluflashembed.js')
        return File(filename, 'application/javascript')

    def _getSWFResource(self):
        if self._hasVideo():
            filename = getFlashFilename('video')
        else:
            filename = getFlashFilename('audio')
        return File(filename, 'application/x-shockwave-flash')

    def _getM3UResource(self):
        m3udata = ("#EXTM3U\n"
                   "#EXTINF:-1:On-Demand Flumotion Stream\n"
                   "%s") % self._getFlvURL()
        return Data(m3udata, 'audio/x-mpegurl')

    def _hasVideo(self):
        return self._properties['has-video']

    def _getFlvURL(self):
        return self._properties['stream-url']

    def _getLocalFile(self, filename):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            filename)


class FlashHTTPPlug(ComponentPlug):
    """I am a component plug for a http-server which plugs in a
    http resource containing a flash file.
    """

    def start(self, component):
        """
        @type component: L{HTTPFileStreamer}
        """
        if not isinstance(component, HTTPFileStreamer):
            raise ComponentStartError(
                "A FlashHTTPPlug %s must be plugged into a "
                "HTTPStreamer component, not a %s" % (
                self, component.__class__.__name__))
        log.debug('flashhttpplug', 'Attaching to %r' % (component, ))
        resource = FlashDirectoryResource(component.getMountPoint(),
                                          self.args['properties'])
        component.setRootResource(resource)


def test():
    import sys
    from twisted.internet import reactor
    from twisted.python.log import startLogging
    from twisted.web.server import Site
    startLogging(sys.stderr)

    properties = {'has-audio': True,
                  'has-video': True,
                  'codebase': '/',
                  'width': 320,
                  'height': 240,
                  'stream-url': sys.argv[1],
                  'buffer-size': 40,
                  'framerate': 1}
    root = FlashDirectoryResource('/', properties)
    site = Site(root)

    reactor.listenTCP(8080, site)
    reactor.run()

if __name__ == "__main__":
    test()
