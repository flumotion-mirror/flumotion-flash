include $(top_srcdir)/common/python.mk

component_PYTHON = __init__.py flv.py wizard_gtk.py par_setter.py
componentdir = $(libdir)/flumotion/python/flumotion/component/muxers/flv
component_DATA = \
	flv.xml

clean-local:
	rm -rf *.pyc *.pyo

EXTRA_DIST = $(component_DATA)
