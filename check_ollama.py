#!/usr/bin/env python3
"""
Check if Ollama is running and model is available
"""

import subprocess
import sys
import platform

def check_ollama_command():
    """Check if ollama command exists"""
    print("[1/3] Checking if Ollama command is available...")
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✓ Ollama found: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ Ollama command failed: {result.stderr}")
            return False
    except FileNotFoundError:
        print("✗ Ollama not found in PATH")
        print("\nTo install Ollama:")
        print("  - Windows: Download from https://ollama.ai")
        print("  - Mac: brew install ollama")
        print("  - Linux: curl https://ollama.ai/install.sh | sh")
        return False
    except Exception as e:
        print(f"✗ Error checking Ollama: {e}")
        return False

def check_ollama_running():
    """Check if Ollama server is running"""
    print("\n[2/3] Checking if Ollama server is running...")
    try:
        # Try to list available models
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✓ Ollama server is responding")
            print(result.stdout)
            return True
        else:
            print(f"✗ Ollama server not responding: {result.stderr}")
            print("\nTo start Ollama server, run:")
            print("  ollama serve")
            return False
    except subprocess.TimeoutExpired:
        print("✗ Ollama server timed out")
        return False
    except Exception as e:
        print(f"✗ Error checking Ollama: {e}")
        return False

def check_model_available():
    """Check if mistral model is available"""
    print("\n[3/3] Checking if mistral:7b-instruct-q4_0 model is available...")
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "mistral:7b-instruct-q4_0" in result.stdout or "mistral" in result.stdout:
            print("✓ Mistral model is available")
            print(result.stdout)
            return True
        else:
            print("✗ Mistral model not found")
            print("\nTo download the model, run:")
            print("  ollama pull mistral:7b-instruct-q4_0")
            print("\nOr pull latest mistral:")
            print("  ollama pull mistral")
            return False
    except Exception as e:
        print(f"✗ Error checking model: {e}")
        return False

def main():
    print("=" * 60)
    print("Ollama Configuration Check")
    print("=" * 60)
    
    cmd_ok = check_ollama_command()
    if not cmd_ok:
        print("\n❌ FAILED: Ollama is not installed")
        sys.exit(1)
    
    server_ok = check_ollama_running()
    if not server_ok:
        print("\n❌ FAILED: Ollama server is not running")
        print("\nFix: Start Ollama with 'ollama serve' in a terminal")
        sys.exit(1)
    
    model_ok = check_model_available()
    if not model_ok:
        print("\n⚠️  WARNING: Mistral model might not be available")
        print("\nFix: Run 'ollama pull mistral' to download")
    else:
        print("\n✅ SUCCESS: Ollama is configured correctly!")
        print("You can now run extractions.")

if __name__ == "__main__":
    main()
