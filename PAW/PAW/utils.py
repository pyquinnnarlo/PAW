class Utils:
    @staticmethod
    def read_html_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
        
import jinja2
from urllib.parse import parse_qs

class Template:
    def __init__(self, template_folder='templates'):
        self.template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_folder))

    def render_template(self, template_name, **kwargs):
        template = self.template_env.get_template(template_name)
        return template.render(**kwargs)
    
    def parser(self, data):
        return parse_qs(data)
    


