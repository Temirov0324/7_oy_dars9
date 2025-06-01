from rest_framework.urls import path
from .views import word_list_create, word_detail, related_words

urlpatterns = [
    path('words/', word_list_create, name='word-list-create'),
    path('words/<int:pk>/', word_detail, name='word-detail'),
    path('words/<int:pk>/related/', related_words, name='related-words'),
]