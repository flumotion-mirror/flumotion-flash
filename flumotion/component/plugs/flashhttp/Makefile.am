include $(top_srcdir)/common/python.mk

flashhttpplugdir = $(libdir)/flumotion/python/flumotion/component/plugs/flashhttp

flashhttpplug_PYTHON = 		\
	__init__.py 		\
	flashhttp.py 		\
	flashhttp_wizard.py	\
	flashplayer_location.py \
	workercheck.py

flashhttpplug_DATA = 		\
	flashhttp.xml		\
	fluflashembed.js	\
	flashplayer.html.template

TAGS_FILES = $(flashhttpplug_PYTHON)

EXTRA_DIST = 			\
	$(flashhttpplug_PYTHON) \
	$(flashhttpplug_DATA)

clean-local:
	rm -rf *.pyc *.pyo
