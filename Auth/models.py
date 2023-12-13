from django.db import models

# Create your models here.    
# ==============================================================//    
class Account(models.Model):
    account_id = models.CharField(primary_key=True, max_length=256)
    account_email = models.CharField(max_length=256)
    account_username = models.CharField(max_length=256)
    account_phone = models.CharField(max_length=256)
    account_name = models.CharField(max_length=256)
    account_password = models.CharField(max_length=256)
    account_role = models.TextField()  # This field type is a guess.
    account_license_plate = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_account'
        
    def __str__(self):
        return self.account_username