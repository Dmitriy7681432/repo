from django.db import models

# Create your models here.
class Tag(models.Model):
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.tag_name}'

class Article(models.Model):
    article_name = models.CharField(max_length=100)
    article_text = models.CharField(max_length= 1000)
    article_date = models.DateTimeField('date published')
    article_tag = models.ManyToManyField(Tag)

    def __str__(self):
        return f'{self.article_name}, published: {self.article_date}'

    '''
    DataField - дата
    TimeField - время
    
    Числовые типы:
    IntegerField
    PositeveIntegerField
    FloatField
    
    Логические типы:
    BooleanField
    
    Байтовый тип:
    BinaryField
    
    Email:
    EmailField
    
    URL:
    URLField
    
    Image:
    ImageField
    '''