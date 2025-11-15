"""
Deployment-ready web interface for Rural Healthcare Access Agent
"""

from flask import Flask, request, jsonify, render_template_string
from agents.healthcare_agents import coordinator
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

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
        <input type="text" id="patient_id" value="PATIENT_001" required>
        
        <label>Location:</label>
        <input type="text" id="location" value="Jabalpur, Madhya Pradesh" required>
        
        <label>Symptoms:</label>
        <textarea id="symptoms" rows="4" required>Fever and cough for 3 days</textarea>
        
        <label>Age:</label>
        <input type="number" id="age" value="30" min="1" max="120" required>
        
        <button type="submit">Get Healthcare Recommendations</button>
        <p class="loading" id="loading">⏳ Processing... Please wait...</p>
    </form>
    
    <div id="result" class="result" style="display:none;"></div>
    
    <script>
        document.getElementById('patientForm').onsubmit = async (e) => {
            e.preventDefault();
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
                document.getElementById('loading').style.display = 'none';
                
                if (response.ok) {
                    document.getElementById('result').style.display = 'block';
                    document.getElementById('result').innerHTML = formatResult(result);
                } else {
                    alert('Error: ' + (result.error || 'Unknown error'));
                }
            } catch (error) {
                document.getElementById('loading').style.display = 'none';
                alert('Error: ' + error.message);
            }
        };
        
        function formatResult(result) {
            const urgency = result.workflow_steps['2_triage'].urgency_data;
            const facilities = result.workflow_steps['3_resources'].facilities.facilities;
            
            let html = '<h2>✅ Assessment Complete</h2>';
            html += '<p><strong>⏱️ Response Time:</strong> ' + result.response_time_seconds + ' seconds</p><hr>';
            html += '<h3>⚠️ Urgency: ' + urgency.urgency_level + '/5 (' + urgency.priority + ')</h3>';
            html += '<p>' + urgency.recommendation + '</p>';
            html += '<h3>🏥 Nearby Facilities:</h3><ul>';
            
            facilities.slice(0, 3).forEach(f => {
                html += '<li><strong>' + f.name + '</strong> - ' + f.distance_km + ' km</li>';
            });
            
            html += '</ul>';
            return html;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/assess', methods=['POST'])
def assess_patient():
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
    return jsonify({'status': 'healthy', 'agent': 'Rural Healthcare Access Agent'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
