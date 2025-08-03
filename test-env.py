#!/usr/bin/env python3
"""
Test GitHub Environment Variables and Token Setup
Verifies that secrets are properly configured
"""

import os
import sys
import requests
import json
from datetime import datetime

def test_environment_variables():
    """Test if environment variables are properly set"""
    print("🔍 Testing Environment Variables...")
    print("=" * 50)
    
    # Check for GitHub username
    username = os.getenv('GH_USERNAME') or os.getenv('GITHUB_USERNAME')
    if username:
        print(f"✅ Username found: {username}")
    else:
        print("❌ Username not found (GH_USERNAME or GITHUB_USERNAME)")
        return False
    
    # Check for GitHub token
    token = os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
    if token:
        print(f"✅ Token found: {token[:8]}...{token[-4:]} (length: {len(token)})")
        if token.startswith('ghp_'):
            print("✅ Token format is correct (starts with 'ghp_')")
        else:
            print("⚠️ Warning: Token doesn't start with 'ghp_' - verify it's correct")
    else:
        print("❌ Token not found (GH_TOKEN or GITHUB_TOKEN)")
        return False
    
    return True, username, token

def test_github_api_access(username, token):
    """Test GitHub API access with the token"""
    print("\n🌐 Testing GitHub API Access...")
    print("=" * 50)
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'GitHub-Analytics-Test'
    }
    
    try:
        # Test 1: Get user information
        print("📋 Testing user information...")
        response = requests.get('https://api.github.com/user', headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ API Access successful!")
            print(f"   - User: {user_data.get('login', 'Unknown')}")
            print(f"   - Name: {user_data.get('name', 'Not set')}")
            print(f"   - Public Repos: {user_data.get('public_repos', 0)}")
            print(f"   - Followers: {user_data.get('followers', 0)}")
        else:
            print(f"❌ API Access failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        # Test 2: Check rate limits
        print("\n📊 Checking rate limits...")
        rate_limit_response = requests.get('https://api.github.com/rate_limit', headers=headers)
        
        if rate_limit_response.status_code == 200:
            rate_data = rate_limit_response.json()
            core_limit = rate_data['resources']['core']
            print(f"✅ Rate limit info:")
            print(f"   - Limit: {core_limit['limit']} requests/hour")
            print(f"   - Remaining: {core_limit['remaining']}")
            print(f"   - Reset: {datetime.fromtimestamp(core_limit['reset']).strftime('%H:%M:%S')}")
        
        # Test 3: Get repositories
        print(f"\n📁 Testing repository access for {username}...")
        repos_response = requests.get(f'https://api.github.com/users/{username}/repos?per_page=5', headers=headers)
        
        if repos_response.status_code == 200:
            repos = repos_response.json()
            print(f"✅ Repository access successful!")
            print(f"   - Found {len(repos)} repositories (showing first 5)")
            for repo in repos[:3]:
                print(f"   - {repo['name']}: ⭐ {repo['stargazers_count']} stars")
        else:
            print(f"❌ Repository access failed: {repos_response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_token_permissions(token):
    """Test token permissions and scopes"""
    print("\n🔐 Testing Token Permissions...")
    print("=" * 50)
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        # Make a request and check the scopes in response headers
        response = requests.get('https://api.github.com/user', headers=headers)
        
        if 'X-OAuth-Scopes' in response.headers:
            scopes = response.headers['X-OAuth-Scopes'].split(', ') if response.headers['X-OAuth-Scopes'] else []
            print(f"✅ Token scopes detected: {', '.join(scopes) if scopes else 'None'}")
            
            # Check required scopes
            required_scopes = ['public_repo', 'read:user', 'read:org']
            missing_scopes = []
            
            for scope in required_scopes:
                if scope in scopes or 'repo' in scopes:  # 'repo' includes 'public_repo'
                    print(f"   ✅ {scope}: Available")
                else:
                    print(f"   ❌ {scope}: Missing")
                    missing_scopes.append(scope)
            
            if missing_scopes:
                print(f"\n⚠️ Missing scopes: {', '.join(missing_scopes)}")
                print("   You may need to regenerate your token with additional permissions.")
                return False
            else:
                print("\n✅ All required scopes are available!")
                return True
        else:
            print("⚠️ Could not determine token scopes from response headers")
            return True  # Assume it's okay if we can't check
            
    except Exception as e:
        print(f"❌ Error checking permissions: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 GitHub Repository Secrets Test")
    print("=" * 60)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Test 1: Environment Variables
    env_result = test_environment_variables()
    if not env_result:
        print("\n❌ Environment variable test failed!")
        print("\n🔧 Troubleshooting:")
        print("1. Check that you've added secrets to GitHub repository:")
        print("   - Go to: Repository → Settings → Secrets and variables → Actions")
        print("   - Add: GH_USERNAME = Xenonesis")
        print("   - Add: GH_TOKEN = ghp_your_token_here")
        print("2. Make sure you're running this in a GitHub Action or with proper env setup")
        return False
    
    success, username, token = env_result
    
    # Test 2: API Access
    api_success = test_github_api_access(username, token)
    
    # Test 3: Token Permissions
    permissions_success = test_token_permissions(token)
    
    # Final Results
    print("\n" + "=" * 60)
    print("🎯 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"Environment Variables: {'✅ PASS' if success else '❌ FAIL'}")
    print(f"GitHub API Access:     {'✅ PASS' if api_success else '❌ FAIL'}")
    print(f"Token Permissions:     {'✅ PASS' if permissions_success else '❌ FAIL'}")
    
    overall_success = success and api_success and permissions_success
    print(f"\nOverall Status: {'🎉 ALL TESTS PASSED!' if overall_success else '❌ SOME TESTS FAILED'}")
    
    if overall_success:
        print("\n✅ Your GitHub repository secrets are properly configured!")
        print("🚀 You can now run: python run-analytics.py")
    else:
        print("\n❌ Please fix the issues above before running the analytics system.")
    
    print("=" * 60)
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)