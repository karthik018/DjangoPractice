from django.db import models

# Create your models here.
REACTION_TYPES = (
        ('NO', 'NONE'),
        ('LI', 'LIKE'),
        ('LO', 'LOVE'),
        ('HA', 'HAHA'),
        ('WO', 'WOW'),
        ('SA', 'SAD'),
        ('AN', 'ANGRY')
    )


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=15)
    profile_pic = models.CharField(max_length=100, default=None)


class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_description = models.CharField(max_length=300)
    post_created_date = models.DateTimeField()


class Likes(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=2, choices=REACTION_TYPES)


class Comments(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_id = models.AutoField(primary_key=True)
    commented_on_id = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    comment_create_date = models.DateTimeField()
    message = models.CharField(max_length=300)


class CommentLikes(models.Model):
    comment_id = models.ForeignKey(Comments, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=2, choices=REACTION_TYPES)

