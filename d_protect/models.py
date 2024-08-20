from django.db import models

# Create your models here.

class Create_Acc(models.Model):
    sno = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200, default='')
    Email_id = models.CharField(max_length=200, unique=True, default='')
    Password = models.CharField(max_length=200)


class Employee(models.Model):
    sno=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    aadhaar = models.CharField(max_length=1000, unique=True)
    mobile = models.CharField(max_length=1000, unique=True)
    address = models.CharField(max_length=200)
    document_path = models.CharField(max_length=255,blank=True, null=True)
    doct_file_name = models.CharField(max_length=255,blank=True, null=True)
    # For CDR
    cdr_files_path = models.CharField(max_length=1000,blank=True, null=True) 
    cdr_files_name = models.CharField(max_length=1000, blank=True, null=True) 

    def __str__(self):
        return self.name  
    

     