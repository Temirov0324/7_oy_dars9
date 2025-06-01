from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .models import Word, Category
from .serializers import WordListSerializers, WordSerializers, RelatedWordsSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.http import Http404

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data,
            'ordering': self.request.query_params.get('ordering', '')
        })

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def word_list_create(request):
    if request.method == 'GET':
        search = request.query_params.get('search', '')
        category = request.query_params.get('category', None)
        ordering = request.query_params.get('ordering', '')
        queryset = Word.objects.all()
        if search:
            queryset = queryset.filter(
                Q(word_uz_lot__icontains=search) |
                Q(word_uz_kr__icontains=search) |
                Q(word_ru__icontains=search) |
                Q(word_en__icontains=search) |
                Q(word_tu__icontains=search)
            )
        if category:
            queryset = queryset.filter(category__id=category)
        if ordering in ['word_uz_lot', '-word_uz_lot', 'word_en', '-word_en']:
            queryset = queryset.order_by(ordering)
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = WordListSerializers(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
    elif request.method == 'POST':
        serializer = WordSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return []

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def word_detail(request, pk):
    try:
        word = get_object_or_404(Word, pk=pk)
    except Http404:
        return Response({'error': "So'z topilmadi"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = WordSerializers(word)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        serializer = WordSerializers(word, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        word.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'error': "So'z topilmadi"})
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def related_words(request, pk):
    try:
        word = get_object_or_404(Word, pk=pk)
    except Http404:
        return Response({'error': "So'z topilmadi"}, status=status.HTTP_404_NOT_FOUND)
    related = Word.objects.filter(category=word.category).exclude(id=pk)[:20]
    serializer = RelatedWordsSerializer(related, many=True)
    return Response(serializer.data)