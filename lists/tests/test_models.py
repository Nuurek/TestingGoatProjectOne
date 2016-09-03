from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_of_items = List()
        list_of_items.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_of_items
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_of_items
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_of_items)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_item.text)
        self.assertEqual(first_saved_item.list, list_of_items)
        self.assertEqual(second_saved_item.text, second_item.text)
        self.assertEqual(second_saved_item.list, list_of_items)

    def test_cannot_save_empty_list_items(self):
        list_of_items = List.objects.create()
        item = Item(list=list_of_items, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        list_of_items = List.objects.create()
        self.assertEqual(
            list_of_items.get_absolute_url(),
            '/lists/%d/' % (list_of_items.id,)
        )
