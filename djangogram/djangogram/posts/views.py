from django.shortcuts import render, get_object_or_404
from djangogram.users.models import User as user_model
from . import models, serializers
from django.db.models import Q
from .forms import CreatePostForm

# Create your views here.


def index(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            user = get_object_or_404(user_model, pk=request.user.pk)
            following = user.following.all()
            posts = models.Post.objects.filter(Q(author__in=following) | Q(author=user))

            serializer = serializers.PostSerializer(posts, many=True)

            return render(
                request,
                "posts/main.html",
                {
                    "posts": serializer.data,
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
