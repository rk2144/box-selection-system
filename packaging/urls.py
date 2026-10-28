from django.urls import path
from .views import RecommendBoxView
from .views import (
    ProductListCreateView,
    BoxListCreateView,
)

urlpatterns = [
    path(
        "products/",
        ProductListCreateView.as_view(),
        name="product-list-create",
    ),
    path(
        "boxes/",
        BoxListCreateView.as_view(),
        name="box-list-create",
    ),
    path(
    "recommend-box/",
    RecommendBoxView.as_view(),
    name="recommend-box",
),
]