from django.urls import re_path

from . import views

app_name = 'usuarios'

urlpatterns = [

    re_path(
        r'^$',
        views.user_login,
        name='login'
    ),

    re_path(
        r'^logout/$',
        view=views.user_logout,
        name='logout'
    ),
]
