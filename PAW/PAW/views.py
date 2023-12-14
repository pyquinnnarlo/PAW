# views.py
from .router import Router
from .model import db

app = Router()

@app.route(r'^/$', methods=['GET', 'POST'])
def home(template_env, form_data=None):
    if form_data:
        title = form_data.get('title', [''])[0]
        description = form_data.get('description', [''])[0]
        db.insert_data('posts', title=title, description=description)
        return f"Hello, {title}!"
    else:
        template = template_env.get_template('home.html')
        return template.render()

@app.route(r'^/about$', methods=['GET'])
def about(template_env):
    template = template_env.get_template('about.html')
    return template.render()

@app.route(r'^/user/(\w+)$', methods=['GET'])
def user(template_env, username):
    template = template_env.get_template('user.html')
    return template.render(username=username)
