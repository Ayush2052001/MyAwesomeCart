from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost


# Create your views here.
# Blog View
def index(request):
    return render(request, 'blog/index.html')


def blogpost(request):
    blogpost = Blogpost.objects.all()
    passed= []
    for blog in blogpost:
        title = blog.title
        head0 = blog.head0
        chead0 = blog.chead0
        params = {'title': title, 'head0': head0, 'chead0': chead0}
        passed.append(params)
    blogged= {'allBlogs': passed}
        # return render(request, 'blog/blogpost.html', params)
    print(blogged)
    return render(request, 'blog/blogpost.html', blogged)
