from django.db import models
from django.contrib.contenttypes.models import ContentType # this model allows generic relationships
from django.contrib.contenttypes.fields import GenericForeignKey # this field allows generic relationships

# adding custom method to Model.objects
# new custom class that has get_tags_for method which is going to add to TaggedItem.objects
class TaggedItemManager(models.Manager):
  def get_tags_for(self, obj_type, obj_id):
    content_type = ContentType.objects.get_for_model(obj_type)

    # TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id=obj_id)
    return TaggedItem.objects \
           .select_related('tag') \
           .filter(
              content_type=content_type, 
              object_id=obj_id
            )
    
class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label
    
    class Meta:
        ordering = ['label']
    

class TaggedItem(models.Model):
    objects = TaggedItemManager() # adding custom method to 'objects' (manager object)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()