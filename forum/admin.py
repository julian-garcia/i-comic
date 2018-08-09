from django.contrib import admin
from .models import ForumTopic, ForumComment, ForumCommentReply

admin.site.register(ForumTopic)
admin.site.register(ForumComment)
admin.site.register(ForumCommentReply)
