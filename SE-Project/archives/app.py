from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dictionary to store state for each instance
audit_states = {}

# Dictionary to store feedback from auditors
auditor_feedback = {}

# Hardcoded login credentials (for demonstration purposes)
client_credentials = {'client_user': 'client_password'}
auditor_credentials = {'auditor_user': 'auditor_password'}

# Define routes and views
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/client_menu', methods=['GET', 'POST'])
def client_menu():
    if request.method == 'POST':
        role = request.form.get('role')
        username = request.form.get('username')
        password = request.form.get('password')

        if role == 'client' and username == client_credentials['client_user'] and password == client_credentials['client_password']:
            return redirect(url_for('client_menu'))

        elif role == 'auditor' and username == auditor_credentials['auditor_user'] and password == auditor_credentials['auditor_password']:
            return redirect(url_for('auditor_menu'))

        else:
            # Invalid credentials, you can handle this case as needed
            return render_template('login.html', error='Invalid credentials. Please try again.')

    return render_template('login.html')

@app.route('/auditor_menu', methods=['GET', 'POST'])
def auditor_menu():
    if request.method == 'POST':
        # Handle form submission and data processing here
        # Example: Get data from the form
        instance_key = request.form.get('instance_key')
        feedback = request.form.get('feedback')

        # Store feedback for this instance
        auditor_feedback[instance_key] = feedback

    return render_template('auditor_menu.html', audit_states=audit_states, feedback=auditor_feedback)

@app.route('/audit', methods=['GET', 'POST'])
def audit():
    if request.method == 'POST':
        # Handle form submission and data processing here
        # Example: Get data from the form
        project_name = request.form.get('project_name')
        model = request.form.get('model')
        documents = request.form.get('documents')

        # Store state for this instance
        instance_key = len(audit_states) + 1
        audit_states[instance_key] = {
            'project_name': project_name,
            'model': model,
            'documents': documents,
        }

        return redirect(url_for('audit', instance_key=instance_key))  # Redirect to the audit page

    return render_template('audit.html', audit_states=audit_states)

if __name__ == '__main__':
    app.run(debug=True)
