from django import forms
from pagedown.widgets import PagedownWidget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from main.models import Post, Comment

CHOICES = (('python','Python'),('java','Java'),('javascript','JavaScript'),('html','HTML'),('css','CSS'))

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email_name = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class NewPageDownWidget(PagedownWidget):
    class Media:
        css = {
            'all': ('pagedown/pagedown.css',)
        }

class PostForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(choices=CHOICES)

    class Meta:
        model = Post
        fields = ('title', 'body', 'tags')
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Title of your post.'}),
            'body': NewPageDownWidget(attrs={'rows': 8,
                                             'placeholder': 'include all the information someone would need to understand you post'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control-sm'})
        self.fields['body'].widget.attrs.update(
            {'class': 'wmd-input pagedownwidget form-control form-control-sm'})
        self.fields['tags'].widget.attrs.update({'class': 'form-control-sm'})


class UserCommentForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Comment
        fields = ('message',)

class GuestCommentForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        pass