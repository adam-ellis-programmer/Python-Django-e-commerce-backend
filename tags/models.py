from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.


class Tag(models.Model):
    label = models.CharField(max_length=255)

# do not make this relient on other Apps


class TaggedItem(models.Model):
    # what tag is applied to what object
    # remove from all assosiated objects
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # identify the object that this tag is applied to

    # Type (product, video, article)
    # ID
    # generic way  to identify a product
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    # gets the actual object taged -- reads the actual obj that tag is applied to
    content_object = GenericForeignKey()
