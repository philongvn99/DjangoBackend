
from django.db import models


# Create your models here.    
# ==============================================================//
class Player(models.Model):
    ROLES = [
        ("GOALKEEPER", "GOALKEEPERS"),
        ("DEFENDER", "DEFENDER"),
        ("MIDFIELDER", "MIDFIELDER"),
        ("FORWARD", "FORWARD"),
    ]
    STATUSES = [
        ("ACTIVE", "ACTIVE"),
        ("LOAN", "LOAN"),
        ("LEFT", "LEFT"),
    ]
    id = models.AutoField(primary_key=True, db_column="n4_id")
    name = models.CharField(max_length=50, db_column="str_name")
    full_name = models.CharField(max_length=50, db_column="str_full_name")
    avatar_link = models.CharField(max_length=100, db_column="str_avatar_link")
    nationality = models.CharField(max_length=30, db_column="str_nationality")
    birthday = models.DateField(db_column="dt_birthday")
    right_foot = models.BooleanField(db_column="is_right_foot")
    kit_number = models.IntegerField(db_column="n4_kit_number")
    height = models.IntegerField(db_column="n4_height")
    role = models.TextField(choices=ROLES, null=True, db_column="str_role") 
    salary = models.IntegerField(blank=True, null=True, db_column="n4_salary")
    status = models.CharField(max_length=50, choices=STATUSES, null=False, db_column="str_status")

    class Meta:
        managed = False
        db_table = 'player'
        ordering = ['birthday']
        
    def __str__(self):
        return self.name

    
