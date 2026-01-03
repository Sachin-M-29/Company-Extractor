"""
Transformers-based LLM extractor using Hugging Face models
Uses Mistral 7B via Transformers library
Compatible with Hugging Face Spaces deployment
"""

import json
import logging
from typing import Optional, Dict, Any
import re
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

logger = logging.getLogger(__name__)


class CLIExtractor:
    """Extractor using Transformers (Mistral 7B)"""
    
    def __init__(self, model: str = "mistralai/Mistral-7B-Instruct-v0.1", gpu_device: int = 0):
        """Initialize Mistral model via Transformers"""
        self.model_name = model
        self.gpu_device = gpu_device
        self.device = f"cuda:{gpu_device}" if torch.cuda.is_available() else "cpu"
        
        logger.info(f"Loading model {model} on device {self.device}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                model,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map=self.device,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            logger.info(f"Model loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def extract_from_text(self, text: str, url: str = "") -> Optional[Dict[str, Any]]:
        """Extract using Transformers model"""
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

            logger.info(f"Running Transformers extraction on {self.device}")
            
            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs["input_ids"],
                    max_length=2000,
                    temperature=0.3,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Remove the prompt from the output
            if prompt in response:
                response = response.split(prompt)[-1].strip()
            
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
                # Attempt light sanitization
                s = json_text.strip()
                start = s.find('{')
                end = s.rfind('}')
                if start != -1 and end > start:
                    s = s[start:end+1]
                s = s.replace('"', '"').replace('"', '"').replace(''', "'")
                s = re.sub(r",\s*([}\]])", r"\1", s)
                if s.count('"') < s.count("'"):
                    s = s.replace("'", '"')
                s = s.replace('\\', r'\\')
                data = json.loads(s)
            
            logger.info("Successfully extracted company information")
            return data
            
        except torch.cuda.OutOfMemoryError:
            logger.error("GPU out of memory during extraction")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            logger.debug(f"Response was: {response[:500] if 'response' in locals() else 'No response'}")
            return None
        except Exception as e:
            logger.error(f"Error during Transformers extraction: {e}")
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
