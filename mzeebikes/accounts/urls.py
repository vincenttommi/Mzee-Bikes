from django.urls import path
from .views import register_view, login_view, user_view, logout_view, bicycle_list,post_bicycle,update_bicycle,delete_bicycle

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('user/', user_view, name='user'),
    path('logout/', logout_view, name='logout'),
    path('bicyles/', bicycle_list, name='bicycle-list'),
    path('post_bicycle/',post_bicycle, name='post_bicycle'),
    path('update_bicycle/<int:pk>/', update_bicycle, name='update_bicycle'),
    path('delete_bicycle/<int:pk>/', delete_bicycle, name='delete_bicycle')
]
