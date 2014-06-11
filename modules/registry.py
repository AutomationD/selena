# !/usr/bin/env python3

get_methods = {}
post_methods = {}

# Decorators

def GET(class_name) :
    def real_dec (func) :
        func_full_name = class_name + '.' + func.__name__
        get_methods[func_full_name] = func
    return real_dec

def POST(class_name) :
    def real_dec (func) :
        func_full_name = class_name + '.' + func.__name__
        post_methods[func_full_name] = func
    return real_dec

# Getter

def get_method(rest_method, method_full_name) :
    if rest_method == 'GET' :
        return get_methods.get(method_full_name, None)
    elif rest_method == 'POST' :
        return post_methods.get(method_full_name, None)
    return None
