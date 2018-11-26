from django.forms import ModelForm

from.models import Comments


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['login_user', 'email_user', 'comments_text']
