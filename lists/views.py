from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from lists.forms import ItemForm
from lists.models import List, Item


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request):
    form = ItemForm(data=request.POST)
    if (form.is_valid()):
        list_of_items = List.objects.create()
        form.save(for_list=list_of_items)
        return redirect(list_of_items)
    else:
        return render(request, 'home.html', {'form': form})


def view_list(request, list_id):
    list_of_items = List.objects.get(id=list_id)
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_of_items)
            return redirect(list_of_items)

    return render(request, 'list.html', {
            'list': list_of_items,
            'form': form,
        }
    )
