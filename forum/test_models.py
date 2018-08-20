from django.test import TestCase
from accounts.models import User
from .models import ForumTopic, ForumComment, ForumCommentReply

class TestForumModels(TestCase):
    def test_forum_topic(self):
        user = User(email='test@test.com', first_name='Test', last_name='Case')
        user.save()
        topic = ForumTopic(topic_title='Test')
        topic.save()
        print('TestForumModels: ForumTopic - test_forum_topic \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format('Test', topic.topic_title,
                                                  'Now', topic.date_created))
        self.assertEqual(topic.topic_title, 'Test')

    def test_forum_comment(self):
        user = User(email='test@test.com', first_name='Test', last_name='Case')
        user.save()
        topic = ForumTopic(topic_title='Test')
        topic.save()
        comment = ForumComment(forum_topic=topic, author=user, comment='my comment')
        comment.save()
        reply = ForumCommentReply(forum_comment=comment, author=user, comment='my reply')
        reply.save()

        print('TestForumModels: ForumComment - test_forum_comment \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3} \n \
               Expected: {4}, Actual: {5} \n \
               Expected: {6}, Actual: {7}'.format('Test', comment.forum_topic.topic_title,
                                                  'my comment', comment.comment,
                                                  'test@test.com', comment.author.email,
                                                  'my reply', reply.comment))

        self.assertEqual(comment.forum_topic.topic_title, 'Test')
        self.assertEqual(comment.comment, 'my comment')
        self.assertEqual(comment.author.email, 'test@test.com')
        self.assertEqual(reply.comment, 'my reply')
