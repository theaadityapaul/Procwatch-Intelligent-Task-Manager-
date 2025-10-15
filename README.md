# 🖥️ ProcWatch: An Intelligent Process Monitoring & Management Tool

ProcWatch is a system utility built in Python that provides intelligent insights into system performance. It moves beyond standard, real-time monitors by logging historical process data to enable trend analysis and proactive resource management.

## ✨ Key Features
- **Live Process Monitoring:** A real-time dashboard of all active processes.
- **Historical Logging:** Saves performance data to `process_log.csv` for analysis.
- **Intelligent Focus Mode:** Proactively lowers the priority of background tasks to free up resources for your main application.
- **Interactive Dashboard:** A user-friendly web UI built with Streamlit.

## 🛠️ Technology Stack
- **Language:** Python 3
- **Core Libraries:**
    - `psutil`: For fetching process and system data.
    - `pandas`: For data manipulation and logging.
    - `streamlit`: For building the interactive web dashboard.

## 🚀 How to Run
1.  **Clone the repository:**
    `git clone <your-repo-link>`
2.  **Install dependencies:**
    `pip3 install -r requirements.txt`
3.  **(Optional) Generate historical data:**
    `python3 procwatch_logger.py`
4.  **Run the main dashboard:**
    `python3 -m streamlit run procwatch_dashboard.py`
