import os

def create_app(app_name):
    app_path = os.path.join(os.getcwd(), app_name)

    # Create the main app folder
    os.makedirs(app_path)

    # Create subfolders (static, templates, PAW)
    app_name_lower = app_name.lower()
    folders = [app_name_lower, 'static', 'templates', 'PAW']
    for folder in folders:
        os.makedirs(os.path.join(app_path, folder))

    # Create files with default content
    default_content = {
        '.gitignore': "# .gitignore",
        f'{app_name_lower}/__init__.py' : 
"""
# __init__.py

""",  
    f'{app_name_lower}/views.py' : "views"
    }

    for file, content in default_content.items():
        file_path = os.path.join(app_path, file)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as f:
            f.write(content)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python paw_app.py <app_name>")
        sys.exit(1)

    app_name = sys.argv[1]
    create_app(app_name)
    print(f"App '{app_name}' created successfully.")
