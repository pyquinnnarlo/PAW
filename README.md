<div align="center">
    
![Asset 6hdpi](https://github.com/pyquinnnarlo/PAW/assets/105549100/fb38796c-be47-493e-8315-242e8b69431d)


<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="teachmentor" data-color="#5F7FFF" data-emoji="🍕"  data-font="Arial" data-text="Buy me a pizza" data-outline-color="#000000" data-font-color="#ffffff" data-coffee-color="#FFDD00" ></script>

<iframe src="https://giphy.com/embed/513lZvPf6khjIQFibF" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/buymeacoffee-buy-me-a-coffee-support-513lZvPf6khjIQFibF">via GIPHY</a></p>

</div>

# PAW Framework


PAW (Python Application Web) is a lightweight web framework written in Python. It provides a simple and flexible structure for building web applications.


## Features

- **Routing**: Easy-to-use routing for defining endpoints and handling HTTP methods.
- **Database Integration**: Simple database integration for common operations like insert, delete, and fetch.
- **Template Rendering**: Support for rendering HTML templates using Jinja2.
- **User Authentication**: Basic user registration and login functionality.
- **Security**: Hashing and password verification for secure user management.

## Getting Started

1. Install PAW:

```bash
pip install paw-framework
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
