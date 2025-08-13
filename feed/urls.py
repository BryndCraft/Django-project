from django.urls import path
from .views import (
    index,
    post_detail,
    create_post,
    like_post,
    add_comment,
    profile,
    follow_user,
    edit_profile,
    SignUpView  # Importa SignUpView correctamente
)

urlpatterns = [
    path('', index, name='index'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('create/', create_post, name='create_post'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('profile/<str:username>/', profile, name='profile'),
    path('profile/<str:username>/follow/', follow_user, name='follow_user'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('register/', SignUpView.as_view(), name='register'),  # Usa .as_view() para vistas basadas en clase
]