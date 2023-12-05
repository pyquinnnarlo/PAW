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


## Contributing
Feel free to contribute to PAW! Fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.





 <div style="max-width: 400px; margin: 50px auto; background-color: #fff; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); border-radius: 8px; overflow: hidden; transition: transform 0.3s ease-in-out;">

<img src="https://placekitten.com/300/200" alt="Card Image" style="width: 100%; height: auto; border-bottom: 1px solid #ddd;">

<div style="padding: 20px;">

<h2 style="font-size: 1.8rem; margin-bottom: 10px; color: #333;">Beautiful Card</h2>

<p style="color: #555; line-height: 1.4;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eget justo ut odio facilisis elementum.</p>

<a href="#" style="display: inline-block; padding: 10px 15px; background-color: #3498db; color: #fff; text-decoration: none; border-radius: 4px; transition: background-color 0.3s;" onmouseover="this.style.backgroundColor='#2980b9'" onmouseout="this.style.backgroundColor='#3498db'">Read More</a>

    </div>
  </div>




