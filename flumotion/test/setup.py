

# This file has been generated by setup.m4 from configure.ac

RELATIVE_PATH = "flumotion/test/setup.py"
FLU_DIR = "/home/dolphy/workdir/gstreamer/gstreamer-head/uninstalled/flumotion/pkgconfig/.."
PROJECT = ""

import os
import sys

_setup = False

# we have a setup.setup() function so we don't import setup without doing
# anything to it
def setup():
    global _setup

    if _setup:
        return _setup

    # make sure we find the original flumotion dir always and firstly
    if not FLU_DIR in sys.path:
        sys.path.insert(0, FLU_DIR)

    # import flumotion and possibly add the original flumotion dir to __path__
    # and rebuild; without this trial seems to not be able to find
    # flumotion.common
    import flumotion
    if not FLU_DIR in flumotion.__path__:
        flumotion.__path__.insert(0, FLU_DIR)
        from twisted.python import rebuild
        rebuild.rebuild(flumotion)

    from flumotion.common import setup, log

    # enable logging
    setup.setup()

    # set up the package paths from FLU_PROJECT_PATH
    setup.setupPackagePath()

    # find out where we are so we can register the current project path
    log.debug('setup', 'RELATIVE_PATH: %s' % RELATIVE_PATH)
    levels = RELATIVE_PATH.count(os.path.sep)
    pplist = ['..'] * levels

    # now register our flumotion dir as an additional one
    # in the .m4, we wrap this in [] so aclocal does not expand __file__
    __thisdir = os.path.dirname(os.path.abspath(__file__))
    pplist.insert(0, __thisdir)

    # in distcheck mode, we need to go up one more
    if __thisdir.find('_build') != -1:
        log.debug('setup', 'distcheck mode (in %s)' % __thisdir)
        pplist.append('..')
    else:
        log.debug('setup', 'normal mode')

    __packagePath = os.path.abspath(os.path.join(*pplist))

    from flumotion.common import package
    log.debug('setup', 'registering our package path %s' % __packagePath)
    package.getPackager().registerPackagePath(__packagePath, PROJECT)

    _setup = __packagePath
    return _setup
