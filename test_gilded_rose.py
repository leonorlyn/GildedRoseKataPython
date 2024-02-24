# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEquals("foo", items[0].name)

    def test_sulfuras_item_never_degrades(self):
        sulfuras = "Sulfuras, Hand of Ragnaros"
        items = [Item(sulfuras, 5, 80), Item(sulfuras, 0, 80)]
        gr = GildedRose(items)

        for _ in range(10):  # Simulate multiple days
            gr.update_quality()

        for item in gr.get_items_by_name(sulfuras):
            assert item.sell_in in [5, 0]  # SellIn does not change
            assert item.quality == 80  # Quality remains constant


    def test_backstage_pass_item_increases_then_drops_to_zero(self):
        backstage_pass = "Backstage passes to a TAFKAL80ETC concert"
        items = [Item(backstage_pass, 15, 20), Item(backstage_pass, 10, 20), Item(backstage_pass, 5, 20), Item(backstage_pass, 0, 20)]
        gr = GildedRose(items)

        gr.update_quality()
        assert gr.get_items_by_name(backstage_pass)[0].quality == 21  # Increases by 1 when > 10 days
        assert gr.get_items_by_name(backstage_pass)[1].quality == 22  # Increases by 2 when <= 10 days
        assert gr.get_items_by_name(backstage_pass)[2].quality == 23  # Increases by 3 when <= 5 days
        assert gr.get_items_by_name(backstage_pass)[3].quality == 0   # Drops to 0 after the concert

    def test_brie_item_increases_in_quality(self):
        brie = "Aged Brie"
        items = [Item(brie, 2, 0), Item(brie, -1, 0)]
        gr = GildedRose(items)

        gr.update_quality()
        for item in gr.get_items_by_name(brie):
            assert item.quality > 0  # Quality increases


if __name__ == '__main__':
    unittest.main()
