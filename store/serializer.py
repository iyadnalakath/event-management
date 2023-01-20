from rest_framework import serializers
from .models import *
from main.functions import get_auto_id,password_generater
from projectaccount.serializer import RegisterEventTeamSerializer
from projectaccount.models import Account

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Area
        fields=[

        'id',
        'area'

        ]

        extra_kwargs={
            'auto_id':{'read_only':True}
        }

    def create(self, validated_data):
        area=Area.objects.create(
            **validated_data,
            auto_id=get_auto_id(Area),
            # creator = self.context['request'].user
        )
        return  area


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
        model=SubCatagory
        fields=[

            'id',
            'sub_catagory_name',
            # 'catagory',
            'image'
        ]

        extra_kwargs={
            'auto_id':{'read_only':True}
        }

    def create(self, validated_data):
        subcatagory=SubCatagory.objects.create(
            **validated_data,
            auto_id=get_auto_id(SubCatagory),
            # creator = self.context['request'].user
        )
        return  subcatagory


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
        model=Account
        fields=[
            'username',
            'team_name',
            'phone',
            'place',
            'work_time',
            'over_view',
            'address',
            'profile_pic'

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
    account_view=EventTeamSerializer(read_only=True,source='account')
    # account_view=serializers.CharField(source='account.username')
    sub_catagory_name=serializers.CharField(source='sub_catagory.sub_catagory_name',read_only=True)
    class Meta:
        model=Service
        fields=[

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
            # 'amount',
            # 'rating',
            # 'is_featured',
            # 'event_team',
            # 'team_name',
            # 'work_time',
            # 'place',
            # 'over_view'


        ]

        
        extra_kwargs={
            'auto_id':{'read_only':True},
            # 'team_name':{'read_only':True},
            # 'work_time':{'read_only':True},
            # 'place':{'read_only':True},
            # 'over_view':{'read_only':True},
                
        }

    # def create(self, validated_data):
    #     service=Service.objects.create(
    #         **validated_data,
    #         auto_id=get_auto_id(Service),
    #         # creator = self.context['request'].user
    #     )
    #     return  service
    
    def create(self, validated_data):
        service=Service.objects.create(
            **validated_data,
            auto_id=get_auto_id(Service),
                                
            # creator = self.context['request'].user
        )
        return  service
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

    

    
