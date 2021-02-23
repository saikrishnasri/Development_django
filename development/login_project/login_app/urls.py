from django.conf.urls import url,include
from . import views

app_name='login_app'

urlpatterns = [
    
    url('home/',views.home_view),
    url('reg/',views.reg_view),
    url('login/',views.login_view),
    url('logout_session_delete/',views.logout_session_delete),
    url('post/',views.post_list),
    url('create/',views.post_create),
    url('update/(?P<id>[0-9]+)/$',views.Post_update),
    url('delete/(?P<id>[0-9]+)/$',views.post_delete)
    
]
