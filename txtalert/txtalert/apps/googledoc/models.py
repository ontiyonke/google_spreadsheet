from django.db import models

class SpreadSheet(models.Model):
    spreadsheet = models.CharField(label='SpreadSheet Name', max_length=200)
