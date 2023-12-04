# from PAW.router import Router
# from urllib.parse import parse_qs
# from PAW.utils import Utils
# from PAW.database import Database

# # Create a database instance
# db = Database()
# @Router.route('/', methods=['GET', 'POST'])
# def home(request):
#     if request.command == 'GET':
        
#         html_content = Utils.read_html_file('temp/home.html')
#         return html_content, 200
#     elif request.command == 'POST':
#         content_length = int(request.headers['Content-Length'])
#         post_data = request.rfile.read(content_length).decode('utf-8')

#         # Parse form data
#         form_data = parse_qs(post_data)
#         input_value = form_data.get('input_name', [''])[0]
        
#         # Insert data into the database
#         db.insert_data(input_value)

#         return f"POST request handled with data: {input_value}", 200
    
    

# @Router.route('/about', methods=['GET'])
# def about(request):
#     # Fetch data from the database
#     data = db.fetch_data()
#     return f"About page. Data from the database: {data}", 200