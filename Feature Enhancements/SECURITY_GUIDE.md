# Security Configuration Guide - Password Protection

## Overview

The app password is **no longer hardcoded** in the source code. This guide shows you how to securely configure your password for different deployment scenarios.

---

## 🚨 IMPORTANT: Before Pushing to GitHub

### Step 1: Add .gitignore

Make sure you have a `.gitignore` file in your repository root with these lines:

```
.env
.streamlit/secrets.toml
*.secret
*.key
```

**This file is provided** - just copy `.gitignore` to your repository root.

### Step 2: Never Commit Secrets

**DO NOT commit these files to GitHub:**
- ❌ `.env`
- ❌ `.streamlit/secrets.toml`
- ❌ Any file with passwords or API keys

**Safe to commit:**
- ✅ `.env.example` (template without real passwords)
- ✅ `secrets.toml.example` (template without real passwords)
- ✅ `.gitignore`
- ✅ All Python code files

---

## 📋 Configuration Methods

Choose the method based on where you're deploying:

### Method 1: Streamlit Cloud (Recommended for Cloud Deployment)

**Best for**: Deploying to share.streamlit.io

#### Steps:

1. **Deploy your app** to Streamlit Cloud from GitHub

2. **Go to app settings**:
   - Click "⚙️ Settings" in the bottom-right of your deployed app
   - Or go to share.streamlit.io → Your apps → Click "⚙" icon

3. **Add secrets**:
   - Click "Secrets" in the left sidebar
   - Add this content:
   ```toml
   APP_PASSWORD = "YourSecurePassword123"
   ```
   
4. **Save and restart**
   - Click "Save"
   - App will automatically restart with new password

#### Screenshot Guide:
```
Streamlit Cloud Dashboard
    ↓
Your App → Settings
    ↓
Secrets (left sidebar)
    ↓
Add: APP_PASSWORD = "YourPassword"
    ↓
Save → Auto-restart
```

---

### Method 2: Local Development with .streamlit/secrets.toml

**Best for**: Running locally on your computer

#### Steps:

1. **Create `.streamlit` folder** in your project directory:
   ```bash
   mkdir .streamlit
   ```

2. **Create `secrets.toml` file** inside `.streamlit/`:
   ```bash
   touch .streamlit/secrets.toml
   ```

3. **Add your password** to `.streamlit/secrets.toml`:
   ```toml
   APP_PASSWORD = "Claire&Goska"
   ```

4. **Verify .gitignore** includes this file:
   ```
   .streamlit/secrets.toml
   ```

5. **Run the app**:
   ```bash
   streamlit run app_phase1_enhanced.py
   ```

#### File Structure:
```
your-project/
├── .streamlit/
│   └── secrets.toml          ← Contains password (NOT in git)
├── app_phase1_enhanced.py
├── density_analysis.py
├── .gitignore                ← Protects secrets.toml
└── README.md
```

---

### Method 3: Environment Variables

**Best for**: Docker, production servers, CI/CD

#### Option A: Set in Terminal (Temporary)

**Linux/Mac:**
```bash
export APP_PASSWORD="Claire&Goska"
streamlit run app_phase1_enhanced.py
```

**Windows (PowerShell):**
```powershell
$env:APP_PASSWORD="Claire&Goska"
streamlit run app_phase1_enhanced.py
```

**Windows (CMD):**
```cmd
set APP_PASSWORD=Claire&Goska
streamlit run app_phase1_enhanced.py
```

#### Option B: .env File (Recommended for Local)

1. **Create `.env` file** in project root:
   ```bash
   touch .env
   ```

2. **Add password** to `.env`:
   ```
   APP_PASSWORD=Claire&Goska
   ```

3. **Verify .gitignore** includes `.env`:
   ```
   .env
   ```

4. **Install python-dotenv** (if using .env):
   ```bash
   pip install python-dotenv
   ```

5. **Load in your code** (optional - for non-Streamlit apps):
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```
   
   *Note: Not needed for our app - Streamlit handles it automatically*

---

## 🔐 Password Best Practices

### Creating a Strong Password

**Good passwords:**
- At least 12 characters
- Mix of uppercase, lowercase, numbers, symbols
- Not a dictionary word
- Examples: `Zm8!Mining*2025`, `ViL@gi0Tr4d!ng`

**Avoid:**
- Common words: "password", "admin"
- Sequential: "12345", "abcdef"
- Personal info: names, birthdays
- Short passwords: <8 characters

### Changing Your Password

1. **Update the password** in your secrets location:
   - Streamlit Cloud: Settings → Secrets
   - Local: `.streamlit/secrets.toml` or `.env`

2. **Restart the app**:
   - Streamlit Cloud: Auto-restarts
   - Local: Stop (Ctrl+C) and restart

3. **Notify users** if it's a shared app

### Multiple Environments

**Recommended Setup:**

```
Development (your laptop):
└── .streamlit/secrets.toml
    APP_PASSWORD = "DevPassword123"

