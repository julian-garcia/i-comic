from django.test import TestCase
from .forms import ForumAddTopicForm, ForumAddCommentForm, ForumAddReplyForm

class TestForumForms(TestCase):
    def test_forum_add_topic_form(self):
        form = ForumAddTopicForm({'topic_title':'Test name'})
        print('TestForumForms: ForumAddTopicForm - test_forum_add_topic_form \n \
               Expected: {0}, Actual: {1}'.format('All form inputs with values populated', form))
        self.assertTrue(form.is_valid())

    def test_forum_comment_form(self):
        form = ForumAddCommentForm({'comment':'my comment'})
        print('TestForumForms: ForumAddCommentForm - test_forum_comment_form \n \
               Expected: {0}, Actual: {1}'.format('All form inputs with values populated', form))
        self.assertTrue(form.is_valid())

    def test_forum_reply_form(self):
        form = ForumAddReplyForm({'comment':'my comment'})
        print('TestForumForms: ForumAddReplyForm - test_forum_reply_form \n \
               Expected: {0}, Actual: {1}'.format('All form inputs with values populated', form))
        self.assertTrue(form.is_valid())
