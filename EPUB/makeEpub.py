from __future__ import print_function
import zipfile
import sys
import os

if len(sys.argv) not in (2,3) or sys.argv[1] in ("-h", "--help"):
	print(
		"""
Usage:
python makeEpub.py <dirName> [epubName]
DirName: The directory that contains your unpacked epub.
epubName: Optional name to call the archive. Must contain .epub if you do this. Defaults to the directory name, with .epub appended.
		""")
	exit()
epubDirName = sys.argv[1]
if not os.path.exists(epubDirName):
	print("That directory does not exist")
	exit()
epubName = epubDirName+".epub"
if len(sys.argv) == 3:
	epubName = sys.argv[2]
with zipfile.ZipFile(epubName, "w") as epub:
	#The mimeType
	epub.write(os.path.join(epubDirName, "mimetype"), "mimetype", compress_type=zipfile.ZIP_STORED)
	#Walk the other directories writing all files.
	for dir, dirnames, filenames in os.walk(epubDirName):
		relativePath = os.path.relpath(dir, epubDirName)
		for filename in filenames:
			#Ignore the mimetype, it's already there, and shouldn't be deflated.
			if filename == "mimetype":
				continue
			pathInBundle = os.path.join(relativePath, filename)
			absPath = os.path.join(dir, filename)
			epub.write(absPath, pathInBundle, zipfile.ZIP_DEFLATED)

print("Your epub", epubName, "Has been created.")