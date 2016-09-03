from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from lists.models import List, Item


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_of_items = List.objects.get(id=list_id)
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'], list=list_of_items)
        return redirect('/lists/%d/' % (list_of_items.id))
    return render(request, 'list.html', {'list': list_of_items})


def new_list(request):
    list_of_items = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_of_items)
    try:
        item.full_clean()
    except ValidationError:
        list_of_items.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect('/lists/%d/' % (list_of_items.id,))
