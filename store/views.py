from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializer import *
from .permission import IsAdmin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny
from django.core.exceptions import PermissionDenied
from .mixin import AdminOnlyMixin
from django.shortcuts import get_object_or_404
from django.db.models import Count
# from django_filters.rest_framework import DjangoFilterBackend,OrderingFilter
from rest_framework.filters import OrderingFilter,SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics



# Create your views here.
class AreaViewSet(ModelViewSet):
    queryset=Area.objects.all().filter(is_deleted=False)
    serializer_class=AreaSerializer
    permission_classes=[IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = AreaSerializer(data=request.data)
        if serializer.is_valid():
            # print (self.request.user.role
            #     )
            if self.request.user.role == 'admin':
                
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        area = self.get_object()
        if request.user.role == 'admin':
            area.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied("You are not allowed to delete this object.")

    def update(self, request, *args, **kwargs):
        area = self.get_object()
        serializer = AreaSerializer(area, data=request.data)
        if serializer.is_valid():
            if request.user.role == 'admin':
                serializer.save()
                return Response(serializer.data)
            else:
                raise PermissionDenied("You are not allowed to update this object.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CatagoryViewSet(ModelViewSet):
#     queryset=Catagory.objects.all()
#     serializer_class=CatagorySerializer
    
#     permission_classes=[AllowAny]
        
#     def create(self, request, *args, **kwargs):
#         serializer = CatagorySerializer(data=request.data)
#         if serializer.is_valid():
#             # print (self.request.user.role
#             #     )
#             if self.request.user.role == 'admin':
                
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 raise PermissionDenied("You are not allowed to create this object.")
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     def destroy(self, request, *args, **kwargs):
#         catagory = self.get_object()
#         if request.user.role == 'admin':
#             catagory.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             raise PermissionDenied("You are not allowed to delete this object.")

#     def update(self, request, *args, **kwargs):
#         catagory = self.get_object()
#         serializer = CatagorySerializer(catagory, data=request.data)
#         if serializer.is_valid():
#             if request.user.role == 'admin':
#                 serializer.save()
#                 return Response(serializer.data)
#             else:
#                 raise PermissionDenied("You are not allowed to update this object.")
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubCatagoryViewSet(ModelViewSet):
    queryset=SubCatagory.objects.all().filter(is_deleted=False)
    serializer_class=SubCatagorySerializer
    permission_classes=[AllowAny]

        
    def create(self, request, *args, **kwargs):
        serializer = SubCatagorySerializer(data=request.data)
        if serializer.is_valid():
            # print (self.request.user.role
            #     )
            if self.request.user.role == 'admin':
                
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        sub_catagory = self.get_object()
        if request.user.role == 'admin':
            sub_catagory.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied("You are not allowed to delete this object.")

    def update(self, request, *args, **kwargs):
        sub_catagory = self.get_object()
        serializer = SubCatagorySerializer(sub_catagory, data=request.data)
        if serializer.is_valid():
            if request.user.role == 'admin':
                serializer.save()
                return Response(serializer.data)
            else:
                raise PermissionDenied("You are not allowed to update this object.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class EventTeamViewSet(ModelViewSet):
#     queryset=EventTeam.objects.all()
#     serializer_class=EventTeamSerializer
#     permission_classes=[AllowAny]

#     def create(self, request, *args, **kwargs):
#         serializer = EventTeamSerializer(data=request.data)
#         if serializer.is_valid():
#             print (self.request.user.role
#                 )
#             if self.request.user.role in ['admin','event_management']:
                
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 raise PermissionDenied("You are not allowed to create this object.")
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
        

class ServiceViewSet(ModelViewSet):
    queryset=Service.objects.select_related('sub_catagory').annotate(rating=Avg('ratings__rating')).filter(is_deleted=False)
    serializer_class=ServiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filterset_fields=['account__district']
    ordering_fields=['rating','amount']
    search_fields = ['service_name']



    def create(self, request, *args, **kwargs):

        
   
        data = request.data.copy()
        # print (self.request.user.role)
        data["account"]=self.request.user.id
        
        serializer = ServiceSerializer(data=data)
        
        if serializer.is_valid():
            print(data)
            print(data)
            # print (self.request.user.role)
            if self.request.user.role in ['admin','event_management']:
                
                # serializer.save(event_team=self.request.user)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def create(self, request, *args, **kwargs):
    #     data = request.data.copy()
    #     data["account"]=self.request.user
    #     serializer = ServiceSerializer(data=data)
    #     if self.request.user.role in ['admin','event_management']:
            
    #         # serializer.save(event_team=self.request.user)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         raise PermissionDenied("You are not allowed to create this object.")

    # def list(self, request, *args, **kwargs):
    #     if self.request.user.role in ['admin', 'customer']:
    #         return super().list(request, *args, **kwargs)
    #     elif self.request.user.role == 'event_management':
    #         queryset = Service.objects.filter(account=self.request.user)
    #         serializer = ServiceSerializer(queryset, many=True)
    #         return Response(serializer.data)
    #     else:
    #         raise PermissionDenied("You are not allowed to retrieve this object.")
        
    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(queryset)
        queryset=self.get_queryset()
        queryset = self.filter_queryset(queryset)
        
        if self.request.user.role in ['admin', 'customer'] and request.GET.get('sub_catagory'):
        # if self.request.user.role in ['admin', 'customer'] and request.GET.get in ['sub_catagory' , '']:
            sub_catagory=self.request.GET.get('sub_catagory')
            queryset=queryset.filter(sub_catagory=sub_catagory)
            # queryset=queryset.filter(sub_catagory=sub_catagory)
            serializer=ServiceSerializer(queryset,many=True)
            # return super().list(request, *args, **kwargs)
            return Response (serializer.data,status=status.HTTP_200_OK)
        elif self.request.user.role == 'event_management':
            queryset = queryset.filter(account=self.request.user)
            serializer = ServiceSerializer(queryset, many=True)
            return Response(serializer.data)
        elif self.request.user.role in ['admin', 'customer']:
            return super().list(request, *args, **kwargs)

        else:
            raise PermissionDenied("You are not allowed to retrieve this object.")

        
    
        
    # def retrieve(self, request, *args, **kwargs):
    #     queryset=self.get_queryset()
    #     if self.request.user.role in ['admin','customer']:
    #         serializer=ServiceSerializer(queryset,many=True)
    #         return Response (serializer.data,status=status.HTTP_200_OK)
    #     elif self.request.user.role == 'event_management':
    #         queryset = Service.objects.filter(account=self.request.user)
    #         serializer = ServiceSerializer(queryset, many=True)
    #         return Response(serializer.data)
    #     elif self.request.user.role == 'admin':
    #         return super().list(request, *args, **kwargs)

    #     else:
    #         raise PermissionDenied("You are not allowed to retrieve this object.")

        
    def retrieve(self, request, service_id=None,*args, **kwargs):
        data = request.data.copy()
        data["service"] = kwargs["service_id"]
        service = Service.objects.get(id=kwargs["service_id"])
        if request.user.role == 'event_management':
            if service.account.id == self.request.user.id:
                        
                queryset = self.get_queryset()
                serializer = EnquirySerializer(queryset, many=True)
                return Response(serializer.data)
        else:
            raise PermissionDenied("You are not the owner of this service.")
        

class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes=[IsAuthenticated]
    
    # def create(self, request, *args, **kwargs):
        
    #     data = request.data.copy()
    #     data["name"]=self.request.user.username
        

    #     serializer = RatingSerializer(data=data)

    #     if serializer.is_valid():
    #         if self.request.user.role in ['admin','customer']:
    #             serializer.save(name=self.request.user.username)
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         else:
    #             raise PermissionDenied("You are not allowed to create this object.")
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def create(self, request, *args, **kwargs):
    #     data = request.data.copy()
    #     data["name"] = self.request.user.username

    #     serializer = RatingSerializer(data=data)

    #     if serializer.is_valid():
    #         if self.request.user.role in ['admin','customer']:
    #             serializer.save(name=self.request.user.username)
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         else:
    #             raise PermissionDenied("You are not allowed to create this object.")
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def create(self, request, *args, **kwargs):
    #     data = request.data.copy()
    #     data["name"] = self.request.user.username

    #     serializer = RatingSerializer(data=data)

    #     if serializer.is_valid():
    #         if self.request.user.role in ['admin','customer']:
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         else:
    #             raise PermissionDenied("You are not allowed to create this object.")
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        serializer = RatingSerializer(data=data)

        if serializer.is_valid():
            if self.request.user.role in ['admin','customer']:
                serializer.save(name=self.request.user.username)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      



class NotificationViewSet(ModelViewSet):
    queryset=Notification.objects.all()
    serializer_class=NotificationSerializer
    permission_classes=[IsAuthenticated]

        
    def create(self, request, *args, **kwargs):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            # print (self.request.user.role
            #     )
            if self.request.user.role == 'admin':
                
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().order_by('auto_id')
        if self.request.user.role in ['admin', 'event_management'] :
            serializer=NotificationSerializer(queryset,many=True)
            # return super().list(request, *args, **kwargs)
            return Response (serializer.data,status=status.HTTP_200_OK)

        else:
            raise PermissionDenied("You are not allowed to retrieve this object.")
        

class EnquiryViewSet(ModelViewSet):
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


    
    # def get_queryset(self):
    #     if self.request.user.is_authenticated:
    #         return Enquiry.objects.filter(sent_by=self.request.user) | Enquiry.objects.filter(received_by=self.request.user)
    #     else:
    #         return Enquiry.objects.none()

    # def create(self, request, *args, **kwargs):
    #     data = request.data.copy()
    #     data["service"] = kwargs["service_id"]
    #     service = Service.objects.get(id=kwargs["service_id"])
    #     if service.account.id == self.request.user.id:
    #         serializer = EnquirySerializer(data=data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         raise PermissionDenied("You are not the owner of this service.")
        
    def list(self, request,*args, **kwargs):
        queryset=self.get_queryset()
        
        # data = request.data.copy()
        # data["service"] = kwargs["service"]
        # service = Service.objects.get(pk=service_id)
        # service = get_object_or_404(Service, pk=service)
        # enquiry=get_object_or_404(Enquiry,pk=enquiry_id)
        
        if request.user.role == 'event_management':
            # if Enquiry.service.account.id == self.request.user.id:
                
                queryset = queryset.filter(service__account__id = self.request.user.id)
                serializer = EnquirySerializer(queryset, many=True)
                return Response(serializer.data)
            # else:
            #     raise PermissionDenied("You are not the owner of this service.")
    
        else:
            raise PermissionDenied("You are not the owner of this service.")



    # def list(self, request, enquiry_id=None, *args, **kwargs):
    #     # check if enquiry_id is provided
    #     if enquiry_id is None:
    #         raise ValueError("enquiry_id is required")
    #     # get enquiry object
    #     enquiry = get_object_or_404(Enquiry, pk=enquiry_id)
    #     if request.user.role == 'event_management':
    #         if enquiry.service.account.id == self.request.user.id:
    #             queryset = self.get_queryset().filter(pk=enquiry_id)
    #             serializer = EnquirySerializer(queryset, many=True)
    #             return Response(serializer.data)
    #         else:
    #             raise PermissionDenied("You are not the owner of this service.")
    
    #     else:
    #         raise PermissionDenied("You are not the owner of this service.")


    # def retrieve(self, request, pk=None, service_id=None):
    #     queryset = self.get_queryset()
    #     enquiry = get_object_or_404(queryset, pk=pk)
    #     serializer = EnquirySerializer(enquiry)
    #     return Response(serializer.data)

class InboxViewSet(ModelViewSet):
    queryset=Inbox.objects.all()
    serializer_class=InboxSerializer
    permission_classes=[IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = InboxSerializer(data=request.data)
        if serializer.is_valid():
            # print (self.request.user.role
            #     )
            if self.request.user.role == 'customer':
                
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request,*args, **kwargs):
        queryset=self.get_queryset()

        if request.user.role == 'event_management':
            # if Enquiry.service.account.id == self.request.user.id:
                
                queryset = queryset.filter(service__account__id = self.request.user.id)
                serializer = EnquirySerializer(queryset, many=True)
                return Response(serializer.data)
            # else:
            #     raise PermissionDenied("You are not the owner of this service.")
        
    
        else:
            raise PermissionDenied("You are not the owner of this service.")
        


# class PopularityViewSet(ModelViewSet):
#     serializer_class = PopularitySerializer

#     # def get_queryset(self):
#     #     popularity = Popularity.objects.all()
#     #     popularity = popularity.annotate(enquiry_count=Count('enquiries'))
#     #     popularity = popularity.order_by('-popularity')
#     #     return popularity

#     def get_queryset(self):
#         eventment_teams = Account.objects.filter(role='event_management')
#         popularity_list = []
#         for eventment_team in eventment_teams:
#             popularity_obj = Popularity()
#             popularity_obj.eventment_team = eventment_team
#             popularity_obj.calculate_popularity()
#             popularity_list.append(popularity_obj)
#         return popularity_list


class PopularityViewSetList(generics.ListAPIView):
    queryset = Service.objects.all().annotate(rating=Avg('ratings__rating')).order_by('-rating').filter(is_deleted=False)
    serializer_class = ServiceSerializer
    permission_classes=[IsAuthenticated]
  




    # def list(self, request, *args, **kwargs):
    #     queryset=self.get_queryset()
    #     if self.request.user.role == 'admin':
    #         serializer=ServiceSerializer(queryset,many=True)
    #         # return super().list(request, *args, **kwargs)
    #         return Response (serializer.data,status=status.HTTP_200_OK)

    #     else:
    #         raise PermissionDenied("You are not allowed to retrieve this object.")
    
# class PopularityViewSet(ModelViewSet):
#     queryset = Popularity.objects.all()
#     serializer_class = PopularitySerializer

    # def get_queryset(self):
    #     queryset = self.queryset
    #     queryset = queryset.annotate(enquiry_count=Count('eventment_team__enquiries'))
    #     queryset = queryset.order_by('-popularity')
    #     return queryset

    # def perform_create(self, serializer):
    #     serializer.save(enquiry_count=self.request.data.get('enquiry_count', 0))
    #     serializer.instance.calculate_popularity()

        
    # def calculate_popularity(self):
    #         total_enquiries = Enquiry.objects.count()
    #         if total_enquiries > 0:
    #             self.popularity = (self.enquiry_count / total_enquiries) * 100
    #         else:
    #             self.popularity = 0.0
    #         self.save()


    # def get_queryset(self):
    #     popularity = Popularity.objects.all()
    #     popularity = popularity.annotate(enquiry_count=Count('eventment_team__enquiries'))
    #     popularity = popularity.order_by('-popularity')
    #     return popularity


    
class ProfileViewSet(ModelViewSet):
    queryset=ProfilePic.objects.all()
    serializer_class=ProfileSerializer
    permission_classes=[IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["account"]=self.request.user.id
        serializer = ProfileSerializer(data=data)

        if serializer.is_valid():
            if self.request.user.role in ['admin','event_management']:
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        if self.request.user.role in ['admin','customer']:
            serializer=ProfileSerializer(queryset,many=True)
            return Response (serializer.data,status=status.HTTP_200_OK)
        elif self.request.user.role == 'event_management':
            queryset=queryset.filter(account=self.request.user)
            serializer=ProfileSerializer(queryset,many=True)
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to retrieve this object.")      
