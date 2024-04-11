import factory
from faker import Faker

from api.models import User, Diary, Note

fake = Faker(['ru_RU'])


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    login = factory.LazyAttribute(
        lambda x: fake.unique.ascii_safe_email())
    password = factory.LazyAttribute(lambda x: fake.pystr(min_chars=8, max_chars=15))
    username = factory.LazyAttribute(
        lambda x: fake.unique.ascii_safe_email())


class DiaryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Diary

    title = 'test'
    expiration = fake.date("2024-04-12")
    kind = 'PRIVATE'
    user = factory.SubFactory(UserFactory)


class NoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Note

    text = fake.text()
    diary = factory.SubFactory(DiaryFactory)

