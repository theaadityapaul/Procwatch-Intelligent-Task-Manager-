# procwatch_logger.py
import psutil
import pandas as pd
import time
import os

LOG_FILE = "process_log.csv"

# --- PASTE THIS ENTIRE CORRECTED FUNCTION ---

# Function to log current process data to a CSV file
def log_process_data():
    processes_data = []
    # Note: We fetch memory_info directly in the loop now
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            # Get the process info dictionary
            proc_info = proc.info
            
            # *** THE FIX IS HERE ***
            # Check if memory_info exists and is not None before using it
            if proc_info['memory_info']:
                data = {
                    'timestamp': pd.Timestamp.now(),
                    'pid': proc_info['pid'],
                    'name': proc_info['name'],
                    'cpu_percent': proc_info['cpu_percent'],
                    # Now it's safe to access .rss
                    'memory_mb': proc_info['memory_info'].rss / (1024 * 1024)
                }
                processes_data.append(data)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # This will catch other potential errors with inaccessible processes
            pass
    
    df = pd.DataFrame(processes_data)
    
    if not os.path.exists(LOG_FILE):
        df.to_csv(LOG_FILE, index=False, header=True)
    else:
        df.to_csv(LOG_FILE, mode='a', index=False, header=False)
    
    print(f"Logged {len(df)} processes to {LOG_FILE}")
def analyze_logs():
    if not os.path.exists(LOG_FILE):
        print("Log file not found. Please run the logger first.")
        return
        
    df = pd.read_csv(LOG_FILE)
    
    # Calculate average CPU and Memory usage for each process
    # groupby('name') aggregates all data points for processes with the same name
    analysis = df.groupby('name').agg(
        avg_cpu=('cpu_percent', 'mean'),
        max_cpu=('cpu_percent', 'max'),
        avg_mem_mb=('memory_mb', 'mean'),
        max_mem_mb=('memory_mb', 'max')
    ).reset_index()

    print("\n--- Top 5 CPU Consumers (Average) ---")
    print(analysis.sort_values(by='avg_cpu', ascending=False).head(5))
    
    print("\n--- Top 5 Memory Consumers (Average) ---")
    print(analysis.sort_values(by='avg_mem_mb', ascending=False).head(5))

# Main function to run the logger
def main():
    print("Starting process logger. Press Ctrl+C to stop.")
    try:
        # Log data every 10 seconds for 5 cycles (50 seconds total)
        for i in range(5):
            log_process_data()
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nLogger stopped.")
    
    # After logging, run the analysis
    analyze_logs()

if __name__ == "__main__":
    main()