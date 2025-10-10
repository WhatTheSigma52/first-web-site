from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=32, verbose_name='Название группы')
    slug = models.SlugField(unique=True, verbose_name='читабельный url группы')
    description = models.TextField(verbose_name='Описание группы')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Post(models.Model):
    text = models.TextField(verbose_name='Текст поста')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts',
                               verbose_name='Автор')
    group = models.ForeignKey(Group,
                              on_delete=models.SET_NULL,
                              related_name='posts',
                              blank=True,
                              null=True,
                              verbose_name='Группа')
    image = models.ImageField(upload_to='posts/',
                              blank=True,
                              verbose_name='Фотография')

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор')
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='Пост')

    def __str__(self):
        return self.text[0:20]

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий',
        verbose_name_plural = 'Комментарии'


class Subscribe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Подписка')
    subscriber = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name='follower',
                                   verbose_name='Подписчик')

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=['author', 'subscriber'],
                                    name='unique_subscribe'),
        )
        verbose_name = 'Подписка',
        verbose_name_plural = 'Подписки'


class Profile(models.Model):
    image = models.ImageField(upload_to='posts/profile/',
                              default='posts/profile/default_photo.png',
                              blank=True,
                              null=True,
                              verbose_name='Фото профиля')
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile',
                                verbose_name='Пользователь')
    nickname = models.TextField(max_length=32,
                                default='No name',
                                blank=True,
                                verbose_name='Ник пользователя')

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Профиль',
        verbose_name_plural = 'Профили'
