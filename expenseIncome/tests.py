from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal
from .models import Expense


def get_auth_headers(user):
    refresh = RefreshToken.for_user(user)
    return {'HTTP_AUTHORIZATION': f'Bearer {str(refresh.access_token)}'}


class ExpenseAPITestCase(TestCase):
    def setUp(self):
        Expense.objects.all().delete()
        User.objects.all().delete()
        
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='pass1234')
        self.user2 = User.objects.create_user(username='user2', password='pass1234')
        self.superuser = User.objects.create_superuser(username='admin', password='admin1234')

    def tearDown(self):
        Expense.objects.all().delete()
        User.objects.all().delete()

    def create_expense(self, user, title):
        return Expense.objects.create(
            user=user,
            title=title,
            description='Test desc',
            amount=Decimal('100.00'),
            transaction_type='debit',
            tax=Decimal('10.00'),
            tax_type='flat'
        )

    def test_create_expense(self):
        url = reverse('expense-list')
        data = {
            'title': 'Dinner',
            'description': 'Dinner with friends',
            'amount': '150.00',
            'transaction_type': 'debit',
            'tax': '15.00',
            'tax_type': 'flat',
        }
        headers = get_auth_headers(self.user1)
        response = self.client.post(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.filter(user=self.user1).count(), 1)

    def test_list_own_expenses(self):
        self.create_expense(self.user1, 'Groceries')
        self.create_expense(self.user2, 'Books')

        url = reverse('expense-list')
        headers = get_auth_headers(self.user1)
        response = self.client.get(url, **headers)
        
        if isinstance(response.data, dict) and 'results' in response.data:
            results = response.data['results']
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]['title'], 'Groceries')
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['title'], 'Groceries')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_own_expense(self):
        expense = self.create_expense(self.user1, 'Groceries')
        url = reverse('expense-detail', kwargs={'pk': expense.pk})
        headers = get_auth_headers(self.user1)
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Groceries')

    def test_retrieve_other_user_expense_forbidden(self):
        expense = self.create_expense(self.user2, 'Books')
        url = reverse('expense-detail', kwargs={'pk': expense.pk})
        headers = get_auth_headers(self.user1)
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_own_expense(self):
        expense = self.create_expense(self.user1, 'Groceries')
        url = reverse('expense-detail', kwargs={'pk': expense.pk})
        data = {
            'title': 'Updated Groceries',
            'description': 'Updated description',
            'amount': '110.00',
            'transaction_type': 'debit',
            'tax': '12.00',
            'tax_type': 'flat',
        }
        headers = get_auth_headers(self.user1)
        response = self.client.put(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expense.refresh_from_db()
        self.assertEqual(expense.title, 'Updated Groceries')

    def test_update_other_user_expense_forbidden(self):
        expense = self.create_expense(self.user2, 'Books')
        url = reverse('expense-detail', kwargs={'pk': expense.pk})
        data = {
            'title': 'Hack Attempt',
            'description': 'Trying to update',
            'amount': '999.00',
            'transaction_type': 'debit',
            'tax': '0.00',
            'tax_type': 'flat',
        }
        headers = get_auth_headers(self.user1)
        response = self.client.put(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_own_expense(self):
        expense = self.create_expense(self.user1, 'Groceries')
        url = reverse('expense-detail', kwargs={'pk': expense.pk})
        headers = get_auth_headers(self.user1)
        response = self.client.delete(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Expense.objects.filter(pk=expense.pk).exists())

    def test_delete_other_user_expense_forbidden(self):
        expense = self.create_expense(self.user2, 'Books')
        url = reverse('expense-detail', kwargs={'pk': expense.pk})
        headers = get_auth_headers(self.user1)
        response = self.client.delete(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_superuser_can_access_all_expenses(self):
        self.create_expense(self.user1, 'Groceries')
        self.create_expense(self.user2, 'Books')

        url = reverse('expense-list')
        headers = get_auth_headers(self.superuser)
        response = self.client.get(url, **headers)
        
        if isinstance(response.data, dict) and 'results' in response.data:
            results = response.data['results']
            self.assertEqual(len(results), 2)
        else:
            self.assertEqual(len(response.data), 2)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)



'''
As i am  a bit new to writing test code i take help from the AI. 
'''