AUTOMAKE_OPTIONS = dist-bzip2 no-dist-gzip 1.8

ACLOCAL_AMFLAGS = -I common

include $(srcdir)/common/common.mk
include $(srcdir)/common/pychecker.mk
include $(srcdir)/common/deb.mk
include $(srcdir)/common/rpm.mk

SUBDIRS = flumotion common misc

EXTRA_DIST = \
	env.in \
	LICENSE.Flumotion \
	flumotion-flash.spec

PYCHECKER_WHITELIST = flumotion/component/*/*/*.py
PYCHECKER_BLACKLIST =

COVERAGE_MODULES = \
	flumotion.component.muxers.flv \
	flumotion.component.encoders.mp3 \
	flumotion.component.encoders.aac \
	flumotion.component.encoders.flv
