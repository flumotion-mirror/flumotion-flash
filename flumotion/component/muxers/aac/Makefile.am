include $(top_srcdir)/common/python.mk

component_PYTHON = __init__.py aac.py
componentdir = $(libdir)/flumotion/python/flumotion/component/muxers/aac
component_DATA = \
	aac.xml

clean-local:
	rm -rf *.pyc *.pyo

EXTRA_DIST = $(component_DATA)
