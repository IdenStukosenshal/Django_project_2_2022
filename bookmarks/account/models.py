from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Чтобы код не зависел от конкретной модели пользователя, используем функцию get_user_model() Она возвращает модель, указанную в настройке AUTH_USER_MODEL, и мы можем заменять класс пользователя, т. к. не обращались напрямую к конкретной модели  settings.AUTH_USER_MODEL == get_user_model()  https://habr.com/ru/post/152603/
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile for user{self.user.username}'


