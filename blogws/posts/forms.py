from django import forms
from .models import Post, Comment, Profile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {'text': 'Текст поста',
                  'group': 'Группа по интересам',
                  'image': 'Фотография'}
        help_texts = {'text': 'Введите текст поста',
                      'group': 'Выберите группу для поста',
                      'image': 'Загрузите фотографию'}

    def clean_text(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError('Поле не должно быть пустым')
        return data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': 'Текст комментария'}
        help_texts = {'text': 'Введите текст'}

    def clean_text(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError('Поле не должно быть пустым')
        return data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('nickname', 'image')
        labels = {'nickname': 'Ник',
                  'image': 'Фото профиля'}
        help_texts = {'image': 'Вставьте фотографию',
                      'nickname': 'Введите свой ник'}

    def clean_text(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError('Поле не должно быть пустым')
        return data
