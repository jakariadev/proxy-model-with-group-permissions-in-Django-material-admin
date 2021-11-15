from django.shortcuts import render, HttpResponseRedirect
from .forms import InstituteForm
from .models import *
from django.contrib import messages 
# Create your views here.

def institute_create(request):
    if request.method=="POST":
        form = InstituteForm(request.POST, request.FILES)
        if form.errors:
            for field in form:
                for error in field.errors:
                    messages.warning(request,str(error)+" for field: " + str(field.name))
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            grp=Group.objects.get(name=str(obj.name)+"_"+str(obj.id)+"_controller")
            grp.user_set.add(request.user)
            messages.success(request, "Successfully Created an Institute!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context ={
        'form': InstituteForm()
    }
    return render(request, 'institute/create.html', context)
