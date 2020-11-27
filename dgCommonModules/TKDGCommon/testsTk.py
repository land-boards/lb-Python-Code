#!/usr/bin/env python
"""
==========
testsTk.py
==========

This program tests the Tkinter elements.

==========
Background
==========

===
API
===

"""
from __future__ import print_function

from builtins import str
from builtins import object
import os
import sys
import datetime
import time
import Tkinter
import tkMessageBox

import dgReadCSVtoListTk

sys.path.append('C:\\HWTeam\\Utilities\\dgCommonModules\\dgCommTk')

top = Tkinter.Tk()

dgReadCSVtoListTk.errorDialog("Testing the error dialog")

