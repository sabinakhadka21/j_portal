from django.contrib import admin
from django.contrib.auth import get_user_model

from account.models import User,Profile

admin.site.register(Profile)
admin.site.register(User)
	