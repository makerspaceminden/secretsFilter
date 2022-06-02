#!/bin/python3
"""
Program to filter out any API Keys / Passwords etc.
Replaces them with a defined String in curly brackets e.g. {APIKey}
"""
import argparse
import json
import keyFilter

if __name__ == "__main__": # Main

	# Arguments for the program
	parser = argparse.ArgumentParser(description="MSM Secrets filter\n\
        MSM Secrets filter Program to filter out any API keys, passwords and other \
   		secrets. Replaces them with a defined string e.g. {APIKey}")
	parser.add_argument('-s', '--scanDir',
		            dest='scanDir',
		            help='Directory where files should be scanned for the names / secrets',
			        required=True,
		            type=str
		            )
	parser.add_argument('-f', '--filter',
		            default='./filter.json',
		            dest='filterFile',
		            help='JSON File containing an array of name: secret mapping: \n\
                        \tExample: {"WifiPassword": "01234567"}',
		            type=str
		            )
	parser.add_argument('-d', '--delimiters',
		            default='{,}',
		            dest='delimiters',
		            help='Delimiters for the string replacing, separated by ","\n\
						Can be used to fit this program for enviroments, Examples:\n\
						\t-d ","   --> in code as a String: "APIKey"\n\
						\t-d /*,*/ --> in code as a comment: /*APIKey*/',
		            type=str
		            )
	parser.add_argument('-r', '--reverseMode',
			        action="count",
		            dest='reverseMode',
		            help='Undoes filtering as long as the same json is used ("filters" in reverse)'
		            )
	parser.add_argument('-v', '--verbose',
			        action="count",
		            dest='verbose',
		            help='Does verbose logging'
		            )
	args = parser.parse_args()

	doReverse = True
	if(args.reverseMode == None):
		doReverse = False

	isVerbose = True
	if(args.verbose == None):
		isVerbose = False

	delimiters = args.delimiters.split(",")
	preDelimiter = delimiters[0]
	postDelimiter = delimiters[1]

	jsonData = {}
	with open (args.filterFile) as jsonFile:
		jsonData = json.loads(jsonFile.read())

	fileFilter = keyFilter.KeyFilter(jsonData, args.scanDir, preDelimiter, postDelimiter, isVerbose, doReverse)
	fileFilter.applyFilter()
