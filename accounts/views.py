from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializers import *
import logging
from logs.models import FrontendLog


logger = logging.getLogger('accounts')  

# Create user.
class RegisterView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request, *args, **kwargs):
        """Create a new user"""
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user, tokens = serializer.save()  # Create user and generate tokens
                user.is_active = True  # Ensure the user is active

                FrontendLog.objects.create(
                    username = user.username,
                    action = 'تسجيل ',
                    message = f"تم انشاء حساب جديد ل {user.username}",
            )

            
                logger.info(f"New user registered: {user.email} ({user.username})")

                return Response({
                    "data": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "full_name": user.full_name,
                        "phone_number": user.phone_number,
                        "role": user.role,
                        "is_active": user.is_active,
                        "refresh_token": tokens["refresh"],
                        "access_token": tokens["access"],
                    }
                }, status=status.HTTP_201_CREATED)

            logger.error(f"User registration failed: {serializer.errors}")
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error during user creation: {str(e)}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

## Login user.
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            # Get user from serializer after validation
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.user
            tokens = response.data  

            FrontendLog.objects.create(
                username=user.username,
                action='تسجيل الدخول',
                message=f"قام المستخدم {user.username} بتسجيل الدخول",
            )

            logger.info(f"User logged in: ({user.username})")

            response.data = {
                "data": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "full_name": user.full_name,
                    "phone_number": user.phone_number,
                    "role": user.role,
                    "refresh_token": tokens.get("refresh"),
                    "access_token": tokens.get("access"),
                }
            }
            return response
        
        except Exception as e:
            logger.error(f"User login failed: {str(e)}")
            return Response({"data": {"error": str(e)}}, status=status.HTTP_400_BAD_REQUEST)


