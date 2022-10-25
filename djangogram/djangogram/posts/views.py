from django.shortcuts import render, get_object_or_404, redirect
from djangogram.users.models import User as user_model
from . import models, serializers
from django.db.models import Q
from .forms import CreatePostForm, CommentForm
from django.urls import reverse

# Create your views here.


def index(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            comment_form = CommentForm()

            user = get_object_or_404(user_model, pk=request.user.pk)
            following = user.following.all()
            posts = models.Post.objects.filter(Q(author__in=following) | Q(author=user))
            comments = models.Comment
            serializer = serializers.PostSerializer(posts, many=True)

            return render(
                request,
                "posts/main.html",
                {
                    "posts": serializer.data,
                    "comment_form": comment_form,
                },
            )


def post_create(request):

    if request.method == "GET":
        form = CreatePostForm()
        return render(request, "posts/post_create.html", {"form": form})

    elif request.method == "POST":
        if request.user.is_authenticated:
            user = get_object_or_404(user_model, pk=request.user.id)
            form = CreatePostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = user
                post.save()

                return render(request, "posts/main.html")
            else:
                print(form.errors)
        else:
            return render(request, "users/main.html")


def comment_create(request, post_id):

    if request.user.is_authenticated:
        post = get_object_or_404(models.Post, pk=post_id)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.posts = post
            comment.save()

            return redirect(reverse("posts:index") + "#comment-" + str(comment.id))
            # '#' 뒤에 있는 html 선택자로 이동
    else:
        return render(request, "users/main.html")
