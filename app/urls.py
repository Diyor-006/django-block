from django.urls import path
from django.contrib.auth.views import LogoutView
from app.views import IndexView, CustomLoginView, register, PostListView, PostDetailView, PostDeleteView, PostCreateView, PostUpdateView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),  # Главная Страница
    path("auth/register", register, name="register"),  # Регистрация
    path("auth/login", CustomLoginView.as_view(), name="login"),  # Авторизация
    path("auth/logout", LogoutView.as_view(next_page="login"), name="logout"),  # Выход из учетки

    # Посты
    path("posts/", PostListView.as_view(), name="post-list"), # Список постов
    path("posts/<int:pk>", PostDetailView.as_view(), name="post-detail"), # Получение Поста
    path("posts/delete/<int:pk>", PostDeleteView.as_view, name="post-delete"), # Удаление Поста
    path("posts/create",PostCreateView.as_view(), name="post-create"),
    path("posts/update/<int:pk>", PostUpdateView.as_view(), name="post-update")

]
