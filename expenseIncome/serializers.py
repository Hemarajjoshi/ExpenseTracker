from rest_framework import serializers
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Expense
        fields = ['id', 'title', 'description', 'amount', 'transaction_type', 
                  'tax', 'tax_type', 'total', 'created_at', 'updated_at', 'user']                           # Could have used fields = '__all__' but total was appering at first which was not looking good
        read_only_fields = ['created_at', 'updated_at', 'total']

    def get_total(self, obj):
        return obj.total
    


    

