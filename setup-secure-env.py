#!/usr/bin/env python3
"""
Secure Environment Variable Setup
Advanced security practices for GitHub token management
"""

import os
import sys
import getpass
import json
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecureEnvManager:
    def __init__(self):
        self.env_file = Path.home() / '.github_analytics_env'
        self.key_file = Path.home() / '.github_analytics_key'
        
    def generate_key(self, password: str) -> bytes:
        """Generate encryption key from password"""
        password_bytes = password.encode()
        salt = b'github_analytics_salt_2024'  # In production, use random salt
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        return key
    
    def encrypt_data(self, data: dict, password: str) -> None:
        """Encrypt and save environment data"""
        key = self.generate_key(password)
        fernet = Fernet(key)
        
        # Convert data to JSON and encrypt
        json_data = json.dumps(data).encode()
        encrypted_data = fernet.encrypt(json_data)
        
        # Save encrypted data
        with open(self.env_file, 'wb') as f:
            f.write(encrypted_data)
        
        # Set restrictive permissions
        os.chmod(self.env_file, 0o600)  # Read/write for owner only
        
        print(f"✅ Encrypted environment data saved to {self.env_file}")
    
    def decrypt_data(self, password: str) -> dict:
        """Decrypt and load environment data"""
        if not self.env_file.exists():
            raise FileNotFoundError("No encrypted environment file found")
        
        key = self.generate_key(password)
        fernet = Fernet(key)
        
        # Load and decrypt data
        with open(self.env_file, 'rb') as f:
            encrypted_data = f.read()
        
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            raise ValueError("Invalid password or corrupted data") from e
    
    def setup_secure_env(self):
        """Interactive setup of secure environment variables"""
        print("🔐 Secure GitHub Analytics Environment Setup")
        print("=" * 50)
        
        # Get GitHub credentials
        username = input("Enter your GitHub username: ").strip()
        
        print("\n📝 GitHub Token Setup:")
        print("1. Go to: https://github.com/settings/tokens")
        print("2. Click 'Generate new token (classic)'")
        print("3. Select scopes: public_repo, read:user, read:org")
        print("4. Copy the token (starts with 'ghp_')")
        print()
        
        token = getpass.getpass("Enter your GitHub token (hidden): ").strip()
        
        if not token.startswith('ghp_'):
            print("⚠️ Warning: Token doesn't start with 'ghp_' - make sure it's correct")
        
        # Get encryption password
        print("\n🔒 Encryption Setup:")
        print("Choose a strong password to encrypt your credentials locally")
        
        while True:
            password = getpass.getpass("Enter encryption password: ").strip()
            confirm = getpass.getpass("Confirm encryption password: ").strip()
            
            if password == confirm:
                if len(password) < 8:
                    print("❌ Password must be at least 8 characters")
                    continue
                break
            else:
                print("❌ Passwords don't match")
        
        # Save encrypted data
        env_data = {
            'GITHUB_USERNAME': username,
            'GITHUB_TOKEN': token,
            'SETUP_DATE': str(Path.ctime(Path.now())),
            'VERSION': '1.0'
        }
        
        self.encrypt_data(env_data, password)
        
        # Create loader script
        self.create_loader_script()
        
        print("\n✅ Secure environment setup completed!")
        print(f"📁 Encrypted file: {self.env_file}")
        print("🔧 Use 'source load_env.sh' to load variables")
    
    def create_loader_script(self):
        """Create script to load environment variables"""
        loader_script = """#!/bin/bash
# Secure Environment Loader for GitHub Analytics
# Usage: source load_env.sh

echo "🔐 Loading secure GitHub Analytics environment..."

# Check if Python script exists
if [ ! -f "setup-secure-env.py" ]; then
    echo "❌ setup-secure-env.py not found"
    return 1
fi

# Load environment variables
eval $(python3 -c "
import sys
sys.path.append('.')
from setup_secure_env import SecureEnvManager
import getpass

try:
    manager = SecureEnvManager()
    password = getpass.getpass('Enter encryption password: ')
    data = manager.decrypt_data(password)
    
    for key, value in data.items():
        if key.startswith('GITHUB_'):
            print(f'export {key}=\"{value}\"')
    
    print('echo \"✅ Environment variables loaded successfully\"')
except Exception as e:
    print(f'echo \"❌ Failed to load environment: {e}\"')
    print('return 1')
")

echo "🚀 Ready to run: python run-analytics.py"
"""
        
        with open('load_env.sh', 'w') as f:
            f.write(loader_script)
        
        os.chmod('load_env.sh', 0o755)  # Make executable
        print("📜 Created load_env.sh script")
    
    def load_env_variables(self):
        """Load environment variables for current session"""
        try:
            password = getpass.getpass("Enter encryption password: ")
            data = self.decrypt_data(password)
            
            # Set environment variables
            for key, value in data.items():
                if key.startswith('GITHUB_'):
                    os.environ[key] = value
            
            print("✅ Environment variables loaded for current session")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load environment: {e}")
            return False

