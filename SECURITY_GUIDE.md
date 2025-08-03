# 🔐 GitHub Analytics Security Guide

Complete guide for secure environment variable setup and GitHub token management.

## 🎯 **Quick Start - Most Secure Method**

```bash
# 1. Install security dependencies
pip install cryptography python-dotenv

# 2. Run secure setup
python setup-secure-env.py

# 3. Choose option 1 (Encrypted local storage)

# 4. Load environment for current session
source load_env.sh
```

## 🔑 **Getting Your GitHub Token**

### **Step 1: Create Personal Access Token**

1. **Navigate to GitHub Settings:**
   ```
   https://github.com/settings/tokens
   ```

2. **Generate New Token:**
   - Click "Generate new token" → "Generate new token (classic)"
   - **Note:** "GitHub Analytics System"
   - **Expiration:** 90 days (recommended)

3. **Required Scopes:**
   ```
   ✅ public_repo          # Access public repositories
   ✅ read:user           # Read user profile information
   ✅ read:org            # Read organization membership (optional)
   ✅ repo:status         # Access commit status
   ```

4. **Copy Token Immediately:**
   ```
   Format: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ⚠️ SAVE IT NOW - You won't see it again!
   ```

### **Step 2: Validate Your Token**

```bash
# Validate token security and permissions
python scripts/secure-token-validator.py
```

## 🛡️ **Security Methods (Ranked by Security)**

### **🥇 Method 1: GitHub Repository Secrets (Most Secure for Actions)**

**For automated GitHub Actions:**

1. **Go to Repository Settings:**
   ```
   Your Repository → Settings → Secrets and variables → Actions
   ```

2. **Add Secrets:**
   ```
   Name: GH_TOKEN
   Secret: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   
   Name: GH_USERNAME
   Secret: Xenonesis
   ```

3. **Automatic Usage:**
   ```yaml
   # GitHub Actions automatically uses these
   env:
     GH_USERNAME: ${{ secrets.GH_USERNAME }}
     GH_TOKEN: ${{ secrets.GH_TOKEN }}
   ```

### **🥈 Method 2: Encrypted Local Storage**

**For local development with maximum security:**

```bash
# Run the secure setup
python setup-secure-env.py

# Choose option 1: Encrypted local storage
# Enter your credentials and encryption password

# Load variables when needed
source load_env.sh
```

**Features:**
- ✅ AES-256 encryption
- ✅ Password-protected
- ✅ Secure file permissions (600)
- ✅ No plaintext storage
- ✅ Automatic .gitignore entries

### **🥉 Method 3: .env File (Simple but Secure)**

```bash
# Create .env file
python setup-secure-env.py
# Choose option 2

# Or create manually:
cat > .env << 'EOF'
GITHUB_USERNAME=Xenonesis
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
EOF

# Set secure permissions
chmod 600 .env

# Add to .gitignore
echo ".env" >> .gitignore
```

**Load in Python:**
```python
from dotenv import load_dotenv
load_dotenv()  # Loads .env file
```

### **🏅 Method 4: System Environment Variables**

**Add to your shell profile:**

```bash
# For bash (~/.bashrc) or zsh (~/.zshrc)
export GITHUB_USERNAME="Xenonesis"
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Reload shell
source ~/.bashrc
```

**Windows (PowerShell):**
```powershell
# Set for current session
$env:GITHUB_USERNAME="Xenonesis"
$env:GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Set permanently
[Environment]::SetEnvironmentVariable("GITHUB_USERNAME", "Xenonesis", "User")
[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "ghp_xxxxxxxxxxxx", "User")
```

## 🔒 **Advanced Security Practices**

### **Token Security Checklist**

```bash
# ✅ Validate your token
python scripts/secure-token-validator.py

# Check for:
✅ Valid token format
✅ Token is active
✅ Correct permissions/scopes
✅ Rate limit status
✅ Security recommendations
```

### **Environment Security**

