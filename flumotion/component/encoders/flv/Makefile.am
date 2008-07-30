include $(top_srcdir)/common/python.mk

component_PYTHON = __init__.py flv.py flv_wizard.py
componentdir = $(libdir)/flumotion/python/flumotion/component/encoders/flv
component_DATA = \
	flv.xml \
	flv-wizard.glade

clean-local:
	rm -rf *.pyc *.pyo

EXTRA_DIST = $(component_DATA)
