from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

# GET: List all books, POST: Create new book
class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# PUT/PATCH: Update a book by ID
class BookUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "id"
