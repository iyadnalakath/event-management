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


# Create your views here.
class AreaViewSet(ModelViewSet):
    queryset=Area.objects.all()
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
    queryset=SubCatagory.objects.all()
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
    queryset=Service.objects.select_related('sub_catagory').all()
    serializer_class=ServiceSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # print (self.request.user.role)
        data["account"]=self.request.user.id
        
        serializer = ServiceSerializer(data=data)
        
        if serializer.is_valid():
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

    def list(self, request, *args, **kwargs):
        if self.request.user.role in ['admin', 'customer']:
            return super().list(request, *args, **kwargs)
        elif self.request.user.role == 'event_management':
            queryset = Service.objects.filter(account=self.request.user)
            serializer = ServiceSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to retrieve this object.")

        

        

