from django.contrib import messages
from django.contrib.auth.models import Group
from django.views.generic import TemplateView
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from institude.models import Institude, InstituteGroups


# class DashboardView(TemplateView):
#     template_name = 'u_dashboard/dashboard.html'
@login_required(login_url='/user/login/')
def dashboard(request):
    template_name = 'u_dashboard/dashboard.html'
    try:
        pay = request.user.payment_status
        if pay.status:
            status = True
        else:
            status = False
    except Exception as e:
        print(e)
        status = False
    if request.user:
        ins = Institude.objects.filter(owner=request.user)
    else:
        ins = []
    context={
        'status':status,
        'ins':ins,
    }
    return render(request, template_name, context)

def groups_list(request, id):
    in_need = Institude.objects.get(id=id)
    groups = InstituteGroups.objects.filter(institutes=in_need)
    template_name = 'u_dashboard/groups_list.html'
    context={
        'groups':groups,
        'id':id,
        'form' : SignUpForm()
    }
    return render(request, template_name, context)

from django.contrib.auth import get_user_model
User = get_user_model()
from accounts.forms import SignUpForm
def create_user(request, id):
    grp = Group.objects.get(id=id)
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.errors:
            for field in form:
                for error in field.errors:
                    messages.warning(request,str(error)+" for field: " + str(field.name))
        if form.is_valid():
            user = form.save()
            messages.success(request, "user created")
            grp.user_set.add(user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def add_user(request, id):
    grp = Group.objects.get(id=id)
    if request.method == 'POST':
        username = request.POST.get('username', None)
        if username:
            if User.objects.filter(username = username).exists():
                user = User.objects.get(username = username)
                grp.user_set.add(user)
                messages.success(request, "user added to group")
            else:
                messages.warning(request, "No user found with this username")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

