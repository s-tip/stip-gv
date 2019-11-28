#!/usr/bin/env python

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ctim.settings")
os.environ.setdefault("CTIM_GV_CONF_PATH", "/home/terra/ctim/gv/conf/ctim_gv.conf")
application = get_wsgi_application()
