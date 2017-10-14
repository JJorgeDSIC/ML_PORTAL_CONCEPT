from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

#csrf things, to POST requests
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf

#Authentication
from django.contrib import auth
from django.contrib.auth.decorators import login_required

#Models
from .models import UserProfile, TrainingFile, TestFile, ModelFile, Problem 

#Forms
from .forms import TrainingFileForm, TestFileForm

#Exceptions
from django.core.exceptions import ObjectDoesNotExist

from tasks import mockup_method, mockup_method_eval

from .utils import validate_csv

import random
import os




def prepare_nav_bar(request, exp_train, exp_start_train, exp_test, exp_start_eval):

    c = {}
    c.update(csrf(request))

    c['expecting_training_file'] = exp_train
    c['expecting_start_training'] = exp_start_train
    c['expecting_test_file'] = exp_test
    c['expecting_start_evaluation'] = exp_start_eval


    c['expecting_training_file_link'] = "/problems/show_problem_status/?q=upload_training"
    c['expecting_start_training_link'] = "/problems/show_problem_status/?q=train"
    c['expecting_test_file_link'] = "/problems/show_problem_status/?q=upload_test"
    c['expecting_start_evaluation_link'] = "/problems/show_problem_status/?q=evaluate"

    # c['expecting_training_file_link'] = "/problems/?q=upload_training"
    # c['expecting_start_training_link'] = "/problems/?q=train"
    # c['expecting_test_file_link'] = "/problems/?q=upload_test"
    # c['expecting_start_evaluation_link'] = "/problems/?q=evaluate"

    return c

def login(request):

    c = {}
    c.update(csrf(request))
    
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    if username is None or username == '':
    	return render(request, 'login/login.html', c)

    user = auth.authenticate(username=username, password=password)

    
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.

        return HttpResponseRedirect("/problems/")
        
    else:
        # Show an error page
        c['errormsg'] = 'Wrong username or password'
        return render(request, 'login/login.html', c)

@login_required
def logout(request):

	auth.logout(request)
	c = {}
	c['logoutmsg'] = 'You are logged out'
	return render(request, 'login/login.html', c) 


def set_nav_status(request, status, request_status):

    if status == Problem.EXPECTING_TRAINING_FILE:
        c = prepare_nav_bar(request, "active","disabled","disabled","disabled")
        next = "problem/upload_training.html"

    elif status == Problem.EXPECTING_START_TRAINING:

        if request_status == 'upload_training':

            c = prepare_nav_bar(request, "complete","active","disabled","disabled")
            next = "problem/upload_training.html"

        else:

            c = prepare_nav_bar(request, "complete","active","disabled","disabled")
            next = "problem/training.html"
            c['expecting'] = True

    elif status == Problem.TRAINING:

        c = prepare_nav_bar(request, "complete","active","disabled","disabled")
        next = "problem/training.html"
        c['running'] = True

    elif status == Problem.EXPECTING_TEST_FILE:

        c = prepare_nav_bar(request, "complete","complete","active","disabled")

        if request_status == 'upload_training':
            
            next = "problem/upload_training.html"

        elif request_status == 'train':
            c['complete'] = True
            next = "problem/training.html"
        else:
       
            next = "problem/upload_test.html"
            
    elif status == Problem.EXPECTING_START_EVALUATION:
        c = prepare_nav_bar(request, "complete","complete","complete","active")

        if request_status == 'upload_training':
            
            next = "problem/upload_training.html"

        elif request_status == 'train':

            c['complete'] = True
            next = "problem/training.html"

        elif request_status == 'upload_test': 
        
            next = "problem/upload_test.html"   

        else:
            c['expecting'] = True
            next = "problem/evaluate.html"

    elif status == Problem.EVALUATION:

        c = prepare_nav_bar(request, "complete","complete","complete","active")
        next = "problem/evaluate.html"
        c['running'] = True

    else: # status == Problem.COMPLETE:

        c = prepare_nav_bar(request, "complete","complete","complete","complete")

        if request_status == 'upload_training':
            
            next = "problem/upload_training.html"

        elif request_status == 'train':

            c['complete'] = True
            next = "problem/training.html"

        elif request_status == 'upload_test':

            next = "problem/upload_test.html"

        else:

            next = "problem/evaluate.html"
            c['complete'] = True


    print c
    print next
    return c, next

