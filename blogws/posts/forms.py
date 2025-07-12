from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {'text': 'Текст поста',
                  'group': 'Группа по интересам'}
        help_texts = {'text': 'Введите текст поста',
                      'group': 'Выберите группу для поста'}

    def clean_text(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError('Поле не должно быть пустым')
        return data
