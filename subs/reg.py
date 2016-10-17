import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django import forms 
from studysubs import settings
from django.template.defaultfilters import filesizeformat

class SubUpload(forms.Form):
   file = forms.FileField(label="File")

   def clean_file(self):
      if 'file' in self.cleaned_data:
         file = self.cleaned_data['file']
         if file._size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError(('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(file._size)))
         return file


class RegistrationForm(forms.Form):
   username = forms.CharField(label='Username', max_length=30)
   password1 = forms.CharField(label='Password',
                          widget=forms.PasswordInput())
   password2 = forms.CharField(label='Password (Again)',
                        widget=forms.PasswordInput())
   
   def clean_password2(self):
      if 'password1' in self.cleaned_data:
         password1 = self.cleaned_data['password1']
         password2 = self.cleaned_data['password2']
         if password1 == password2:
            return password2
         raise forms.ValidationError('Passwords do not match.')
   
   def clean_username(self):
      username = self.cleaned_data['username']
      if not re.search(r'^\w+$', username):
         raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
      try:
         User.objects.get(username=username)
      except ObjectDoesNotExist:
         return username
      raise forms.ValidationError('Username is already taken.')


#class SubDownload(forms.Form):
#   new_button = forms.SubmitButtonField(label="new", initial=u"NEW")
#   all_button = forms.SubmitButtonField(label="all", initial=u"ALL")

#   def clean_file(self):
#      if 'new_button' in self.cleaned_data:
#         button = self.cleaned_data['new_button']
         #
#      else:
#         button = self.cleaned_data['all_button']
#      return button