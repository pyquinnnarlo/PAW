# urls.py

from PAW.router import Router
from .views import post_detail, app, dashboard  # Import your view functions

# Define your routes
Router.route('/', methods=['GET'])(app)
Router.route('/post_detail/<int:post_id>', methods=['GET'])(post_detail)
Router.route('/dashboard', methods=['GET'])(dashboard)
# Add more routes as needed
