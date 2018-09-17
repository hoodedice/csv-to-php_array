import sys
import fileinput
import csv
import os

wasDeleted = False
output = ""
modelname = ""
isQuoted = []
outputfile = None

# check if a filename was passed at all
if (sys.argv[1:] == []):
	print ("A filename should be specified")
	exit()

# write output to file
def write_to_file(output):
	global wasDeleted
	# technically should be a php file but whatever
	path = modelname + '.txt'

	# nuke the file before writing anything
	if not wasDeleted:
		if os.path.exists(path): 
			os.remove(path)
			wasDeleted = True

	# actually write the contents
	with open(path, 'a+') as outputfile:
		print(output)
		outputfile.write(output)

	return

# open the file and read it
with open(sys.argv[1:][0], newline='') as inputfile:
	# get the name of the database table/laravel model from the csv filename
	# print(str(inputfile.name).rpartition('/')[2].split('.')[0])
	modelname = str(inputfile.name).rpartition('/')[2].split('.')[0]

	# set up the php array
	output = "$" + modelname + " = array(\n\n"
	write_to_file(output)

	# try and detect the dialect of the csv file
	dialect = csv.Sniffer().sniff(inputfile.readline())
	inputfile.seek(0)

	# first line
	isQuoted = inputfile.readline().split(',')
	print("is quote bruh")
	print(isQuoted)
	# start up the csv dictreader
	reader = csv.DictReader(inputfile)

	# every row in the csv file is an array
	for rows in reader:
		output = "\tarray(\n"
		idx = 0
		# the meat
		for row, value in rows.items():
			if isQuoted[idx] == 'True':
				output += "\t\t\'" + row .strip()+ "\' => \'" + value.strip() + "\',\n"
			else:
				output += "\t\t\'" + row .strip()+ "\' => " + value.strip() + ",\n"
			idx += 1
		
		#close the row array
		output += "\n\t),\n\n"
		write_to_file(output)

	# close the php array
	output = ");"
	write_to_file(output)


exit()