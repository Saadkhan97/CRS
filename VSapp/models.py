from django.db import models


# Create your models here.
class UserInformation(models.Model):
    ROLE_CHOICES = (
        ('User', 'User'),
        ('Verifier', 'Verifier'),
        ('Reviewer', 'Reviewer'),

    )

    username = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    password1 = models.CharField(max_length=200,null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')

    def __str__(self):
        return self.username

class Hadith_Text_Image(models.Model):
    verification_STATUS = (
        ('Verified', 'Verified'),
        ('Wrong', 'Wrong'),
        ('Pending', 'Pending'),
    )
    analyzation_STATUS = (
        ('Not Analyzed', 'Not Analyzed'),
        ('Analyzed', 'Analyzed'),
        ('Wrong', 'Wrong'),
    )
    hadith_choice_status = (
        ('Approved','Approved'),
        ('Wrong','Wrong'),
        ('Pending','Pending'),
        ('Reviewed','Reviewed'),
    )
    user_id = models.CharField(max_length=10,null=True)
    hadith_text = models.CharField(max_length=500,null=True)
    verifier_id = models.ForeignKey(UserInformation,on_delete=models.CASCADE,limit_choices_to={'role': 'Verifier'},related_name='Verifier',null=True)
    reviewer_id = models.ForeignKey(UserInformation,on_delete=models.CASCADE,limit_choices_to={'role': 'Reviewer'},related_name='Reviewer',null=True)

    hadith_due_date = models.DateField(null=True)
    # analyzed_date = models.DateField(null=True)
    verification_status = models.CharField(max_length=30, choices=verification_STATUS,default='Pending')
    # analyzation_status = models.CharField(max_length=30, choices=analyzation_STATUS, default='Not Analyzed')
    urdu_translation = models.CharField(max_length=100000,null=True)
    englist_translation = models.CharField(max_length=100000,null=True)
    hadith_status = models.CharField(max_length=35,choices=hadith_choice_status,default='Pending')
    book_id = models.CharField(max_length=254,default="0")
    url = models.CharField(max_length=100000000000,null=True)

    def __str__(self):
        return self.hadith_text
    
class ImgSaveFile(models.Model):
    userid=models.CharField(max_length=200,null=True)
    image_file=models.FileField(upload_to='image_files', max_length=254)

class Book_Table(models.Model):
    book_name = models.CharField(max_length=1000000,null=True)
    book_files = models.FileField(upload_to='Book_PDF',max_length=200000)