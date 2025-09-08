from core.models import Users
from users.models import Logins
import json
from django.utils.deprecation import MiddlewareMixin
from io import BytesIO


TOKEN_USER = '/users/token/'


class LogLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        This method runs before the view is executed.
        It reads the POST body for the /users/token/ endpoint,
        extracts the username, and saves it on the request object
        for later use in process_response.
        """
        if request.path == TOKEN_USER and request.method == 'POST':
            # Read the raw body of the request
            body_bytes = request.body.strip()

            # Decode JSON and extract username
            username = None
            try:
                data = json.loads(body_bytes.decode('utf-8'))
                username = data.get('username')
            except json.JSONDecodeError:
                pass

            # Save username in the request for later use
            request._login_username = username

            # Reset the request stream so the view can read it again
            request._stream = BytesIO(body_bytes)

    def process_response(self, request, response):
        """
        This method runs after the view has processed the request.
        It logs the login attempt into the Logins model,
        marking it as SUCCESS if the response status code is 200,
        otherwise as FAIL.
        """
        if request.path == TOKEN_USER and request.method == 'POST':
            # Get the username saved in process_request
            username = getattr(request, '_login_username', None)

            # Try to get the user object, if it exists
            user = Users.objects.filter(username=username).first()

            # Determine login status based on response status code
            status_code = response.status_code
            status = Logins.Status.SUCCESS if status_code == 200 else Logins.Status.FAIL

            # Create a login log entry
            Logins.objects.create(user=user, status=status, username=username)

        # Return the original response
        return response
