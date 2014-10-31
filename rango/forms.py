from django import forms 
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Enter what category you would like to place this under:")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	# An inline classto provide additional info on the form
	class Meta: 
		#provide association between modelform and modelform
		model = Category

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=128, help_text="Enter the title of the page:")
	url = forms.CharField(max_length=200, help_text="Enter the URL:")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Page 

		fields = ('title', 'url', 'views')

	def  clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')

		#If Url is not empty and dont start with 'http://' prepend 'http://'

		if url and not url.startswith('http://'):
			url = 'http://' + url
			cleaned_data['url'] = url

		return cleaned_data

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = {'username', 'email', 'password'}

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('website', 'picture')


