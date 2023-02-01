from rest_framework import serializers
from .models import *
from main.functions import get_auto_id, password_generater
from projectaccount.serializer import RegisterEventTeamSerializer
from projectaccount.models import Account


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = [

            'id',
            'area'

        ]

        extra_kwargs = {
            'auto_id': {'read_only': True}
        }

    def create(self, validated_data):
        area = Area.objects.create(
            **validated_data,
            auto_id=get_auto_id(Area),
            # creator = self.context['request'].user
        )
        return area


# class CatagorySerializer(serializers.ModelSerializer):
#     # image = serializers.ImageField(required=False)
#     class Meta:
#         model=Catagory
#         fields=[

#             'id',
#             'catagory_name',
#             'image'

#         ]

#         extra_kwargs={
#             'auto_id':{'read_only':True}
#         }

#     def create(self, validated_data):
#         catagory=Catagory.objects.create(
#             **validated_data,
#             auto_id=get_auto_id(Catagory),
#             # creator = self.context['request'].user
#         )
#         return  catagory


class SubCatagorySerializer(serializers.ModelSerializer):
    # catagory_name=serializers.CharField(source='subcatagory.sub_catagory_name',read_only=True)
    class Meta:
        model = SubCatagory
        fields = [

            'id',
            'sub_catagory_name',
            # 'catagory',
            'image'
        ]

        extra_kwargs = {
            'auto_id': {'read_only': True}
        }

    def create(self, validated_data):
        subcatagory = SubCatagory.objects.create(
            **validated_data,
            auto_id=get_auto_id(SubCatagory),
            # creator = self.context['request'].user
        )
        return subcatagory


# class EventTeamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=EventTeam
#         fields=[

#             'id',
#             'name',
#             'area',
#             'address',
#             'phone',
#             'image',
#             'over_view',
#             'working_time'

#         ]

#         extra_kwargs={
#             'auto_id':{'read_only':True}
#         }

#     def create(self, validated_data):
#         eventteam=EventTeam.objects.create(
#             **validated_data,
#             auto_id=get_auto_id(EventTeam),
#             # creator = self.context['request'].user
#         )
#         return  eventteam

class EventTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'username',
            'team_name',
            'phone',
            'place',
            'work_time',
            'over_view',
            'address',
            # 'profile_pic'

        ]

        def create(self, validated_data):
            password = password_generater(8)
            validated_data["password"] = password
            validated_data["password2"] = password

            account_serializer = EventTeamSerializer(data=validated_data)
            if account_serializer.is_valid():
                account = account_serializer.save()

            return account

    #     extra_kwargs={
    #         'auto_id':{'read_only':True}
    #     }

    # def create(self, validated_data):
    #     event_team=EventTeamSerializer.objects.create(
    #         **validated_data,
    #         auto_id=get_auto_id(EventTeamSerializer),
    #         # creator = self.context['request'].user
    #     )
    #     return event_team

                     

class ServiceSerializer(serializers.ModelSerializer):
    # event_team_name=serializers.CharField(source='event_team.name',read_only=True)
    account_view = EventTeamSerializer(read_only=True, source='account')
    # account_view=serializers.CharField(source='account.username')
    sub_catagory_name = serializers.CharField(
        source='sub_catagory.sub_catagory_name', read_only=True)
    # popularity = serializers.FloatField(read_only=True)
    # enquiry=EnquirySerializer(read_only=True,source='enquiries')


    class Meta:
        model = Service
        fields = [

            'id',
            'service_name',
            # 'event_team',
            # 'event_team_name',
            'auto_id',
            'sub_catagory',
            'sub_catagory_name',
            'amount',
            'account',
            'account_view',
            'rating',
            # 'popularity'
            # 'enquiry'
            # 'amount',
            # 'rating',
            # 'is_featured',
            # 'event_team',
            # 'team_name',
            # 'work_time',
            # 'place',
            # 'over_view'


        ]

        

        extra_kwargs = {
            'auto_id': {'read_only': True},
            'rating':{'read_only':True}
            # 'team_name':{'read_only':True},
            # 'work_time':{'read_only':True},
            # 'place':{'read_only':True},
            # 'over_view':{'read_only':True},

        }



    def get_rating(self, obj):
        return obj.rating

    # def create(self, validated_data):
    #     service=Service.objects.create(
    #         **validated_data,
    #         auto_id=get_auto_id(Service),
    #         # creator = self.context['request'].user
    #     )
    #     return  service

    def create(self, validated_data):
        service = Service.objects.create(
            **validated_data,
            auto_id=get_auto_id(Service),

            # creator = self.context['request'].user
        )
        return service
    # def create(self, validated_data):
    #     print("create ///.")
    #     account_serializer = EventTeamSerializer(data=validated_data["account"])

    #     if(account_serializer.is_valid()):

    #         validated_data["account"] = account_serializer.save()

    #         service=Service.objects.create(
    #         **validated_data,
    #         auto_id=get_auto_id(Service),
    #         # creator = self.context['request'].user
    #     )
    #     return service


