include $(top_srcdir)/common/python.mk

component_PYTHON = __init__.py mp3.py wizard_gtk.py
componentdir = $(libdir)/flumotion/python/flumotion/component/encoders/mp3
component_DATA = \
	mp3.xml

clean-local:
	rm -rf *.pyc *.pyo

EXTRA_DIST = $(component_DATA)
