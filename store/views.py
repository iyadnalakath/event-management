from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializer import *
from .permission import IsAdmin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.core.exceptions import PermissionDenied
from .mixin import AdminOnlyMixin
from django.shortcuts import get_object_or_404
from django.db.models import Count

# from django_filters.rest_framework import DjangoFilterBackend,OrderingFilter
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from django.db.models import OuterRef, Subquery, Max, F
from rest_framework.views import APIView


# Create your views here.
class AreaViewSet(ModelViewSet):
    queryset = Area.objects.all().filter(is_deleted=False)
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = AreaSerializer(data=request.data)
        if serializer.is_valid():
            # print (self.request.user.role
            #     )
            if self.request.user.role == "admin":
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        area = self.get_object()
        if request.user.role == "admin":
            area.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied("You are not allowed to delete this object.")

    def update(self, request, *args, **kwargs):
        area = self.get_object()
        serializer = AreaSerializer(area, data=request.data)
        if serializer.is_valid():
            if request.user.role == "admin":
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
    queryset = SubCatagory.objects.all().filter(is_deleted=False)
    serializer_class = SubCatagorySerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = SubCatagorySerializer(data=request.data)
        if serializer.is_valid():
            # print (self.request.user.role
            #     )
            if self.request.user.role == "admin":
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        sub_catagory = self.get_object()
        if request.user.role == "admin":
            sub_catagory.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied("You are not allowed to delete this object.")

    def update(self, request, *args, **kwargs):
        sub_catagory = self.get_object()
        serializer = SubCatagorySerializer(sub_catagory, data=request.data)
        if serializer.is_valid():
            if request.user.role == "admin":
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
    queryset = (
        Service.objects.select_related("sub_catagory")
        .annotate(rating=Avg("ratings__rating"))
        .filter(is_deleted=False)
    )
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["account__district"]
    ordering_fields = ["rating", "amount"]
    search_fields = ["service_name"]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["account"] = self.request.user.id
        # data["profile"]= data.prefetch_related(
        #     'profiles').filter(photos__account_id=F('account_id'))

        # Check if the user is an event_management
        if self.request.user.role == "event_management":
            sub_catagory_id = data.get("sub_catagory")
            account_id = self.request.user.id

            # Check if a service with this sub_catagory and account already exists
            if Service.objects.filter(
                sub_catagory=sub_catagory_id, account_id=account_id
            ).exists():
                return Response(
                    {
                        "error": "You can only create one service in one sub_catagory, if you want add new serice or details you can update in your current service section or delete your current service and add new service details"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = ServiceSerializer(data=data)

        if serializer.is_valid():
            if self.request.user.role in ["admin", "event_management"]:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
        data["account"]=self.request.user.id
        # Check if the current user created this service
        if instance.account != self.request.user:
            raise PermissionDenied("You are not allowed to update this object.")
        else:
            serializer = self.get_serializer(instance, data, partial=kwargs.get('partial', False))
            serializer.is_valid(raise_exception=True)

            serializer.save()
            return Response(serializer.data)

    # def update(self, request, *args, **kwargs):
    #     service = self.get_object()
    #     data = request.data.copy()
    #     data["account"] = self.request.user.id
    #     # data["sub_catagory"] = data.get("sub_catagory_id")
    #     # data[""]
    #     serializer = ServiceSerializer(service, data)
    #     if serializer.is_valid():
    #         if request.user.role == "event_management":
    #             if service.account.id == self.request.user.id:
    #                 serializer.save()
    #                 return Response(serializer.data)
    #             else:
    #                 raise PermissionDenied("You are not allowed to update this object.")
    #         else:
    #             raise PermissionDenied("only autherised team allowed to update it")
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def create(self, request, *args, **kwargs):

    #     data = request.data.copy()
    #     # print (self.request.user.role)
    #     data["account"]=self.request.user.id

    #     serializer = ServiceSerializer(data=data)

    #     if serializer.is_valid():
    #         # print (self.request.user.role)
    #         if self.request.user.role in ['admin','event_management']:

    #             # serializer.save(event_team=self.request.user)
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         else:
    #             raise PermissionDenied("You are not allowed to create this object.")
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(queryset)
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)

        # if self.request.user.role in ['admin', 'customer'] and request.GET.get('sub_catagory'):
        if self.request.GET.get("sub_catagory"):
            sub_catagory = self.request.GET.get("sub_catagory")
            queryset = queryset.filter(sub_catagory=sub_catagory)
            # subquery = Service.objects.filter(account=OuterRef('account_id'))
            # queryset=queryset.filter(sub_catagory=sub_catagory)
            serializer = ServiceSerializer(queryset, many=True)
            # return super().list(request, *args, **kwargs)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif self.request.user.role == "event_management":
            queryset = queryset.filter(account=self.request.user)
            serializer = ServiceSerializer(queryset, many=True)
            return Response(serializer.data)
        elif self.request.user.role in ["admin", "customer"]:
            return super().list(request, *args, **kwargs)

        else:
            raise PermissionDenied("You are not allowed to retrieve this object.")

    # def list(self, request, *args, **kwargs):
    #     # Get the base queryset and filter it with the filter_backends
    #     queryset = self.filter_queryset(self.get_queryset())

    #     # Get the sub-category ID from the query string, if it exists
    #     sub_category_id = self.request.GET.get('sub_catagory')
    #     if sub_category_id:
    #         # If a sub-category ID is specified, filter the queryset to include only services in that sub-category
    #         queryset = queryset.filter(sub_catagory=sub_category_id)
    #     elif self.request.user.role == 'event_management':
    #         # If the user is an event manager, filter the queryset to include only services associated with their account
    #         queryset = queryset.filter(account=self.request.user)
    #     else:
    #         # Otherwise, use the default behavior of the superclass (list all services)
    #         return super().list(request, *args, **kwargs)

    #     # Use a subquery to group the services by event team and select the maximum rating for each group
    #     subquery = Service.objects.filter(
    #         account=OuterRef('account_id')
    #     ).values('account_id').annotate(
    #         max_rating=Max('ratings')
    #     ).values('max_rating')

    #     # Filter the queryset to include only the services with the maximum rating for each event team
    #     queryset = queryset.filter(
    #         rating__in=Subquery(subquery)
    #     )

    #     # Serialize the filtered queryset and return it in a Response object
    #     serializer = ServiceSerializer(queryset, many=True)
    #     return Response(serializer.data)

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

    # def retrieve(self, request, service_id=None,*args, **kwargs):
    #     data = request.data.copy()
    #     data["service"] = kwargs["service_id"]
    #     service = Service.objects.get(id=kwargs["service_id"])
    #     if request.user.role == 'event_management':
    #         if service.account.id == self.request.user.id:

    #             queryset = self.get_queryset()
    #             serializer = EnquirySerializer(queryset, many=True)
    #             return Response(serializer.data)
    #     # elif self.request.user:
    #     #     return super().list(request, *args, **kwargs)
    #     else:
    #         raise PermissionDenied("You are not the owner of this service.")

    def destroy(self, request, *args, **kwargs):
        service = self.get_object()
        if request.user.role == "admin":
            service.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.user.role == "event_management":
            if service.account.id == self.request.user.id:
                service.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You are not allowed to delete this object.")
        else:
            raise PermissionDenied("You are not allowed to delete this object.")


class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

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
        data["customer"] = self.request.user.id
        serializer = RatingSerializer(data=data)

        if serializer.is_valid():
            if self.request.user.role in ["admin", "customer"]:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        rating = self.get_object()
        if request.user.role == "admin":
            rating.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.user.role == "customer":
            if rating.customer.id == self.request.user.id:
                rating.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You are not allowed to delete this object.")
        else:
            raise PermissionDenied("You are not allowed to delete this object.")

    def update(self, request, *args, **kwargs):
        rating = self.get_object()
        serializer = RatingSerializer(rating, data=request.data)
        if serializer.is_valid():
            if request.user.role == "customer":
                if rating.customer.id == self.request.user.id:
                    serializer.save()
                    return Response(serializer.data)
                else:
                    raise PermissionDenied("You are not allowed to update this object.")
            else:
                raise PermissionDenied("only autherised team allowed to update it")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            # print (self.request.user.role
            #     )
            if self.request.user.role == "admin":
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by("auto_id")
        if self.request.user.role in ["admin", "event_management"]:
            serializer = NotificationSerializer(queryset, many=True)
            # return super().list(request, *args, **kwargs)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            raise PermissionDenied("You are not allowed to retrieve this object.")

    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        serializer = NotificationSerializer(notification, data=request.data)
        if serializer.is_valid():
            if request.user.role == "admin":
                serializer.save()
                return Response(serializer.data)
            else:
                raise PermissionDenied("You are not allowed to update this object.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    def create(self, request, *args, **kwargs):
        serializer = EnquirySerializer(data=request.data)
        if serializer.is_valid():
            # print (self.request.user.role
            #     )
            if self.request.user.role == "customer":
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # data = request.data.copy()
        # data["service"] = kwargs["service"]
        # service = Service.objects.get(pk=service_id)
        # service = get_object_or_404(Service, pk=service)
        # enquiry=get_object_or_404(Enquiry,pk=enquiry_id)

        if request.user.role == "event_management":
            # if Enquiry.service.account.id == self.request.user.id:

            queryset = queryset.filter(service__account__id=self.request.user.id)
            serializer = EnquirySerializer(queryset, many=True)
            return Response(serializer.data)
        # else:
        #     raise PermissionDenied("You are not the owner of this service.")

        else:
            raise PermissionDenied("You are not the owner of this service.")

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        enquiry = get_object_or_404(queryset, pk=pk)

        if (
            request.user.role == "event_management"
            and enquiry.service.account.id == self.request.user.id
        ):
            serializer = EnquirySerializer(enquiry)
            return Response(serializer.data)
        # elif request.user.role == 'customer' and inbox.user == self.request.user:
        #     serializer = InboxSerializer(inbox)
        #     return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to access this object.")

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


class InboxViewSet(ModelViewSet):
    queryset = Inbox.objects.all()
    serializer_class = InboxSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = InboxSerializer(data=request.data)
        if serializer.is_valid():
            # print (self.request.user.role
            #     )
            if self.request.user.role == "customer":
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if request.user.role == "event_management":
            # if Enquiry.service.account.id == self.request.user.id:

            queryset = queryset.filter(service__account__id=self.request.user.id)
            serializer = InboxSerializer(queryset, many=True)
            return Response(serializer.data)
            # else:
            #     raise PermissionDenied("You are not the owner of this service.")

        else:
            raise PermissionDenied("You are not the owner of this service.")

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        inbox = get_object_or_404(queryset, pk=pk)

        if (
            request.user.role == "event_management"
            and inbox.service.account.id == self.request.user.id
        ):
            serializer = InboxSerializer(inbox)
            return Response(serializer.data)
        # elif request.user.role == 'customer' and inbox.user == self.request.user:
        #     serializer = InboxSerializer(inbox)
        #     return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to access this object.")


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
    queryset = (
        Service.objects.all()
        .annotate(rating=Avg("ratings__rating"))
        .order_by("-rating")
        .filter(is_deleted=False)
    )
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

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
    queryset = ProfilePic.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["account"] = self.request.user.id

        serializer = ProfileSerializer(data=data)

        if serializer.is_valid():
            if self.request.user.role in ["admin", "event_management"]:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if self.request.user.role in ["admin", "customer"]:
            serializer = ProfileSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif self.request.user.role == "event_management":
            queryset = queryset.filter(account=self.request.user)
            serializer = ProfileSerializer(queryset, many=True,context={'request':self.request})
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to retrieve this object.")

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        data = request.data.copy()
        data["account"] = self.request.user.id

        serializer = ProfileSerializer(profile, data)
        if serializer.is_valid():
            if request.user.role == "event_management":
                if profile.account.id == self.request.user.id:
                    serializer.save()
                    return Response(serializer.data)
                else:
                    raise PermissionDenied("You are not allowed to update this object.")
            else:
                raise PermissionDenied("only autherised team allowed to update it")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()
        if request.user.role == "admin":
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.user.role == "event_management":
            if profile.account.id == self.request.user.id:
                profile.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You are not allowed to delete this object.")
        else:
            raise PermissionDenied("You are not allowed to delete this object.")







class TeamProfileViewSet(ModelViewSet):
    queryset = TeamProfile.objects.all()
    serializer_class = TeamProfileSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["account"] = self.request.user.id

        # serializer = TeamProfileSerializer(data=data)

        existing_profile =TeamProfile.objects.first()

        # If the user already has a profile, update it instead of creating a new one
        if existing_profile:
            serializer = TeamProfileSerializer(existing_profile, data=data)
        else:
            serializer = TeamProfileSerializer(data=data)

        if serializer.is_valid():
            if self.request.user.role in ["admin", "event_management"]:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if self.request.user.role in ["admin", "customer"]:
            serializer = TeamProfileSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif self.request.user.role == "event_management":
            queryset = queryset.filter(account=self.request.user)
            serializer = TeamProfileSerializer(queryset, many=True,context={'request':self.request})
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to retrieve this object.")

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        data = request.data.copy()
        data["account"] = self.request.user.id

        serializer = TeamProfileSerializer(profile, data)
        if serializer.is_valid():
            if request.user.role == "event_management":
                if profile.account.id == self.request.user.id:
                    serializer.save()
                    return Response(serializer.data)
                else:
                    raise PermissionDenied("You are not allowed to update this object.")
            else:
                raise PermissionDenied("only autherised team allowed to update it")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()
        if request.user.role == "admin":
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.user.role == "event_management":
            if profile.account.id == self.request.user.id:
                profile.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You are not allowed to delete this object.")
        else:
            raise PermissionDenied("You are not allowed to delete this object.")
