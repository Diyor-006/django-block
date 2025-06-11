from django.contrib import admin

from app.models import Post, Like, DisLike, Report, Comment, Media


class CommentInline(admin.TabularInline):
    model = Comment  # Моделька для которой мы делаем Инлайн
    extra = 0  # При создании сколько обьектов должно появляться


class MediaInline(admin.StackedInline):
    model = Media
    extra = 2
    max_num = 10  # максимальное кол-во которое можно создать для определенного поста


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Админ Панель для Модельки Поста
    """
    # Помогает нам видеть какие столбцы должны быть в списке Постов
    list_display = ["pk", "title", "author", "created_at", "get_like_count", "get_dislike_count", "get_comment_count"]
    # Помогает нам создать фильтры для определенных столбцов
    list_filter = ["author", "created_at"]
    # Помогает реализовать поиск по определенным столбцам
    search_fields = ["title"]
    # Помогает реализовать пагинацию разделение на страницы
    list_per_page = 50
    # Подключение Вкладок с привязанными к нашей модели других
    inlines = [CommentInline, MediaInline]

    # TODO: Нужно реализовать логику кол-во лайков, дизлайков и комментов

    def get_like_count(self, obj):
        """
        Метод для подсчета кол-во Лайков
        :param obj: Моделька Post
        :return: Кол-во Лайков
        """
        return obj.likes.count()

    get_like_count.short_description = "Лайки"

    def get_comment_count(self, obj):
        """
        Для Подсчета Комментариев
        :param obj: Моделька Post
        :return: Кол-во Комментариев
        """
        return obj.comments.count()

    get_comment_count.short_description = "Комменты"

    def get_dislike_count(self, obj):
        """
        Для Подсчета ДизЛайков
        :param obj: Моделька Post
        :return: Кол-во Дизлайков
        """
        return obj.dislikes.count()

    get_dislike_count.short_description = "Дизлайки"


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["theme", "post", "user", "is_solve", "created_at"]
    list_filter = ["user", "theme", "is_solve", "created_at"]
    list_per_page = 35
