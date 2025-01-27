from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customer, Staff
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class UserListView(APIView):
    """
    API view to retrieve a list of active and inactive users.
    Combines data from both 'Customer' and 'Staff' models to produce two categorized lists, active users and inactive users.

    """
    def get(self, request):
        """
        Handles GET requests to retrieve lists of active and inactive users.

        Queries the 'Customer' and 'Staff' models for active and inactive users to fetch users categorized by their active status.

        Returns a JSON object with two keys as Response:
            - 'active users': List of active users, including both customers and staffs, with unified fields ('id', 'type', etc.).
            - 'inactive users': List of inactive users, formatted similarly to active users.

        """
        # Querying the database for active and inactive users (customer and staff), sorting them by the last update timestamp.
        active_customers = Customer.objects.filter(active=True).order_by('-last_update').values('customer_id', 'first_name', 'last_name', 'active','last_update')
        inactive_customers = Customer.objects.filter(active=False).order_by('-last_update').values('customer_id', 'first_name', 'last_name', 'active','last_update')
        active_staff = Staff.objects.filter(active=True).order_by('-last_update').values('staff_id', 'first_name', 'last_name', 'active','last_update')
        inactive_staff = Staff.objects.filter(active=False).order_by('-last_update').values('staff_id', 'first_name', 'last_name', 'active','last_update')

        # Reformat the data for users (active/inactive customers/staff) to unify keys (id, type)
        for user in active_customers:
            user['id'] = user.pop('customer_id', None)
            user['type'] = 'customer'
        for user in inactive_customers:
            user['id'] = user.pop('customer_id', None)
            user['type'] = 'customer'
        for user in active_staff:
            user['id'] = user.pop('staff_id', None)
            user['type'] = 'staff'
        for user in inactive_staff:
            user['id'] = user.pop('staff_id', None)
            user['type'] = 'staff'
        
        return Response({
            'active_users': list(active_customers) + list(active_staff),
            'inactive_users': list(inactive_customers) + list(inactive_staff),
        })

# View to handle updates to user statuses
@method_decorator(csrf_exempt, name='dispatch')  # For testing purposes
class UpdateUserStatusView(APIView):
    """
    API view to update the 'active' status of a user (customer or staff).
    This view is used by the drag-and-drop functionality in the frontend (user_list.html) to change the user's status dynamically.
    
    """
    def patch(self, request):
        """
        Handles PATCH requests to update a user's active status.
        Args: 
            request(HttpRequest) contains
                - 'id' (int): The user's ID.
                - 'type' (str): The user's type (customer or staff)
                - 'active' (bool): The new status (True for active, False for inactive)
        Returns:
            Response: A JSON response indicating success or error.

        """
        user_id = request.data.get('id')  
        user_type = request.data.get('type')  
        active = request.data.get('active')  

        try:
            # Identify the user type and retrieving corresponding user record
            if user_type == 'customer':
                user = Customer.objects.get(customer_id=user_id)
            elif user_type == 'staff':
                user = Staff.objects.get(staff_id=user_id)
            else:
                return Response({'error': 'Invalid user type'}, status=400)

            # Update the user's active status field and save the changes to the database.
            user.active = active  
            user.save()
            return Response({'message': f'{user_type} status updated successfully'}, status=200)

        except (Customer.DoesNotExist, Staff.DoesNotExist):
            return Response({'error': f'{user_type} not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)