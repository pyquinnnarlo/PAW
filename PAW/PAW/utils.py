class Utils:
    @staticmethod
    def read_html_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()