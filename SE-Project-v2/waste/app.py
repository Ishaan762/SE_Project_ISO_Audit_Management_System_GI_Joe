from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Update app.py
# Add these import statements at the top
from flask import render_template_string



# Add this route for client to view feedback
@app.route('/client_feedback/<project_name>')
def client_feedback(project_name):
    global feedback
    # Get feedback for the specified project name
    project_feedback = feedback.get('auditor', {})
    if project_feedback.get('project_name') == project_name:
        return render_template('client_feedback.html', project_feedback=project_feedback)
    else:
        return render_template_string('<p>No feedback available for this project.</p>')


# Dummy data to simulate user credentials
user_credentials = {
    'client': {'username': '1', 'password': '1'},
    'auditor': {'username': '0', 'password': '0'}
}

# Variables to store project details and feedback
project_details = {'client': [], 'auditor': []}
feedback = {'client': None, 'auditor': None}


@app.route('/')
def welcome():
    return render_template('welcome.html')


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
# Variables to store project entries
project_entries = []

@app.route('/client_dashboard', methods=['GET', 'POST'])
def client_dashboard():
    global project_details, feedback, project_entries

    if request.method == 'POST':
        # Get project details from the form
        project_name = request.form.get('project_name')
        client_username = user_credentials['client']['username']

        # Store the project entry
        project_entry = {'project_name': project_name, 'client_username': client_username}
        project_entries.append(project_entry)

        # Show success message
        return render_template('client_dashboard.html', success='Project details uploaded successfully', project=project_entry, project_entries=project_entries)

    return render_template('client_dashboard.html', project=project_details['client'], project_entries=project_entries)



@app.route('/auditor_dashboard')
def auditor_dashboard():
    global project_details, feedback
    return render_template('auditor_dashboard.html', project_entries=project_entries, feedback=feedback['client'])

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


if __name__ == '__main__':
    app.run(debug=True)
