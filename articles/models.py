from django.db import models


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_text = models.TextField()
    article_uuid = models.UUIDField()
