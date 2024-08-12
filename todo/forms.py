from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django import forms
from .models import Project, Task, Profile, Message
from django_select2.forms import Select2MultipleWidget

# - Register an user
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# - Login an user
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

# - Create a task

class CreateTaskForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),  # Initially empty
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = ['title', 'content', 'priority', 'members']

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        if project:
            self.fields['members'].queryset = project.users.all()
            
# - Update a task
class UpdateTaskForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),  
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = ['title', 'content', 'priority', 'members']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)  
        super().__init__(*args, **kwargs)
        if project:
            
            self.fields['members'].queryset = project.users.all()
# - Update an user
class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'birthday', 'personality', 'hobbies', 'skills', 'github']

# - Update a profile picture
class UpdateProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Profile
        fields = ['profile_pic']




# - Create a project
class CreateProjectForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=Select2MultipleWidget,  
        required=False
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'users']


# - Update a project
class UpdateProjectForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=Select2MultipleWidget,  
        required=False
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'users']


# - Group chat

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'file']  # Thêm trường 'file'
        widgets = {
            'content': forms.Textarea(attrs={'rows': 1, 'placeholder': 'Type a message...'}),
        }

