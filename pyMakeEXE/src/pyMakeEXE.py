"""
Make EXE from .py
"""

import os
from Tkinter import Tk
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory

"""
Get Python File
"""
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
src_file = askopenfilename(initialdir = "C:\HWTeam\Utilities",
									title = "Select Python File",
									filetypes = (("python","*.py"),("all files","*.*")),
									) # show an "Open" dialog box and return the path to the selected file

"""
Get Folder to save to
"""

if (src_file != ""):
	Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
	save_folder = src_file[:src_file.rfind("/",0,src_file.rfind("/"))]
	
	build_folder =  str(save_folder) + "/build"
	dist_folder = str(save_folder) + "/dist"
	spec_folder = str(save_folder) + "/spec"

	run_cmd = 'pyinstaller --distpath "' + dist_folder + '" --workpath "' + build_folder + '" --specpath "' + spec_folder + '" --onefile "' + str(src_file) + '"'

	os.system(run_cmd)


	print "\nExecutable file at: %s\n" %(dist_folder)
	print "\nBuild files at: %s\n" %(build_folder)
	print "\nSpec file at: %s\n" %(spec_folder)
	print "Press enter to exit:\n"
	raw_input("")

		
else:
	print "No file selected enter to exit:\n"
	raw_input("")