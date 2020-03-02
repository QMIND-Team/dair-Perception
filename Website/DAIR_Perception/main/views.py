from django.shortcuts import render
from django.http import HttpResponse

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