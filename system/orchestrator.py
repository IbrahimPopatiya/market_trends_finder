import os
import shutil
import subprocess
import re
from datetime import datetime
from system.db_manager import DBManager

class Orchestrator:
    def __init__(self, workspace_root):
        self.workspace_root = os.path.abspath(workspace_root)
        self.projects_dir = os.path.join(self.workspace_root, "projects")
        self.runs_dir = os.path.join(self.workspace_root, "runs")
        self.utils_dir = os.path.join(self.workspace_root, "utils")
        self.master_req_file = os.path.join(self.workspace_root, "requirements.txt")

    def initialize_run(self, workflow_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_name = f"{workflow_name}_{timestamp}"
        run_path = os.path.join(self.runs_dir, workflow_name, timestamp)
        
        os.makedirs(run_path, exist_ok=True)
        os.makedirs(os.path.join(run_path, "utils"), exist_ok=True)
        
        # 1. Copy workflow file
        workflow_file = os.path.join(self.projects_dir, f"{workflow_name}.md")
        if os.path.exists(workflow_file):
            shutil.copy(workflow_file, run_path)
            print(f"Copied workflow: {workflow_file} -> {run_path}")
        else:
            print(f"Warning: Workflow file {workflow_file} not found.")

        # 2. Copy existing utils (master -> run)
        if os.path.exists(self.utils_dir):
            for item in os.listdir(self.utils_dir):
                s = os.path.join(self.utils_dir, item)
                d = os.path.join(run_path, "utils", item)
                if os.path.isfile(s):
                    shutil.copy2(s, d)
            print(f"Synchronized existing utils to run directory.")

        # 3. Copy requirements (master -> run)
        if os.path.exists(self.master_req_file):
            shutil.copy(self.master_req_file, run_path)
            print(f"Synchronized requirements to run directory.")

        return run_path, timestamp

    def run_docker_container(self, run_path, workflow_name):
        print(f"Launching Docker container for {workflow_name}...")
        
        # Ensure image is built
        # subprocess.run(["docker", "build", "-t", "mie-agent:latest", "."], cwd=self.workspace_root, check=True)
        
        # Run container with volume mount
        # Note: We mount the run_path to /run inside the container
        # Note: We use absolute path for mounting
        abs_run_path = os.path.abspath(run_path)
        abs_env_path = os.path.join(self.workspace_root, ".env")
        
        # We mount the run_path to /run and the .env file if it exists
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{abs_run_path}:/run",
        ]
        
        if os.path.exists(abs_env_path):
            cmd.extend(["-v", f"{abs_env_path}:/run/.env"])
            print("Mounting .env for OpenAI Authentication.")
        
        cmd.extend([
            "mie-agent:latest",
            "--workflow", f"/run/{workflow_name}.md"
        ])
        
        print(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error during execution: {result.stderr}")
        else:
            print(f"Execution Output:\n{result.stdout}")
        
        return result.returncode

    def sync_back(self, run_path):
        print(f"Starting post-execution synchronization...")

        # 1. Sync Utils (Run -> Master)
        run_utils_dir = os.path.join(run_path, "utils")
        if os.path.exists(run_utils_dir):
            for item in os.listdir(run_utils_dir):
                s = os.path.join(run_utils_dir, item)
                d = os.path.join(self.utils_dir, item)
                if os.path.isfile(s):
                    if not os.path.exists(d):
                        print(f"Found new tool! Merging: {item} -> master utils/")
                        shutil.copy2(s, d)
                    else:
                        # Existing file, might want to check for updates or versioning
                        # For now, we'll just skip to prevent overwriting master blindly
                        print(f"Skill '{item}' already exists in master workspace. Skipping.")

        # 2. Sync Requirements (Run -> Master)
        run_req_file = os.path.join(run_path, "requirements.txt")
        if os.path.exists(run_req_file):
            with open(self.master_req_file, 'r') as f:
                master_requirements = set(line.strip() for line in f if line.strip())
            
            with open(run_req_file, 'r') as f:
                run_requirements = set(line.strip() for line in f if line.strip())

            new_requirements = run_requirements - master_requirements
            
            if new_requirements:
                print(f"Found new dependencies! Adding: {', '.join(new_requirements)} to master requirements.txt")
                with open(self.master_req_file, 'a') as f:
                    for req in sorted(new_requirements):
                        f.write(f"{req}\n")
        # 3. Parse and Save 10-point report (Phase 3 Persistence)
        run_results_file = os.path.join(run_path, "results.txt")
        if os.path.exists(run_results_file):
            print(f"Parsing 10-point intelligence report...")
            with open(run_results_file, 'r') as f:
                content = f.read()
            
            # Simple extractor for the 10 points
            def extract_point(point_num, next_point_num, text):
                pattern = rf"{point_num}\.(.*?)(?={next_point_num}\.|$)"
                match = re.search(pattern, text, re.DOTALL)
                return match.group(1).strip() if match else ""

            gap_data = {
                "name": extract_point(1, 2, content),
                "origin_country": extract_point(2, 3, content),
                "description": extract_point(3, 4, content),
                "growth_signal": extract_point(4, 5, content),
                "viability_score": float(re.search(r"(\d+)", extract_point(6, 7, content)).group(1)) if re.search(r"(\d+)", extract_point(6, 7, content)) else 5.0,
                "adaptation_strategy": extract_point(7, 8, content),
                "execution_plan": extract_point(8, 9, content),
                "risks": extract_point(9, 10, content),
                "final_verdict": extract_point(10, 11, content),
                "full_report": content
            }
            
            db = DBManager()
            db.save_market_gap(gap_data)

        print("Synchronization completed.")
