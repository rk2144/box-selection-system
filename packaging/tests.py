from decimal import Decimal
from types import SimpleNamespace

from django.test import TestCase, SimpleTestCase
from rest_framework.test import APIClient

from .models import Product, Box
from .services import can_pack, recommend_box


class PackingAlgorithmTests(SimpleTestCase):
    def make_box(self, length, width, height):
        return SimpleNamespace(
            inner_length=Decimal(str(length)),
            inner_width=Decimal(str(width)),
            inner_height=Decimal(str(height)),
        )

    def test_product_fits_in_box(self):
        box = self.make_box(20, 15, 10)
        self.assertTrue(can_pack([(10, 10, 5)], box))

    def test_product_fits_after_rotation(self):
        box = self.make_box(10, 5, 4)
        self.assertTrue(can_pack([(5, 10, 4)], box))

    def test_product_does_not_fit(self):
        box = self.make_box(10, 10, 10)
        self.assertFalse(can_pack([(11, 5, 5)], box))

    def test_two_products_fit_without_overlap(self):
        box = self.make_box(10, 5, 5)
        items = [(5, 5, 5), (5, 5, 5)]
        self.assertTrue(can_pack(items, box))

    def test_two_products_cannot_fit(self):
        box = self.make_box(9, 5, 5)
        items = [(5, 5, 5), (5, 5, 5)]
        self.assertFalse(can_pack(items, box))


class BoxRecommendationTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Laptop",
            length=Decimal("10"),
            width=Decimal("8"),
            height=Decimal("4"),
            weight=Decimal("2"),
        )

        self.cheap_box = Box.objects.create(
            name="Small Box",
            inner_length=Decimal("12"),
            inner_width=Decimal("10"),
            inner_height=Decimal("6"),
            max_weight=Decimal("5"),
            cost=Decimal("20"),
        )

        self.expensive_box = Box.objects.create(
            name="Large Box",
            inner_length=Decimal("20"),
            inner_width=Decimal("20"),
            inner_height=Decimal("20"),
            max_weight=Decimal("20"),
            cost=Decimal("50"),
        )

    def test_selects_cheapest_suitable_box(self):
        result = recommend_box([
            {"product": self.product, "quantity": 1}
        ])
        self.assertEqual(result, self.cheap_box)

    def test_rejects_box_with_insufficient_weight_capacity(self):
        self.cheap_box.max_weight = Decimal("1")
        self.cheap_box.save()

        result = recommend_box([
            {"product": self.product, "quantity": 1}
        ])
        self.assertEqual(result, self.expensive_box)

    def test_returns_none_when_no_box_is_suitable(self):
        Box.objects.all().delete()

        result = recommend_box([
            {"product": self.product, "quantity": 1}
        ])
        self.assertIsNone(result)

    def test_empty_order_is_rejected(self):
        with self.assertRaises(ValueError):
            recommend_box([])

    def test_zero_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            recommend_box([
                {"product": self.product, "quantity": 0}
            ])


class RecommendationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/recommend-box/"

    def test_invalid_product_id_returns_400(self):
        response = self.client.post(
            self.url,
            {
                "items": [
                    {"product_id": 999999, "quantity": 1}
                ]
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_empty_items_returns_400(self):
        response = self.client.post(
            self.url,
            {"items": []},
            format="json",
        )
        self.assertEqual(response.status_code, 400)