```bash
# ✅ Secure file permissions
chmod 600 .env                    # Only owner can read/write
chmod 600 ~/.github_analytics_env # Encrypted storage

# ✅ Git security
echo ".env" >> .gitignore
echo ".github_analytics_env" >> .gitignore
echo "*.key" >> .gitignore

# ✅ Check for accidental commits
git log --all --full-history -- .env
```

### **Token Rotation Schedule**

```bash
# Set up token rotation reminder
echo "# GitHub Token expires on $(date -d '+90 days' '+%Y-%m-%d')" >> .env

# Create calendar reminder
# Linux/Mac:
echo "0 0 * * 0 echo 'Rotate GitHub token!' | mail -s 'Security Reminder' you@email.com" | crontab -
```

## 🚨 **Security Incident Response**

### **If Token is Compromised:**

1. **Immediate Actions:**
   ```bash
   # 1. Revoke token immediately
   # Go to: https://github.com/settings/tokens
   # Click "Delete" next to compromised token
   
   # 2. Generate new token
   # Follow the creation steps above
   
   # 3. Update all systems
   python setup-secure-env.py  # Update local storage
   # Update GitHub repository secrets
   # Update any CI/CD systems
   ```

2. **Investigation:**
   ```bash
   # Check recent activity
   # Go to: https://github.com/settings/security-log
   
   # Review repository access logs
   # Check for unauthorized commits/changes
   ```

### **Prevention Measures:**

```bash
# ✅ Enable 2FA
# Go to: https://github.com/settings/security

# ✅ Monitor token usage
# Check rate limits regularly
python scripts/secure-token-validator.py

# ✅ Use fine-grained tokens when possible
# More restrictive permissions
# Repository-specific access
```

## 🔧 **Testing Your Setup**

### **Verify Environment Variables:**

```bash
# Test if variables are loaded
python -c "
import os
print('Username:', os.getenv('GITHUB_USERNAME', 'NOT SET'))
print('Token:', 'SET' if os.getenv('GITHUB_TOKEN') else 'NOT SET')
"
```

### **Test API Access:**

```bash
# Test GitHub API access
curl -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/user

# Should return your user information
```

### **Run Analytics Test:**

```bash
# Test the analytics system
python run-analytics.py --collect-only

# Should collect data successfully
```

## 📋 **Security Audit Checklist**

**Monthly Security Review:**

- [ ] Token still valid and not expired
- [ ] Rate limits are reasonable
- [ ] No unauthorized repository access
- [ ] Environment files have correct permissions
- [ ] .gitignore includes sensitive files
- [ ] No tokens in commit history
- [ ] 2FA is enabled on GitHub account
- [ ] Security log shows no suspicious activity

**Quarterly Actions:**

- [ ] Rotate GitHub token
- [ ] Update encryption passwords
- [ ] Review repository access permissions
- [ ] Audit all systems using the token
- [ ] Update security dependencies

## 🆘 **Troubleshooting**

### **Common Issues:**

**"Token not found" error:**
```bash
# Check if environment variable is set
echo $GITHUB_TOKEN

# If empty, reload environment
source load_env.sh
# or
source ~/.bashrc
```

**"Invalid token" error:**
```bash
# Validate token
python scripts/secure-token-validator.py

# Check token hasn't expired
# Verify correct scopes are selected
```

**"Rate limit exceeded" error:**
```bash
# Check current limits
curl -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/rate_limit

# Wait for reset or use authenticated requests
```

## 🎯 **Best Practices Summary**

1. **🔐 Use GitHub Repository Secrets** for automated workflows
2. **🔒 Encrypt local storage** for development
3. **🔄 Rotate tokens every 90 days**
4. **📱 Enable 2FA** on your GitHub account
5. **🚫 Never commit tokens** to version control
6. **👀 Monitor usage** regularly
7. **🗑️ Delete unused tokens** immediately
8. **📊 Use minimal required scopes**
9. **🛡️ Keep security tools updated**
10. **📋 Regular security audits**

---

**🎉 Your GitHub Analytics system is now secure and ready to use!**

For questions or issues, check the troubleshooting section or validate your setup with the provided security tools.