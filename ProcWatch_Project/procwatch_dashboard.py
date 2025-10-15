# procwatch_dashboard.py
import streamlit as st
import pandas as pd
import psutil
import time

# Set the page title and a wide layout
st.set_page_config(page_title="ProcWatch Dashboard", layout="wide")

st.title("🖥️ ProcWatch - Real-Time Process Dashboard")
st.write("An intelligent tool to monitor, analyze, and manage system processes.")

# --- Helper Functions ---
def get_process_df():
    """Gets current process info and returns as a pandas DataFrame."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        processes.append(proc.info)
    return pd.DataFrame(processes)

# --- Main Dashboard Layout ---

# Create two columns for layout
col1, col2 = st.columns([3, 2]) # Main content is 3 parts, sidebar is 2

with col1:
    st.header("Active Processes")
    
    # Add a placeholder for live updates
    placeholder = st.empty()
    
    # Continuously update the process list
    while True:
        df = get_process_df()
        df = df.sort_values(by='cpu_percent', ascending=False)
        with placeholder.container():
            st.dataframe(df, height=500, use_container_width=True)
        time.sleep(2) # Refresh every 2 seconds


with col2:
    st.header("Process Management")
    
    pid_to_manage = st.text_input("Enter PID to Kill or Inspect:", help="Enter a Process ID (PID) from the table on the left.")
    
    if st.button("Inspect Process 🔍"):
        if pid_to_manage:
            try:
                proc = psutil.Process(int(pid_to_manage))
                st.success(f"Details for PID {pid_to_manage} ({proc.name()})")
                st.json({
                    "PID": proc.pid,
                    "Name": proc.name(),
                    "Status": proc.status(),
                    "CPU %": proc.cpu_percent(interval=0.1),
                    "Memory (MB)": proc.memory_info().rss / 1024 / 1024,
                })
            except (psutil.NoSuchProcess, ValueError):
                st.error("Invalid or non-existent PID.")
        else:
            st.warning("Please enter a PID.")
            
    if st.button("Terminate Process ❌", type="primary"):
        st.warning("Warning: Terminating processes can be risky.", icon="⚠️")
        if pid_to_manage:
            try:
                proc = psutil.Process(int(pid_to_manage))
                proc.terminate()
                st.success(f"Termination signal sent to PID {pid_to_manage}.")
                # A short delay to allow the main table to refresh
                time.sleep(1)
            except psutil.AccessDenied:
                st.error("Access Denied. Cannot terminate this process.")
            except (psutil.NoSuchProcess, ValueError):
                st.error("Invalid or non-existent PID.")
        else:
            st.warning("Please enter a PID.")

# Add a section for historical analysis from the log file
st.header("Historical Performance Analysis")
st.write("This section analyzes the `process_log.csv` file created by the logger.")

try:
    log_df = pd.read_csv("process_log.csv")
    
    # Create a selector to choose a process to analyze
    process_names = log_df['name'].unique()
    selected_process = st.selectbox("Select a process to visualize:", process_names)
    
    if selected_process:
        # Filter data for the selected process
        process_data = log_df[log_df['name'] == selected_process]
        process_data['timestamp'] = pd.to_datetime(process_data['timestamp'])
        
        st.subheader(f"Memory Usage Over Time for `{selected_process}`")
        st.line_chart(process_data.set_index('timestamp')['memory_mb'])
        
        st.subheader(f"CPU Usage Over Time for `{selected_process}`")
        st.line_chart(process_data.set_index('timestamp')['cpu_percent'])
        
except FileNotFoundError:
    st.info("Run `procwatch_logger.py` to generate a log file for analysis.")