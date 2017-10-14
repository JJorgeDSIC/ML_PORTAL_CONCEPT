import csv
import re
import os
import numpy as np


from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

def get_upload_training_path(instance, filename):

    return "{path}/data/train/{filename}".format(path=instance.path, item_id=instance.id,filename=filename)

def get_upload_test_path(instance, filename):

    return "{path}/data/test/{filename}".format(path=instance.path, item_id=instance.id,filename=filename)



def validate_csv(data):

	#print data

	return True
	# tmp = os.path.join(settings.MEDIA_ROOT, "tmp", data.name) 

	# path = default_storage.save(tmp, ContentFile(data.read()))

	# print path

	# f = open(path, 'r')
	# #print re.split(r'[\n\r]+', data)

	# data_str = f.read()

	# lines = filter(None, re.split("[\n]+", data_str))

	# rows = [filter(None, re.split("[,;]+", l)) for l in lines]

	
	# f.close()

	# os.remove(path)

	# print "SAMPLES: " + str(len(rows))
	# print "FIELDS: " + str(len(rows[0]))
	# print "SOME SAMPLES: " 
	# print rows[0:10]
	
	# registers = np.array(rows)

	# print registers
	# labels = set(registers[:,-1])

	# print labels



	# f = open(path, 'r')

	# lines = f.readlines()

	
	
	# lines = [l.strip() for l in lines ]

	# #print lines	
	# one_row = filter(None, re.split("[,;]+", lines[0]))
	# print "SAMPLES: " + str(len(lines))
	# print "FIELDS: " + str(len(one_row))
	# print filter(None, re.split("[,;]+", lines[0]))

	# f.close()

	# os.remove(path)

	# reader = csv.reader(data)

	# samples = reader.line_num

	# print "There are " + str(samples) + " samples."

	# for row in reader:
	# 	print row
	# 	for element in row:
	# 		if element == '':
	# 			return False


	# f = open(data, 'r')

	# lines = f.readlines()

	# print lines[0]

	#AQUI ME QUEDE

	# f = open(data, 'r')

	# SEPARATOR =","

	# lines = data.split("\n")

	# samples = len(lines)

	# print "SAMPLES: " + str(samples)

	# if samples > 0:

	# 	fields = len(lines[0].split(SEPARATOR))
	# 	print lines[0].split(SEPARATOR)
	# 	print "FIELDS: " + str(fields)

	# for line in lines:
	# 	print line[:-1]
	# 	tokens = line[:-1].split(SEPARATOR)
	# 	for token in tokens:
	# 		print token
	# 		if token == '':
	# 			return False

  	#return True