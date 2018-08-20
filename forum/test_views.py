from django.shortcuts import reverse
from django.test import TestCase, RequestFactory
from accounts.models import User
from .views import forum, add_topic, add_comment, add_reply, view_topic
from .models import ForumTopic, ForumComment, ForumCommentReply

class TestForumViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.credentials = {'email': 'user@test.com', 'password': 'Secret12'}
        self.user = User.objects.create_user(**self.credentials)

    def test_forum(self):
        '''
        Verify that the forum topic listing is rendered at the correct url
        '''
        request = self.factory.get(reverse('forum'))
        request.user = self.user

        response = forum(request)
        print('TestForumViews: forum - test_forum \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format(200, response.status_code,
                                                  'forum', request.path))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.path, "/forum/")

    def test_forum_add_topic(self):
        '''
        Add a forum topic view displays the form at the expected URL
        '''
        request = self.factory.get(reverse('add_topic'))
        request.user = self.user

        response = add_topic(request)
        print('TestForumViews: add_topic - test_forum_add_topic \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format(200, response.status_code,
                                                  '/forum/add-topic', request.path))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.path, '/forum/add-topic')

    def test_view_topic(self):
        '''
        Single topic view displays all comments under the expected URL
        '''
        topic = ForumTopic(topic_title='Test')
        topic.save()

        request = self.factory.get(reverse('view_topic', args=[topic.id]))
        request.user = self.user

        response = view_topic(request, topic.id)
        print('TestForumViews: view_topic - test_view_topic \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format(200, response.status_code,
                                                  '/forum/view/{0}'.format(topic.id), request.path))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.path, '/forum/view/{0}'.format(topic.id))

    def test_add_comment(self):
        '''
        Topic comment addition form is rendered under the expected URL
        '''
        topic = ForumTopic(topic_title='Test')
        topic.save()

        request = self.factory.get(reverse('add_comment', args=[topic.id]))
        request.user = self.user

        response = add_comment(request, topic.id)
        print('TestForumViews: add_comment - test_add_comment \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format(200, response.status_code,
                                                  '/forum/comment/{0}'.format(topic.id), request.path))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.path, '/forum/comment/{0}'.format(topic.id))

    def test_add_reply(self):
        '''
        Topic comment reply form is rendered under the expected URL
        '''
        topic = ForumTopic(topic_title='Test')
        topic.save()
        comment = ForumComment(forum_topic=topic, comment='Test comment', author = self.user)
        comment.save()

        request = self.factory.get(reverse('add_reply', args=[comment.id]))
        request.user = self.user

        response = add_reply(request, comment.id)
        print('TestForumViews: add_reply - test_add_reply \n \
               Expected: {0}, Actual: {1} \n \
               Expected: {2}, Actual: {3}'.format(200, response.status_code,
                                                  '/forum/reply/{0}'.format(comment.id), request.path))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.path, '/forum/reply/{0}'.format(comment.id))
