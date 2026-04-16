from django.shortcuts import render , redirect
from blogs.models import Category , Blog
from  django.contrib.auth.decorators import login_required
from .forms import CategoryForm , PostForm , AddUserForm , EdituserForm
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your views here.


@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.all().count()
    blog_count = Blog.objects.all().count()
    context = {
                    'category_count':category_count,
                    'blog_count':blog_count
    }
    return render(request, 'dashboard/dashboard.html',context)


def categories(request):
    return render(request, 'dashboard/categories.html')


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm()
    context = {'form':form }
    return render(request , 'dashboard/add_category.html',context)


def edit_category(request,pk):
    category = get_object_or_404(Category , pk = pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST , instance = category)
        if form.is_valid():
            form.save()
            return redirect('categories')

    form = CategoryForm(instance = category)
    context = {
        'form':form,
         'category':category
        }
    return render (request , 'dashboard/edit_category.html',context)


def delete_category(request , pk):
    cat = get_object_or_404(Category , pk = pk)
    cat.delete()
    return redirect('categories')


# POST CRUD

def posts(request):
    posts = Blog.objects.all()
    context = {
        'posts':posts,
    }
    return render (request , 'dashboard/posts.html',context)

def add_posts(request):  # for image insert must add enctype in form and here request.FILES.
    if request.method == "POST":
        form = PostForm(request.POST , request.FILES)
        if form.is_valid():
            post = form.save(commit = False) #temp saving form/ gives time to use tabel data
            post.author =  request.user
            post.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title)+ '-'+str(post.id)
            post.save() 
            return redirect('posts')
        else:
            print("form is invalid")
            print(form.errors)

#this below code for render blank form on page
    form = PostForm()
    context = {
        'form':form
    }
    return render(request, 'dashboard/add_posts.html',context)



def edit_posts(request , pk):
    posts = get_object_or_404(Blog, pk = pk)
    if request.method == 'POST':
        form = PostForm(request.POST , request.FILES ,  instance= posts ) 
        if form.is_valid():
            posts = form.save()
            title = form.cleaned_data['title']
            posts.slug = slugify(title)+'-'+str(posts.id)
            posts.save()
            return redirect('posts')

    form = PostForm(instance=posts)
    context = {
        'form':form,
        'post':posts,  #posts for when user click on update button to update particular id
    }
    return render(request, 'dashboard/edit_posts.html',context)


def delete_posts(request, pk):
    blog = get_object_or_404(Blog , pk = pk)
    blog.delete()
    return redirect('posts')


# user crud

def users(request):
    users = User.objects.all()
    context = {
        'users':users,
    }
    return render(request, 'dashboard/users.html',context)

def add_users(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
        else:
            print("form is invalid")
            print(form.errors)

    form = AddUserForm()
    context = {
        'form':form,
    }
    return render(request, 'dashboard/add_users.html', context)


def edit_users(request, pk):
    user = get_object_or_404(User , pk = pk)
    if request.method == 'POST':
        form = EdituserForm(request.POST , instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
        else:
            print("form is invalid")
            print(form.errors)


    form = EdituserForm(instance = user) #for render form with data.
    context = {
        'form':form,
        'user':user,
    }
    return render(request, 'dashboard/edit_user.html', context)



def delete_users(request, pk):
    user = User.objects.get(pk = pk)
    user.delete()
    return redirect('users')