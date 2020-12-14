from django.shortcuts import render, redirect
from .models import Book, Author


def books(request):
    context = {
        'books': Book.objects.all()
    }
    return render(request, 'books.html', context)


def authors(request):
    context = {
        'authors': Author.objects.all()
    }
    return render(request, 'authors.html', context)


def authors_view(request, author_id):
    context = {
        'author': Author.objects.get(id=author_id),
        'author_books':  Author.objects.get(id=author_id).books.all(),
        'books': Book.objects.all(),
    }
    print(context)
    return render(request, 'authors_view.html', context)


def books_view(request, book_id):
    context = {
        'book': Book.objects.get(id=book_id),
        'book_authors':  Book.objects.get(id=book_id).authors.all(),
        'authors': Author.objects.all(),
    }
    print(context)
    return render(request, 'books_view.html', context)


def process(request):
    print(request.POST)
    action = redirect('/')
    type_ = getSet(request, 'type')
    if type_ == 'add_book':
        Book.objects.create(
            title=getSet(request, 'title'), desc=request.POST['desc']
        )
    if type_ == 'update_book':
        book_id = request.POST['book_id']
        author_id = request.POST['author_id']
        book_to_update = Book.objects.get(id=book_id)
        author_to_add = Author.objects.get(id=author_id)
        book_to_update.authors.add(author_to_add)
        action = redirect(f"/books/{book_id}")
    if type_ == 'update_author':
        book_id = request.POST['book_id']
        author_id = request.POST['author_id']
        author_to_update = Author.objects.get(id=author_id)
        book_to_add = Book.objects.get(id=book_id)
        author_to_update.books.add(book_to_add)
        action = redirect(f"/authors/{author_id}")
    if type_ == 'add_author':
        print(type_)
        Author.objects.create(
            first_name=getSet(request, 'first_name'),
            last_name=request.POST['last_name'],
            notes=request.POST['notes']
        )
        action = redirect('/authors')
    return action


def getSet(request, name):
    response = 0
    try:
        if request.POST[name]:
            response = request.POST[name]
            request.session[name] = response
    except:
        pass
    for key, value in request.session.items():
        if key == name:
            response = value

    return response
