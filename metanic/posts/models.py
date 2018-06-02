from zope import interface

from metanic.core import models
from metanic.collector import collection

from metanic.accounts import models as accounts_models
from metanic.posts import renderer


class Post(renderer.Renderable, models.CreateUpdateModel):
    subject = models.TextField()
    body = models.TextField()

    author = models.ForeignKey(
        accounts_models.User,
        on_delete=models.PROTECT,
        null=True,
    )

    in_reply_to = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='replies',
    )


class History(models.CreateUpdateModel):
    post = models.ForeignKey(
        Post,
        related_name='history',
        on_delete=models.PROTECT,
    )


@interface.implementer(collection.ICollection)
class Topic(models.CreateUpdateModel):
    name = models.TextField(unique=True)

    posts = models.ManyToManyField(
        Post,
        related_name='topics',
        blank=True,
        editable=False,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower().strip()
        return super(Topic, self).save(*args, **kwargs)

    class Meta(models.CreateUpdateModel.Meta):
        verbose_name_plural = 'topics'


class Category(Topic):
    class Meta(models.CreateUpdateModel.Meta):
        verbose_name_plural = 'categories'

    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if self.parent == self:
            self.parent = None

        return super(Category, self).save(*args, **kwargs)
