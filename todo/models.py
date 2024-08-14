from django.db import models

from django.contrib.auth.models import User
# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User, related_name='projects')

    def __str__(self):
        return self.name
    

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    
    title = models.CharField(max_length=100, null=True)
    content = models.CharField(max_length=1000, null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    date_posted = models.DateTimeField(auto_now_add=True, null=True)
    members = models.ManyToManyField(User, related_name='tasks', blank=True)  # Use ManyToManyField
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
"""
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    full_name = models.CharField(max_length=100, default='Unnamed')
    birthday = models.DateField(null=True, blank=True)
    personality = models.TextField(null=True, blank=True)
    hobbies = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    full_name = models.CharField(max_length=100, default='Unnamed')
    birthday = models.DateField(null=True, blank=True)
    personality = models.TextField(null=True, blank=True)
    hobbies = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'
"""
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    full_name = models.CharField(max_length=100, blank=True)  # Cho phép trường này bỏ trống
    birthday = models.DateField(null=True, blank=True)  # Cho phép null và bỏ trống
    personality = models.TextField(null=True, blank=True)
    hobbies = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}'