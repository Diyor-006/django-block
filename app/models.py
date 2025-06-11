from django.db import models
from django.contrib.auth.models import User


# Посты
class Post(models.Model):
    """
    Моделька Постов, тут будет храниться все посты пользователей

    Attributes:
        title: Поле Название Поста максимально 256 символов
        content: Поле Контента Поста максимально 3000 символов
        created_at: Поле Дата Создания автоматически определяет время создания
        author: Поле Автор привязан к модели Пользователь(User)
    """
    title = models.CharField(max_length=256, verbose_name="Название Поста")
    content = models.CharField(max_length=3000, verbose_name="Контент Поста")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата Создания")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")

    def __str__(self):
        return self.title

    # Метод Подсчета Лайков
    def get_likes_count(self):
        return self.likes.count()

    # Метод Подсчета ДизЛайков
    def get_dislikes_count(self):
        return self.dislikes.count()

    # Метод Подсчета Комментов
    def get_comments_count(self):
        return self.comments.count()

    # Метод Доставания первого изображения
    def get_first_media(self):
        return self.media.order_by("created_at").first()

    class Meta:
        verbose_name_plural = "Посты"


# Комменты
class Comment(models.Model):
    """
    Моделька Комменты, она привязана к посту, у каждого поста будет комментарии

    Attributes:
        post: Пост которому был написан комментарий
        body: Содержимое Комментария
        user: Пользователь который написал Комментарий
        created_at: Время написания комментария
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="Пост")
    body = models.CharField(max_length=1024, verbose_name="Содержимое")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата Создания")

    def __str__(self):
        return f"{self.post.title}-{self.user.username}"

    class Meta:
        verbose_name_plural = "Комментарии"


# Лайки
class Like(models.Model):
    """
    Моделька для подсчета Лайков Постов

    Attributes:
        post: Пост которому поставили Лайк
        user: Пользователь который поставил Лайк
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes", verbose_name="Пост")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")


# Дизлайки
class DisLike(models.Model):
    """
    Моделька для подсчета ДизЛайков Постов

    Attributes:
        post: Пост которому поставили ДизЛайк
        user: Пользователь который поставил ДизЛайк
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="dislikes", verbose_name="Пост")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")


# Жалоба
class Report(models.Model):
    """
    Моделька Жалоб на посты

    Attributes:
        theme: Тема Жалобы
        post: Пост на который пожаловались
        user: Пользователь который пожаловался
        description: Описание Жалобы
        created_at: Время Жалобы
        is_solve: Решена ли жалоба?
    """
    # Choice
    THEMES = (
        ("NI", "Не Интересно"),
        ("CE", "Цензура"),
        ("SP", "Спам"),
        ("OT", "Другое")
    )
    theme = models.CharField(max_length=3, choices=THEMES, verbose_name="Тема")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    description = models.CharField(max_length=1024, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата Создания")
    is_solve = models.BooleanField(default=False, verbose_name="Решена")

    def __str__(self):
        return f"{self.post.title}-{self.user.username}-{self.theme}"

    class Meta:
        verbose_name_plural = "Жалобы"


# Медиа
class Media(models.Model):
    """
    Моделька для медиафайлов Постов

    Attributes:
        post: Пост к которому привязан Медиафайл
        created_at: Дата Создания Медиафайла
        url: Ссылка на изображение
        file: Сам файл
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media", verbose_name="Пост")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата Создания")
    url = models.URLField(null=True, blank=True, verbose_name="Ссылка")  # tesxt.com
    file = models.ImageField(upload_to="post-gallery/", null=True, blank=True)  # jpg png jpeg svg webp

    class Meta:
        verbose_name_plural = "Медиа"

# pip install pillow
