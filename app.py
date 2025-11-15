"""
Deployment-ready web interface for Rural Healthcare Access Agent
Can be deployed to Google Cloud Run, Render, Hugging Face, or any Python hosting
"""

from flask import Flask, request, jsonify, render_template_string
from agents.healthcare_agents import coordinator
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# HTML template for web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Rural Healthcare Access Agent</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #1a73e8; }
        input, textarea { width: 100%; padding: 10px; margin: 10px 0; box-sizing: border-box; }
        button { background: #1a73e8; color: white; padding: 10px 20px; border: none; cursor: pointer; border-radius: 4px; }
        button:hover { background: #1557b0; }
        .result { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .loading { display: none; color: #1a73e8; }
    </style>
</head>
<body>
    <h1>🏥 Rural Healthcare Access Agent</h1>
    <p>AI-powered healthcare triage for rural Madhya Pradesh</p>
    
    <form id="patientForm">
        <label>Patient ID:</label>
        <input type="text" id="patient_id" placeholder="Enter Patient ID" value="PATIENT_001" required>
        
        <label>Location:</label>
        <input type="text" id="location" placeholder="City, State" value="Jabalpur, Madhya Pradesh" required>
        
        <label>Symptoms:</label>
        <textarea id="symptoms" placeholder="Describe symptoms in detail" rows="4" required>Fever and cough for 3 days</textarea>
        
        <label>Age:</label>
        <input type="number" id="age" placeholder="Patient age" value="30" min="1" max="120" required>
        
        <button type="submit">Get Healthcare Recommendations</button>
        <p class="loading" id="loading">⏳ Processing... Please wait...</p>
    </form>
    
    <div id="result" class="result" style="display:none;"></div>
    
    <script>
        document.getElementById('patientForm').onsubmit = async (e) => {
            e.preventDefault();
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            
            const data = {
                patient_id: document.getElementById('patient_id').value,
                location: document.getElementById('location').value,
                symptoms: document.getElementById('symptoms').value,
                age: parseInt(document.getElementById('age').value)
            };
            
            try {
                const response = await fetch('/api/assess', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                // Hide loading
                document.getElementById('loading').style.display = 'none';
                
                if (response.ok) {
                    document.getElementById('result').style.display = 'block';
                    document.getElementById('result').innerHTML = formatResult(result);
                } else {
                    alert('Error: ' + (result.error || 'Unknown error'));
                }
            } catch (error) {
                document.getElementById('loading').style.display = 'none';
                alert('Error connecting to server: ' + error.message);
            }
        };
        
        function formatResult(result) {
            const intake = result.workflow_steps['1_intake'].summary;
            const urgency = result.workflow_steps['2_triage'].urgency_data;
            const explanation = result.workflow_steps['2_triage'].explanation;
            const facilities = result.workflow_steps['3_resources'].facilities.facilities;
            const recommendation = result.workflow_steps['3_resources'].recommendation;
            const telemedicine = result.workflow_steps['4_telemedicine'].recommendation;
            
            let html = '<h2>✅ Healthcare Assessment Complete</h2>';
            html += '<p><strong>⏱️ Response Time:</strong> ' + result.response_time_seconds + ' seconds</p>';
            html += '<hr>';
            
            html += '<h3>📋 Patient Intake</h3>';
            html += '<p>' + intake + '</p>';
            
            html += '<h3>⚠️ Urgency Assessment</h3>';
            html += '<p><strong>Level:</strong> ' + urgency.urgency_level + '/5</p>';
            html += '<p><strong>Priority:</strong> ' + urgency.priority + '</p>';
            html += '<p><strong>Recommendation:</strong> ' + urgency.recommendation + '</p>';
            html += '<p>' + explanation + '</p>';
            
            html += '<h3>🏥 Nearby Healthcare Facilities</h3>';
            html += '<ul>';
            facilities.slice(0, 3).forEach(f => {
                html += '<li><strong>' + f.name + '</strong><br>';
                html += 'Type: ' + f.type + ' | Distance: ' + f.distance_km + ' km | ';
                html += '24x7: ' + (f.available_24x7 ? 'Yes' : 'No') + '</li>';
            });
            html += '</ul>';
            html += '<p>' + recommendation + '</p>';
            
            html += '<h3>💻 Telemedicine Options</h3>';
            html += '<p>' + telemedicine + '</p>';
            
            return html;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Web interface for agent"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/assess', methods=['POST'])
def assess_patient():
    """API endpoint for patient assessment"""
    try:
        data = request.json
        result = coordinator.process_patient(
            patient_id=data.get('patient_id', 'UNKNOWN'),
            location=data.get('location', 'Jabalpur, MP'),
            symptoms=data.get('symptoms', ''),
            age=data.get('age', 30)
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint for cloud deployment"""
    return jsonify({
        'status': 'healthy',
        'agent': 'Rural Healthcare Access Agent',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    # For local development and cloud deployment
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
