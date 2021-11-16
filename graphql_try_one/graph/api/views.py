from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from graph.models import Order
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer, OrderUpdateStatusSerializer
from rest_framework.renderers import JSONRenderer
import json


class EmberJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = {"order": data}
        return super(EmberJSONRenderer, self).render(
            data, accepted_media_type, renderer_context
        )


class OrderViewSetAPI(ModelViewSet):

    """
    Testing viewset for correct structure

    """

    renderer_classes = (EmberJSONRenderer,)

    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderUpdateStatusAPI(APIView):
    def post(self, request):
        order_id = request.data.get("order")["id"]
        stat = request.data.get("order")["status"]
        substatus = request.data.get("order")["substatus"]
        try:
            qs = Order.objects.get(id=order_id)
            qs.status = stat
            qs.substatus = substatus
            qs.save()

            response = {"id": qs.id, "status": qs.status, "substatus": qs.substatus}

            return Response(
                json.dumps(response),
                status=status.HTTP_200_OK,
            )
        except:

            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)
