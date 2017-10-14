from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import pre_delete, post_delete
from django.dispatch.dispatcher import receiver

from django.conf import settings

#Exceptions
from django.core.exceptions import ObjectDoesNotExist

#additional imports
import os
import time
import utils


class TrainingFile(models.Model):
    
    title = models.CharField(max_length=100, blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True)
    path=models.CharField(max_length=200, blank=True, null=True)
    docfile = models.FileField(upload_to=utils.get_upload_training_path, blank=True, null=True)
    
    def __unicode__(self):
        return self.title

    def delete_file(self):
        print os.path.join(settings.MEDIA_ROOT, self.docfile)


@receiver(pre_delete, sender=TrainingFile)
def TrainingFile_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.docfile.delete(False)

class TestFile(models.Model):
    
    title = models.CharField(max_length=100, blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True)
    path=models.CharField(max_length=200, blank=True, null=True)
    docfile = models.FileField(upload_to=utils.get_upload_test_path, blank=True, null=True)

    def __unicode__(self):
        return self.title


@receiver(pre_delete, sender=TestFile)
def TestFile_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.docfile.delete(False)

class ModelFile(models.Model):

    title = models.CharField(max_length=100, blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True)
    path=models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return self.title




class Problem(models.Model):

    EXPECTING_TRAINING_FILE = 0
    EXPECTING_START_TRAINING = 1
    TRAINING = 2
    EXPECTING_TEST_FILE = 3
    EXPECTING_START_EVALUATION = 4
    EVALUATION = 5
    COMPLETE = 6

    STATUS_CHOICES = (
        (EXPECTING_TRAINING_FILE, 'expecting_training_file'),
        (EXPECTING_START_TRAINING, 'expecting_start_training'),
        (TRAINING, 'training'),
        #(TRAINING_FINISHED, 'training_finished'),
        (EXPECTING_TEST_FILE, 'expecting_test_file'),
        (EXPECTING_START_EVALUATION, 'expecting_start_evaluation'),
        (EVALUATION, 'evaluation'),
        #(EVALUATION_FINISHED, 'evaluation_finished'),
        (COMPLETE, 'complete')
    )


    title = models.CharField(max_length=100)
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    #blank=True => optional
    trainingfile=models.ForeignKey(TrainingFile, null=True)
    testfile=models.ForeignKey(TestFile, null=True)
    modelsfile=models.ForeignKey(ModelFile, null=True)
    creation_date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.title



class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, unique=True)
    problem = models.OneToOneField(Problem, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=60, blank=True)
    state_province = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=50, blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username



@receiver(pre_delete, sender=User)
def User_delete(sender, instance, **kwargs):

   
    # Pass false so FileField doesn't save the model.
    print os.path.join(settings.MEDIA_ROOT, instance.username)
    try:
        userprofile = UserProfile.objects.get(user=instance)
        print userprofile
        if userprofile:
            problem = userprofile.problem
            print problem
            if problem:
                trainingfile=problem.trainingfile
                testfile=problem.testfile
                modelsfile=problem.modelsfile

                print trainingfile
              
                if trainingfile:
                    trainingfile.delete()

                if testfile:
                    testfile.delete()

                if modelsfile:
                    modelsfile.delete()

                problem.delete()

            for root, dirs, files in os.walk(os.path.join(settings.MEDIA_ROOT, instance.username), topdown=False):
                print root
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

            os.rmdir(os.path.join(settings.MEDIA_ROOT, instance.username))
    except ObjectDoesNotExist:
        print "No userprofile..."

# @receiver(pre_delete, sender=UserProfile)
# def post_delete_user(sender, instance, *args, **kwargs):
#     if instance.problem: # just in case user is not specified
#         instance.problem.delete()