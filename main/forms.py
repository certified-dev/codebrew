from django import forms
from pagedown.widgets import PagedownWidget

from main.models import Post, UserComment

CHOICES = (('python','Python'),('java','Java'),('javascript','JavaScript'))


class NewPageDownWidget(PagedownWidget):
    class Media:
        css = {
            'all': ('pagedown/pagedown.css',)
        }

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(choices=[CHOICES])

    class Meta:
        model = Post
        fields = ('title', 'body', 'tags')
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Title of your post.'}),
            'body': NewPageDownWidget(attrs={'rows': 8,
                                             'placeholder': 'include all the information someone would need to unserstand you post'})
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
        model = UserComment
        field = ('message',)

class GuestCommentForm(forms.Form):
    name = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        pass