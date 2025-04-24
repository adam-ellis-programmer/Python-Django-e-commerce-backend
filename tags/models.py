from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
# custom manager


class TaggedItemManager(models.Manager):

    def get_tags_for(self, obj_type, obj_id):

        # represents a specific Product row int the CONTENT table
        content_type = ContentType.objects.get_for_model(obj_type)

    # USED IN THE TAG ITEM MODEL
    # select related loads tag first to prevent unwnated queries
        return TaggedItem.objects\
            .select_related('tag')\
            .filter(
                content_type=content_type,
                object_id=obj_id
            )


class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


# do not make this relient on other Apps


class TaggedItem(models.Model):
    objects = TaggedItemManager()
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
