from django.forms import ModelForm
from .models import Post, Comment


class CreatePostForm(ModelForm):
    class Meta:
        exclude = ('date_time', 'author')
        model = Post

    def save(self, user):
        post = Post.objects.create(
            title=self.cleaned_data['title'],
            content=self.cleaned_data['content'],
            image=self.cleaned_data['image'],
            author=user,
        )
        return post


class CreateCommentForm(ModelForm):
    class Meta:
        exclude = ('post', 'name', 'date_added')
        model = Comment

    def save(self, post, user):
        comment = Post.objects.create(
            post=post,
            name=user,
            body=self.cleaned_data['body'],
        )
        return comment
