from django.shortcuts import render , get_object_or_404 , redirect
from django.http import HttpResponse 
from .models import Blog , Category


def posts_by_category(request,category_id):
    #fetch the posts that belog to the category with id = category_id
    posts = Blog.objects.filter(status='Published', category = category_id)
   
    context = {
        'posts':posts,
       
    }
    return render(request, 'posts_by_category.html', context)
    