@login_required
def show_problem_status(request):

    print request.user.userprofile

    if request.user.userprofile is not None:

        status = request.user.userprofile.problem.status
        print "Show problems status..."
        request_status = request.GET.get('q','')
        print request_status

        c, next = set_nav_status(request, status,request_status)

        return render(request, next, c)

    else:

        return render(request, "login/login.html")
    # if request_status == 'upload_training':

        

    #     c['problem'] = request.user.userprofile.problem
    #     return render(request, next, c)

    # elif request_status == 'train':   
        
    #     c, next = set_nav_status(request, status,request_status)

    #     c['problem'] = request.user.userprofile.problem
    #     return render(request, next, c)

    # elif request_status == 'upload_test':  

    #     c, next = set_nav_status(request, status,request_status)

    #     c['problem'] = request.user.userprofile.problem
    #     return render(request, next, c)

    # elif request_status == 'evaluate':  

    #     c, next = set_nav_status(request, status,request_status)

    #     c['problem'] = request.user.userprofile.problem
    #     return render(request, next, c)

    # else:

    #     return render(request, "login/login.html", c)

@login_required
def load_problem(request):

    print "Loading problems..."

    request_status = request.GET.get('q','')

    status = request.user.userprofile.problem.status

    print status

    if status == Problem.EXPECTING_TRAINING_FILE:
        print "Expecting Training File"
        c = prepare_nav_bar(request, "active","disabled","disabled","disabled")
        c['problem'] = request.user.userprofile.problem
        return render(request, "problem/upload_training.html", c)
        #return HttpResponseRedirect("/problems/upload_training/")

    elif status == Problem.EXPECTING_START_TRAINING or status == Problem.TRAINING:
        print "Expecting Start training OR view training status"
        #return HttpResponseRedirect("/problems/train/")
        c = prepare_nav_bar(request, "complete","active","disabled","disabled")
        if status == Problem.TRAINING:
            print "Running..."
            c['running'] = True

        if status == Problem.EXPECTING_START_TRAINING:
            print "Show button..."
            c['expecting'] = True

        return render(request, "problem/training.html", c)

    elif status == Problem.EXPECTING_TEST_FILE:
        c = prepare_nav_bar(request, "complete","complete","active","disabled")
        print "Expecting Test File"
        print "Expecting Training File"
        c['problem'] = request.user.userprofile.problem
        return render(request, "problem/upload_test.html", c)
        #return HttpResponseRedirect("/problems/upload_test/")

    #status == Problem.EXPECTING_START_EVALUATION or status == Problem.EVALUATION or status == Problem.COMPLETE:
    else:
        print "Expecting Start Evaluation OR view Evaluation status"
        #return HttpResponseRedirect("/problems/train/")
        c = prepare_nav_bar(request, "complete","complete","complete","active")
        if status == Problem.EVALUATION:
            print "Running..."
            c['running'] = True

        if status == Problem.EXPECTING_START_EVALUATION:
            print "Show button..."
            c['expecting'] = True

        if status == Problem.COMPLETE:
            print "Running..."
            c['complete'] = True

        return render(request, "problem/evaluate.html", c)
        #return HttpResponseRedirect("/problems/evaluate/")


def validate_training(data):

    return validate_csv(data)

    # if random.random() < 0.9:
    #     return True
    # else:
    #     return False


def validate_test(data):

    return validate_csv(data)
    # if random.random() < 0.9:
    #     return True
    # else:
    #     return False


@csrf_protect
@login_required
def upload_training(request):

    print "Upload_Training"

    if request.method == 'POST':

        profile = request.user.userprofile

        problem = request.user.userprofile.problem

        #data = request.FILES['file'].read()

        valid = validate_training(request.FILES['file'])

        if valid:

            try:
                trainingfile = problem.trainingfile
            except ObjectDoesNotExist:
                trainingfile = None


            if trainingfile is not None:

                problem.trainingfile = None
                problem.status = Problem.EXPECTING_TRAINING_FILE
                problem.save()

                trainingfile.delete()

                if problem.testfile is not None:

                    test_file = problem.testfile

                    problem.testfile = None
                    problem.status = Problem.EXPECTING_TEST_FILE
                    problem.save()

                    test_file.delete()
                
                

            new_file = TrainingFile(title=request.FILES['file'], path=profile.user.username, docfile=request.FILES['file'])
            new_file.save()

            problem.status = Problem.EXPECTING_START_TRAINING
            problem.trainingfile = new_file
            problem.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Wrong Format!'})
    else:
        return JsonResponse({'success': False})

@login_required
def check_upload_training(request):

    status = request.user.userprofile.problem.status

    print status

    if status == Problem.EXPECTING_TRAINING_FILE:
        return JsonResponse({'filetitle': None})

    else:
        training_file = request.user.userprofile.problem.trainingfile
        return JsonResponse({'filetitle': training_file.title, 'filesize': training_file.docfile.size})

