from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name=models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Bids(models.Model):
    bid=models.DecimalField(max_digits=100, decimal_places=2,default=0)
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="ubid", null=True)

    def __str__(self):
        return str(self.bid)

class Auction_listings(models.Model):
    title=models.CharField(max_length=64)
    Owner=models.ForeignKey(User, on_delete=models.CASCADE , related_name="seller")
    description=models.CharField(max_length=350)
    imgurl=models.CharField(max_length=99999)
    startingbid=models.ForeignKey(Bids, on_delete=models.CASCADE, related_name="bidn")
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cars')
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return f' {self.id} {self.title}'
    
class Watchlist(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    listing=models.ForeignKey(Auction_listings, on_delete=models.CASCADE)

    class Meta:
        unique_together=('user', 'listing')

    def __str__(self):
        return f"{self.user}'s watchlist: {self.listing.title}"
    

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)  
    listing = models.ForeignKey(Auction_listings, on_delete=models.CASCADE,null=True) 
    content = models.CharField(max_length=99999,null=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.listing.title}"  