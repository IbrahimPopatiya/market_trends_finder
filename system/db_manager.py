import sqlite3
import os
from datetime import datetime

class DBManager:
    def __init__(self, db_path="data/mie_vault.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """
        Creates the tables if they don't exist.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Trends Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                topic TEXT NOT NULL,
                viral_score REAL,
                description TEXT,
                url TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Companies Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                origin_country TEXT,
                model_type TEXT,
                description TEXT,
                growth_signal TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Market Gaps & Strategic Playbook Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_gaps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER,
                target_market TEXT,
                viability_score REAL,
                adaptation_strategy TEXT, -- 7. How to Adapt
                execution_plan TEXT,      -- 8. Step-by-Step
                risks TEXT,               -- 9. Risks
                final_verdict TEXT,       -- 10. Final Verdict
                full_report TEXT,         -- The entire 10-point text
                FOREIGN KEY (company_id) REFERENCES companies (id)
            )
        """)
        
        conn.commit()
        conn.close()

    def add_trend(self, trend_dict):
        """
        Adds a single trend discovery.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO trends (platform, topic, viral_score, description, url)
            VALUES (?, ?, ?, ?, ?)
        """, (
            trend_dict.get("platform"),
            trend_dict.get("topic"),
            trend_dict.get("viral_score"),
            trend_dict.get("description"),
            trend_dict.get("url")
        ))
        conn.commit()
        conn.close()

    def add_company(self, company_dict):
        """
        Adds a discovered company/startup.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO companies (name, origin_country, model_type, description, growth_signal)
            VALUES (?, ?, ?, ?, ?)
        """, (
            company_dict.get("name"),
            company_dict.get("origin_country"),
            company_dict.get("model_type"),
            company_dict.get("description"),
            company_dict.get("growth_signal")
        ))
        conn.commit()
        conn.close()

    def get_all_trends(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trends ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def save_market_gap(self, gap_dict):
        """
        Saves a full 10-point analysis report.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 1. Ensure company exists
        self.add_company({
            "name": gap_dict.get("name"),
            "origin_country": gap_dict.get("origin_country"),
            "model_type": "D2C/SaaS",  # Generic for now
            "description": gap_dict.get("description"),
            "growth_signal": gap_dict.get("growth_signal")
        })
        
        # 2. Get company ID
        cursor.execute("SELECT id FROM companies WHERE name = ?", (gap_dict.get("name"),))
        res = cursor.fetchone()
        if not res:
             return
        company_id = res[0]
        
        # 3. Insert Gap Analysis
        cursor.execute("""
            INSERT INTO market_gaps (
                company_id, target_market, viability_score, 
                adaptation_strategy, execution_plan, risks, 
                final_verdict, full_report
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            company_id,
            "India",
            gap_dict.get("viability_score"),
            gap_dict.get("adaptation_strategy"),
            gap_dict.get("execution_plan"),
            gap_dict.get("risks"),
            gap_dict.get("final_verdict"),
            gap_dict.get("full_report")
        ))
        
        conn.commit()
        conn.close()
        print(f"[DB] Successfully saved Gap Analysis for {gap_dict.get('name')}")
