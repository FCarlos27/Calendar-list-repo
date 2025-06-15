from flask import Flask, request, render_template
from datetime import datetime
from Py_files.GHL_Auth import get_access_token
from Py_files.Get_gist import get_json_gist, update_tks_in_gist, retrieve_tks_json 
from Py_files.Get_calendar import get_calendar_events, set_start_and_end_time, create_list, tokens

app = Flask(__name__)

@app.route('/')
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    data = None
    auth_token = tokens()[0]  # Get access token

    if request.method == 'POST':
        option = request.form.get('option')
        date_input = request.form.get('date', "")

        if option == "1":
            start_time, end_time = set_start_and_end_time(1)
            json_file = get_calendar_events(start_time, end_time, auth_token)
            data = create_list(json_file, 1)

        elif option == "2":
            start_time, end_time = set_start_and_end_time(2)
            json_file = get_calendar_events(start_time, end_time, auth_token)
            data = create_list(json_file, 2)

        elif option == "3" and date_input:
            curr_year = datetime.now().year
            formatted_date = f"{curr_year}-{date_input}"

            try:
                datetime.strptime(formatted_date, "%Y-%m-%d")  # Validate date format
                start_time, end_time = set_start_and_end_time(3, formatted_date)
                json_file = get_calendar_events(start_time, end_time, auth_token)
                data = create_list(json_file, 3, formatted_date)
            except ValueError:
                data = "<p style='color:red;'>Invalid date format. Please use MM-DD.</p>"

        elif option == "4":
            return "Exiting the program."

    return render_template("menu.html", data=data)


# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == "POST":
#         return redirect(url_for('user', usr=request.form['nm']))
#     else: 
#         return render_template('login.html')

# @app.route('/<usr>')
# def user(usr):
#     return f'<h1>Hello, {usr}!</h1>'

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Run the Flask app on port 5000