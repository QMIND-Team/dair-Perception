from django.shortcuts import render
from django.http import HttpResponse
import subprocess

def launchClock(request):
    if request.POST:
        subprocess.call(['start-image-read', 'clock'])

    return render(request,'home.html',{})

def launchBottle(request):
    if request.POST:
        subprocess.call(['start-image-read', 'bottle'])

    return render(request,'home.html',{})

def launchGiraffe(request):
    if request.POST:
        subprocess.call(['start-image-read', 'giraffe'])

    return render(request,'home.html',{})

def launchPlant(request):
    if request.POST:
        subprocess.call(['start-image-read', 'pottedplant'])

    return render(request,'home.html',{})

def stop(request):
    if request.POST:
        subprocess.call('stop-image-read')

    return render(request,'home.html',{})


def robot(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def images(request):
    return render(request, 'images.html')

def test(request):
    return render(request, 'test.html')

'''
if request.method == 'POST' and 'run_script' in request.POST:

    # import function to run
    from path_to_script import function_to_run

    # call function
    function_to_run() 

    # return user to required page
    return HttpResponseRedirect(reverse(app_name:view_name)
'''