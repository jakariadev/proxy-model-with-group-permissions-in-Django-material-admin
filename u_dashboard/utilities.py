from .models import *

def get_hostname(request):
    return request.get_host().split(":")(0).lower()


def get_domain(request):
    hostname = get_hostname(request)
    subdomain = hostname.split(":")(0).lower()
    return Domain.objects.filter(subdomain=subdomain).first()
    
