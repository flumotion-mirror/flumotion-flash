AUTOMAKE_OPTIONS = dist-bzip2 no-dist-gzip 1.8

ACLOCAL_AMFLAGS = -I common

include $(srcdir)/common/changelog.mk
include $(srcdir)/common/common.mk
include $(srcdir)/common/pychecker.mk
include $(srcdir)/common/deb.mk
include $(srcdir)/common/rpm.mk

SUBDIRS = flumotion common misc

EXTRA_DIST = \
	env.in \
        .version \
        RELEASE \
	LICENSE.LGPL \
	flumotion-flash.spec

PYCHECKER_WHITELIST = flumotion/component/*/*/*.py
PYCHECKER_BLACKLIST =

COVERAGE_MODULES = \
	flumotion.component.muxers.flv \
	flumotion.component.encoders.mp3 \
	flumotion.component.encoders.aac \
	flumotion.component.encoders.flv

BUILT_SOURCES = $(top_srcdir)/.version
$(top_srcdir)/.version:
	echo $(VERSION) > $@-t && mv $@-t $@

dist: changelog
