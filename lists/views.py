from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from lists.forms import ItemForm
from lists.models import List, Item


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_of_items = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['text'], list=list_of_items)
            item.full_clean()
            item.save()
            return redirect(list_of_items)
        except ValidationError:
            error = "You can't have an empty list item"

    return render(request, 'list.html', {
        'list': list_of_items,
        'error': error},
    )


def new_list(request):
    list_of_items = List.objects.create()
    item = Item.objects.create(
        text=request.POST['text'],
        list=list_of_items
    )

    try:
        item.full_clean()
    except ValidationError:
        list_of_items.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})

    return redirect(list_of_items)
