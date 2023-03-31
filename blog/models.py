from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from taggit.models import TaggedItemBase
from taggit.models import Tag as TaggitTag
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager


class BlogPage(Page):
    description = models.CharField(max_length=250, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]


class PostPage(Page):
    header_image = models.ForeignKey("wagtailimages.Image", on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    tags = ClusterTaggableManager(through="PostPageTags", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("header_image"),
        FieldPanel('tags'),
        InlinePanel('categories', label="category"),

    ]


class PostPageBlogCategory(models.Model):
    Page = ParentalKey("blog.PostPage", on_delete=models.CASCADE, blank=True, related_name='categories')
    blog_category = models.ForeignKey("BlogCategory", on_delete=models.CASCADE, blank=True, related_name='post_pages')

    panels = [
        FieldPanel("blog_category"),
    ]

    class Meta:
        unique_together = ("Page", "blog_category")


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=80, unique=True)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'blog categories'


class PostPageTags(TaggedItemBase):
    content_object = ParentalKey(
        'blog.PostPage',
        blank=True,
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


@register_snippet
class Tags(TaggitTag):
    class Meta:
        proxy = True
