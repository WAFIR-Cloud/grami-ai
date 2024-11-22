#!/usr/bin/env python3
import asyncio
import multiprocessing
import subprocess
import sys
import os

def run_growth_manager():
    """Run the Growth Manager process."""
    os.chdir('/Users/ferasalawadi/PycharmProjects/grami-ai')
    subprocess.run([sys.executable, 'examples/growth_manager.py'], 
                   check=True)

def run_client():
    """Run the Client process."""
    os.chdir('/Users/ferasalawadi/PycharmProjects/grami-ai')
    subprocess.run([sys.executable, 'examples/client.py'], 
                   check=True)

def main():
    """
    Main function to run Growth Manager and Client concurrently.
    
    This script ensures that:
    1. Growth Manager starts first
    2. Client connects to the Growth Manager
    3. Both processes can be run and monitored
    """
    print("🚀 Starting Grami AI Framework 🚀")
    print("--------------------------------")
    
    # Create processes
    growth_manager_process = multiprocessing.Process(target=run_growth_manager)
    client_process = multiprocessing.Process(target=run_client)
    
    try:
        # Start Growth Manager first
        growth_manager_process.start()
        
        # Give Growth Manager a moment to start
        asyncio.run(asyncio.sleep(2))
        
        # Start Client
        client_process.start()
        
        # Wait for both processes to complete
        growth_manager_process.join()
        client_process.join()
    
    except Exception as e:
        print(f"Error running Grami AI Framework: {e}")
    
    finally:
        # Ensure all processes are terminated
        if growth_manager_process.is_alive():
            growth_manager_process.terminate()
        if client_process.is_alive():
            client_process.terminate()

if __name__ == '__main__':
    # Ensure multiprocessing works correctly on macOS
    multiprocessing.set_start_method('spawn')
    main()
