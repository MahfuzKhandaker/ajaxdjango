from django.shortcuts import render
from django.http import JsonResponse
from django.views import generic
from ajaxify.models import Post
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator


def create_post(request):
    posts = Post.objects.all()
    response_data = {}

    if request.POST.get('action') == 'post':
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        description = request.POST.get('description')

        response_data['title'] = title
        response_data['slug'] = slug
        response_data['description'] = description

        Post.objects.create(
            title = title,
            slug = slug,
            description = description,
            )
        return JsonResponse(response_data)

    return render(request, 'create_post.html', {'posts':posts})    



def post_list(request):
    posts = Post.objects.all()
    # paginator = Paginator(posts, 2)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    context = {
        'posts': posts,
    }
    return render(request, 'post_list.html', context)


# class PostListView(generic.ListView):
#     model = Post
#     template_name = 'post_list.html'

#     def get_context_data(self, **kwargs):
#         context = super(PostListView, self).get_context_data(**kwargs)
#         context['posts'] = Post.objects.all()
#         context['post_num'] = Post.objects.count()
#         return context


class SearchResultsListView(generic.ListView):
    model = Post
    template_name = 'search_results.html'
    context_object_name = 'post_list'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Post.objects.filter(
            Q(title__icontains=query) | Q(categories__name__icontains=query)
        )


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.number_of_views = post.number_of_views+1
    post.save()

    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes,
    }

    return render(request, 'post_detail.html', context)


def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-created_on'
    )
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'blog_category.html', context)


def like(request):
    post = get_object_or_404(Post, slug = request.POST.get('slug'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        print(request.user.id)
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    
    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.likes.count(),
    }
    if request.is_ajax():
        html = render_to_string('like_section.html', context=context, request=request)
        return JsonResponse({'form': html})