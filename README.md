# PS: 25040- FloatChat - AI-Powered Conversational Interface for ARGO Ocean Data Discovery and Visualization

This README provides an overview of the project, including team details, relevant links, tasks completed, tech stack, key features, and steps to run the project locally.

## Team Details

**Team Name:** HelloWorld

**Team Leader:** [@kirtigarg38](https://github.com/kirtigarg38) - Kirti Garg

**Team Members:**

- **Maithri Sri Meda** - 2022UCS1568 - [@SmartPotter](https://github.com/SmartPotter)
- **Akansha Pandey** - 2022UCS1609 - [@Akansha2004pandey](https://github.com/Akansha2004pandey)
- **Dhruv Sarkar** - 2022UCA1946 - [@drv44](https://github.com/drv44)
- **Sanskriti** - 2022UCS1550 - [@Sans11Pentium](https://github.com/Sans11Pentium)
- **Kanishka Singh** - 2022UCA1928 - [@skanishka01](https://github.com/skanishka01)

**Collaborator:** [@drv44](https://github.com/drv44), [@Sans11Pentium](https://github.com/Sans11Pentium)

## Project Links

- **SIH Presentation:** [Final SIH Presentation](https://onedrive.live.com/personal/d4c0dbd0e7ba7ad3/_layouts/15/Doc.aspx?sourcedoc=%7B7aef39bb-f227-49c8-beec-199021d5ecf7%7D&action=default&redeem=aHR0cHM6Ly8xZHJ2Lm1zL3AvYy9kNGMwZGJkMGU3YmE3YWQzL0ViczU3M29uOHNoSnZ1d1prQ0hWN1BjQjZQVnlWY0lvVU1mYjB6eERyeGlKaEE_ZT1MQmZmY0I&slrid=004bc8a1-906b-0000-fa69-158fe8923ce5&originalPath=aHR0cHM6Ly8xZHJ2Lm1zL3AvYy9kNGMwZGJkMGU3YmE3YWQzL0ViczU3M29uOHNoSnZ1d1prQ0hWN1BjQjZQVnlWY0lvVU1mYjB6eERyeGlKaEE_cnRpbWU9QnVzZ0hQXzUzVWc&CID=67d8b92b-ed90-42a4-b73b-73fc10af48b1&_SRM=0:G:56&file=SIH2025-IDEA-Presentation-Format.pptx)
- **Video Demonstration:** [Watch Video](https://www.youtube.com/watch?v=fU1Fn5ZRlaM)
- **Live Deployment:** [View Deployment](https://float-chat-eight.vercel.app/), [Microsite-Oceanic Data Platform](https://float-chat-kg-gxdo.vercel.app/)
- **Source Code:** [View Source Code](https://github.com/SmartPotter/FloatChat)
- **Additional Resources:** [Indian Argo Project](https://incois.gov.in/OON/index.jsp)

## Key Features

- AI-powered conversational interface for ARGO float data queries.  
- Interactive dashboard for visualization of float measurements (temperature, salinity, depth, etc.).  
- Knowledge graph integration linking floats, locations, and temporal data.  
- Real-time and localized insights for oceanographic analysis.  
- Modular architecture for future expansion with new datasets or AI models.  

## Tech Stack

- **Backend:** Python, FastAPI  
- **Frontend:** ReactJS, TailwindCSS  
- **Database:** PostgreSQL / SQLite (for float metadata)  
- **AI & ML:** OpenAI GPT-based conversational model, NLP pipelines  
- **Visualization:** Plotly, D3.js (charts & graphs)  
- **Deployment:** Docker, Cloud hosting (AWS/GCP/Heroku)  

## Quick Start / Setup

1. **Clone the repository:**  
   ```bash
   git clone <GITHUB_REPO_LINK>
   cd floatchat
   ```
2. **Set up Virtual Environment**
```
python -m venv .venv
# Activate on Linux/Mac
source .venv/bin/activate
# Activate on Windows
.venv\Scripts\activate
```
3. **Install Dependencies**
```
pip install -r requirements.txt
```

4. **Run Backend**
```
uvicorn app.main:app --reload
```

5. **Run Frontend (React App)**
```
cd frontend
npm install
npm start
```
