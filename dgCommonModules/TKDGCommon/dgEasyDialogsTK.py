from __future__ import print_function
import pygtk
pygtk.require('2.0')

import gtk
# Check for new pygtk: this is new class in PyGtk 2.4
if gtk.pygtk_version < (2,3,90):
	print("PyGtk 2.3.90 or later required for this example")
	raise SystemExit

def errorDialog(errorString):
	"""errorDialog(errorString)
	Prints an error message as a gtk style dialog box (with exclamation box for error).
	
	:param errorString: The string to print in a dialog box
	
	"""
	message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
	message.set_markup(errorString)
	message.run()		# Display the dialog box and hang around waiting for the "OK" button
	message.destroy()	# Takes down the dialog box
	return

def infoDialog(infoString):
	"""
	Prints an error message as a gtk style dialog box (with light bulb for status)
	
	:param infoString: The string to print in a dialog box
	
	"""
	message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
	message.set_markup(infoString)
	message.run()		# Display the dialog box and hang around waiting for the "OK" button
	message.destroy()	# Takes down the dialog box
	return
