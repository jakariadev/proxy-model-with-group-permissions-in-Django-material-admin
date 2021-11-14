from django.urls import path
from .views import *
# urlpatterns = [
#       # for rest api
#     path('register/',registrationAPI),

# ]

app_name = 'accounts'

urlpatterns = [
    path('signup/', sign_up, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', user_profile, name='profile'),
]


#http://127.0.0.1:8000/user/login/
#http://127.0.0.1:8000/user/signup/
#http://127.0.0.1:8000/user/logout/
#http://127.0.0.1:8000/user/profile/

