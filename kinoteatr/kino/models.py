from django.db import models
from django.contrib.auth.models import User

from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

class Products(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    types = [
        ('Пол.метр.','Полнометражный' ),
        ('Кор.метр.','Короткометражный'),
    ]
    type = models.CharField(max_length=50,choices=types)
    studios = models.CharField(max_length=255)
    statuses = [
        ('Зак.','Законнченный'),
        ('В раз','В разработке')
    ]
    status = models.CharField(max_length=100,choices=statuses)
    duration = models.FloatField()
    qualities = [
        ('HD','HD'),
        ('FHD','FHD'),
        ('LOW','LOW',),
        ('2k','2K')
    ]
    quality = models.CharField(max_length=100,choices=qualities)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    highlighted = models.TextField()

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
        full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведения'
        verbose_name_plural = 'Произведения'
        

class Session(models.Model):
    film = models.ForeignKey(Products, on_delete=models.CASCADE)  
    session_time = models.DateTimeField()
    hall_number = models.IntegerField()

    def __str__(self):
        return f"{self.film.name} - {self.session_time.strftime('%Y-%m-%d %H:%M')} в зале {self.hall_number}"
    class Meta:
        verbose_name = 'Сеансы'
        verbose_name_plural = 'Сеансы'

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey('Session', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Билет на {self.session.film.name} - {self.session.session_time.strftime('%Y-%m-%d %H:%M')}"
    class Meta:
        verbose_name = 'Билеты'
        verbose_name_plural = 'Билеты'