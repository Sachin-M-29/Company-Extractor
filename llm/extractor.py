"""
LLM Information Extractor
Uses Mistral or Phi-3 for structured data extraction from company websites
"""

import json
import logging
from typing import Optional, Dict, Any
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are an information extraction system for company websites.

Your task is to extract comprehensive structured company information from provided website text.

EXTRACTION RULES:
1. Extract ONLY information that exists in the text
2. If data is not found, return null (NOT empty string, NOT "N/A")
3. Output MUST be valid JSON
4. Do NOT hallucinate or invent information
5. Be precise and concise
6. For lists (products, services, certifications, people), extract all items found

FIELDS TO EXTRACT:

BASIC COMPANY INFO:
- company_name: Official company name
- website: The website URL you're analyzing
- logo_url: URL to company logo image
- short_description: Brief 1-2 sentence summary
- long_description: Detailed description (2-4 sentences)
- industry: Main industry (e.g., "Information Technology", "Healthcare")
- sub_industry: Specific sub-sector (e.g., "Web Development", "AI Development")
- sector: Broad sector classification (e.g., "Technology", "Healthcare")
- sic_code: Standard Industrial Classification code if mentioned
- sic_text: SIC description text

CONTACT INFORMATION:
- email: Contact email address (primary)
- phone: Phone number (include country code if available)
- address: Physical address or headquarters location

SOCIAL MEDIA:
- linkedin: LinkedIn company page URL
- facebook: Facebook page URL
- twitter: Twitter/X profile URL
- instagram: Instagram profile URL
- youtube: YouTube channel URL
- blog: Blog URL
- articles: Articles or news section URL

PRODUCTS & SERVICES:
- products: List of products offered (extract as many as found)
- services: List of services offered (extract as many as found)

CERTIFICATIONS:
- certifications: List of certifications, standards, compliance (e.g., "ISO 9001", "HIPAA", "GDPR", "SOC2")

PEOPLE:
- people: List of key people found with structure:
  [
    {
      "name": "Full Name",
      "title": "Job Title",
      "email": "email if available or null",
      "profile_url": "LinkedIn/profile URL or null"
    }
  ]

OUTPUT FORMAT:
Return ONLY valid JSON, no markdown or additional text:
{
  "company_name": "string or null",
  "website": "string or null",
  "logo_url": "string or null",
  "short_description": "string or null",
  "long_description": "string or null",
  "industry": "string or null",
  "sub_industry": "string or null",
  "sector": "string or null",
  "sic_code": "string or null",
  "sic_text": "string or null",
  "email": "string or null",
  "phone": "string or null",
  "address": "string or null",
  "linkedin": "string or null",
  "facebook": "string or null",
  "twitter": "string or null",
  "instagram": "string or null",
  "youtube": "string or null",
  "blog": "string or null",
  "articles": "string or null",
  "products": ["product1", "product2"] or null,
  "services": ["service1", "service2"] or null,
  "certifications": ["cert1", "cert2"] or null,
  "people": [{"name": "Name", "title": "Title", "email": null, "profile_url": null}] or null,
  "confidence": 0.0-1.0,
  "extraction_notes": "Any uncertainties or assumptions"
}

CONFIDENCE SCORING:
- 1.0: Comprehensive data extraction with most fields populated
- 0.7-0.9: Good extraction, key fields found, some secondary fields missing
- 0.4-0.6: Limited information found, basic fields only
- <0.4: Very limited or mostly null results

EXAMPLE:
Input: "AyaData is an AI company. CEO: Freddie Monk. COO: Ama Larbi Siaw. Services: AI annotation, data labeling. Certifications: ISO 9001, GDPR, SOC2. Email: info@ayadata.ai. LinkedIn: linkedin.com/company/aya-data"
Output: 
{
  "company_name": "AyaData",
  "website": "ayadata.ai",
  "logo_url": null,
  "short_description": "AI company specializing in data annotation.",
  "long_description": "AyaData is an AI company that provides AI annotation and data labeling services.",
  "industry": "Artificial Intelligence",
  "sub_industry": "AI Development",
  "sector": "Information Technology",
  "sic_code": null,
  "sic_text": null,
  "email": "info@ayadata.ai",
  "phone": null,
  "address": null,
  "linkedin": "linkedin.com/company/aya-data",
  "facebook": null,
  "twitter": null,
  "instagram": null,
  "youtube": null,
  "blog": null,
  "articles": null,
  "products": null,
  "services": ["AI annotation", "data labeling"],
  "certifications": ["ISO 9001", "GDPR", "SOC2"],
  "people": [
    {"name": "Freddie Monk", "title": "CEO", "email": null, "profile_url": null},
    {"name": "Ama Larbi Siaw", "title": "COO", "email": null, "profile_url": null}
  ],
  "confidence": 0.85,
  "extraction_notes": "Found key company info, leadership team, and certifications. Social media partially available."
}

Remember: Extract what EXISTS, don't hallucinate."""


