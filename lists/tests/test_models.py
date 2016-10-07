from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_of_items = List.objects.create()
        item = Item()
        item.list = list_of_items
        item.save()
        self.assertIn(item, list_of_items.item_set.all())

    def test_cannot_save_empty_list_items(self):
        list_of_items = List.objects.create()
        item = Item(list=list_of_items, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_of_items = List.objects.create()
        Item.objects.create(list=list_of_items, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_of_items, text='bla')
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()

    def test_list_ordering(self):
        list_of_items = List.objects.create()
        item1 = Item.objects.create(list=list_of_items, text='i1')
        item2 = Item.objects.create(list=list_of_items, text='item2')
        item3 = Item.objects.create(list=list_of_items, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        item = Item(text='some_text')
        self.assertEqual(str(item), 'some_text')


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_of_items = List.objects.create()
        self.assertEqual(
            list_of_items.get_absolute_url(),
            '/lists/%d/' % (list_of_items.id,)
        )
