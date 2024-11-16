import graphene
from graphene_django.types import DjangoObjectType
from .models import CustomUser

import graphene

class GenderEnum(graphene.Enum):
    MALE = "male"
    FEMALE = "female"

class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'age', 'gender')

    gender = GenderEnum()

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int(required=True))

    def resolve_all_users(root, info):
        return CustomUser.objects.all()

    def resolve_user(root, info, id):
        try:
            return CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return None
