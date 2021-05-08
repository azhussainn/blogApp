from django.db import models
from datetime import datetime
from django.template.defaultfilters import slugify


class Categories(models.TextChoices):
    WORLD = 'world'
    ENVIRONMENT = 'environment'
    TECHNOLOGY = 'technology'
    DESIGN = 'design'
    CULTURE = 'culture'
    BUSINESS = 'business'
    POLITICS = 'politics'
    OPINION = 'opinion'
    SCIENCE = 'science'
    HEALTH = 'health'
    STYLE = 'style'
    TRAVEL = 'travel'


class BlogPost(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    category = models.CharField(max_length=50, choices=Categories.choices, default=Categories.WORLD)
    thumbnail = models.ImageField(upload_to='photos/%Y/%m/%d')
    excerpt = models.CharField(max_length=150)
    month = models.CharField(max_length=3)
    day = models.CharField(max_length=2)
    content = models.TextField()
    featured = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        #making a slug of title
        original_slug = slugify(self.title)

        #getting count of slugs that match our slug
        queryset = BlogPost.objects.all().filter(slug__iexact=original_slug).count()

        count = 1
        slug = original_slug

        #add numbers to slug to make it unique
        while queryset:
            slug = f'{original_slug}-{count}'
            count += 1
            queryset = BlogPost.objects.all().filter(slug__iexact=slug).count()

        #storing the unique slug back in the model
        self.slug = slug

        #removing featured post if the current post is featured
        if self.featured:
            try:

                #getting previous featured object
                temp = BlogPost.objects.get(featured=True)

                #checking if the previous featured != current post
                if self != temp:
                    temp.featured = False
                    temp.save()

            except BlogPost.DoesNotExist:
                pass

        super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        return self.title