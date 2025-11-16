# Rural Healthcare Access Agent - Multi-Agent AI System

## Problem Statement
In rural Madhya Pradesh, people struggle to access healthcare because:
- No nearby doctors or hospitals
- Don't know which facilities are available
- Can't travel long distances for medical care

## Solution
Our AI agent system automatically:
1. Takes patient symptoms/complaints
2. Finds nearest healthcare facilities
3. Schedules telemedicine appointments
4. Provides medical recommendations

## Architecture
[Will add diagram image here - see TASK 2]

## How To Run (Super Simple - No Coding Needed)

### For Kaggle Notebook Users:
1. Open the notebook: https://www.kaggle.com/code/drdeepanshdubey/rural-healthcare-access-agent-multi-agent-ai-sys
2. Click the blue "Run All" button at the top
3. Wait 2-3 minutes for it to run
4. Scroll down to see results

### For GitHub Users (Download and Run):
1. Click green "Code" button on GitHub → "Download ZIP"
2. Unzip the folder on your computer
3. Open file called "requirements.txt" (don't edit it, just see it)
4. Get free API key from: https://makersuite.google.com/app/apikey (takes 1 minute)
5. Copy your key, go back to notebook, paste it where it says "YOUR_API_KEY_HERE"
6. Click "Run All" again

### For Docker Users (If you have Docker installed):
docker build -t rural-healthcare-agent .
docker run -d -p 8080:8080 -e GEMINI_API_KEY=your_actual_key rural-healthcare-agent

Then open browser → http://localhost:8080

## Features Used (From Course)
✅ Multi-agent system (5 agents working together)
✅ Gemini LLM-powered agents (uses Gemini AI for thinking)
✅ Custom tools (web search, resource finding)
✅ Sessions & Memory (remembers patient history)
✅ Observability (shows logs of what agent is doing)

## Sample Results
[Will add screenshot here - see TASK 2]

## Team
- Deepansh Dubey (drdeepanshdubey)

## Contributing
Want to help? We need:
- Hindi language translation
- Support for more districts in MP
- Better UI design

Fork this repo and submit a pull request!

## License
Apache 2.0
[Patient Input]
    ↓
[Intake Agent - Collects symptoms]
    ↓
[Triage Agent - Assesses severity]
    ↓
[Resource Finder - Finds nearest hospital]
    ↓
[Telemedicine Agent - Books appointment]
    ↓
[Coordinator Agent - Confirms everything]
    ↓
[Output - Healthcare recommendations]
