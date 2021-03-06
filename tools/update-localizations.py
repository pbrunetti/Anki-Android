#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2010 norbert.nagold@gmail.com
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This script extract localization from ankidroid.zip into the right folders.
# http://crowdin.net/download/project/ankidroid.zip

# Below is the list of official AnkiDroid localizations.
# Add a language if 01-core.xml is translated
# Do not remove languages.
# When you add a language, please also add it to mAppLanguages in Preferences.java

languages = ['ar', 'bg', 'ca', 'cs', 'de', 'el', 'es-AR', 'es-ES', 'et', 'fa', 'fi', 'fr', 'gl', 'he', 'hi', 'hu', 'id', 'it', 'ja', 'ko', 'lt', 'nl', 'no', 'pl', 'pt-PT', 'pt-BR', 'ro', 'ru', 'sk', 'sl', 'sr', 'sv-SE', 'th', 'tr', 'uk', 'vi', 'zh-CN', 'zh-TW'];
# languages which are localized for more than one region
localizedRegions = ['es', 'pt', 'zh']

fileNames = ['01-core', '02-strings', '03-dialogs', '04-network', '05-feedback', '06-statistics', '07-cardbrowser', '08-widget', '09-backup', '10-preferences', '11-arrays', '12-tutorial', '13-newfeatures', '14-marketdescription', '15-markettitle']
anyError = False
titleFile = '../docs/marketing/localized_description/ankidroid-titles.txt'
titleString = 'AnkiDroid Flashcards'


import os
import zipfile
import urllib
import string
import re
import difflib

def replacechars(filename, fileExt, isCrowdin):
	s = open(filename,"r+")
	newfilename = filename + ".tmp"
	fin = open(newfilename,"w")
	errorOccured = False
	if fileExt != '.csv':
		for line in s.readlines():
			if line.startswith("<?xml"):
				line = "<?xml version=\"1.0\" encoding=\"utf-8\"?> \n <!-- \n ~ Copyright (c) 2009 Andrew <andrewdubya@gmail> \n ~ Copyright (c) 2009 Edu Zamora <edu.zasu@gmail.com> \n ~ Copyright (c) 2009 Daniel Svaerd <daniel.svard@gmail.com> \n ~ Copyright (c) 2009 Nicolas Raoul <nicolas.raoul@gmail.com> \n ~ Copyright (c) 2010 Norbert Nagold <norbert.nagold@gmail.com> \n ~ This program is free software; you can redistribute it and/or modify it under \n ~ the terms of the GNU General Public License as published by the Free Software \n ~ Foundation; either version 3 of the License, or (at your option) any later \n ~ version. \n ~ \n ~ This program is distributed in the hope that it will be useful, but WITHOUT ANY \n ~ WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A \n ~ PARTICULAR PURPOSE. See the GNU General Public License for more details. \n ~ \n ~ You should have received a copy of the GNU General Public License along with \n ~ this program.  If not, see <http://www.gnu.org/licenses/>. \n --> \n \n"
			else:
				# some people outwitted crowdin's "0"-bug by filling in "0 ", this changes it back:
				if line.startswith("	<item>0 </item>"): 
					line = "    <item>0</item>\n"
				line = string.replace(line, '\'', '\\\'')
				line = string.replace(line, '\\\\\'', '\\\'')
				line = string.replace(line, '\n\s', '\\n')
				line = string.replace(line, 'amp;', '')
				if re.search('%[0-9]\\s\\$|%[0-9]\\$\\s', line) != None:
					errorOccured = True
