from django.conf import settings
from graphene_django import DjangoObjectType
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from .models import Note as NoteModel

class Note(DjangoObjectType):
    class Meta:
        model = NoteModel
        filter_fields = ('title','content')
        interfaces = (graphene.relay.Node,)

class Query(graphene.ObjectType):
    notes = graphene.relay.Node.Field(Note)
    all_notes = DjangoFilterConnectionField(Note)
    # notes = graphene.List(Note)
    # def resolve_notes(self,info):
    #     user = info.context.user
    #     """Decide which notes to return"""
    #     if settings.DEBUG:
    #         return NoteModel.objects.filter(user=user_debug)
    #     elif user.is_anonymous:
    #         return NoteModel.objects.none()
    #     else:
    #         return NoteModel.objects.filter(user=user)


schema = graphene.Schema(query=Query)
        