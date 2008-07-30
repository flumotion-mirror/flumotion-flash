include $(top_srcdir)/common/python.mk

component_PYTHON = __init__.py aac.py wizard_gtk.py
componentdir = $(libdir)/flumotion/python/flumotion/component/encoders/aac
component_DATA = \
	aac.xml

clean-local:
	rm -rf *.pyc *.pyo

EXTRA_DIST = $(component_DATA)
