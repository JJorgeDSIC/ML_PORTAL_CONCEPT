from django.contrib import admin

from .models import UserProfile, TrainingFile, TestFile, ModelFile, Problem 

# Register your models here.

admin.site.register(UserProfile)

admin.site.register(TrainingFile)
admin.site.register(TestFile)
admin.site.register(ModelFile)

admin.site.register(Problem)