from django.db import models

class Products(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    types = [
        ('TVS','TV Series'),
        ('Пол.метр.','Полнометражный' ),
        ('Кор.метр.','Короткометражный'),
    ]
    type = models.CharField(max_length=50,choices=types)
    studios = models.CharField(max_length=255)
    statuses = [
        ('Зак.','Законнченный'),
        ('В раз','В разработке')
    ]
    status = models.CharField(max_length=100)
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
