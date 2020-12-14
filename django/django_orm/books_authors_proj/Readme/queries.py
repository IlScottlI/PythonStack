from books_authors_app.models import Book, Author

# Query: Create 5 books with the following names: C Sharp, Java, Python, PHP, Ruby
Book.objects.create(title='C Sharp')
Book.objects.create(title='Java')
Book.objects.create(title='Python')
Book.objects.create(title='PHP')
Book.objects.create(title='Ruby')

# Query: Create 5 different authors: Jane Austen, Emily Dickinson, Fyodor Dostoevsky, William Shakespeare, Lau Tzu
Author.objects.create(first_name='Jane', last_name='Austen')
Author.objects.create(first_name='Emily', last_name='Dickinson')
Author.objects.create(first_name='Fyodor', last_name='Dostoevsky')
Author.objects.create(first_name='William', last_name='Shakespeare')
Author.objects.create(first_name='Lau', last_name='Tzu')

# Query: Change the name of the C Sharp book to C#
book_to_update = Book.objects.filter(title='C Sharp')[0]
book_to_update.title = 'C#'
book_to_update.save()

# Query: Change the first name of the 4th author to Bill
author_to_update = Author.objects.get(id=4)
author_to_update.first_name = 'Bill'
author_to_update.save()

# Query: Assign the first author to the first 2 books
author_to_update = Author.objects.get(id=1)
book_to_assign = Book.objects.get(id=1)
author_to_update.books.add(book_to_assign)
book_to_assign = Book.objects.get(id=2)
author_to_update.books.add(book_to_assign)

# Query: Assign the second author to the first 3 books
author_to_update = Author.objects.get(id=2)
book_to_assign = Book.objects.get(id=1)
author_to_update.books.add(book_to_assign)
book_to_assign = Book.objects.get(id=2)
author_to_update.books.add(book_to_assign)
book_to_assign = Book.objects.get(id=3)
author_to_update.books.add(book_to_assign)

# Query: Assign the third author to the first 4 books
author_to_update = Author.objects.get(id=3)
book_to_assign = Book.objects.get(id=1)
author_to_update.books.add(book_to_assign)
book_to_assign = Book.objects.get(id=2)
author_to_update.books.add(book_to_assign)
book_to_assign = Book.objects.get(id=3)
author_to_update.books.add(book_to_assign)
book_to_assign = Book.objects.get(id=4)
author_to_update.books.add(book_to_assign)

# Query: Assign the fourth author to the first 5 books (or in other words, all the books)
author_to_update = Author.objects.get(id=4)
book_to_assign = Book.objects.get(id=1)
author_to_update.books.add(book_to_assign)
book_to_assign = Book.objects.get(id=2)
author_to_update.books.add(book_to_assign)
book_to_assign = Book.objects.get(id=3)
author_to_update.books.add(book_to_assign)
book_to_assign = Book.objects.get(id=4)
author_to_update.books.add(book_to_assign)
book_to_assign = Book.objects.get(id=5)
author_to_update.books.add(book_to_assign)

# Query: Retrieve all the authors for the 3rd book
book_to_retrieve = Book.objects.get(id=3)
book_to_retrieve.authors.all()

# Query: Remove the first author of the 3rd book
book_to_retrieve = Book.objects.get(id=3)
author_to_remove = book_to_retrieve.authors.first()
book_to_retrieve.authors.remove(author_to_remove)

# Query: Add the 5th author as one of the authors of the 2nd book
book_to_update = Book.objects.get(id=2)
author_to_add = Author.objects.get(id=5)
book_to_update.authors.add(author_to_add)

# Query: Find all the books that the 3rd author is part of
author_to_search = Author.objects.get(id=3)
author_to_search.books.all()

# Query: Find all the authors that contributed to the 5th book
book_to_search = Book.objects.get(id=5)
book_to_search.authors.all()
