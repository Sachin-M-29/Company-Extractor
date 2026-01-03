"""
Hugging Face Transformers-based LLM extractor
Uses Mistral 7B Instruct model via Transformers library (no Ollama needed)
"""

import json
import logging
from typing import Optional, Dict, Any
import re
import torch

# Import Transformers
from transformers import AutoModelForCausalLM, AutoTokenizer

logger = logging.getLogger(__name__)


class HFExtractor:
    """Extractor using Hugging Face Transformers with Mistral 7B"""
    
    def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct-v0.1", use_gpu: bool = True):
        """Initialize HF extractor with Mistral model
        
        Args:
            model_name: HuggingFace model ID
            use_gpu: Whether to use GPU if available
        """
        self.model_name = model_name
        self.use_gpu = use_gpu and torch.cuda.is_available()
        self.device = "cuda" if self.use_gpu else "cpu"
        
        logger.info(f"Loading model {model_name} on {self.device}")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Load model with 8-bit quantization for efficiency (if available)
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if self.use_gpu else torch.float32,
                device_map="auto" if self.use_gpu else None,
                load_in_8bit=self.use_gpu  # 8-bit quantization for memory efficiency
            )
        except Exception as e:
            logger.warning(f"Could not load with 8-bit, loading normally: {e}")
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if self.use_gpu else torch.float32,
            )
            if self.use_gpu:
                self.model = self.model.to(self.device)
        
        logger.info(f"Model loaded successfully on {self.device}")
    
    def extract_from_text(self, text: str, url: str = "") -> Optional[Dict[str, Any]]:
        """Extract company information using Mistral 7B Instruct
        
        Args:
            text: Website content to extract from
            url: Website URL for context
            
        Returns:
            Dict with extracted company information or None if extraction fails
        """
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

            logger.info(f"Extracting from URL: {url}")
            
            # Tokenize with attention mask
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=4096,
                padding=True
            )
            
            if self.use_gpu:
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=1024,
                    temperature=0.3,  # Lower temperature for more consistent extraction
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    attention_mask=inputs.get("attention_mask")
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract the part after the prompt
            if prompt in response:
                response = response.split(prompt)[-1].strip()
            
            logger.info(f"Model response received, parsing JSON...")
            
            # Parse JSON from response
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
                start = s.find('{')
                end = s.rfind('}')
                if start != -1 and end > start:
                    s = s[start:end+1]
                # Normalize curly quotes
                s = s.replace('"', '"').replace('"', '"').replace(''', "'")
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
            
        except torch.cuda.OutOfMemoryError:
            logger.error("GPU out of memory during extraction")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            return None
        except Exception as e:
            logger.error(f"Extraction error: {e}")
            return None
