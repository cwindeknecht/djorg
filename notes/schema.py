from django.conf import settings
from graphene_django import DjangoObjectType
import graphene
import uuid
from graphene_django.filter import DjangoFilterConnectionField
from .models import Note as NoteModel

class Note(DjangoObjectType):
    class Meta:
        model = NoteModel
        # filter_fields = {'title','content','created_date','modified_date'}
        interfaces = (graphene.relay.Node,)

class Query(graphene.ObjectType):
    # notes = graphene.relay.Node.Field(Note)
    # all_notes = DjangoFilterConnectionField(Note)

    # def resolve_all_notes(self, info, **kwargs):
    #     return NoteModel.objects.all()
        
    all_notes = graphene.List(Note)
    single_note = graphene.Field(Note, id=graphene.String(), title=graphene.String())
    matching_notes = graphene.List(Note, content=graphene.String(), title=graphene.String())

    def resolve_all_notes(self,info):
      user = info.context.user

      if user.is_anonymous:
        return NoteModel.objects.none()
      else:
        return NoteModel.objects.filter(user=user)

    def resolve_matching_notes(self,info, **kwargs):
      user = info.context.user
      title = kwargs.get('title')
      content = kwargs.get('content')

      if user.is_anonymous:
        return NoteModel.objects.none()
      else:
        if title is not None:
          return NoteModel.objects.filter(user=user).filter(title__contains=title)
        if content is not None:
          return NoteModel.objects.filter(user=user).filter(content__contains=content)

    def resolve_single_note(self,info, **kwargs):
      user = info.context.user
      title = kwargs.get('title')
      note = kwargs.get('id')
      
      if user.is_anonymous:
        return NoteModel.objects.none()
      else:
        if title is not None:
          return NoteModel.objects.filter(user=user).get(title=title)
        if note is not None:
          return NoteModel.objects.filter(user=user).get(note_id=note)
        return NoteModel.objects.none()

class CreateEditNote(graphene.Mutation):
  class Arguments:
    title=graphene.String()
    content=graphene.String()
    note=graphene.String()

  ok = graphene.Boolean()
  note = graphene.Field(Note)

  def mutate(self,info,**kwargs):
    user = info.context.user
    title = kwargs.get('title')
    content = kwargs.get('content')
    poop = kwargs.get('note')
    
    if user.is_anonymous:
        ok = False
        return CreateEditNote(ok=ok)
    elif poop:
        ok = True
        print("Yup1")
        note_to_update = NoteModel.objects.filter(user=user)
        note_to_update = note_to_update.get(note_id = poop)
        if title:
          note_to_update.title = title
        if content:
          note_to_update.content = content
        note_to_update.save()
        print("Yup1")
        return CreateEditNote(note=note_to_update, ok=ok)
    else:
        ok = True
        newNote = NoteModel(title=title, content=content, user=user)
        newNote.save()
        return CreateEditNote(note=newNote, ok=ok)

class Mutation(graphene.ObjectType):
  create_edit_note = CreateEditNote.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

"""QUERIES
query{
  allNotes{
    noteId
    id
    title
    content
  }
}

# mutation{
#   createEditNote(title:"Sweet",content:"Finally",note:"8cc3eb94-431c-4e08-b3d1-82f41586cfa5") {
#     note{
#       noteId
#       id
#       title
#       content
#     }
#     ok
#   }
# }
"""