## Change user password by admin.
class AdminChangeUserPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Only allow admin users
        if not request.user.role == 'admin':
            return Response({"error": "Only admins can change users' passwords."}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get("user_id")
        new_password = request.data.get("new_password")

        if not user_id or not new_password:
            return Response({"error": "user_id and new_password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(new_password)
        user.save()
        FrontendLog.objects.create(
            username=user.username,
            action='تغيير كلمة السر',
            description=f'تم تغيير كلمة السر ل {user.username}',
        )
        
        return Response({"message": f"Password updated for user {user.username}."}, status=status.HTTP_200_OK)


## Logout user and deactivate account.
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                logger.error("Logout failed: Refresh token missing")
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Blacklist the refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()

                # Deactivate the user once the token is blacklisted
                request.user.is_active = False
                request.user.save()
                FrontendLog.objects.create(
                    username=request.user.username,
                    action='تسجيل خروج',
                    description=f'تم تسجيل خروج من {request.user.username}',
                    )
                

                logger.info(f"User logged out successfully and deactivated: {request.user.username}")
                return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)

            except TokenError:
                logger.error("Logout failed: Invalid or expired refresh token")
                return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error during logout: {str(e)}")
            return Response({"error": f"An unexpected error occurred:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


## User management view for admin to manage users ( can view , put,delete users).
class UserManagementView(APIView):
    permission_classes = [AllowAny]

    def get(self, request , pk=None):
        if pk:
            """Get user by ID"""
            try:
                user = CustomUser.objects.filter(id=pk).first()
                if not user:
                    logger.error(f"User with ID {pk} not found")
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

                serializer = UserSerializer(user)
                logger.info(f"User details accessed for ID {pk}")
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error while fetching user details: {str(e)}")
                return Response({"error": "Could not retrieve user."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            """Get list of all users"""
            try:
                users = CustomUser.objects.all().order_by('-id')
                serializer = UserSerializer(users, many=True)
                logger.info("User list accessed")


                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error while fetching user list: {str(e)}")
                return Response({"error": "Could not retrieve users."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        """Update user info (not password)"""
        try:
            user = CustomUser.objects.filter(id=pk).first()
            if not user:
                logger.error(f"Update failed: User with ID {pk} not found")
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            update_data = request.data.copy()
            update_data.pop("password", None)  # Strip password if it's accidentally sent

            serializer = UserSerializer(user, data=update_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                FrontendLog.objects.create(
                    username=user.username,
                    action='تعديل',
                    message=f"تم تعديل حساب {user.username}",
                )
                logger.info(f"User {user.username} updated successfully.")
                return Response({"message": "User updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                logger.warning(f"User update failed: {serializer.errors}")
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error during user update: {str(e)}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """Delete a user"""
        try:
            user = CustomUser.objects.filter(id=pk).first()
            if not user:
                logger.error(f"Delete failed: User with ID {pk} not found")
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            user.delete()
            FrontendLog.objects.create(
                username=user.username,
                action='حذف',
                message=f"تم حذف حساب {user.username}",
            )
            logger.info(f"User {user.username} deleted successfully")
            return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Unexpected error during user deletion: {str(e)}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Toggle user activity (activate/deactivate account).

class ToggleUserActivity(APIView):
    permission_classes = [AllowAny]
    def put(self,request,pk):
        try:
            user = CustomUser.objects.filter(id=pk).first()
            if not user:
                logger.error(f"Toggle activity failed: User with ID {pk} not found")
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            user.is_active = not user.is_active
            user.save()

            FrontendLog.objects.create(
                username=user.username,
                action='تغيير حالة التفعيل',
                message=f"تم {'تفعيل' if user.is_active else 'تعطيل'} حساب {user.username}",
            )

            logger.info(f"User {user.username} activity toggled to {user.is_active}")
            return Response({
                "data" : {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "full_name": user.full_name,
                    "phone_number": user.phone_number,
                    "role": user.role,
                    "is_active": user.is_active
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Unexpected error during toggle activity: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


## Reset user password (self-service).
class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            user_id = request.data.get("id")
            old_password = request.data.get("old_password")
            new_password = request.data.get("new_password")

            if not user_id or not old_password or not new_password:
                logger.warning(f"[{user.username}] Password change failed: Missing fields")
                return Response({"error": "id, old_password, and new_password are required."}, status=status.HTTP_400_BAD_REQUEST)

            if str(user.id) != str(user_id):
                logger.warning(f"[{user.username}] ID mismatch during password change attempt")
                return Response({"error": "You are not authorized to change this user's password."}, status=status.HTTP_403_FORBIDDEN)

            if not user.check_password(old_password):
                logger.warning(f"[{user.username}] Incorrect old password")
                return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            logger.info(f"[{user.username}] Password changed successfully")

            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"[{request.user.username}] Unexpected error during password change: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Device registration and management view.
class DeviceView(APIView):
    model = Device
    serializer_class = DeviceSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            logger.info("Device registration initiated")

            fcm_token = request.data.get("fcmToken")
            user_id = request.data.get("user_id")

            if not fcm_token:
                return Response({"error": "fcmToken is required."}, status=status.HTTP_400_BAD_REQUEST)
            if not user_id:
                return Response({"error": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            # ✅ Register or update the device
            device, created = self.model.objects.update_or_create(
                user_id=user,
                defaults={
                    "fcmToken": fcm_token,
                    # Add more fields here if needed
                }
            )

            serializer = self.serializer_class(device, context={'request': request})
            action = "created" if created else "updated"
            logger.info(f"[{user.username}] Device {action} successfully")

            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Unexpected error during device registration: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        try:
            logger.info(f"[{request.user.username}] Device retrieval initiated")
            devices = self.model.objects.all()
            serializer = self.serializer_class(devices, many=True, context={'request': request})
            logger.info(f"[{request.user.username}] Device retrieval successful")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"[{request.user.username}] Unexpected error during device retrieval: {str(e)}")

            return Response({"error": "An unexpected error occurred."} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request, pk=None):

        """Delete a device by ID"""
        if pk:
            try:
                device = self.model.objects.filter(id=pk).first()
                if not device:
                    logger.error(f"[{request.user.username}] Device with ID {pk} not found")
                    return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

                device.delete()
                logger.info(f"[{request.user.username}] Device with ID {pk} deleted successfully")
                return Response({"message": "Device deleted successfully"}, status=status.HTTP_200_OK)

            except Exception as e:
                logger.error(f"[{request.user.username}] Unexpected error during device deletion: {str(e)}")
                return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            devices = self.model.objects.all()
            if not devices:
                logger.warning(f"[{request.user.username}] No devices found for deletion")
                return Response({"message": "No devices to delete"}, status=status.HTTP_404_NOT_FOUND)
            try:
                devices.delete()
                logger.info(f"[{request.user.username}] All devices deleted successfully")
                return Response({"message": "All devices deleted successfully"}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"[{request.user.username}] Unexpected error during device deletion: {str(e)}")
                return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 



