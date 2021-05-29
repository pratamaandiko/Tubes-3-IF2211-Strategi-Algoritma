from django.db import models

# Create your models here.

class DaftarKata(models.Model):
    kosakata = models.CharField(max_length=25,unique= True)

class Pengingat(models.Model):
    matkul = models.CharField(max_length=15)
    topik_tugas = models.CharField(max_length=220)
    jenis_tugas = models.ForeignKey(DaftarKata, on_delete=models.CASCADE)
    tenggat = models.DateField()