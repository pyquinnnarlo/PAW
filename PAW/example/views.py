# views.py
from PAW.router import Router

app = Router()
# Create views code below.


@app.route(r'^/$', methods=['GET'])
def home(template_env):
        template = template_env.get_template('index.html')
        return template.render()
    

@app.route(r'^/about$', methods=['GET'])
def about(template_env):
    template = template_env.get_template('about.html')
    return template.render()


