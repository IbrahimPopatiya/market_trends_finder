import os
import sys
import argparse
from system.orchestrator import Orchestrator
from system.playbook_builder import PlaybookBuilder

def main():
    parser = argparse.ArgumentParser(description="Market Intelligence Engine Workflow Runner")
    parser.add_argument("workflow", help="Name of the workflow to run (without .md extension)")
    args = parser.parse_args()

    # Determine workspace root (current directory)
    workspace_root = os.getcwd()
    
    orchestrator = Orchestrator(workspace_root)
    
    print(f"--- Starting Workflow: {args.workflow} ---")
    
    # 1. Initialize Sandbox
    run_path, timestamp = orchestrator.initialize_run(args.workflow)
    print(f"Run directory created: {run_path}")
    
    # 2. Execute in Docker (Optional: skip if docker is not running, for simulation)
    # For this demo, let's assume we WANT to run it, but we handle errors gracefully.
    try:
        # Check if Docker image exists, if not build it
        # subprocess.run(["docker", "build", "-t", "mie-agent:latest", "."], check=True)
        
        # This part requires Docker to be installed and running.
        # Since I am an AI, I can't guarantee Docker is available in the user's environment.
        # However, the code is structured correctly to use it.
        exit_code = orchestrator.run_docker_container(run_path, args.workflow)
        print(f"Workflow finished with exit code {exit_code}")
        
    except Exception as e:
        print(f"Execution Error (Make sure Docker is running): {e}")

    # 3. Synchronize Back & Persist
    orchestrator.sync_back(run_path)
    
    # 4. Phase 3: Auto-generate Playbook
    print(f"--- Generating Replication Playbook ---")
    builder = PlaybookBuilder(workspace_root)
    # The workflow name is a good proxy for the company/topic name for now
    # In a more advanced version, we'd extract the company name from the DB result
    builder.generate_playbook(args.workflow)
    
    print(f"--- Workflow Execution Finished ---")

if __name__ == "__main__":
    main()
