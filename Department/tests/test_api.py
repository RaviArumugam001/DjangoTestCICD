import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from Department.models import Book   # 👈 adjust if your app name differs

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
@pytest.mark.django_db
def create_book():
    return Book.objects.create(title="Django Basics", author="John Doe", published_year=2021)


# ------------------------
# 10 TEST CASES
# ------------------------

@pytest.mark.django_db
def test_get_empty_book_list(api_client):
    url = reverse("book-list-create")
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.django_db
def test_create_book(api_client):
    url = reverse("book-list-create")
    data = {"title": "Python 101", "author": "Alice", "published_year": 2022}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    assert response.data["title"] == "Python 101"

@pytest.mark.django_db
def test_get_book_list_with_data(api_client, create_book):
    url = reverse("book-list-create")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1

@pytest.mark.django_db
def test_update_book_put(api_client, create_book):
    url = reverse("book-update", args=[create_book.id])
    data = {"title": "Advanced Django", "author": "Jane Doe", "published_year": 2023}
    response = api_client.put(url, data, format="json")
    assert response.status_code == 200
    assert response.data["title"] == "Advanced Django"

@pytest.mark.django_db
def test_partial_update_book_patch(api_client, create_book):
    url = reverse("book-update", args=[create_book.id])
    data = {"author": "New Author"}
    response = api_client.patch(url, data, format="json")
    assert response.status_code == 200
    assert response.data["author"] == "New Author"

@pytest.mark.django_db
def test_update_book_invalid_id(api_client):
    url = reverse("book-update", args=[999])
    data = {"title": "Does Not Exist", "author": "X", "published_year": 2000}
    response = api_client.put(url, data, format="json")
    assert response.status_code == 404

@pytest.mark.django_db
def test_create_book_missing_field(api_client):
    url = reverse("book-list-create")
    data = {"author": "Missing Title", "published_year": 2020}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
    assert "title" in response.data

@pytest.mark.django_db
def test_create_book_invalid_year(api_client):
    url = reverse("book-list-create")
    data = {"title": "Bad Year", "author": "Test", "published_year": "abc"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400

@pytest.mark.django_db
def test_list_books_status_code(api_client, create_book):
    url = reverse("book-list-create")
    response = api_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_update_book_only_year(api_client, create_book):
    url = reverse("book-update", args=[create_book.id])
    data = {"published_year": 2030}
    response = api_client.patch(url, data, format="json")
    assert response.status_code == 200
    assert response.data["published_year"] == 2031
