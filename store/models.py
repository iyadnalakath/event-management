from django.db import models
from main.models import BaseModel
from projectaccount.models import Account


# Create your models here.
class Area(BaseModel):
    area=models.CharField(max_length=255,null=False,blank=False)

    def __str__(self):
        return self.area

# class Catagory(BaseModel):
#     catagory_name=models.CharField(max_length=255,null=False,blank=False)
#     image=models.ImageField(upload_to ='mediafiles')

#     def __str__(self) -> str:
#         return self.catagory_name

class SubCatagory(BaseModel):
    sub_catagory_name=models.CharField(max_length=255,null=False,blank=False)
    # catagory=models.ForeignKey(Catagory, on_delete=models.PROTECT)
    image=models.ImageField(upload_to ='mediafiles')

    def __str__(self) -> str:
        return self.sub_catagory_name

# class EventTeam(BaseModel):
#     name=models.CharField(max_length=255,null=False,blank=False)
#     area=models.ForeignKey(Area,on_delete=models.PROTECT)
#     address=models.CharField(max_length=255,null=False,blank=False)
#     phone=models.IntegerField(null=False,blank=False)
#     image=models.ImageField(upload_to ='mediafiles')
#     over_view=models.TextField(null=False,blank=False)
#     working_time=models.TimeField(null=True,blank=True)

#     def __str__(self):
        # return self.name


class Service(BaseModel):
    service_name=models.CharField(max_length=50,null=True,blank=True)
    # event_team=models.ForeignKey(EventTeam,on_delete=models.CASCADE)
    sub_catagory=models.ForeignKey(SubCatagory,on_delete=models.CASCADE)
    amount=models.IntegerField(null=True,blank=True)
    # rating=models.IntegerField(null=True,blank=True)
    # is_featured=models.BooleanField(default=False)
    account = models.ForeignKey(Account,on_delete=models.PROTECT,related_name='event_team')
