from django.shortcuts import render
from django.views.generic import ListView
from .models import Post

# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#
#     return render(
#         request,
#         'blog/post_list.html',
#         {
#             'post': posts,
#         }
#     )

class PostList(ListView):
    model = Post
    #template_name = 'blog/index.html'
    ordering = '-pk'


def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/single_post_page.html',
        {
            'post': post,
        }
    )




