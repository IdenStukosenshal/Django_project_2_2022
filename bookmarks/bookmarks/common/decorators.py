from django.http import HttpResponseBadRequest

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'  # в учебнике это место устарело

"""https://django.fun/qa/182525/

Метод HttpRequest.is_ajax() устарел, 
так как он полагался на специфический для jQuery способ обозначения AJAX-вызовов, 
в то время как в настоящее время, как правило, используется JavaScript Fetch API.
"""

def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not is_ajax(request=request):  #not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap

