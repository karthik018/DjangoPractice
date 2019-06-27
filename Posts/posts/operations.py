from .models import User, Posts, CommentLikes, Comments, REACTION_TYPES, Likes
from django.utils import timezone as t


reactions_types = {"NO": "NONE", "LI": "LIKE", "LO": "LOVE", "SA":"SAD", "WO": "WOW", "AN": "ANGRY", "HA": "HAHA"}


def getreaction(reaction_type):
    for reaction in reactions_types:
        if reactions_types[reaction] == reaction_type:
            return reaction
    return


def getreactiontype(likes):
    reactions_type = []
    for like in likes:
        reaction = like['reaction']
        reactions_type.append(reactions_types[reaction])
    return reactions_type


def get_post(post_id):
    post = Posts.objects.filter(post_id=post_id)
    posted_by = {"name": post[0].user_id.user_name, "user_id": post[0].user_id.user_id, "profile_pic_url": post[0].user_id.profile_pic}
    posted_at = post[0].post_created_date
    posted_at = ' '.join([str(posted_at.date()), str(posted_at.time())])
    post_content = post[0].post_description
    post_likes = Likes.objects.filter(post_id=post_id)
    post_likes = post_likes.values('reaction').distinct()
    post_reactions = getreactiontype(post_likes)
    comments = Comments.objects.filter(post_id=post_id, commented_on_id=None)
    comments_count = len(comments)
    post_comments = []
    for comment in comments:
        post_replies = []
        commenter = {"user_id": comment.user_id.user_id, "name": comment.user_id.user_name, "profile_pic_url": comment.user_id.profile_pic}
        commented_at = comment.comment_create_date
        commented_at = ' '.join([str(commented_at.date()), str(commented_at.time())])
        reaction = CommentLikes.objects.filter(comment_id=comment.comment_id)
        reaction_count = len(reaction)
        reaction_type = reaction.values('reaction')
        reactions = getreactiontype(reaction_type)
        comment_reactions = {"count": reaction_count, "type": reactions}
        replies = Comments.objects.filter(post_id=post_id, commented_on_id=comment.comment_id)
        replies_count = len(replies)
        for reply in replies:
            replied_at = reply.comment_create_date
            replied_at = ' '.join([str(replied_at.date()), str(replied_at.time())])
            reply_reaction = CommentLikes.objects.filter(comment_id=reply.comment_id)
            reply_react_count = len(reply_reaction)
            reply_react_type = reply_reaction.values('reaction')
            reply_react_type = getreactiontype(reply_react_type)
            replier = {"comment_id": reply.comment_id, "commenter": {"user_id": reply.user_id.user_id, "name": reply.user_id.user_name, "profile_pic_url": reply.user_id.profile_pic}, "commented_at": replied_at, "comment_content": reply.message,
                       "reactions": {"count": reply_react_count, "type": reply_react_type}}
            post_replies.append(replier)
        post_comment = {"comment_id": comment.comment_id, "commenter": commenter, "commented_at": commented_at, "comment_content": comment.message, "reactions": comment_reactions, "replies_count": replies_count, "replies": post_replies}
        post_comments.append(post_comment)

    result = {"post_id": post_id, "posted_by": posted_by, "posted_at": posted_at, "post_content": post_content, "reactions": post_reactions, "comments": post_comments, "comments_count": comments_count}
    return result


def create_post(user_id, post_content):
    user = User.objects.get(user_id=user_id)
    post = Posts(user_id=user, post_description=post_content, post_created_date=t.now())
    post.save()


def add_comment(post_id, comment_user_id, comment_text):
    user = User.objects.get(user_id=comment_user_id)
    post = Posts.objects.get(post_id=post_id)
    comment = Comments(post_id=post, user_id=user, comment_create_date=t.now(), message=comment_text)
    comment.save()


def reply_to_comment(comment_id, reply_user_id, reply_text):
    user = User.objects.get(user_id=reply_user_id)
    comment = Comments.objects.get(comment_id=comment_id)
    reply_id = comment.commented_on_id.comment_id
    if reply_id is None:
        comment = Comments.objects.get(comment_id=comment_id, commented_on_id=None)
    else:
        comment = Comments.objects.get(comment_id=reply_id)
    post = Posts.objects.get(post_id=comment.post_id.post_id)
    reply = Comments(post_id=post, user_id=user, commented_on_id=comment, comment_create_date=t.now(),
                     message=reply_text)
    reply.save()


def react_to_post(user_id, post_id, reaction_type):
    user = User.objects.get(user_id=user_id)
    post = Posts.objects.get(post_id=post_id)
    reaction_type = getreaction(reaction_type)
    try:
        react = Likes.objects.get(user_id=user, post_id=post)
        if react.reaction == reaction_type:
            reaction_type = "NO"
        else:
            reaction_type = reaction_type
        react.reaction = reaction_type
        react.save()
    except:
        react = Likes(user_id=user, post_id=post, reaction=reaction_type)
        react.save()


def react_to_comment(user_id, comment_id, reaction_type):
    user = User.objects.get(user_id=user_id)
    comment = Comments.objects.get(comment_id=comment_id)
    reaction_type = getreaction(reaction_type)
    try:
        react = CommentLikes.objects.get(user_id=user, comment_id=comment)
        if react.reaction == reaction_type:
            reaction_type = "NO"
        else:
            reaction_type = reaction_type
        react.reaction = reaction_type
        react.save()
    except:
        react = CommentLikes(user_id=user, comment_id=comment, reaction=reaction_type)
        react.save()


def get_user_posts(user_id):
    user = User.objects.get(user_id=user_id)
    posts_list = []
    posts = Posts.objects.filter(user_id=user)
    for post in posts:
        posts_list.append(get_post(post.post_id))

    return posts_list


def get_posts_with_more_positive_reactions():
    posts = Posts.objects.all()
    positive_posts = []
    for post in posts:
        p = get_post(post.post_id)
        reactions = p['reactions']
        print(reactions)
        positive_reactions = ["LIKE", "LOVE", "WOW", "HAHA"]
        negative_reactions = ["SAD", "ANGRY"]
        positive = 0
        negative = 0
        for react in reactions:
            if react in positive_reactions:
                positive += 1
            elif react in negative_reactions:
                negative += 1
        if positive > negative:
            positive_posts.append(post.post_id)
    return positive_posts


def get_posts_reacted_by_user(user_id):
    user = User.objects.get(user_id=user_id)
    likes = Likes.objects.filter(user_id=user)
    posts_list = []
    for like in likes:
        posts_list.append(get_post(like.post_id.post_id))
    return posts_list