from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from app.models import Post
from app.forms import PostForm, CustomUserCreationForm

# TODO: Сделать Страницу Главную Index
class IndexView(ListView):
    """
    Представления для Главной Страницы
    """
    # Для подключения Модели
    model = Post
    # Устанавливаем Шаблон HTML
    template_name = "app/index.html"
    # Имя переменной в Шаблоне
    context_object_name = "posts"
    # Сортировка по какому то полю либо несколько полей
    ordering = ["-created_at"]  # по убыванию
    # Для реализации пагинации
    paginate_by = 30


# TODO: Авторизацию
# TODO: Регистрацию
# TODO: Сделать Страницу Создание Поста
class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Представления для Создания Поста
    Но Посты могут создавать только авторизованные пользователи
    """
    # Для Подключения Модельки чтоб знать обьект какой модельки он должен создать
    model = Post
    # Для Создания Поста нужно указывать форму
    form_class = PostForm
    # Шаблон HTML
    template_name = "app/post_form.html"
    # Куда перенаправлять после создания
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# TODO: Сделать Страницу Списка Постов
class PostListView(ListView):
    """
    Представления для Списка Постов
    """
    # Для подключения Модели
    model = Post
    # Устанавливаем Шаблон HTML
    template_name = "app/post_list.html"
    # Имя переменной в Шаблоне
    context_object_name = "posts"
    # Сортировка по какому то полю либо несколько полей
    ordering = ["-created_at"]  # по убыванию
    # Для реализации пагинации
    paginate_by = 50


# TODO: Сделать Страницу Просмотра Поста
class PostDetailView(DetailView):
    """
    Представления для Получения Одного Конкретного Поста
    """
    # Моделька
    model = Post
    # Шаблон HTML
    template_name = "app/post_detail.html"
    # Имя Переменной в Шаблон
    context_object_name = "post"


# TODO: Сделать Страницу Изменение Поста
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "app/post_form.html"
    form_class = PostForm

    # success_url = reverse_lazy("post-detail", pk=pk)
    def get_success_url(self):  # /posts/3
        return reverse_lazy("post-detail", pk=self.object.pk)

    def test_func(self):
        """
        Проверка того что пользователь является автором изменяемого поста
        :return:
        """
        post = self.get_object()
        return self.request.user == post.author


# TODO: Сделать Страницу Подтверждение Удаления
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "app/post_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        """
        Проверка того что пользователь является автором удаляемого поста
        :return:
        """
        post = self.get_object()
        return self.request.user == post.author


# TODO: Сделать Страницу Создание Жалоб

# TODO: Сделать Страницу Список жалоб Пользователя

# TODO: Сделать Авторизацию и Регистрацию
# Регистрацию
def register(request):
    if request.method == "POST":  # Пользователь уже зашел на страницу и заполнил форму
        form = CustomUserCreationForm(request.POST)  # Тут вставили в форму данные которые дал пользователь
        if form.is_valid():  # Мы проверили что он правильно заполнил форму
            user = form.save()  # Сохранили Пользователя
            return redirect("login")
    else:  # Пользователь только зашел на страницу
        form = CustomUserCreationForm()  # Отправили пустую пользователю чтобы он ее заполнил
    return render(
        request,  # запрос пользователя
        "app/register.html",  # шаблон который должна показать пользователю
        {
            "form": form
        }  # Контекст (Данные) которые должны показаться пользователю
    )


# Логин
class CustomLoginView(LoginView):
    template_name = "app/login.html"
    success_url = reverse_lazy("index")

