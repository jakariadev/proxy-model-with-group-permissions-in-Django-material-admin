# from django.contrib import admin

# # Register your models here.


# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.utils.translation import gettext_lazy as _
# from .models import (
#     User,
#     Profile,
#     Education,
#     Address,
#     ControllerMore,
#     Controller,
#     TeacherMore,
#     StudentMore,
#     GuardianMore,
#     EmployeeMore,
#     Employee,
# )

# # Define a Custom User admin


# class UserAdmin(BaseUserAdmin):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # update fieldsets
#         _fieldsets = list(super().fieldsets)
#         try:
#             _fieldsets.insert(2, (_('Account Types'), {'fields': ('types',)}))
#         except Exception as e:
#             _fieldsets.append((_('Account Types'), {'fields': ('types',)}))
#         self.fieldsets = tuple(_fieldsets)

#         # update search_fields
#         self.search_fields = list(super().search_fields)
#         self.search_fields.append('types')

#         # update list_filter
#         # self.list_filter = list(super().list_filter)
#         # self.list_filter.append('types')


# admin.site.register(User, UserAdmin)

# admin.site.register(Profile)
# admin.site.register(ControllerMore)
# admin.site.register(TeacherMore)
# admin.site.register(StudentMore)
# admin.site.register(GuardianMore)
# admin.site.register(EmployeeMore)
# admin.site.register(Employee)
# admin.site.register(Controller)


from django.apps import apps
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import *
from django.contrib.sessions.models import Session

from django.contrib.admin import ModelAdmin, register
from accounts.models import *


@register(Address)
class MaterialAddressAdmin(ModelAdmin):
    icon_name = 'place'

@register(ControllerMore)
class MaterialControllerMoreAdmin(ModelAdmin):
    icon_name = 'power'

@register(Education)
class MaterialEducationAdmin(ModelAdmin):
    icon_name = 'school'

@register(EmployeeMore)
class MaterialEmployeeMoreAdmin(ModelAdmin):
    icon_name = 'wc'

@register(GuardianMore)
class MaterialGuardianMoreAdmin(ModelAdmin):
    icon_name = 'person_pin'
@register(StudentMore)
class MaterialStudentMoreAdmin(ModelAdmin):
    icon_name = 'people_outline'
@register(TeacherMore)
class MaterialTeacherMoreAdmin(ModelAdmin):
    icon_name = 'supervisor_account'

@register(Profile)
class MaterialProfileAdmin(ModelAdmin):
    icon_name = 'contacts'




class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(ListAdminMixin, self).__init__(model, admin_site)


models = apps.get_models()

for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass

admin.site.unregister(ContentType)
admin.site.unregister(Teacher)
admin.site.unregister(Student)
admin.site.unregister(Guardian)
admin.site.unregister(Employee)
admin.site.unregister(Controller)
admin.site.unregister(HistoricalAddress)
admin.site.unregister(HistoricalEducation)
admin.site.unregister(HistoricalTeacherMore)
admin.site.unregister(HistoricalStudentMore)
admin.site.unregister(HistoricalProfile)
admin.site.unregister(HistoricalControllerMore)
admin.site.unregister(HistoricalEmployeeMore)
admin.site.unregister(HistoricalGuardianMore)


