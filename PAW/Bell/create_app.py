import os
import shutil

def create_app(app_name):
    app_path = os.path.join(os.getcwd(), app_name)

    # Create the main app folder
    os.makedirs(app_path)

    # Create subfolders (views, templates, PAW)
    folders = ['views', 'templates', 'PAW']
    for folder in folders:
        os.makedirs(os.path.join(app_path, folder))

    # Create files with default content
    default_content = {
        'main_file.py': "# Your main application file",
        'router.py': "# Your router file",
        'utils.py': "# Your utility functions",
        'views/home.py': "# Your home view",
        'views/about.py': "# Your about view",
        'templates/home.html': "<html><body><h1>Welcome to your app!</h1></body></html>",
        'templates/about.html': "<html><body><h1>About Page</h1></body></html>",
        'PAW/__init__.py': "# Initialization for your framework",
        'PAW/server.py': "# Your framework server logic",
        'PAW/router.py': "# Your framework router logic",
        'PAW/utils.py': "# Utility functions for your framework",
    }

    for file, content in default_content.items():
        file_path = os.path.join(app_path, file)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as f:
            f.write(content)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python create_app.py <app_name>")
        sys.exit(1)

    app_name = sys.argv[1]
    create_app(app_name)
    print(f"App '{app_name}' created successfully.")
