import graphene
from graphene_django.types import DjangoObjectType
from .models import TestModel


class SnippetType(DjangoObjectType):
    class Meta:
        model = TestModel


class Query(graphene.ObjectType):
    all_snippets = graphene.List(SnippetType)

    def resolve_all_snippets(self, info, **kwargs):
        return TestModel.objects.all()
