from django.db import models
class student(models.Model):
    cName = models.CharField(max_length=20, null=False)
    cSex = models.CharField(max_length=2, default='M', null=False)
    cBirthday = models.DateField(null=False)
    cEmail = models.EmailField(max_length=100, blank=True, default='')
    cPhone = models.CharField(max_length=50, blank=True, default='')
    cAddr = models.CharField(max_length=255,blank=True, default='')

# 建立資料模型
# 建立students類別，繼承「models.Model」，並在students類別建立欄位
# 之後建立的django資料庫就會包含，myapp中，models檔案裡面，類別名為student的資料表