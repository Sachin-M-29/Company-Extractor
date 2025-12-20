"""
Database Module
Stores extracted data in SQLite and vectors in FAISS for semantic search
"""

import sqlite3
import json
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CompanyDatabase:
    def __init__(self, db_path: str = "companies.db"):
        """
        Initialize SQLite database
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create tables if they don't exist"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Companies table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_name TEXT NOT NULL,
                    website TEXT UNIQUE,
                    logo_url TEXT,
                    short_description TEXT,
                    long_description TEXT,
                    industry TEXT,
                    sub_industry TEXT,
                    sector TEXT,
                    sic_code TEXT,
                    sic_text TEXT,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    raw_data JSON,
                    confidence REAL,
                    extraction_notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Social Media table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS social_media (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER NOT NULL,
                    linkedin TEXT,
                    facebook TEXT,
                    twitter TEXT,
                    instagram TEXT,
                    youtube TEXT,
                    blog TEXT,
                    articles TEXT,
                    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
                )
            """)
            
            # Products table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER NOT NULL,
                    product_name TEXT,
                    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
                )
            """)
            
            # Services table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER NOT NULL,
                    service_name TEXT,
                    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
                )
            """)
            
            # Certifications table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS certifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER NOT NULL,
                    certification_name TEXT,
                    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
                )
            """)
            
            # People table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS people (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER NOT NULL,
                    person_name TEXT,
                    title TEXT,
                    email TEXT,
                    profile_url TEXT,
                    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
                )
            """)
            
            # Metadata table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER NOT NULL,
                    scrape_url TEXT,
                    scrape_method TEXT,
                    content_length INTEGER,
                    processing_time_ms REAL,
                    raw_content TEXT,
                    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
                )
            """)
            
            # Create indexes for faster queries
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_website ON companies(website)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_company_name ON companies(company_name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_industry ON companies(industry)")
            
            conn.commit()
            conn.close()
            
            logger.info(f"Database initialized: {self.db_path}")
            
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise

    def insert_company(self, data: Dict[str, Any], scrape_url: str = "", 
                      scrape_method: str = "", content_length: int = 0,
                      processing_time: float = 0, raw_content: str = "") -> Optional[int]:
        """
        Insert extracted company data
        
        Args:
            data: Extracted company data dict
            scrape_url: URL that was scraped
            scrape_method: "static" or "playwright"
            content_length: Length of scraped content
            processing_time: Processing time in milliseconds
            raw_content: Original scraped content
            
        Returns:
            Company ID or None if failed
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insert company
            cursor.execute("""
                INSERT OR REPLACE INTO companies 
                (company_name, website, logo_url, short_description, long_description,
                 industry, sub_industry, sector, sic_code, sic_text,
                 email, phone, address, confidence, extraction_notes, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get("company_name"),
                data.get("website"),
                data.get("logo_url"),
                data.get("short_description"),
                data.get("long_description"),
                data.get("industry"),
                data.get("sub_industry"),
                data.get("sector"),
                data.get("sic_code"),
                data.get("sic_text"),
                data.get("email"),
                data.get("phone"),
                data.get("address"),
                data.get("confidence", 0),
                data.get("extraction_notes"),
                json.dumps(data)
            ))
            
            company_id = cursor.lastrowid
            
            # Insert social media
            cursor.execute("""
                INSERT INTO social_media 
                (company_id, linkedin, facebook, twitter, instagram, youtube, blog, articles)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                company_id,
                data.get("linkedin"),
                data.get("facebook"),
                data.get("twitter"),
                data.get("instagram"),
                data.get("youtube"),
                data.get("blog"),
                data.get("articles")
            ))
            
            # Insert products
            products = data.get("products", [])
            if products:
                for product in products:
                    cursor.execute("""
                        INSERT INTO products (company_id, product_name)
                        VALUES (?, ?)
                    """, (company_id, product))
            
            # Insert services
            services = data.get("services", [])
            if services:
                for service in services:
                    cursor.execute("""
                        INSERT INTO services (company_id, service_name)
                        VALUES (?, ?)
                    """, (company_id, service))
            
            # Insert certifications
            certifications = data.get("certifications", [])
            if certifications:
                for cert in certifications:
                    cursor.execute("""
                        INSERT INTO certifications (company_id, certification_name)
                        VALUES (?, ?)
                    """, (company_id, cert))
            
            # Insert people
            people = data.get("people", [])
            if people:
                for person in people:
                    cursor.execute("""
                        INSERT INTO people (company_id, person_name, title, email, profile_url)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        company_id,
                        person.get("name"),
                        person.get("title"),
                        person.get("email"),
                        person.get("profile_url")
                    ))
            
            # Insert metadata
            cursor.execute("""
                INSERT INTO metadata 
                (company_id, scrape_url, scrape_method, content_length, 
                 processing_time_ms, raw_content)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                company_id,
                scrape_url,
                scrape_method,
                content_length,
                processing_time,
                raw_content
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Inserted company: {data.get('company_name')} (ID: {company_id})")
            
            return company_id
            
        except Exception as e:
            logger.error(f"Error inserting company: {str(e)}")
            return None

    def get_company_by_website(self, website: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve company by website URL
        
        Args:
            website: Website URL
            
        Returns:
            Company data dict or None
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM companies WHERE website = ?
            """, (website,))
            
            row = cursor.fetchone()
            
            if row:
                # Get column names
                col_names = [description[0] for description in cursor.description]
                company_dict = dict(zip(col_names, row))
                
                # Get products
                cursor.execute("""
                    SELECT product_name FROM products WHERE company_id = ?
                """, (company_dict['id'],))
                
                products = [p[0] for p in cursor.fetchall()]
                company_dict['products'] = products
                
                conn.close()
                return company_dict
            
            conn.close()
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving company: {str(e)}")
            return None

    def search_by_industry(self, industry: str) -> List[Dict[str, Any]]:
        """
        Search companies by industry
        
        Args:
            industry: Industry name
            
        Returns:
            List of company dicts
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM companies WHERE industry LIKE ? ORDER BY confidence DESC
            """, (f"%{industry}%",))
            
            rows = cursor.fetchall()
            col_names = [description[0] for description in cursor.description]
            
            results = []
            for row in rows:
                company_dict = dict(zip(col_names, row))
                
                # Get products
                cursor.execute("""
                    SELECT product_name FROM products WHERE company_id = ?
                """, (company_dict['id'],))
                
                products = [p[0] for p in cursor.fetchall()]
                company_dict['products'] = products
                
                results.append(company_dict)
            
            conn.close()
            return results
            
        except Exception as e:
            logger.error(f"Error searching by industry: {str(e)}")
            return []

    def get_all_companies(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all companies with pagination"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM companies 
                ORDER BY created_at DESC 
                LIMIT ? OFFSET ?
            """, (limit, offset))
            
            rows = cursor.fetchall()
            col_names = [description[0] for description in cursor.description]
            
            results = []
            for row in rows:
                company_dict = dict(zip(col_names, row))
                
                cursor.execute("""
                    SELECT product_name FROM products WHERE company_id = ?
                """, (company_dict['id'],))
                
                products = [p[0] for p in cursor.fetchall()]
                company_dict['products'] = products

                cursor.execute("""
                    SELECT service_name FROM services WHERE company_id = ?
                """, (company_dict['id'],))
                services = [s[0] for s in cursor.fetchall()]
                company_dict['services'] = services

                cursor.execute("""
                    SELECT certification_name FROM certifications WHERE company_id = ?
                """, (company_dict['id'],))
                certifications = [c[0] for c in cursor.fetchall()]
                company_dict['certifications'] = certifications

                cursor.execute("""
                    SELECT person_name, title, email, profile_url FROM people WHERE company_id = ?
                """, (company_dict['id'],))
                people_rows = cursor.fetchall()
                company_dict['people'] = [
                    {
                        "name": pr[0],
                        "title": pr[1],
                        "email": pr[2],
                        "profile_url": pr[3],
                    }
                    for pr in people_rows
                ]

                cursor.execute("""
                    SELECT linkedin, facebook, twitter, instagram, youtube, blog, articles
                    FROM social_media WHERE company_id = ?
                """, (company_dict['id'],))
                social = cursor.fetchone()
                if social:
                    sm_fields = ["linkedin", "facebook", "twitter", "instagram", "youtube", "blog", "articles"]
                    for idx, field in enumerate(sm_fields):
                        company_dict[field] = social[idx]
                
                results.append(company_dict)
            
            conn.close()
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving companies: {str(e)}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM companies")
            total_companies = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(confidence) FROM companies")
            avg_confidence = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT COUNT(DISTINCT industry) FROM companies WHERE industry IS NOT NULL")
            unique_industries = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT industry, COUNT(*) as count 
                FROM companies 
                WHERE industry IS NOT NULL 
                GROUP BY industry 
                ORDER BY count DESC 
                LIMIT 5
            """)
            top_industries = {row[0]: row[1] for row in cursor.fetchall()}
            
            conn.close()
            
            return {
                "total_companies": total_companies,
                "avg_confidence": round(avg_confidence, 2),
                "unique_industries": unique_industries,
                "top_industries": top_industries
            }
            
        except Exception as e:
            logger.error(f"Error getting stats: {str(e)}")
            return {}


class FAISSVectorStore:
    """
    FAISS-based vector store for semantic search
    Requires: pip install faiss-cpu or faiss-gpu
    """
    
    def __init__(self, index_path: str = "companies.faiss", dimension: int = 384):
        """
        Initialize FAISS vector store
        
        Args:
            index_path: Path to FAISS index file
            dimension: Embedding dimension (384 for MiniLM, 768 for standard)
        """
        self.index_path = index_path
        self.dimension = dimension
        self.company_ids = []
        
        try:
            import faiss
            self.faiss = faiss
            self.index = self._load_or_create_index()
            logger.info(f"FAISS vector store initialized: {index_path}")
        except ImportError:
            logger.warning("FAISS not installed. Install with: pip install faiss-cpu")
            self.faiss = None
            self.index = None

    def _load_or_create_index(self):
        """Load existing FAISS index or create new one"""
        if os.path.exists(self.index_path):
            return self.faiss.read_index(self.index_path)
        else:
            return self.faiss.IndexFlatL2(self.dimension)

    def save_index(self):
        """Save FAISS index to disk"""
        if self.index:
            self.faiss.write_index(self.index, self.index_path)
            logger.info(f"FAISS index saved: {self.index_path}")

    def add_company_embedding(self, company_id: int, embedding: list):
        """
        Add company embedding to vector store
        
        Args:
            company_id: Company database ID
            embedding: 1D embedding vector
        """
        if not self.index:
            logger.warning("FAISS not initialized")
            return
        
        try:
            import numpy as np
            
            embedding_array = np.array([embedding], dtype=np.float32)
            self.index.add(embedding_array)
            self.company_ids.append(company_id)
            
        except Exception as e:
            logger.error(f"Error adding embedding: {str(e)}")

    def search(self, query_embedding: list, k: int = 5) -> List[tuple]:
        """
        Search for similar companies
        
        Args:
            query_embedding: Query embedding vector
            k: Number of results to return
            
        Returns:
            List of (company_id, distance) tuples
        """
        if not self.index or not self.company_ids:
            return []
        
        try:
            import numpy as np
            
            query_array = np.array([query_embedding], dtype=np.float32)
            distances, indices = self.index.search(query_array, min(k, len(self.company_ids)))
            
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx < len(self.company_ids):
                    results.append((self.company_ids[idx], float(distance)))
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching: {str(e)}")
            return []


if __name__ == "__main__":
    # Test database operations
    db = CompanyDatabase()
    
    # Test data
    test_data = {
        "company_name": "TechCorp AI",
        "industry": "Artificial Intelligence",
        "products": ["AI Analytics", "ML Platform"],
        "email": "sales@techcorp.ai",
        "phone": "+1-415-555-0100",
        "address": "San Francisco, CA",
        "website": "https://techcorp.ai",
        "description": "Leading AI solutions provider",
        "confidence": 0.85
    }
    
    # Insert
    company_id = db.insert_company(test_data, "https://techcorp.ai", "static", 15000, 2.5)
    
    # Retrieve
    if company_id:
        company = db.get_company_by_website("https://techcorp.ai")
        print(json.dumps(company, indent=2, default=str))
        
        # Stats
        stats = db.get_stats()
        print(f"\nDatabase Stats: {json.dumps(stats, indent=2)}")
