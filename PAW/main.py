"""AI is creating summary for 

Returns:
    [type]: [If you want to dynamically generate route 
            wrapper functions in the main_file.py based 
            on the functions defined in views.py, you can 
            use a decorator or a loop to iterate through 
            the functions in views.py and create corresponding 
            wrappers in main_file.py. Here's an example using 
            a decorator:]
            
            # # Parse form data
            # form_data = parse_qs(post_data)
            # input_value = form_data.get('input_name', [''])[0]
"""





from PAW.server import PAWFrameworkServer
from example.views import *

# Define a decorator for generating route wrapper functions
def generate_route_wrapper(route_func):
    def wrapper(request):
        return route_func(request)
    return wrapper

# Iterate through functions in views.py and generate corresponding wrappers
for func_name in dir():
    if func_name.startswith("_"):
        continue

    func = globals().get(func_name)
    if callable(func) and hasattr(func, "route_path"):
        wrapper_func = generate_route_wrapper(func)
        setattr(globals(), func_name + "_wrapper", wrapper_func)

if __name__ == '__main__':
    PAWFrameworkServer.run()
