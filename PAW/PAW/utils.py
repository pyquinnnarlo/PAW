import jinja2
from urllib.parse import parse_qs


class Utils:
    @staticmethod
    def read_html_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
        


class Template:
    def __init__(self, template_folder='templates'):
        self.template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_folder))

    def render_template(self, template_name, **kwargs):
        template = self.template_env.get_template(template_name)
        return template.render(**kwargs)

    @staticmethod
    def parse_form_data(request):
        content_length = int(request.headers.get('Content-Length', 0))
        post_data = request.rfile.read(content_length).decode('utf-8')
        return parse_qs(post_data)

    @staticmethod
    def parse_form_data_fields(form_data, field_names):
        parsed_fields = {}
        for field_name in field_names:
            parsed_fields[field_name] = form_data.get(field_name, [''])[0]
        return parsed_fields
    
    


