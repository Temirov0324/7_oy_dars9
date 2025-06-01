from rest_framework import serializers
from .models import Word, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class WordListSerializers(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Word
        fields = ['id', 'word_uz_lot', 'word_uz_kr', 'word_ru', 'word_en', 'word_tu', 'category']


class WordSerializers(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)


    class Meta:
        model = Word
        fields = '__all__'


class RelatedWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'word_uz_lot', 'word_uz_kr', 'word_ru', 'word_en', 'word_tu']