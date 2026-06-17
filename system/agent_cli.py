import os
import sys
import argparse
from dotenv import load_dotenv
from openai import OpenAI

# Load .env if available (local dev), otherwise rely on container env vars
load_dotenv("/run/.env", override=False)

def analyze_business_model(data_summary):
    """
    Uses OpenAI to analyze the business model of the discovered data.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Warning: OpenAI API Key not found. Skipping analysis."

    client = OpenAI(api_key=api_key)
    
    prompt = f"""
    You are a startup analyst specializing in US to India replication opportunities.
    Analyze the following market intelligence data and provide a detailed 10-point report:
    
    DATA:
    {data_summary}
    
    STRUCTURE:
    1. Company / Idea Name:
    2. Origin Country:
    3. What They Do (simple explanation):
    4. Why It Is Growing (data-backed reasoning, trends, user behavior):
    5. Current Presence in India (None / Weak / Emerging):
    6. Copy Opportunity Score (1–10):
    7. How to Adapt for India:
       - Pricing strategy
       - Distribution/channel
       - Cultural/local changes
    8. Step-by-Step Execution Plan:
       - Step 1:
       - Step 2:
       - Step 3:
    9. Risks & Challenges:
    10. Final Verdict (Is it worth building in India? Why?)
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during AI analysis: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="MIE Agent CLI")
    parser.add_argument("--workflow", help="Path to the workflow file")
    args = parser.parse_args()

    print(f"--- Agent CLI Started (Phase 2 Intelligence) ---")
    
    if args.workflow:
        print(f"Executing workflow: {args.workflow}")
        with open(args.workflow, 'r') as f:
            workflow_content = f.read()
            print("Workflow Loaded.")
    
    # Simulate Discovery
    # In a real scenario, this would call specialized scrapers from /app/utils/
    discovery_summary = "Discovered a US-based D2C Brand 'GlowScale' focusing on custom skincare routines. Growing 50% MoM on TikTok."
    
    print("\n[STRETCH] Analyzing Discovery with OpenAI...")
    analysis = analyze_business_model(discovery_summary)
    print("\n--- AI ANALYSIS RESULTS ---")
    print(analysis)
    print("---------------------------\n")

    # Save Results to Run folder
    run_results_path = "/run/results.txt"
    with open(run_results_path, "w") as f:
        f.write(f"Discovery: {discovery_summary}\n\nAnalysis:\n{analysis}")

    print("Agent execution completed successfully.")
    print(f"--- Agent CLI Finished ---")

if __name__ == "__main__":
    main()
