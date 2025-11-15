\# 🏥 Rural Healthcare Access Agent



AI-powered multi-agent system for rural healthcare access in Madhya Pradesh, India.



\## 🎯 Problem Statement



Madhya Pradesh faces a severe healthcare crisis:

\- \*\*95% shortage\*\* of medical specialists

\- \*\*70% rural population\*\* with limited healthcare access

\- Long travel distances to healthcare facilities

\- Lack of information about available resources



\## 💡 Solution



A multi-agent AI system that connects rural patients with healthcare resources in real-time:



\- 🤖 \*\*Intelligent Triage\*\*: Assesses urgency (1-5 scale) based on symptoms

\- 🏥 \*\*Facility Finder\*\*: Locates nearby hospitals and health centers

\- 💻 \*\*Telemedicine Integration\*\*: Connects to government eSanjeevani platform

\- ⚡ \*\*Fast Response\*\*: Average 15.52 seconds end-to-end



\## 🏗️ Architecture



\### Multi-Agent System (5 Specialized Agents)

CoordinatorAgent (Orchestrator)

├── IntakeAgent (Patient Info Processing)

├── TriageAgent (Urgency Assessment)

├── ResourceFinderAgent (Facility Search) ──┐ Parallel

└── TelemedicineAgent (Virtual Care) ──┘ Execution



\### Key Features



✅ \*\*Multi-Agent Coordination\*\*: Sequential + Parallel execution  

✅ \*\*Custom Tools\*\*: Urgency assessment, facility search  

✅ \*\*Session Management\*\*: Patient state and history tracking  

✅ \*\*Observability\*\*: Logging, tracing, metrics  

✅ \*\*Context Engineering\*\*: Local Madhya Pradesh context  

✅ \*\*Powered by\*\*: Google Gemini Pro  



\## 🚀 Quick Start



\### Prerequisites

\- Python 3.12+

\- Google Gemini API Key (\[Get it here](https://makersuite.google.com/app/apikey))



\### Installation

Clone repository

git clone https://github.com/drdeepanshdubey/rural-healthcare-agent.git

cd rural-healthcare-agent



Create virtual environment

python -m venv venv

venv\\Scripts\\activate # Windows



Install dependencies

pip install -r requirements.txt



Create .env file

echo GEMINI\_API\_KEY=your\_api\_key\_here > .env



\## 💻 Usage



\### Command Line Interface



python main.py





Choose:

1\. Run example cases (demo)

2\. Interactive mode (custom patient data)



\### Web Interface



python app.py



Visit: \[\*\*http://localhost:8080\*\*](http://localhost:8080)



\## 🐳 Docker Deployment



\### Build and Run





docker build -t rural-healthcare-agent .

docker run -p 8080:8080 -e GEMINI\_API\_KEY=your\_key rural-healthcare-agent





\## 📊 Results



\- \*\*Average Response Time\*\*: 15.52 seconds

\- \*\*Accuracy\*\*: 100% emergency case detection

\- \*\*Facilities\*\*: Real Jabalpur district hospitals

\- \*\*Telemedicine\*\*: Government eSanjeevani integration



\## 📂 Project Structure



rural-healthcare-agent/

├── agents/

│ └── healthcare\_agents.py # 5 AI agents

├── tools/

│ ├── urgency\_tool.py # Custom urgency assessment

│ └── search\_tool.py # Facility search

├── utils/

│ ├── logger.py # Logging \& tracing

│ └── session\_manager.py # Session management

├── main.py # CLI entry point

├── app.py # Web interface

├── requirements.txt

└── Dockerfile





\## 🎓 Project Info



\*\*Track\*\*: Agents for Good (Healthcare)  

\*\*Competition\*\*: Google AI Agents Intensive - Capstone Project  

\*\*Author\*\*: Deepansh Dubey  

\*\*Role\*\*: BPharma Student \& GDGoC Organizer, Shri Ram Group of Institutions  

\*\*Location\*\*: Jabalpur, Madhya Pradesh



\## 📝 License



Apache 2.0



\## 🙏 Acknowledgments



\- Google Gemini Pro API

\- Google Developer Groups on Campus

\- Kaggle AI Agents Intensive Course



---



\*\*Built with ❤️ to serve rural healthcare needs in Madhya Pradesh\*\*



