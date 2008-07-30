include $(top_srcdir)/common/python.mk

component_PYTHON = __init__.py vp6.py vp6_wizard.py
componentdir = $(libdir)/flumotion/python/flumotion/component/encoders/vp6
component_DATA = \
	vp6.xml \
	vp6-wizard.glade

clean-local:
	rm -rf *.pyc *.pyo

EXTRA_DIST = $(component_DATA)
