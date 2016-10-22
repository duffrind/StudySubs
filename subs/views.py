from django.contrib.auth.models import User, Group
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect, Http404
#from .models import Srs
import csv
from subs.reg import *
from django.template import RequestContext
#from django.db import models
from subs.models import Srs
import re
import MeCab
import json

def register(request):
   form = RegistrationForm()
   if request.method == 'POST':
      form = RegistrationForm(request.POST)
      if form.is_valid():
         user = User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
         #user.groups.add(Group.objects.get(name='user'))
         return HttpResponseRedirect('login')
   variables = RequestContext(request, {'form': form})
   return render(request, 'registration/register.html',variables)

def login(request):
   if request.method == 'POST':
      form = UserCreationForm(request.POST)
      if form.is_valid():
         form.save()
         return HttpResponseRedirect('/')
      else:
         form = UserCreationForm()
   token = {}
   token.update(csrf(request))
   token['form'] = form
   return render(request, 'registration/login.html', token)

def index(request):
   if request.method == 'POST':
      form = SubUpload(request.POST, request.FILES)
      if form.is_valid():
         file = request.FILES['file']
         s = file.read()
         try:
            m = re.findall("""[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9faf\uff62-\uff9f].*\n?""" , s.decode(file.encoding))
         except:
            try:
               m = re.findall("""[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9faf\uff62-\uff9f].*\n?""" , s.decode('UTF8'))
            except:
               try:
                  m = re.findall("""[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9faf\uff62-\uff9f].*\n?""" , s.decode('UTF16'))
               except:
                  try:
                     m = re.findall("""[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9faf\uff62-\uff9f].*\n?""" , s.decode('SHIFT-JIS'))
                  except:
                     try:
                        m = re.findall("""[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9faf\uff62-\uff9f].*\n?""" , s.decode('EUC-JP'))
                     except:
                        m = re.findall("""[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9faf\uff62-\uff9f].*\n?""" , s.decode('UTF32'))
         request.session['m'] = m
         return HttpResponseRedirect('/upload')
   else:
      form = SubUpload()
   user = request.user.id
   anon = not request.user.is_authenticated()
   if anon:
      name = 'Guest'
      download = 0
   else:
      download = len(Srs.objects.filter(owner=user)) != 0
      name = request.user.username
   context = {
      'down': download,
      'anon': anon,
      'name': name,
      'form': form,
   }
   return render(request, 'main/index.html', context)


def upload(request):
   user = request.user.id
   anon = not request.user.is_authenticated()
   if anon:
   	name = 'Guest'
   else:
   	name = request.user.username
   context = {
      #'words':words,
      #'word_set':word_set,
      'name':name,
      'anon':anon,
      'empty':request.session.get('m') == []#False,#word_set == set(),
      #'form':form,
   }
   return render(request, 'upload.html', context)#word_dict[word_list])
	#out_string = 'vocab,pronunciation,meaning,frequency \n'
	#for out_element in output:
#		out_string += out_element.vocab + ',' + out_element.pronunciation + ',' + out_element.meaning + ',' + str(out_element.frequency) + '\n'
#	return HttpResponse(out_string)

def all_down(request): #this downloads ALL vocabulary from file
   response = HttpResponse(content_type='text/csv')
   response['Content-Disposition'] = 'attachment; filename="studysubs.csv"' #change filename to MOVIENAME.csv
   writer = csv.writer(response,delimiter='\t')
   m = request.session.get('m')
   word_set = set()
   for line in m:
      mecab = MeCab.Tagger('-Osimple')
      word_set = word_set | set(mecab.parse(line).split('\n')[:-1])
   with open('subs/word_dictionary.json', 'r') as f:
      try:
         word_dict = json.load(f)
      except ValueError:
         word_dict = {}
   word_set = word_set & set(word_dict.keys())
   writer.writerow(['vocab','pronunciation','part of speech','meaning'])
   for word in word_set:
      writer.writerow([word] + word_dict[word].split('\t'))
   #query database for user. update
   user = request.user.id
   if not request.user.is_authenticated():
      owned = []
   else:
      user = request.user
      owned = Srs.objects.filter(owner=user)
   new_set = word_set.copy()
   for x in list(owned):
      if x.vocab in new_set:
         new_set.remove(x.vocab)
   #new_set = set([x.vocab if not in word_set for x in list(owned)])#new_set = word_set - set(owned.vocab)
   if request.user.is_authenticated():
      for word in new_set:
         try:
            temp = Srs.objects.get(vocab=word) # CHANGE BACK TO TRY EXCEPT
            temp.owner.add(user)
            temp.save()
         except:
            temp = word_dict[word].split('\t')
            new_srs = Srs.objects.create(vocab=word,pronunciation=temp[0],pos=temp[1],meaning=temp[2])
            new_srs.owner.add(user)
            new_srs.save()
   return response

def new_down(request): #this downloads NEW vocabulary from file
   response = HttpResponse(content_type='text/csv')
   response['Content-Disposition'] = 'attachment; filename="studysubs.csv"' #change filename to MOVIENAME.csv
   writer = csv.writer(response,delimiter='\t')
   m = request.session.get('m')
   word_set = set()
   for line in m:
      mecab = MeCab.Tagger('-Osimple')
      word_set = word_set | set(mecab.parse(line).split('\n')[:-1])
   with open('subs/word_dictionary.json', 'r') as f:
      try:
         word_dict = json.load(f)
      except ValueError:
         word_dict = {}
   word_set = word_set & set(word_dict.keys())
   writer.writerow(['vocab','pronunciation','part of speech','meaning'])
   #query database for user, update
   user = request.user.id
   owned = Srs.objects.filter(owner=user)
   new_set = word_set.copy()
   for x in list(owned):
   	if x.vocab in new_set:
         new_set.remove(x.vocab)#new_set = set([x.vocab not in word_set for x in list(owned)])
   for word in new_set:
      try:
         temp = Srs.objects.get(vocab=word)
         temp.owner.add(user)
         temp.save()
      except:
         temp = word_dict[word].split('\t')
         new_srs = Srs.objects.create(vocab=word,pronunciation=temp[0],pos=temp[1],meaning=temp[2])#,owner=user)
         new_srs.owner.add(user)
         new_srs.save()
      writer.writerow([word] + word_dict[word].split('\t'))
   return response

def down(request): #this downloads ALL vocabulary from db
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="studysubs.csv"' #change filename to MOVIENAME.csv
	writer = csv.writer(response, delimiter='\t')
	writer.writerow(['vocab', 'pronunciation', 'part of speech', 'meaning'])
	user = request.user.id #User.objects.get(username='duffrind') #change to find current user
	output = Srs.objects.filter(owner=user)
	#out_string = 'vocab,pronunciation,meaning,frequency \n'
	for out_element in output: #if empty, return nothing and give a message
		writer.writerow([out_element.vocab, out_element.pronunciation, out_element.pos, str(out_element.meaning)])
	return response


def fourohfour(request):
	raise Http404("Page does not exist")
	return HttpResponse("Page does not exist")

# Create your views here.


# Select whichever user you want to (any of these work)
#user = User.objects.get(username='admin')
#user = User.objects.get(id=64)
#user = request.user

# Then filter by that user
#user_games = Game.objects.filter(owner=user)
