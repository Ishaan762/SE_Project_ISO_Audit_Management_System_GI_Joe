from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Update app.py
# Add these import statements at the top
from flask import render_template_string

# Add this route for auditor feedback
@app.route('/auditor_feedback/<project_name>', methods=['GET', 'POST'])
def auditor_feedback(project_name):
    global feedback

    if request.method == 'POST':
        # Get feedback from the form
        feedback_text = request.form.get('feedback_text')

        # Save feedback indexed by project name
        feedback['auditor'] = {'project_name': project_name, 'feedback_text': feedback_text}

        # Redirect to the auditor dashboard after submitting feedback
        return redirect(url_for('auditor_dashboard'))

    return render_template('auditor_feedback.html', project_name=project_name)

@app.route('/client_feedback/<project_name>')
def client_feedback(project_name):
    global feedback

    try:
        # Get feedback for the specified project name
        project_feedback = feedback.get('auditor', {})
        if project_feedback.get('project_name') == project_name:
            return render_template('client_feedback.html', project_feedback=project_feedback)
        else:
            raise Exception("No feedback available for this project.")
    
    except Exception as e:
        # Render a new webpage with a centered box in the middle of the page
        error_message = str(e)
        return render_template_string('''
            <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Client Feedback</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
    <style>
        body {
            background-color: #2B3499;
            color: #FFD099;
            font-family: 'Arial', sans-serif;
            text-align: center;
            padding: 50px;
        }

        .content-box {
            background-color: #FFF;
            border-radius: 10px;
            padding: 20px;
            margin: 20px;
            text-align: center;
        }

        button {
            background-color: #FFD099;
            color: #2B3499;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            margin-top: 20px;
        }

        button:hover {
            background-color: #FF9209;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="content-box">
                    <h1>No Feedback found</h1>
                    <p>Please come back later for feedback</p>
                    <button onclick="window.location.href='/client_dashboard'">Back to Client Dashboard</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Bootstrap JS and Popper.js -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
</body>
</html>
        ''', error_message=error_message)


# Dummy data to simulate user credentials
user_credentials = {
    'client': {'username': '1', 'password': '1'},
    'auditor': {'username': '0', 'password': '0'}
}

# Variables to store project details and feedback
project_details = {'client': None, 'auditor': None}
feedback = {'client': None, 'auditor': None}


@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/client_feedback/')
def client_feedback_page():
    return render_template('client_feedback_page.html')

@app.route('/client_login', methods=['GET', 'POST'])
def client_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the provided credentials match the dummy data
        if (
            user_credentials['client']['username'] == username
            and user_credentials['client']['password'] == password
        ):
            # Successful login
            return redirect(url_for('client_dashboard'))
        else:
            # Failed login
            return render_template('client_login.html', error='Invalid credentials')

    return render_template('client_login.html')


@app.route('/auditor_login', methods=['GET', 'POST'])
def auditor_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the provided credentials match the dummy data
        if (
            user_credentials['auditor']['username'] == username
            and user_credentials['auditor']['password'] == password
        ):
            # Successful login
            return redirect(url_for('auditor_dashboard'))
        else:
            # Failed login
            return render_template('auditor_login.html', error='Invalid credentials')

    return render_template('auditor_login.html')


@app.route('/client_dashboard', methods=['GET', 'POST'])
def client_dashboard():
    global project_details

    if request.method == 'POST':
        # Get project details from the form
        project_details['client'] = {
            'project_name': request.form.get('project_name'),
            'project_description': request.form.get('project_description'),
            'model_used': request.form.get('model_used'),  # Save the model type
            # Add more details as needed
        }
        # Show success message
        return render_template('client_dashboard.html', success='Project details uploaded successfully', project=project_details['client'])

    return render_template('client_dashboard.html', project=project_details['client'])

@app.route('/auditor_dashboard')
def auditor_dashboard():
    global project_details, feedback
    return render_template('auditor_dashboard.html', project=project_details['client'], feedback=feedback['client'])


if __name__ == '__main__':
    app.run(debug=True)
