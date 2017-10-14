from django.db.models.signals import post_save
from django.contrib.auth.models import User
from models import UserProfile, Problem
from django.db import models

import os

def create_profile(sender, **kw):
	
    user = kw["instance"]
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if kw["created"]:
    	os.mkdir(os.path.join(base + '/documents/', user.username))
    	os.mkdir(os.path.join(base + '/documents/' + user.username, 'models'))
    	os.mkdir(os.path.join(base + '/documents/' + user.username, 'logs'))
    	os.mkdir(os.path.join(base + '/documents/' + user.username, 'data'))

        profile = UserProfile(user=user)
        profile.save()
        problem = Problem(title='Problema_' + user.username, status=Problem.EXPECTING_TRAINING_FILE)
        problem.save()
        profile.problem = problem
        profile.save()

post_save.connect(create_profile, sender=User, dispatch_uid="users-profilecreation-signal")