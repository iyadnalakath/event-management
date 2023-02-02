from django.contrib import admin
from .models import *

# Register your models here.

class AreaAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'area'

    )
admin.site.register(Area,AreaAdmin)


class SubCatagoryAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'sub_catagory_name',
        'image'
        

    )
admin.site.register(SubCatagory,SubCatagoryAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'service_name',
        'sub_catagory',
        'amount',
        'account'


        

    )
admin.site.register(Service,ServiceAdmin)

class RatingAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'rating',
        'service',
        'review',
        'created_at',
        'name'

    )
admin.site.register(Rating,RatingAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'notification'
    )
admin.site.register(Notification,NotificationAdmin)

class ProfilePicAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'account',
        'profile_pic',
        'more_photos'


    )
admin.site.register(ProfilePic,ProfilePicAdmin)