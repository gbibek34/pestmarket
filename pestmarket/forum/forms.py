from django.forms import ModelForm
from .models import Post


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