class RatingSerializer(serializers.ModelSerializer):
    # account=serializers.CharField(source='account.username',read_only=True)
    class Meta:
        model = Rating
        fields = [

            'id',
            # 'user',
            'service',
            'rating',
            'review',
            'created_at',
            'name'
            # 'account'

        ]


    def validate_rating(self, value):
        if value > 5.0 or value < 0.0:
            raise serializers.ValidationError("Rating should be between 0.0 and 5.0")
        return value

        # extra_kwargs = {
        #     'name': {'read_only': True}
        # }

    # def create(self, validated_data):
    #     rating = Rating.objects.create(
    #         **validated_data,
    #         auto_id=get_auto_id(Rating),
    #         # creator = self.context['request'].user
    #     )
    #     return rating

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields=[
            'id',
            'notification'
            ]
        extra_kwargs = {
            'auto_id': {'read_only': True}
        }

    def create(self, validated_data):
        notification = Notification.objects.create(
            **validated_data,
            auto_id=get_auto_id(Notification),
            # creator = self.context['request'].user
        )
        return notification
    

    #     extra_kwargs = {
    #         'auto_id': {'read_only': True}
    #     }

    # def create(self, validated_data):
    #     enquiry = Enquiry.objects.create(
    #         **validated_data,
    #         auto_id=get_auto_id(Enquiry),
    #         # creator = self.context['request'].user
    #     )
    #     return enquiry
    
class EnquirySerializer(serializers.ModelSerializer):
    # service = ServiceSerializer(read_only=True)
    # service=serializers.CharField(source='service.service_name')
    class Meta:
        model = Enquiry
        fields = ( 
                    'id', 
                    'service',
                    'phone',
                    'created_at',
                    'name'
        )

class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model=Inbox
        fields=(
            'id',
            'service',
            'email',
            'subject',
            'message'
        )

class PopularitySerializer(serializers.ModelSerializer):
    service = ServiceSerializer(source=Service)
    event_management_name=serializers.CharField(source='service.account__team_name',read_only=True)
    rating=serializers.FloatField(source='service.ratings__rating')
    class Meta:
        model = Popularity
        fields = (
                'id',
                'service',
                'event_management_name',
                'rating'              

                     )
 
        
    #     extra_kwargs = {
    #         'auto_id': {'read_only': True}
    #     }

    # def create(self, validated_data):
    #     popularity = Popularity.objects.create(
    #         **validated_data,
    #         auto_id=get_auto_id(Popularity),
    #         # creator = self.context['request'].user
    #     )
    #     return popularity

class ProfileSerializer(serializers.ModelSerializer):
    account_view = EventTeamSerializer(read_only=True, source='account')
    class Meta:
        model=ProfilePic
        fields=(
            'id',
            'account',
            'account_view',
            'profile_pic',
            'more_photos'

        )
        extra_kwargs = {
            'auto_id': {'read_only': True}
        }

    def create(self, validated_data):
        profile_pic = ProfilePic.objects.create(
            **validated_data,
            auto_id=get_auto_id(ProfilePic),
            # creator = self.context['request'].user
        )
        return profile_pic