Staging (test server):
└── Environment Variable
    APP_PASSWORD = "StagingPassword456"

Production (Streamlit Cloud):
└── Streamlit Secrets
    APP_PASSWORD = "ProdPassword789"
```

Use different passwords for each environment!

---

## ✅ Verification Checklist

Before pushing to GitHub, verify:

- [ ] `.gitignore` file exists in repository root
- [ ] `.gitignore` includes `.env` and `.streamlit/secrets.toml`
- [ ] Password is NOT in `app_phase1_enhanced.py`
- [ ] Password IS in either:
  - [ ] `.streamlit/secrets.toml` (local)
  - [ ] Environment variable (server/Docker)
  - [ ] Streamlit Cloud secrets (cloud)
- [ ] `.env.example` exists (template for others)
- [ ] `secrets.toml.example` exists (template for others)
- [ ] Real `.env` is NOT committed
- [ ] Real `secrets.toml` is NOT committed

### Test Your Setup:

1. **Check git status**:
   ```bash
   git status
   ```
   You should NOT see:
   - `.env`
   - `.streamlit/secrets.toml`

2. **Test the app**:
   ```bash
   streamlit run app_phase1_enhanced.py
   ```
   Should work without errors

3. **Test password prompt**:
   - Open app in browser
   - Should show password prompt
   - Enter your password
   - Should authenticate successfully

---

## 🐛 Troubleshooting

### Error: "Password not configured!"

**Cause**: App can't find password in secrets or environment

**Solution**:
1. Check if `.streamlit/secrets.toml` exists
2. Check if `APP_PASSWORD` is set in environment
3. Verify spelling: `APP_PASSWORD` (case-sensitive)
4. Restart the app after adding password

### Error: "Access denied" / Wrong password

**Cause**: Password mismatch

**Solution**:
1. Verify password in secrets matches what you're entering
2. Check for extra spaces or quotes
3. Make sure it's `APP_PASSWORD`, not `PASSWORD`

### Secret file not found locally

**Solution**:
```bash
# Create the directory and file
mkdir -p .streamlit
cat > .streamlit/secrets.toml << 'EOF'
APP_PASSWORD = "Claire&Goska"
EOF
```

### Git is tracking my secrets file!

**If you already committed secrets:**

```bash
# Remove from git but keep local file
git rm --cached .streamlit/secrets.toml
git rm --cached .env

# Add to .gitignore
echo ".streamlit/secrets.toml" >> .gitignore
echo ".env" >> .gitignore

# Commit the removal
git commit -m "Remove secrets from git"
git push
```

**⚠️ Important**: Those secrets are now in git history. You should:
1. Change your passwords immediately
2. Consider using `git filter-branch` to remove from history (advanced)

---

## 📚 Quick Reference

### Local Development:
```
.streamlit/secrets.toml:
APP_PASSWORD = "YourPassword"

Then run:
streamlit run app_phase1_enhanced.py
```

### Streamlit Cloud:
```
1. Deploy app from GitHub
2. Settings → Secrets
3. Add: APP_PASSWORD = "YourPassword"
4. Save
```

### Docker:
```dockerfile
ENV APP_PASSWORD=YourPassword
```

### Production Server:
```bash
export APP_PASSWORD="YourPassword"
```

---

## 🔒 Advanced Security (Optional)

### Using Hashed Passwords

For extra security, you can store hashed passwords:

```toml
# In secrets.toml
APP_PASSWORD_HASH = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
```

Then update your code to compare hashes.

### Multiple Users

For multiple users with different passwords, use a dictionary:

```toml
# In secrets.toml
[passwords]
admin = "AdminPassword123"
viewer = "ViewerPassword456"
```

### Rotation Schedule

**Recommended**: Change passwords every 90 days

Keep a log:
```
2024-01: Changed to Password123
2024-04: Changed to Password456
2024-07: Changed to Password789
```

---

## 📞 Support

If you encounter issues:

1. Check this guide first
2. Verify your `.gitignore` is working: `git status`
3. Test locally before deploying to cloud
4. Check Streamlit documentation: https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management

---

## ✅ Security Achieved!

With this setup:
- ✅ Password is NOT in GitHub
- ✅ App works locally and in cloud
- ✅ Easy to change password
- ✅ Secure by default
- ✅ Team members can set their own passwords

**Your app is now production-ready and secure!** 🔐
