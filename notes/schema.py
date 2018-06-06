from graphene_django import DjangoObjectType
import graphene
from .models import Note as NoteModel

class Note(DjangoObjectType):
    class Meta:
        model = NoteModel
        interfaces = (graphene.relay.Node,)

class Query(graphene.ObjectType):
    all_notes = graphene.List(Note)
    single_note = graphene.Field(Note, id=graphene.String(), title=graphene.String())
    matching_notes = graphene.List(Note, content=graphene.String(), title=graphene.String())
    matching_tags = graphene.List(Note, tags=graphene.String())

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

    def resolve_matching_tags(self,info,tags):
      user = info.context.user
      notes_to_return = []

      tags = tags.split(",")

      if user.is_anonymous:
        return NoteModel.objects.none()
      else:
        if tags is not None:
          notes = NoteModel.objects.filter(user=user)
          for tag in tags:
            if notes.filter(tags__contains=tag):
              notes_to_return += notes.filter(tags__contains=tag)
          return notes_to_return
        return NoteModel.objects.none()

class CreateEditNote(graphene.Mutation):
  class Arguments:
    title=graphene.String()
    content=graphene.String()
    note=graphene.String()
    tags=graphene.String()

  ok = graphene.Boolean()
  note = graphene.Field(Note)

  def mutate(self,info,**kwargs):
    user = info.context.user
    title = kwargs.get('title')
    content = kwargs.get('content')
    note = kwargs.get('note')
    tags = kwargs.get('tags')
    
    if user.is_anonymous:
        ok = False
        return CreateEditNote(ok=ok)
    elif note:
        ok = True
        note_to_update = NoteModel.objects.filter(user=user).get(note_id = note)
        if title:
          note_to_update.title = title
        if content:
          note_to_update.content = content
        if tags:
          note_to_update.tags = tags
        note_to_update.save()
        return CreateEditNote(note=note_to_update, ok=ok)
    else:
        ok = True
        newNote = NoteModel(title=title, content=content, user=user, tags=tags)
        newNote.save()
        return CreateEditNote(note=newNote, ok=ok)

class Mutation(graphene.ObjectType):
  create_edit_note = CreateEditNote.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

"""
QUERIES
All Notes
{
  allNotes {
    noteId
    title
    content
    tags
  }
}

Single Note by ID:
{
  singleNote(id: "8cc3eb94-431c-4e08-b3d1-82f41586cfa5") {
    noteId
    title
    content
    tags
  }
}

Single Note by Title:
{
  singleNote(title: "Sweet") {
    noteId
    title
    content
    tags
  }
}

All Notes by Content:
{
  matchingNotes(content: "Finally") {
    noteId
    title
    content
    tags
  }
}

All Notes by Title:
{
  matchingNotes(title: "Notha") {
    noteId
    title
    content
    tags
  }
}

Single Tag
{
	matchingTags(tags:"hate"){
    noteId
    title
    content
    tags
  }
}

Multiple Tag; 
{
	matchingTags(tags:"hate,love"){
    noteId
    title
    content
    tags
  }
}
"""
"""
MUTATIONS:
Create a Note:

mutation {
  createEditNote(title: "Notha", content: "Note") {
    note {
      noteId
      title
      content
      tags
    }
    ok
  }
}

Edit a Note:

mutation {
  createEditNote(title: "Sweet", content: "Finally", note: "8cc3eb94-431c-4e08-b3d1-82f41586cfa5") {
    note {
      noteId
      title
      content
      tags
    }
    ok
  }
}
"""