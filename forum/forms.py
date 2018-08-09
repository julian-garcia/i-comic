from django import forms
from .models import ForumTopic, ForumComment, ForumCommentReply

class ForumAddTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ['topic_title']

class ForumAddCommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ['comment']

class ForumAddReplyForm(forms.ModelForm):
    class Meta:
        model = ForumCommentReply
        fields = ['comment']