def setup_dotenv_file():
    """Create .env file with secure practices"""
    print("\n📄 Alternative: .env File Setup")
    print("-" * 30)
    
    username = input("Enter your GitHub username: ").strip()
    token = getpass.getpass("Enter your GitHub token: ").strip()
    
    env_content = f"""# GitHub Analytics Environment Variables
# Keep this file secure and never commit to version control!

GITHUB_USERNAME={username}
GITHUB_TOKEN={token}

# Optional: Email notifications
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
# EMAIL_USER=your-email@gmail.com
# EMAIL_PASS=your-app-password
# NOTIFICATION_EMAIL=notifications@example.com
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    # Set restrictive permissions
    os.chmod('.env', 0o600)
    
    # Create .gitignore entry
    gitignore_entry = """
# Environment variables
.env
.github_analytics_env
.github_analytics_key
load_env.sh
"""
    
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'a') as f:
            f.write(gitignore_entry)
    else:
        with open('.gitignore', 'w') as f:
            f.write(gitignore_entry)
    
    print("✅ .env file created with secure permissions")
    print("✅ .gitignore updated to exclude sensitive files")
    print("\n🔧 To use .env file, install python-dotenv:")
    print("pip install python-dotenv")

def main():
    """Main setup function"""
    print("🛡️ GitHub Analytics - Advanced Security Setup")
    print("=" * 55)
    
    print("\nChoose setup method:")
    print("1. 🔐 Encrypted local storage (Most Secure)")
    print("2. 📄 .env file (Simple)")
    print("3. 🌐 GitHub Repository Secrets (For Actions)")
    print("4. 💻 System environment variables")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == '1':
        manager = SecureEnvManager()
        manager.setup_secure_env()
        
    elif choice == '2':
        setup_dotenv_file()
        
    elif choice == '3':
        print("\n🌐 GitHub Repository Secrets Setup:")
        print("1. Go to your repository on GitHub")
        print("2. Click Settings → Secrets and variables → Actions")
        print("3. Click 'New repository secret'")
        print("4. Add these secrets:")
        print("   - Name: GH_USERNAME, Secret: Xenonesis")
        print("   - Name: GH_TOKEN, Secret: ghp_xxxxxxxxxxxx")
        print("5. The GitHub Actions workflow will use these automatically")
        
    elif choice == '4':
        print("\n💻 System Environment Variables:")
        print("Add these to your shell profile (~/.bashrc, ~/.zshrc, etc.):")
        print()
        username = input("Enter your GitHub username: ").strip()
        token = getpass.getpass("Enter your GitHub token: ").strip()
        print(f"\nexport GITHUB_USERNAME='{username}'")
        print(f"export GITHUB_TOKEN='{token}'")
        print("\nThen run: source ~/.bashrc (or restart terminal)")
        
    else:
        print("❌ Invalid choice")
        return
    
    print("\n🎉 Setup completed! Your credentials are now secure.")

if __name__ == "__main__":
    # Check for required packages
    try:
        import cryptography
    except ImportError:
        print("📦 Installing required security packages...")
        os.system(f"{sys.executable} -m pip install cryptography python-dotenv")
    
    main()