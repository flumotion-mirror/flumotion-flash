include $(top_srcdir)/common/python.mk

component_PYTHON = __init__.py h264.py wizard_gtk.py
componentdir = $(libdir)/flumotion/python/flumotion/component/encoders/h264
component_DATA = \
	h264.xml \
	h264-wizard.glade

clean-local:
	rm -rf *.pyc *.pyo

EXTRA_DIST = $(component_DATA)
