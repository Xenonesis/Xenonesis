#!/usr/bin/env python3
"""
GitHub Token Security Validator
Validates token permissions and security best practices
"""

import requests
import os
import re
from datetime import datetime, timedelta

class GitHubTokenValidator:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def validate_token_format(self) -> bool:
        """Validate token format"""
        print("🔍 Validating token format...")
        
        # GitHub Personal Access Token patterns
        patterns = {
            'classic': r'^ghp_[A-Za-z0-9]{36}$',
            'fine_grained': r'^github_pat_[A-Za-z0-9_]{82}$'
        }
        
        for token_type, pattern in patterns.items():
            if re.match(pattern, self.token):
                print(f"✅ Valid {token_type} token format")
                return True
        
        print("❌ Invalid token format")
        print("Expected formats:")
        print("  - Classic: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print("  - Fine-grained: github_pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        return False
    
    def check_token_validity(self) -> bool:
        """Check if token is valid and active"""
        print("\n🔐 Checking token validity...")
        
        try:
            response = requests.get('https://api.github.com/user', headers=self.headers)
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Token is valid for user: {user_data.get('login')}")
                return True
            elif response.status_code == 401:
                print("❌ Token is invalid or expired")
                return False
            else:
                print(f"⚠️ Unexpected response: {response.status_code}")
                return False
                
        except requests.RequestException as e:
            print(f"❌ Network error: {e}")
            return False
    
    def check_rate_limits(self) -> dict:
        """Check current rate limit status"""
        print("\n📊 Checking rate limits...")
        
        try:
            response = requests.get('https://api.github.com/rate_limit', headers=self.headers)
            
            if response.status_code == 200:
                rate_data = response.json()
                core = rate_data['resources']['core']
                
                remaining = core['remaining']
                limit = core['limit']
                reset_time = datetime.fromtimestamp(core['reset'])
                
                print(f"✅ Rate limit: {remaining}/{limit} remaining")
                print(f"📅 Resets at: {reset_time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                if remaining < 100:
                    print("⚠️ Warning: Low rate limit remaining")
                
                return rate_data
            else:
                print("❌ Could not check rate limits")
                return {}
                
        except requests.RequestException as e:
            print(f"❌ Error checking rate limits: {e}")
            return {}
    
    def check_token_scopes(self) -> list:
        """Check token permissions/scopes"""
        print("\n🔑 Checking token scopes...")
        
        try:
            response = requests.get('https://api.github.com/user', headers=self.headers)
            
            if response.status_code == 200:
                scopes = response.headers.get('X-OAuth-Scopes', '').split(', ')
                scopes = [scope.strip() for scope in scopes if scope.strip()]
                
                print("📋 Current scopes:")
                for scope in scopes:
                    print(f"  ✅ {scope}")
                
                # Check required scopes
                required_scopes = ['public_repo', 'read:user']
                missing_scopes = []
                
                for required in required_scopes:
                    if required not in scopes and 'repo' not in scopes:
                        missing_scopes.append(required)
                
                if missing_scopes:
                    print(f"\n⚠️ Missing required scopes: {', '.join(missing_scopes)}")
                else:
                    print("\n✅ All required scopes present")
                
                return scopes
            else:
                print("❌ Could not check token scopes")
                return []
                
        except requests.RequestException as e:
            print(f"❌ Error checking scopes: {e}")
            return []
    
    def security_recommendations(self) -> None:
        """Provide security recommendations"""
        print("\n🛡️ Security Recommendations:")
        print("-" * 30)
        
        recommendations = [
            "🔄 Rotate tokens every 90 days",
            "🚫 Never commit tokens to version control",
            "🔒 Use repository secrets for GitHub Actions",
            "📱 Enable 2FA on your GitHub account",
            "👀 Regularly audit token usage",
            "🗑️ Delete unused tokens immediately",
            "📊 Monitor rate limit usage",
            "🔐 Use fine-grained tokens when possible",
            "💾 Store tokens encrypted locally",
            "🚨 Set up token expiration alerts"
        ]
        
        for rec in recommendations:
            print(f"  {rec}")
    
    def comprehensive_validation(self) -> bool:
        """Run all validation checks"""
        print("🔐 GitHub Token Comprehensive Security Validation")
        print("=" * 55)
        
        all_passed = True
        
        # Format validation
        if not self.validate_token_format():
            all_passed = False
        
        # Validity check
        if not self.check_token_validity():
            all_passed = False
            return False  # No point continuing if token is invalid
        
        # Rate limits
        self.check_rate_limits()
        
        # Scopes
        scopes = self.check_token_scopes()
        
        # Security recommendations
        self.security_recommendations()
        
        print(f"\n{'✅' if all_passed else '❌'} Overall validation: {'PASSED' if all_passed else 'FAILED'}")
        
        return all_passed

def main():
    """Main validation function"""
    print("🔐 GitHub Token Security Validator")
    print("=" * 40)
    
    # Get token from environment or input
    token = os.getenv('GITHUB_TOKEN')
    
    if not token:
        import getpass
        print("No GITHUB_TOKEN environment variable found.")
        token = getpass.getpass("Enter your GitHub token: ").strip()
    
    if not token:
        print("❌ No token provided")
        return False
    
    # Validate token
    validator = GitHubTokenValidator(token)
    return validator.comprehensive_validation()

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)