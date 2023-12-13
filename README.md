<div align="center">
    
![Asset 6hdpi](https://github.com/pyquinnnarlo/PAW/assets/105549100/fb38796c-be47-493e-8315-242e8b69431d)

![github](https://github.com/pyquinnnarlo/PAW/assets/105549100/f1c9fcb2-bff7-4189-bd28-67329579f09a)

</div>

# PAW Framework

PAW (Python Application Web) is a lightweight web framework written in Python. It provides a simple and flexible structure for building web applications.






## Features

- **Routing**: Easy-to-use routing for defining endpoints and handling HTTP methods.
- **Database Integration**: Simple database integration for common operations like insert, delete, and fetch.
  - Sqlite3
  - MongoDB
  
- **Template Rendering**: Support for rendering HTML templates using Jinja2.
- **User Authentication**: Basic user registration and login functionality.
- **Security**: Hashing and password verification for secure user management.
- **Dynamic URL Routing**
- **Server Auto-Restart**

## Getting Started

1. Install PAW:

```bash
pip install PAW
```

```bash
python paw_createapp your_app_name
cd your_app_name
```


```bash
python main.py
```

## Example Usage

Define routes in views.py:

```python
# views.py

from PAW.router import Router

@Router.route('/', methods=['GET'])
def home(request):
    return "Hello, PAW!", 200
```

Run your app:

```bash
python main.py
```


<section>
<h1>
    Contributing 👋
</h1>

<ul>
<li>
    Clone the project.
</li>

```bash

git clone https://github.com/pyquinnnarlo/PAW.git

```

<li>
    cd into project directory.
</li>

```bash

cd PAW

```

<li>
    Run the framework (PAW).
</li>

```bash

python main.py

```

<li>
    Go to localhost 8000
</li>

```bash

localhost:8000

```

</ul>

</section>

<br />
<br />


## License
This project is licensed under the MIT License - see the LICENSE file for details.