@login_required
def delete_training(request):

    print "On Delete"

    try:
        problem = request.user.userprofile.problem
        trainingfile = problem.trainingfile

        problem.trainingfile = None
        problem.status = Problem.EXPECTING_TRAINING_FILE
        problem.save()

        trainingfile.delete()

        if problem.testfile is not None:

            test_file = problem.testfile

            problem.testfile = None
            problem.save()

            test_file.delete()

        return JsonResponse({'success': True})

    except Exception:

        return JsonResponse({'success': False})

    

    # training_file = request.user.userprofile.problem.trainingfile
    # training_file.delete()

    # request.user.userprofile.problem.status = Problem.EXPECTING_TRAINING_FILE
    # request.user.userprofile.problem.save()




@csrf_protect
@login_required
def upload_test(request):

    print "Upload_Test"

    if request.method == 'POST':

        profile = request.user.userprofile

        problem = request.user.userprofile.problem

        #data = request.FILES['file'].read()

        valid=validate_test(request.FILES['file'])

        if valid:

            try:
                testfile = problem.testfile
            except ObjectDoesNotExist:
                testfile = None

            if testfile is not None:

                problem.testfile = None
                problem.status = Problem.EXPECTING_TEST_FILE
                problem.save()

                testfile.delete()

            new_file = TestFile(title=request.FILES['file'], path=profile.user.username, docfile=request.FILES['file'])
            new_file.save()

            problem.status = Problem.EXPECTING_START_EVALUATION
            problem.testfile = new_file
            problem.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Wrong Format!'})
    else:
        return JsonResponse({'success': False, 'message': 'Wrong request!'})

@login_required
def check_upload_test(request):

    status = request.user.userprofile.problem.status

    print status

    if status == Problem.EXPECTING_TEST_FILE:
        return JsonResponse({'filetitle': None})

    else:
        test_file = request.user.userprofile.problem.testfile
        return JsonResponse({'filetitle': test_file.title, 'filesize': test_file.docfile.size})

@login_required
def delete_test(request):

    print "On Delete"

    try:

        problem = request.user.userprofile.problem
        test_file = problem.testfile

        problem.testfile = None
        problem.status = Problem.EXPECTING_TEST_FILE
        problem.save()

        test_file.delete()

        return JsonResponse({'success': True})

    except Exception:

        return JsonResponse({'success': False})

    

    # training_file = request.user.userprofile.problem.trainingfile
    # training_file.delete()

    # request.user.userprofile.problem.status = Problem.EXPECTING_TRAINING_FILE
    # request.user.userprofile.problem.save()

@login_required
def check_training(request):

    c = {}
    c.update(csrf(request))

    problem = request.user.userprofile.problem

    if problem.status == Problem.EXPECTING_TEST_FILE:

        # print "Show button..."
        # c['complete'] = True
        # return render(request, "problem/training.html", c)
        return JsonResponse({'progress' : 1.0})

    st = "documents/" + request.user.username + "/logs/training_log.txt"
    print st
    print os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    f = open(st)

    part = f.read().split()[-1]

    print part.split("/")

    porc = float(part.split("/")[0]) / float(part.split("/")[1])
    
    print porc

    if porc == 1.0:

        problem.status = Problem.EXPECTING_TEST_FILE

        problem.save()


    return JsonResponse({'progress' : porc})



@login_required
def start_training(request):

    print "On start training..."

    profile = request.user.userprofile
    
    problem = request.user.userprofile.problem

    problem.status = Problem.TRAINING

    problem.save()

    mockup_method.delay(request.user.username)

    return JsonResponse({'progress' : 0})






@login_required
def check_evaluation(request):

    c = {}
    c.update(csrf(request))

    problem = request.user.userprofile.problem

    if problem.status == Problem.COMPLETE:
        # print "Show button..."
        # c['complete'] = True
        # return render(request, "problem/evaluation.html", c)
        return JsonResponse({'progress' : porc})

    st = "documents/" + request.user.username + "/logs/evaluation_log.txt"

    print st
    print os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    f = open(st)

    part = f.read().split()[-1]

    print part.split("/")

    porc = float(part.split("/")[0]) / float(part.split("/")[1])
    
    print porc

    if porc == 1.0:

        problem.status = Problem.COMPLETE

        problem.save()


    return JsonResponse({'progress' : porc})



@login_required
def start_evaluation(request):

    print "On start evaluation..."

    profile = request.user.userprofile
    
    problem = request.user.userprofile.problem

    problem.status = Problem.EVALUATION

    problem.save()

    mockup_method_eval.delay(request.user.username)

    return JsonResponse({'progress' : 0})