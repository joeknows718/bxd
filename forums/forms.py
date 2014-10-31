from PIL import Image as PImage
from os.path import join as pjoin
from rango.models import UserProfile
from bxd.settings import MEDIA_ROOT
from django.shortcuts import render_to_response
from django import forms





class ProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		exclude = ["posts", "user"] 








