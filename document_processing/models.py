from django.db import models



class Image(models.Model):
    name = models.CharField(max_length=150)
    picture = models.ImageField(upload_to='images')
    picture_width=models.IntegerField()
    picture_height=models.IntegerField()
    no_channel=models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class PDF(models.Model):
    name = models.CharField(max_length=150)
    pdf_document=models.FileField(upload_to='documents')
    page_count = models.IntegerField()
    page_width = models.IntegerField()
    page_height = models.IntegerField()
    
    def __str__(self) -> str:
        return self.name

    