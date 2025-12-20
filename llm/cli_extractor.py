"""
CLI-based LLM extractor for when HTTP API has issues
Uses subprocess to call ollama run directly
"""

import json
import subprocess
import logging
from typing import Optional, Dict, Any
import re
import os

logger = logging.getLogger(__name__)


class CLIExtractor:
    """Extractor using Ollama CLI instead of HTTP API"""
    
    def __init__(self, model: str = "mistral:7b-instruct-q4_0", gpu_device: int = 0):
        self.model = model
        self.gpu_device = gpu_device
        
        # Set GPU environment for Ollama
        os.environ['CUDA_VISIBLE_DEVICES'] = str(gpu_device)
        os.environ['OLLAMA_NUM_GPU'] = '1'
        
        logger.info(f"Initialized CLI Extractor with model: {model}, GPU: {gpu_device}")
    
    def extract_from_text(self, text: str, url: str = "") -> Optional[Dict[str, Any]]:
        """Extract using ollama run command"""
        try:
            # Build prompt (limit text to 4000 chars for better extraction)
            max_text_len = 4000
            prompt = f"""You are a data extraction expert. Extract comprehensive company information from this website.

WEBSITE TEXT:
{text[:max_text_len]}

WEBSITE URL: {url}

IMPORTANT: Extract ONLY information that ACTUALLY appears in the text. DO NOT make up or infer information.

Return ONLY valid JSON wrapped in ```json code fences with these exact fields:

{{
  "company_name": "exact name from website",
  "website": "{url}",
  "logo_url": "logo URL if found, else null",
  "short_description": "1-2 sentence summary",
  "long_description": "detailed description (3-4 sentences)",
  "industry": "primary industry",
  "sub_industry": "specific sub-industry or null",
  "sector": "business sector or null",
  "email": "contact email if found",
  "phone": "phone number if found",
  "address": "physical address if found",
  "linkedin": "LinkedIn URL if found",
  "facebook": "Facebook URL if found",
  "twitter": "Twitter URL if found",
  "instagram": "Instagram URL if found",
  "youtube": "YouTube URL if found",
  "products": ["product1", "product2"],
  "services": ["service1", "service2"],
  "certifications": ["cert1", "cert2"],
  "people": [
    {{"name": "Full Name", "title": "Job Title", "email": "email@example.com", "profile_url": "linkedin.com/in/person"}}
  ],
  "confidence": 0.85,
  "extraction_notes": "brief notes about data quality"
}}

EXTRACT ONLY WHAT YOU SEE. Return JSON only."""

            logger.info(f"Running CLI extraction with {self.model} on GPU {self.gpu_device}")
            
            # Set environment for GPU acceleration
            env = os.environ.copy()
            env['CUDA_VISIBLE_DEVICES'] = str(self.gpu_device)
            env['OLLAMA_NUM_GPU'] = '1'
            
            # Call ollama via subprocess with GPU env
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
                timeout=300,  # 5 minutes for enriched runs with GPU
                env=env
            )
            
            if result.returncode != 0:
                logger.error(f"CLI command failed: {result.stderr}")
                return None
            
            response = result.stdout.strip()
            
            # Parse JSON from response
            # Sometimes model wraps in ```json blocks
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_text = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                json_text = response[json_start:json_end].strip()
            elif response.startswith("{"):
                json_text = response
            else:
                # Try to find JSON object in response
                start_idx = response.find("{")
                end_idx = response.rfind("}") + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_text = response[start_idx:end_idx]
                else:
                    logger.error("No JSON found in response")
                    return None
            
            # Parse JSON
            try:
                data = json.loads(json_text)
            except json.JSONDecodeError:
                # Attempt light sanitization: normalize quotes, escape backslashes, remove trailing commas
                s = json_text.strip()
                # Clip to outermost {}
                start = s.find('{'); end = s.rfind('}')
                if start != -1 and end > start:
                    s = s[start:end+1]
                # Normalize curly quotes
                s = s.replace('“','"').replace('”','"').replace('’',"'")
                # Remove trailing commas before } or ]
                s = re.sub(r",\s*([}\]])", r"\1", s)
                # If single quotes dominate, switch to double quotes
                if s.count('"') < s.count("'"):
                    s = s.replace("'", '"')
                # Escape backslashes
                s = s.replace('\\', r'\\')
                data = json.loads(s)
            logger.info("Successfully extracted company information")
            return data
            
        except subprocess.TimeoutExpired:
            logger.error("CLI extraction timed out")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            logger.debug(f"Response was: {response[:500]}")
            return None
        except Exception as e:
            logger.error(f"Error during CLI extraction: {e}")
            return None


if __name__ == "__main__":
    # Test
    extractor = CLIExtractor()
    test_text = "AyaData is an AI annotation company. CEO: Freddie Monk. Email: info@ayadata.ai. Services: AI labeling, data annotation. Certifications: ISO 9001, GDPR."
    result = extractor.extract_from_text(test_text, "ayadata.ai")
    
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("Extraction failed")
