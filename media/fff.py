class BaseUser(models.Model):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Admin(User):
    class Meta:
        proxy = True
    def save(self, *args, **kwargs):
        kwargs['is_admin'] = True
        return super().save(*args, **kwargs)
        objects = models.Manager().filter(is_admin=True) # Default manager for regular queries

class Customer(User):

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        kwargs['is_customer'] = True
        return super().save(*args, **kwargs)
        objects = models.Manager().filter(is_customer=True) # Default manage
        recent_customers = models.Manager().filter(is_customer=True).order_by('-date_joined')[:5] # Custom queryset for recent customers