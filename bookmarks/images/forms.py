from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {'url': forms.HiddenInput, }  # Поле url не будет видно пользователю

    def clean_url(self):
        """возможность проверять каждое поле формы по отдельности с помощью мето-
        дов вида clean_<fieldname>(). Эти методы вызываются, когда мы обращаемся
        к методу is_valid() формы."""

        url = self.cleaned_data['url']

        valid_extensions = ['bmp', 'png', 'jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower() # отделяет расширение файла(строка из 2-ух->список->последний элем->lower)
        #if extension not in valid_extensions:
            #raise forms.ValidationError('The given URL does not match valid image extensions.')

        # Пришлось убрать, т.к. url картинки часто не оканчивается расширением картинки

        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        """Переопределение метода, чтобы заполнять форму и скачивать изображение
        при любом сохранении формы, а не только в конкретном обработчике"""

        image = super(ImageCreateForm, self).save(commit=False)  # вызывается метод базового класса
        image_url = self.cleaned_data['url']
        image_name = f'{slugify(image.title)}.{image_url.rsplit(".", 1)[1].lower()}'

        response = request.urlopen(image_url)  # Скачиваем img
        image.image.save(image_name, ContentFile(response.read()), save=False)

        if commit:
            image.save()
        return image




