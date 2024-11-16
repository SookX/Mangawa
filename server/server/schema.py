import graphene
import user.schema

class Query(user.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
