# Upload to GitHub - Instructions

## Option 1: Using GitHub CLI (Easiest)

If you have GitHub CLI installed:

```bash
# Create repo and push (will prompt for repo details)
gh repo create llm-persona-discharge-study --public --source=. --push
```

## Option 2: Using GitHub Website

### Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `llm-persona-discharge-study` (or your preferred name)
3. Description: "Persona-based discharge summary comprehension study using ChatGPT"
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **Create repository**

### Step 2: Push Your Code

After creating the repo, GitHub will show you commands. Use these:

```bash
# Add GitHub as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/llm-persona-discharge-study.git

# Rename branch to main (optional, recommended)
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 3: Verify

Visit your repository URL:
```
https://github.com/YOUR_USERNAME/llm-persona-discharge-study
```

## Quick Commands Reference

```bash
# Check current status
git status

# Add new/modified files
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push

# Pull latest changes
git pull
```

## Making Updates Later

After making changes to your code:

```bash
git add .
git commit -m "Description of changes"
git push
```

## .gitignore Protects You

Your `.gitignore` file prevents accidentally committing:
- API keys (`.env` files)
- Result files (`*_results.json`)
- Python cache files
- IDE settings

Always safe to run `git add .` - sensitive files won't be added!
