from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ForumTopic, ForumComment, ForumCommentReply
from .forms import ForumAddTopicForm, ForumAddCommentForm, ForumAddReplyForm


def forum(request):
    '''
    A simple paginated list of all forum topics
    '''
    topics = ForumTopic.objects.all()

    paginator = Paginator(topics, 5)
    page = request.GET.get('page')
    topic_list = paginator.get_page(page)

    return render(request, 'forum.html', {'topic_list': topic_list})

@login_required
def add_topic(request):
    '''
    Any registered and logged in user can add a new forum topic for discussion.
    '''
    if request.method == 'POST':
        topic_form = ForumAddTopicForm(request.POST)
        if topic_form.is_valid():
            topic_form.save()
            return redirect(reverse('forum'))
    else:
        topic_form = ForumAddTopicForm()

    return render(request, 'add_topic.html', {'topic_form': topic_form})

def view_topic(request, id):
    '''
    Paginated listing of all comments and comment replies within a specific forum topic
    '''
    topic = ForumTopic.objects.get(pk=id)
    comments = ForumComment.objects.filter(forum_topic=topic).order_by('-date_created')
    # Retrieve the list of comment ids so that we can extract the relevant comment replies
    ids = [c.id for c in comments]
    replies = ForumCommentReply.objects.filter(forum_comment__in=ids).order_by('date_created')

    paginator = Paginator(comments, 5)
    page = request.GET.get('page')
    topic_comments = paginator.get_page(page)

    return render(request, 'forum_topic.html', {'topic': topic,
                                                'topic_comments': topic_comments,
                                                'replies': replies})

@login_required
def add_comment(request, id):
    '''
    Allow any logged in user to add a comment within a forum topic
    '''
    topic = ForumTopic.objects.get(pk=id)

    if request.method == 'POST':
        comment_form = ForumAddCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.forum_topic = topic
            comment.save()
            return redirect(reverse('view_topic', args=[id]))
    else:
        comment_form = ForumAddCommentForm()

    return render(request, 'add_comment.html', {'comment_form': comment_form, 'topic': topic})

@login_required
def add_reply(request, id):
    '''
    All comments can have an unlimited number of replies posted
    '''
    comment = ForumComment.objects.get(pk=id)
    topic = ForumTopic.objects.get(pk=comment.forum_topic.id)

    if request.method == 'POST':
        reply_form = ForumAddReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.author = request.user
            reply.forum_comment = comment
            reply.save()
            return redirect(reverse('view_topic', args=[topic.id]))
    else:
        reply_form = ForumAddReplyForm()

    return render(request, 'add_reply.html', {'reply_form': reply_form, 'comment': comment})
