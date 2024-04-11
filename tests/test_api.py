import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from api.models import Diary, Note


@pytest.mark.django_db
def test_create_user(user_factory):
    user_factory.create()
    assert True


@pytest.mark.django_db
def test_create_diary(user, user_client, diary_factory):
    url = reverse('create_diary')
    data = {'title': diary_factory.title,
            'expiration': diary_factory.expiration,
            'kind': diary_factory.kind,
            'user': user.pk
            }
    response = user_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_filed_create_diary(user, guest_client, diary_factory):
    url = reverse('create_diary')
    data = {'title': diary_factory.title,
            'expiration': diary_factory.expiration,
            'kind': diary_factory.kind,
            'user': user.pk
            }
    response = guest_client.post(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_update_diary(user, user_client, diary_factory):
    diary = diary_factory.create()
    url = "/api/v1/diary/update/{id}/"
    data = {'title': 'New title',
            'expiration': diary.expiration,
            'kind': diary.kind,
            'user': user.pk}
    response = user_client.put(url.format(id=diary.id), data, format='json')
    updated_diary = Diary.objects.get(pk=diary.id)

    assert response.status_code == status.HTTP_200_OK
    assert updated_diary.title != diary.title


@pytest.mark.django_db
def test_filed_update_diary(user, guest_client, diary_factory):
    diary = diary_factory.create()
    url = "/api/v1/diary/update/{id}/"
    data = {'title': 'New title',
            'expiration': diary.expiration,
            'kind': diary.kind,
            'user': user.pk}
    response = guest_client.put(url.format(id=diary.id), data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_delete_diary(user, user_client, diary_factory):
    diary = diary_factory.create()
    url = "/api/v1/diary/delete/{id}/"
    response = user_client.delete(url.format(id=diary.id))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Diary.objects.filter(id=diary.id).exists()


@pytest.mark.django_db
def test_filed_delete_diary(user, guest_client, diary_factory):
    diary = diary_factory.create()
    url = "/api/v1/diary/delete/{id}/"
    response = guest_client.delete(url.format(id=diary.id))
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_note(user_client, note_factory, diary):
    url = reverse('create_note')
    data = {'text': note_factory.text,
            'diary': diary.id,
            }
    response = user_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_filed_create_note(guest_client, note_factory, diary):
    url = reverse('create_note')
    data = {'text': note_factory.text,
            'diary': diary.id,
            }
    response = guest_client.post(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_update_note(diary, user_client, note_factory):
    note = note_factory.create()
    url = "/api/v1/note/update/{id}/"
    data = {'text': 'New text',
            'diary': diary.id,}
    response = user_client.put(url.format(id=note.id), data, format='json')
    updated_note = Note.objects.get(pk=note.id)

    assert response.status_code == status.HTTP_200_OK
    assert updated_note.text != note.text


@pytest.mark.django_db
def test_filed_update_note(diary, guest_client, note_factory):
    note = note_factory.create()
    url = "/api/v1/note/update/{id}/"
    data = {'text': 'New text',
            'diary': diary.id,}
    response = guest_client.put(url.format(id=note.id), data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_delete_note(user, user_client, note_factory):
    note = note_factory.create()
    url = "/api/v1/note/delete/{id}/"
    response = user_client.delete(url.format(id=note.id))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Note.objects.filter(id=note.id).exists()


@pytest.mark.django_db
def test_filed_delete_note(user, guest_client, note_factory):
    note = note_factory.create()
    url = "/api/v1/note/delete/{id}/"
    response = guest_client.delete(url.format(id=note.id))
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_get_diaries(user, user_client):
    url = '/api/v1/diaries/'
    response = user_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_notes(user, user_client):
    url = '/api/v1/notes/'
    response = user_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_filed_get_diaries(user, guest_client):
    url = '/api/v1/diaries/'
    response = guest_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_filed_get_notes(user, guest_client):
    url = '/api/v1/notes/'
    response = guest_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