#			print line		
			fin.write(line)
	else:
		fin.write("<?xml version=\"1.0\" encoding=\"utf-8\"?> \n <!-- \n ~ Copyright (c) 2011 Norbert Nagold <norbert.nagold@gmail.com> \n ~ This program is free software; you can redistribute it and/or modify it under \n ~ the terms of the GNU General Public License as published by the Free Software \n ~ Foundation; either version 3 of the License, or (at your option) any later \n ~ version. \n ~ \n ~ This program is distributed in the hope that it will be useful, but WITHOUT ANY \n ~ WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A \n ~ PARTICULAR PURPOSE. See the GNU General Public License for more details. \n ~ \n ~ You should have received a copy of the GNU General Public License along with \n ~ this program.  If not, see <http://www.gnu.org/licenses/>. \n --> \n \n \n<resources> \n <string-array name=\"tutorial_questions\"> \n")
		content = re.sub('([^\"])\n', "\\1", s.read()).split("\n")
		length = len(content)
		line = []
		for i in range(length - 1):
			if isCrowdin:
				start = content[i].rfind('\",\"') + 3
			else:
				start=content[i].find('\"') + 1
			contentLine = content[i][start:len(content[i])-1]
			sepPos = contentLine.find('<separator>')
			if sepPos == -1:
				if len(contentLine) > 2:
					errorOccured = True
					print contentLine
				continue
			line.append(["<![CDATA[" + contentLine[:sepPos] + "]]>", "<![CDATA[" + contentLine[sepPos+11:] + "]]>"])
		for fi in line:
			fi[0] = re.sub('\"+', '\\\"', fi[0])
			fi[0] = re.sub('\'+', '\\\'', fi[0])
			fi[0] = re.sub('\\\\{2,}', '\\\\', fi[0])
			fin.write("    <item>" + fi[0] + "</item> \n");
		fin.write(" </string-array>\n <string-array name=\"tutorial_answers\">\n");
		for fi in line:
			fi[1] = re.sub('\"+', '\\\"', fi[1])
			fi[1] = re.sub('\'+', '\\\'', fi[1])
			fi[1] = re.sub('\\\\{2,}', '\\\\', fi[1])
			fin.write("    <item>" + fi[1] + "</item> \n");
		fin.write(" </string-array>\n</resources>");
	s.close()
	fin.close()
	os.rename(newfilename, filename)
	if errorOccured:
		#os.remove(filename)
		print 'error in file ' + filename
		return False
	else:
		print 'file ' + filename + ' successfully copied'
		return True

def fileExtFor(f):
	if f == '12-tutorial':
		return '.csv'
	elif f == '14-marketdescription':
		return '.txt'
	elif f == '15-markettitle':
		return '.txt'
	else:
		return '.xml'

def createIfNotExisting(directory):
	if not os.path.isdir(directory):
		os.mkdir(directory)

def update(valuesDirectory, f, source, fileExt, isCrowdin, language=''):
	if f == '14-marketdescription':
		newfile = '../docs/marketing/localized_description/marketdescription' + '-' + language + fileExt
		file(newfile, 'w').write(source)
		# translations must be compared to the old version of marketdescription (bug of crowdin)
		oldContent = open('../docs/marketing/localized_description/oldVersionJustToCompareWith.txt').readlines()
		newContent = open(newfile).readlines()
		for i in range(0, len(oldContent)):
			if oldContent[i] != newContent[i]:
				print 'file ' + newfile + ' successfully copied'
				return True			
		os.remove(newfile)
		print 'file marketdescription is not translated into language ' + language
		return True
	elif f == '15-markettitle':
#		newfile = '../docs/marketing/localized_description/marketdescription' + '-' + language + fileExt
#		file(newfile, 'w').write(source)
		translatedTitle = source.replace("\n", "")
		if titleString != translatedTitle:
			s = open(titleFile, 'a')
			s.write("\n" + language + ': ' + translatedTitle)
			s.close()
			print 'added translated title'
		else:
			print 'title not translated'
		return True
	else:
		newfile = valuesDirectory + f + '.xml'
		file(newfile, 'w').write(source)
		return replacechars(newfile, fileExt, isCrowdin)

zipname = 'ankidroid.zip'

print "downloading crowdin-file"
req = urllib.urlopen('http://crowdin.net/download/project/ankidroid.zip')
file(zipname, 'w').write(req.read())
req.close()

zip = zipfile.ZipFile(zipname, "r")

#create title file
t = open(titleFile, 'w')
t.write(titleString)
t.close()

for language in languages:
	if language[:2] in localizedRegions:
		androidLanguage = string.replace(language, '-', '-r')
	else:
		androidLanguage = language[:2] # Example: es-ES becomes es

	print "\ncopying language files for: " + androidLanguage
	valuesDirectory = "../res/values-" + androidLanguage + "/"
	createIfNotExisting(valuesDirectory)

	# Copy localization files, mask chars and append gnu/gpl licence
	for f in fileNames:
		fileExt = fileExtFor(f)
		anyError = not(update(valuesDirectory, f, zip.read(language + "/" + f + fileExt), fileExt, True, language)) or anyError

	if anyError:
		if raw_input("At least one file of the last handled language contains an error. Please check\nContinue anyway? (y/n)") != 'y':
			break
		else:
			anyError = False

# Special case: English tutorial.
valuesDirectory = "../res/values/"
createIfNotExisting(valuesDirectory)
f = '12-tutorial'
fileExt = fileExtFor(f)
source = open("../assets/" + 'tutorial' + fileExt)
#Note: the original tutorial.csv has less columns, therefore we have special
#support for its syntax.
print
update(valuesDirectory, f, source.read(), fileExt, False)

print "\nremoving crowdin-file\n"
os.remove(zipname)	


