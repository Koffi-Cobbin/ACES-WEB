from .models import Configuration
from django.http.request import HttpRequest



def global_context (request: HttpRequest, *args, **kwargs):
    return  {
        'config': Configuration.object(),
    }