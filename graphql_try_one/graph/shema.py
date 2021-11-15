import graphene
from graphene_django.types import DjangoObjectType
from .models import TestModel, Order


class SnippetType(DjangoObjectType):
    class Meta:
        model = TestModel


class OrderType(DjangoObjectType):
    class Meta:
        model = Order


class Query(graphene.ObjectType):
    all_snippets = graphene.List(SnippetType)
    all_orders = graphene.List(OrderType)

    def resolve_all_snippets(self, info, **kwargs):
        return TestModel.objects.all()

    def resolve_all_orders(self, info, **kwargs):
        return Order.objects.all()
