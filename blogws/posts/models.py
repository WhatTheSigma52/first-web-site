from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=30, verbose_name='Имя группы')
    slug = models.SlugField(unique=True, verbose_name='Slug группы')
    description = models.TextField(verbose_name='Описание группы')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    # добавить параметры из ссылки с урока
    

class Post(models.Model):
    text = models.TextField(verbose_name='Текст поста')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания поста')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор поста')
    group = models.ForeignKey(Group,
                              on_delete=models.SET_NULL,
                              related_name='posts',
                              blank=True,
                              null=True,
                              verbose_name='Группа к которому относится пост')
    def __str__(self):
        return self.text[:20]
    
    # добавить параметры из ссылки с урока

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
