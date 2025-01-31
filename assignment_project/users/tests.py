from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Customer, Staff

# Create your tests here.

class UserViewsTestCase(TestCase):
    """
    Test case for the UserListView API endpoint.
    """

    def setUp(self):
        """
        Set up the environment for the test by creating test data and initializing the API client.
        """

        # Initialize the API client to simulate HTTP requests in the test
        self.client = APIClient()

        # Define the URL for the user list API endpoint
        self.user_list_url = reverse('api_user_list')

        # Creating test customers
        self.customer1 = Customer.objects.create(customer_id=1, first_name='Blue', last_name='Blue', active=True)
        self.customer2 = Customer.objects.create(customer_id=2, first_name='Green', last_name='Green', active=False)
        
        # Creating test staffs
        self.staff1 = Staff.objects.create(staff_id=1, first_name='Pink', last_name='Pink', active=True)
        self.staff2 = Staff.objects.create(staff_id=2, first_name='Lila', last_name='Lila', active=False)

    def test_user_list_view(self):
        """
        This test sends a GET request to the 'user_list_url' and verifies that the API response contains the correct 'active_users' and 'inactive_users' lists.   

        Asserts:
            - The response status code is HTTP 200 OK.
            - The response contains the keys 'active_users' and 'inactive_users'.
            - The 'active_users' list contains exactly 2 users (1 active customer and 1 active staff).
            - The 'inactive_users' list contains exactly 2 users (1 inactive customer and 1 inactive staff).
        """

        # Send a GET request to the user list endpoint
        response = self.client.get(self.user_list_url)

        # Assert the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Parse the response data
        data = response.json()

        # Assert the response contains active and inactive users
        self.assertIn('active_users', data)
        self.assertIn('inactive_users', data)

        # Assert that the active_users list contains exactly 2 users : 1 customer and 1 staff
        active_users = data['active_users']
        self.assertEqual(len(active_users), 2, "Active users list does not contain exactly 2 users.")
        self.assertTrue(any(user['first_name'] == 'Blue' for user in active_users))  # Active customer
        self.assertTrue(any(user['first_name'] == 'Pink' for user in active_users))  # Active staff

        # Assert that the inactive_users list contains exactly 2 users : 1 customer and 1 staff
        inactive_users = data['inactive_users']
        self.assertEqual(len(inactive_users), 2, "Inactive users list does not contain exactly 2 users.")
        self.assertTrue(any(user['first_name'] == 'Green' for user in inactive_users))  # Inactive customer
        self.assertTrue(any(user['first_name'] == 'Lila' for user in inactive_users))  # Inactive staff
    
class UpdateUserStatusViewTests(TestCase):
    """
    Test case for the UpdateUserStatusView API endpoint.
    """

    def setUp(self):
        """
        Set up the environment for the test by creating test data and initializing the API client.
        """

        self.client = APIClient()
        self.update_status_url = reverse('api_update_status')

        self.customer = Customer.objects.create(customer_id=3, first_name='Red', last_name='Customer', active=True)
        self.staff = Staff.objects.create(staff_id=3, first_name='Yellow', last_name='Staff', active=False)
    
    def test_update_customer_status(self):
        """
        Test case to update the status of an active customer to inactive.

        Asserts:
            - An active customer exists for the update.
            - The PATCH request is processed successfully (status code 200).
            - The customer's status is correctly updated in the database.
        """

        customer = Customer.objects.filter(active=True).first()
        self.assertIsNotNone(customer, "No active customer found for testing.")

        # Prepare the data payload for the PATCH request; updating the customer to set 'active' to False
        data = {
            'id': customer.customer_id,
            'type': 'customer',
            'active': False
        }

        # Send a PATCH request to the update status endpoint with the data
        response = self.client.patch(self.update_status_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the customer object from the database to get the updated status
        customer.refresh_from_db()

        # Assert the customer's status was updated to inactive (False)
        self.assertFalse(customer.active)

    def test_update_staff_status(self):
        """
        Test case to update the status of an inactive staff to active.

        Asserts:
            - An inactive staff exists for the update.
            - The PATCH request is processed successfully (status code 200).
            - The staff's status is correctly updated in the database.
        """
        
        staff = Staff.objects.filter(active=False).first()
        self.assertIsNotNone(staff, "No inactive staff found for testing.")

        # Prepare the data payload for the PATCH request; updating the staff to set 'active' to True
        data = {
            'id': staff.staff_id,
            'type': 'staff',
            'active': True
        }

        response = self.client.patch(self.update_status_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        staff.refresh_from_db()

        # Assert the staff's status was updated to active (True)
        self.assertTrue(staff.active)