from django.db import models

# Create your models here.
AD_TYPE_CHOICES = (
        ('O','OFFER'),
        ('W', 'WANTED')
        )
PRICE_TYPE_CHOICES = (
        ('F', 'FIXED'),
        ('GA', 'GIVE_AWAY'),
        ('C', 'CONTACT'),
        ('ST', 'SWAP_TRADE'),
        )


class PostableItem(models.Model):
    created = models.DateTimeField(auto_now_add = True)
    address = models.CharField(max_length=500)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    categoryId = models.CharField(max_length=10)
    adType=models.CharField(choices = AD_TYPE_CHOICES, max_length = 2)
    priceType=models.CharField(choices = PRICE_TYPE_CHOICES, max_length = 1)
    priceAmount=models.IntegerField()
    locationId=models.CharField(max_length=20,default='1700212')
    username=models.CharField(max_length=40)
    password=models.CharField(max_length=40)

class PostableAttr(models.Model):
    related_item = models.ForeignKey(PostableItem, on_delete=models.CASCADE, related_name = 'attr') 
    key = models.CharField(max_length=500)
    val = models.CharField(max_length=500)

    class Meta:
        unique_together = ('related_item', 'key')

    def __unicode__(self):
        return key+":"+val

