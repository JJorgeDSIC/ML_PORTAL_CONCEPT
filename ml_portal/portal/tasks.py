from __future__ import absolute_import

from celery import shared_task, task

from django.contrib.auth.models import User
from .models import UserProfile, TrainingFile, TestFile, ModelFile, Problem 


import os
import time
import random

@task
def mockup_method(path):

	user = User.objects.get(username=path)

	print user

	print user.userprofile

	profile = user.userprofile
	
	problem = profile.problem

	print os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

	f = open("documents/" + path  + "/logs/training_log.txt", 'wb+')

	total = 10
	i = 0
	while i < total:
		i+=1

		st = "Evaluando: " + str(i) + "/" + str(total) + "\n"
		print st
		f.write(st)
		f.flush()
		time.sleep(random.random() * 10)

	f.close()

	problem.status = Problem.EXPECTING_TEST_FILE

	problem.save()

@task
def mockup_method_eval(path):

	user = User.objects.get(username=path)

	print user

	print user.userprofile

	profile = user.userprofile
	
	problem = profile.problem

	print os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

	f = open("documents/" + path  + "/logs/evaluation_log.txt", 'wb+')

	total = 10
	i = 0
	while i < total:
		i+=1

		st = "Evaluando: " + str(i) + "/" + str(total) + "\n"
		print st
		f.write(st)
		f.flush()
		time.sleep(random.random() * 10)

	f.close()

	problem.status = Problem.COMPLETE

	problem.save()