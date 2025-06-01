from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Word(models.Model):
    word_uz_lot = models.CharField(max_length=100)
    word_uz_kr = models.CharField(max_length=100)
    word_ru = models.CharField(max_length=100)
    word_en = models.CharField(max_length=100)
    word_tu = models.CharField(max_length=100)
    meaning = models.TextField()
    sinon = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='words')

    def __str__(self):
        return self.word_uz_lot