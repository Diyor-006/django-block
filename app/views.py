from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from app.models import Post, Like, DisLike, Report
from app.forms import PostForm, CustomUserCreationForm, CommentForm, ReportForm, UserChangeForm
from django.contrib.auth.decorators import login_required

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context

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

@login_required

def like_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)

        DisLike.objects.filter(post=post, user=request.user).delete()

        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()

        return redirect("post-detail", post_id)

def dislike_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)

        Like.objects.filter(post=post, user=request.user).delete()

        dislike, created = DisLike.objects.get_or_create(user=request.user, post=post)

        if not created:
            dislike.delete()

        return redirect("post-detail", post_id)
        
def create_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect("post-detail", post_id)
        else:
            return redirect("post-detail", post_id)
    else:
        return redirect("post-detail", post_id)

def about_us(request):
    pass

@login_required
# TODO: Создание Жалоб
def create_report(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.post = post
            report.save()
            return redirect("index")
        else:
            form = ReportForm()
            return render(
                request,
                "app/report_form.html",
                {
                    "form": form,
                    "post_id": post_id
                }
            )
    else:
        form = ReportForm()
        return render(
                request,
                "app/report_form.html",
                {
                    "form": form,
                    "post_id": post_id
                }
            )


# TODO: Получение Списка Жалоб
class ReportListView(ListView):
    model = Report 
    template_name = "app/report_list.html"
    context_object_name = "reports"

    def get_queryset(self):
        return Report.object.filter(user=self.request.user)


@login_required
def profile_view(request):
    user = get_object_or_404(User, request.user)
    return render(
        request,
        "app/profile.html",
        {
            "user": user
        }
    )

class UserUpdateView(UpdateView):
    form_class = UserChangeForm
    template_name = "app/user_form.html"
    success_url = reverse_lazy("index")
    model =User