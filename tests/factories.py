import factory
import factory.fuzzy

from app.models.book import Book, BookCategoryEnum
from app.models.lending import Lending
from app.models.user import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.name}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.name}@example.com')
    role = 'admin'


class BookFactory(factory.Factory):
    class Meta:
        model = Book

    name = factory.Faker('sentence', nb_words=3)
    author = factory.Faker('name')
    category = factory.fuzzy.FuzzyChoice(list(BookCategoryEnum))
    total_copies = factory.fuzzy.FuzzyInteger(1, 10)


class LendingFactory(factory.Factory):
    class Meta:
        model = Lending

    user_id = 1
    book_id = 1
    quantity = 1
