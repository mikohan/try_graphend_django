import graphene
from graph.shema import Query as snippet_query


class Query(snippet_query):
    pass


schema = graphene.Schema(query=Query)
