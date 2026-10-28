from rest_framework import generics
from .models import Product, Box
from .serializers import ProductSerializer, BoxSerializer
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import recommend_box


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BoxListCreateView(generics.ListCreateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer


class OrderItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)


class OrderSerializer(serializers.Serializer):
    items = OrderItemSerializer(many=True, allow_empty=False)


class RecommendBoxView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from .models import Product

        order_items = []
        errors = []

        for item in serializer.validated_data["items"]:
            product = Product.objects.filter(
                pk=item["product_id"]
            ).first()

            if product is None:
                errors.append({
                    "product_id": item["product_id"],
                    "error": "Product not found",
                })
            else:
                order_items.append({
                    "product": product,
                    "quantity": item["quantity"],
                })

        if errors:
            return Response(
                {"errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            box = recommend_box(order_items)
        except ValueError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if box is None:
            return Response(
                {"message": "No suitable box found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response({
            "box_id": box.pk,
            "box_name": box.name,
            "cost": str(box.cost),
            "total_weight": str(sum(
                item["product"].weight * item["quantity"]
                for item in order_items
            )),
        })