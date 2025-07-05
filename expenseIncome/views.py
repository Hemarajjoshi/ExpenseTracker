from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status


from .models import Expense 
from .serializers import ExpenseSerializer
from .permissions import IsOwnerOrIsAdmin
from .pagination import ExpensePagination


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrIsAdmin]
    pagination_class = ExpensePagination
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Expense.objects.all().order_by('-created_at')
        else:
            return Expense.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response({
            'message': "Record Created Successfully"
        }, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': "Record Deleted Successfully"
        }, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        partial = False
        instance = self.get_object()
        serializer = self.get_serializer(
                instance, data=request.data, partial=partial
        )
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response({
                'message': "Record Updated Successfully"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def partial_update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
            )
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response({
                'message': "Record Updated Successfully"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
