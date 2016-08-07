from django.shortcuts import redirect, render
from lists.models import List, Item


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_of_items = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_of_items})


def new_list(request):
    list_of_items = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_of_items)
    return redirect('/lists/%d/' % (list_of_items.id,))


def add_item(request, list_id):
    list_of_items = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_of_items)
    return redirect('/lists/%d/' % (list_of_items.id,))
