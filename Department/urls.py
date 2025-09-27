from django.urls import path
from .views import BookListCreateAPIView, BookUpdateAPIView

urlpatterns = [
    path("books/", BookListCreateAPIView.as_view(), name="book-list-create"),
    path("books/<int:id>/", BookUpdateAPIView.as_view(), name="book-update"),
]
