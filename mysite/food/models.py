from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinLengthValidator

# Create your models here.
class item(models.Model):
    
    def __str__(self):
        return self.item_name
    
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    item_name = models.CharField(max_length = 200)
    item_disc = models.CharField(max_length = 200)
    item_price = models.IntegerField()
    #item_image = models.CharField(max_length = 800, default='https://images.pexels.com/photos/4439444/pexels-photo-4439444.jpeg?auto=compress&cs=tinysrgb&w=800')
    item_image =  models.ImageField(null =True, blank = True, upload_to='item_pictures')
    likes = models.ManyToManyField(User, related_name="item_likes")

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse("food:detail", kwargs = {"pk": self.pk}) 



class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    Item = models.ForeignKey(item, related_name="comments", on_delete=models.CASCADE)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'



