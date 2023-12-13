def authenticate_user(route_func):
    def wrapper(request, *args, **kwargs):
        # Check if the user is authenticated
        if 'user_id' in request.session_data:
            return route_func(request, *args, **kwargs)
        else:
            # Redirect to the login page or another route if not authenticated
            redirect_url = '/'  # Change this to your login route
            headers = {'Location': redirect_url}
            return '', 302, headers

    return wrapper