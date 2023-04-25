from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import BaseUserManager
from django.db import models
from users.models import CustomUser

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, username, password, fitst_name, last_name):
#         if not email:
#             raise ValueError("Users must have an email address")

#         user = self.model(
#             email=self.normalize_email(email),
#             date_of_birth=date_of_birth,
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(
#         self,
#         email,
#         username,
#         password,
#         fitst_name,
#         last_name,
#     ):
#         """
#         Creates and saves a superuser with the given email, date of
#         birth and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#             date_of_birth=date_of_birth,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user


admin.site.register(CustomUser, UserAdmin)
