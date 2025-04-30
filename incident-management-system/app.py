from flask import Flask, render_template, request, jsonify, send_file
from flask_mail import Mail, Message
from models import db, Incident
import csv
import io
import os
from dotenv import load_dotenv  # Import dotenv to load environment variables

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Configuring the app for database and mail
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Gmail address
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Gmail app password
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')  # Default sender email

# Initialize database and mail
db.init_app(app)
mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/incidents', methods=['POST'])
def create_incident():
    data = request.json
    incident = Incident(
        title=data['title'],
        description=data['description'],
        severity=data.get('severity', 'Low'),
        status=data.get('status', 'Open'),
        reported_by=data.get('reported_by', ''),
        assigned_to=data.get('assigned_to', ''),
        notes=data.get('notes', '')
    )
    db.session.add(incident)
    db.session.commit()

    # Email notification logic
    assigned_to = incident.assigned_to
    if assigned_to:
        try:
            
            # Prepare the email
            msg = Message(
                subject=f"New Incident Assigned: {incident.title}",
                recipients=[assigned_to],
                html=f"""
                    <p>You have been assigned a new incident:</p>
                    <p>
                    <strong>Title:</strong> {incident.title}<br>
                    <strong>Severity:</strong> {incident.severity}<br>
                    <strong>Status:</strong> {incident.status}<br>
                    <strong>Description:</strong> {incident.description}
                    </p>
                    </p>
                    <strong>Note:</strong> {incident.notes}
                    </p>
                    <p>Please check the Incident Management System for more details.</p>
                    """
            )
            mail.send(msg)
                
        except Exception as e:
            
            print(f"Failed to send email to {assigned_to}: {e}")

    
    return jsonify({"message": "Incident created", "id": incident.id}), 201

@app.route('/api/incidents', methods=['GET'])
def get_incidents():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return jsonify([{
        "id": i.id,
        "title": i.title,
        "description": i.description,
        "severity": i.severity,
        "status": i.status,
        "reported_by": i.reported_by,
        "assigned_to": i.assigned_to,
        "notes": i.notes,
        "created_at": i.created_at.strftime("%Y-%m-%d %H:%M")
    } for i in incidents])

@app.route('/api/incidents/<int:incident_id>', methods=['PUT'])
def update_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    data = request.json
    if 'status' in data:
        incident.status = data['status']
    if 'notes' in data:
        incident.notes = data['notes']
    db.session.commit()
    return jsonify({"message": "Incident updated"})

@app.route('/api/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    db.session.delete(incident)
    db.session.commit()
    return jsonify({"message": "Incident deleted"})

@app.route('/api/incidents/export')
def export_incidents():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Title', 'Description', 'Severity', 'Status', 'Reported By', 'Assigned To', 'Created At'])

    for i in Incident.query.all():
        writer.writerow([i.id, i.title, i.description, i.severity, i.status,
                         i.reported_by, i.assigned_to, i.created_at.strftime("%Y-%m-%d %H:%M")])

    output.seek(0)
    return send_file(io.BytesIO(output.read().encode()),
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='incident_report.csv')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
