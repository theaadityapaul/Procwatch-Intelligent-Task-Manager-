# procwatch_cli.py
import psutil
import os

# Function to list all running processes with key details [cite: 38]
def list_processes():
    print(f"{'PID':>7} {'%CPU':>5} {'%MEM':>5} {'Name':<30}")
    print("-" * 50)
    
    # Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            # Format and print process information
            pid = proc.info['pid']
            name = proc.info['name']
            cpu = proc.info['cpu_percent']
            mem = proc.info['memory_percent']
            print(f"{pid:>7} {cpu:5.1f} {mem:5.1f} {name:<30}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass # Ignore processes that have terminated or are inaccessible

# Function to get detailed information for a specific process [cite: 39]
def inspect_process(pid):
    try:
        proc = psutil.Process(pid)
        print("\n--- Detailed Process Information ---")
        print(f"  PID: {proc.pid}")
        print(f"  Name: {proc.name()}")
        print(f"  Status: {proc.status()}")
        print(f"  CPU Usage: {proc.cpu_percent(interval=1.0)}%")
        print(f"  Memory Info: {proc.memory_info().rss / 1024 / 1024:.2f} MB")
        print(f"  Username: {proc.username()}")
        print(f"  Executable: {proc.exe()}")
        print("----------------------------------\n")
    except psutil.NoSuchProcess:
        print(f"Error: No process with PID {pid} found.")

# Function to terminate a process [cite: 39]
def kill_process(pid):
    # IMPORTANT: Terminating processes can cause data loss or system instability.
    try:
        proc = psutil.Process(pid)
        proc_name = proc.name()
        # Send a termination signal
        proc.terminate() 
        print(f"Success: Sent termination signal to process {pid} ({proc_name}).")
    except psutil.NoSuchProcess:
        print(f"Error: No process with PID {pid} found.")
    except psutil.AccessDenied:
        # This will happen if you try to kill a system process without admin rights
        print(f"Error: Access denied. You may need to run this script with 'sudo'.")

# Main menu to run the tool
def main():
    while True:
        print("\n===== ProcWatch CLI Menu =====")
        print("1. List all processes")
        print("2. Inspect a process by PID")
        print("3. Kill a process by PID")
        print("q. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            list_processes()
        elif choice == '2':
            try:
                pid = int(input("Enter the PID to inspect: "))
                inspect_process(pid)
            except ValueError:
                print("Invalid PID. Please enter a number.")
        elif choice == '3':
            try:
                pid = int(input("Enter the PID to kill: "))
                kill_process(pid)
            except ValueError:
                print("Invalid PID. Please enter a number.")
        elif choice.lower() == 'q':
            print("Exiting ProcWatch.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()