class LLMExtractor:
    def __init__(self, model: str = "mistral:7b-instruct-q4_0", 
                 ollama_host: str = "http://localhost:11434"):
        """
        Initialize LLM Extractor
        
        Args:
            model: Model name in Ollama
            ollama_host: Ollama server URL
        """
        self.model = model
        self.ollama_host = ollama_host
        self.api_endpoint = f"{ollama_host}/api/generate"
        
        logger.info(f"Initialized LLM Extractor with model: {model}")

    def extract_from_text(self, text: str, url: str = "") -> Optional[Dict[str, Any]]:
        """
        Extract company information from text using LLM
        
        Args:
            text: Website text content
            url: Source URL (optional)
            
        Returns:
            Extracted data as dict or None if failed
        """
        try:
            # Truncate text if too long (token limit)
            max_tokens = 4000
            text = text[:max_tokens]
            
            user_prompt = f"""Extract company information from this website text:

TEXT:
{text}

{"WEBSITE_URL: " + url if url else ""}

Extract and return ONLY the JSON response, nothing else."""
            
            logger.info(f"Sending extraction request to LLM: {self.model}")
            
            response = requests.post(
                self.api_endpoint,
                json={
                    "model": self.model,
                    "prompt": user_prompt,
                    "system": SYSTEM_PROMPT,
                    "stream": False,
                    "temperature": 0.2,  # Very low temperature for consistent extraction
                    "top_p": 0.9,
                    "num_predict": 2000,  # Allow longer responses for comprehensive extraction
                },
                timeout=300  # 5 minutes for comprehensive extraction
            )
            
            response.raise_for_status()
            
            result = response.json()
            generated_text = result.get("response", "").strip()
            
            # Parse JSON response
            extracted_data = self._parse_json_response(generated_text)
            
            if extracted_data:
                logger.info("Successfully extracted company information")
                return extracted_data
            else:
                logger.warning("Failed to parse LLM response as JSON")
                return None
                
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama server. Make sure Ollama is running: ollama serve")
            return None
        except Exception as e:
            logger.error(f"Error during extraction: {str(e)}")
            return None

    @staticmethod
    def _parse_json_response(text: str) -> Optional[Dict[str, Any]]:
        """
        Parse JSON from LLM response (handles markdown code blocks)
        
        Args:
            text: LLM response text
            
        Returns:
            Parsed JSON dict or None
        """
        try:
            # Try direct JSON parse first
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON from markdown code block
        try:
            if "```json" in text:
                json_str = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                json_str = text.split("```")[1].split("```")[0].strip()
            else:
                # Try to find JSON object
                start = text.find("{")
                end = text.rfind("}") + 1
                if start != -1 and end > start:
                    json_str = text[start:end]
                else:
                    return None
            
            return json.loads(json_str)
        except (json.JSONDecodeError, IndexError):
            logger.warning("Could not parse JSON from LLM response")
            return None

    def batch_extract(self, texts_with_urls: list[tuple[str, str]]) -> list[Dict[str, Any]]:
        """
        Extract from multiple texts
        
        Args:
            texts_with_urls: List of (text, url) tuples
            
        Returns:
            List of extracted data dicts
        """
        results = []
        for text, url in texts_with_urls:
            result = self.extract_from_text(text, url)
            if result:
                results.append(result)
        
        return results


# Alternative: Using Hugging Face Transformers (if not using Ollama)
class HFExtractor:
    def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct-v0.2"):
        """
        Initialize with Hugging Face model
        Requires: pip install transformers bitsandbytes accelerate
        """
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            import torch
            
            logger.info(f"Loading Hugging Face model: {model_name}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                load_in_4bit=True,  # 4-bit quantization for RTX 2050
                device_map="auto",
            )
            
            logger.info("Model loaded successfully")
            
        except ImportError:
            logger.error("Install transformers: pip install transformers bitsandbytes accelerate")
            raise

    def extract_from_text(self, text: str, url: str = "") -> Optional[Dict[str, Any]]:
        """Extract company information using HF model"""
        try:
            text = text[:4000]
            
            user_prompt = f"""Extract company information from this website text:

TEXT:
{text}

{"WEBSITE_URL: " + url if url else ""}

Extract and return ONLY the JSON response:"""
            
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
            
            # Format for Mistral
            formatted_prompt = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            inputs = self.tokenizer(formatted_prompt, return_tensors="pt")
            
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=1024,
                temperature=0.3,
                top_p=0.9,
            )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract JSON from response
            extracted_data = LLMExtractor._parse_json_response(response)
            
            return extracted_data
            
        except Exception as e:
            logger.error(f"Error during HF extraction: {str(e)}")
            return None


if __name__ == "__main__":
    # Test extraction
    extractor = LLMExtractor()
    
    sample_text = """
    Welcome to TechCorp AI Solutions. We are a leading provider of artificial intelligence 
    and machine learning solutions for enterprises. Based in San Francisco, California, 
    we help companies transform their operations with AI.
    
    Contact us: sales@techcorp.ai | Phone: +1-415-555-0100
    
    Our products include:
    - AI Analytics Platform
    - Machine Learning Pipeline Builder
    - Enterprise NLP Solutions
    
    Visit us at 123 Tech Street, San Francisco, CA 94105
    """
    
    result = extractor.extract_from_text(sample_text, "https://techcorp.ai")
    
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("Extraction failed. Make sure Ollama is running: ollama serve")
