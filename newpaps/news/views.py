from django.views.generic import (ListView,DetailView,CreateView,DeleteView,UpdateView)
from django.http import HttpResponse
from .models import *
from .filters import PostFilter
from .forms import PostForm,SignUpForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import redirect,render,get_object_or_404
from django.core.cache import cache
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.core.mail import send_mail



from django.http import HttpResponse
from django.views import View
from .tasks import hello
from datetime import datetime, timedelta

class IndexView(View):
    def get(self, request):
        printer.apply_async([10],
                            eta = datetime.now() + timedelta(seconds=5))
        hello.delay()
        return HttpResponse('Hello!')

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'

    template_name = 'registration/signup.html'






class AuthorList(ListView):
    model=Author
    context_object_name='Author'
    template_name='news/author_list.html'


class PostList(ListView):
    model = Post
    context_object_name = 'Post'
    template_name = 'post.html'
    ordering = 'title'
    paginate_by= 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        return context


def index(request):
    news= New.objects.all()
    return render(request,'index.html',context={'news':news})

def default(request,slug):
    new=New.objects.get(slug__iexact=slug)
    return render(request,'default.html',context={'new':new})


class PostDetail(DetailView):
    model = Post
    template_name='news/post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news/search.html'
    context_object_name = 'search'





class PostCreate( PermissionRequiredMixin,CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    context_object_name = 'create'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.quantity = 10
        author = form.save(commit=False)
        author.quantity = authoruser
        return super().form_valid(form)

class PostDelete(PermissionRequiredMixin,DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_edit')



class Posts(LoginRequiredMixin,ListView):
    model=Post
    template_name='posts.html'
    context_object_name='posts'
    ordering='title'
    pfginate_by=2

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,queryset=self.get_queryset())
        context['is_not_author']= not self.request.user.groups.filter(name='authors').exists()
        return context


class PostUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'



class CategoryListView(ListView):
    model=Post
    template_name='category_list.html'
    context_odject_name='category_news_list'

    def get_queryset(self):
        self.category=get_object_or_404(Category,id=self.kwargs['pk'])
        queryset=Post.object.filter(category=self.category).order_by('-date')
        return queryset

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['is_not_subscriber']=self.request.user not in self.category.subscribers.all()
        context['category']=self.category
        return context

@login_required
def subscribe(request,pk):
    user=request.user
    category=Category.object.get(id=pk)
    category.subscribers.add(user)

    message='Вы успешно подписались на рассылку новостей категории'
    return render(request,'news/subscribe.html',{'category':category,'message':message})


