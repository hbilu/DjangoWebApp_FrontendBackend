from django.urls import path
from .views import UserListView, UpdateUserStatusView
from django.views.generic import TemplateView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'), # api/
    path('user/', TemplateView.as_view(template_name="users/user_list.html"),name='drag-drop'),
    path('status/', UpdateUserStatusView.as_view(), name='update_status'),
    ]