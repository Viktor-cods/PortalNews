from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db import models
from django.shortcuts import reverse
from django.core.validators import MinValueValidator
from django.urls import reverse



class New(models.Model):
    title=models.CharField(max_length=64)
    text=models.TextField()
    dat_public=models.DateTimeField(auto_now_add=True)
    slug=models.SlugField(max_length=128,unique=True)



    def get_absolute_url(self):
        return reverse('default',kwargs={'slug':self.slug})

    def __str__(self):
        return f'{self.title}:{self.text[:20]}'



class Author(models.Model):
    authorUser=models.OneToOneField(User,on_delete=models.CASCADE)
    ratingAuthor=models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat=self.Post_set.aggregate(postRating=Sum('rating'))
        pRat=0
        pRat+=postRat.get('postRating')

        commentRat=self.authorUser.comment_set_aggregate(commentRating=Sum('rating'))
        cRat=0
        cRat+=commentRat.get('CommentRating')

        self.ratingAuthor=pRat*3+cRat
        self.save()

class Category(models.Model):
    name=models.CharField(max_length=64, unique=True)
    subscribers=models.ManyToManyField(User, blank=True, null=True , related_name='categories')

    def __str__(self):
        return self.name

class Post(models.Model):
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    News='NW'
    ARTICLE="AR"
    CATEGORY_CHOICES=(
        (News,'Новость'),
        (ARTICLE,'Статья')
    )
    categoryType=models.CharField(max_length=2,choices=CATEGORY_CHOICES,default=ARTICLE)
    dateCreation=models.DateTimeField(auto_now_add=True)
    postCategory=models.ManyToManyField(Category,through='PostCategory')
    title=models.CharField(max_length=128)
    text=models.TextField()
    rating=models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.title}'

    def like(self):
        self.rating+=1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    postThrought=models.ForeignKey(Post,on_delete=models.CASCADE)
    categoryThrought = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost=models.ForeignKey(Post,on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text=models.TextField()
    dateCreation=models.DateTimeField(auto_now_add=True)
    rating=models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123]+'...'

class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )



