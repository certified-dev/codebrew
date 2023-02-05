from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=10000)
    tags = models.CharField(max_length=100)
    posted_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.title

    def add_views(self, request):
        session_key = 'viewed_question_{}'.format(self.pk)
        if not request.session.get(session_key, False):
            self.views += 1
            self.save()
            request.session[session_key] = True
    
    def get_tags(self):
        new_tag = ""
        for i in self.tags:
            if i not in ["[","'"," ","]"]:
               new_tag += i

        new_tag.strip()
        tag_list = new_tag.split(",")
        return tag_list


class Comment(models.Model):
    commented_by = models.CharField(max_length=50,blank=True, null=True)
    posted_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE,blank=True,null=True)
    email = models.CharField(max_length=80,blank=True, null=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.message

   
