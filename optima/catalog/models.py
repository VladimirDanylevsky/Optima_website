from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from more_itertools import grouper


class CatalogIndexPage(Page):
    sphere = models.CharField(blank=False, max_length=90, default='Medicine')
    description = RichTextField(blank=False)
    short_title = models.CharField(blank=False, max_length=90, default='Manufacturer')

    class Meta:
        verbose_name = "Сторінка каталогу виробника, або можете " \
                       "використати як вкладений каталог (Вкладений каталог)"

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    def simple_pagination(self, elements=3):
        products = self.get_children()
        if len(products) == 0:
            return None
        if len(products) < elements+1:
            return products
        return grouper(elements, products, fillvalue=None)

    search_fields = Page.search_fields + [
        index.SearchField('description'),
        index.SearchField('short_title'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('sphere', classname="full"),
        FieldPanel('short_title', classname="full"),
        FieldPanel('description', classname="full"),
        InlinePanel('gallery_images', label="Галерея зображень")
    ]


class CatalogIndexPageGalleryImage(Orderable):
    page = ParentalKey(CatalogIndexPage, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        ImageChooserPanel('image'),
    ]


class CatalogMainPage(Page):
    intro = RichTextField(blank=False)

    class Meta:
        verbose_name = "Сторінка головного каталогу, НЕ СТВОРЮЙТЕ ЦЮ СТОРІНКУ (Головний каталог)"

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


class CatalogTilesPage(Page):
    description = RichTextField(blank=False, verbose_name='Опис розділу', default='ADD DESCRIPTION')

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    def simple_pagination(self, elements=3):
        products = self.get_children()
        if len(products) == 0:
            return None
        if len(products) < elements+1:
            return products
        return grouper(elements, products, fillvalue=None)

    def animation_time(self, start_time=0.0):
        for element in range(len(self.simple_pagination())):
            start_time = start_time + 0.2
            yield start_time


    class Meta:
        verbose_name = "Сторінка-каталог у вигляді тайлів, для однотипної продукції (Каталог-тайли)"

    search_fields = Page.search_fields + [
        index.SearchField('description'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        InlinePanel('gallery_images', label='Галерея зображень')
    ]


class CatalogTilesPageGalleryImage(Orderable):
    page = ParentalKey(CatalogTilesPage, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        ImageChooserPanel('image'),
    ]


class CatalogProductPage(Page):
    description = RichTextField(blank=False, verbose_name='Опис продукту')

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    class Meta:
        verbose_name = "Кінцева сторінка продукту (Сторінка продукту)"

    search_fields = Page.search_fields + [
        index.SearchField('description'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        InlinePanel('gallery_images', label="Галерея зображень")
    ]


class CatalogProductPageGalleryImage(Orderable):
    page = ParentalKey(CatalogProductPage, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    panels = [
        ImageChooserPanel('image'),
    ]
'''
class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-date
        context = super(BlogIndexPage, self).get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'), ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images")
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
'''