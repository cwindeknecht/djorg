from rest_framework import serializers, viewsets
from .models import Note
from django.contrib.auth import get_user

class NoteSerializer(serializers.HyperlinkedModelSerializer):
    def create(self,validated_data):
        user = self.context['request'].user
        note = Note.objects.create(user=user, **validated_data)
        return note
    class Meta:
        model = Note
        fields = ('title','content', 'tags')

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Note.objects.none()
        else:
            return Note.objects.filter(user=self.request.user)
            