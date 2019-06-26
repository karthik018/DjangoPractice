from .models import User, Posts, CommentLikes, Comments, REACTION_TYPES, Likes


def get_post(post_id):
    post = Posts.objects.filter(post_id=post_id)
    posted_by = {"name": post[0].user_id.user_name, "user_id": post[0].user_id.user_id, "profile_pic_url": post[0].user_id.profile_pic}
    posted_at = post[0].post_created_date
    print(posted_at.date(), posted_at.time())
    result = {"posted_by": posted_by, "posted_at": posted_at}
    print(result)