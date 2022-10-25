from django.db import models
from djangogram.users import models as user_moedel

# Create your models here.
class TimeStamedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Post(TimeStamedModel):
    author = models.ForeignKey(
        user_moedel.User,
        null=True,
        on_delete=models.CASCADE,
        related_name="post_author",
    )
    image = models.ImageField(blank=False)
    caption = models.TextField(blank=False)
    image_likes = models.ManyToManyField(
        user_moedel.User, blank=True, related_name="post_image_likes"
    )

    def __str__(self):
        return f"{self.author}:{self.caption}"


class Comment(TimeStamedModel):
    author = models.ForeignKey(
        user_moedel.User,
        null=True,
        on_delete=models.CASCADE,
        related_name="comment_author",
    )
    posts = models.ForeignKey(
        Post,
        null=True,
        on_delete=models.CASCADE,
        related_name="comment_post",
    )
    contents = models.TextField(blank=False)
    # 데이터 구분을 위한 메소드
    def __str__(self):
        return f"{self.author}:{self.contents}"
