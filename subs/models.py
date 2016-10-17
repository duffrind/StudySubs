from django.contrib.auth.models import User
from django.db import models

from django.http import HttpResponseRedirect
from django.shortcuts import render
#from .forms import ModelFormWithFileField

def upload_file(request):
   if request.method == 'POST':
      #form = ModelFormWithFileField(request.POST, request.FILES)
      if form.is_valid():
         # file is saved
         form.save()
         return HttpResponseRedirect('/')
   else:
      form = ModelFormWithFileField()
   return render(request, 'main/index.html', {'form': form})



# Create your models here.
class Srs(models.Model):
   vocab = models.CharField(max_length=20)
   pronunciation = models.CharField(max_length=30)
   meaning = models.CharField(max_length=50)
   pos = models.CharField(max_length=40)
   owner = models.ManyToManyField(User)

   @classmethod
   def create(cls, vocab, pronunciation, meaning, pos, owner):
      srs = cls(vocab=vocab,pronunciation=pronunciation,meaning=meaning,pos=pos,owner=owner)
      return srs

   def clean_vocab(self):
   	if 'vocab' in self.cleaned_data:
   		vocab = self.cleaned_data['vocab']
   		return vocab
   #first_date = models.DateTimeField('date found')

# Select whichever user you want to (any of these work)
#user = User.objects.get(username='admin')
#user = User.objects.get(id=64)
#user = request.user

# Then filter by that user
#user_games = Game.objects.filter(owner=user)