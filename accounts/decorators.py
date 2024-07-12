from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrappter_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else: 
            return view_func(request, *args, **kwargs)
    
    return wrappter_func

def allowed_users(allowred_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None           
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowred_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponse('you are not allowed')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        print('it ran')
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':
            return redirect('user-page')
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        return HttpResponse("You are not authorized to access this page.")
    return wrapper_func


        
            