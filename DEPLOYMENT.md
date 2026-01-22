# Deployment Guide

## Netlify Deployment with Password Protection

This site is configured for deployment to Netlify with optional password protection.

### Quick Start

1. **Build locally to test**:
   ```bash
   source venv/bin/activate
   mkdocs build
   ```

2. **Deploy to Netlify** (choose one method):
   - **Via Git**: Push to GitHub/GitLab and connect to Netlify
   - **Via CLI**: Use `netlify deploy --prod`

3. **Set up password protection** (see options below)

---

## Password Protection Options

### Option 1: Netlify Site-Wide Password (Requires Pro Plan)

**Cost**: $19/month per member
**Setup**:
1. Go to Site Settings → Access Control
2. Enable "Password protection"
3. Set your password

**Pros**: Simple, no code required
**Cons**: Requires paid plan

---

### Option 2: Basic Auth via Edge Functions (Free!)

**Cost**: Free (included in Free plan)
**Setup**:

1. **Set environment variables in Netlify**:
   - Go to Site Settings → Environment Variables
   - Add `SITE_USERNAME` (e.g., "admin")
   - Add `SITE_PASSWORD` (your secure password)

2. **Deploy** - the edge function is already configured in `netlify.toml`

**Pros**: Works on free plan, secure with env variables
**Cons**: Basic HTTP auth (browser popup)

**Testing locally**:
```bash
netlify dev
# The edge function will work locally too
```

---

### Option 3: Netlify Identity + Netlify Functions

**Cost**: Free up to 1,000 users
**Setup**: More complex, good for multiple users with different access levels

This would require additional configuration. Let me know if you need this option.

---

## Deployment Steps

### Method A: Git-Based Deployment (Recommended)

1. **Initialize git** (if not done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push to GitHub/GitLab**:
   ```bash
   # Create repo on GitHub first, then:
   git remote add origin <your-repo-url>
   git branch -M main
   git push -u origin main
   ```

3. **Connect to Netlify**:
   - Visit [app.netlify.com](https://app.netlify.com)
   - Click "Add new site" → "Import an existing project"
   - Select your Git provider
   - Choose your repository
   - Settings are auto-detected from `netlify.toml`
   - Click "Deploy"

4. **Set environment variables** (for password protection):
   - Go to Site Settings → Environment Variables
   - Add `SITE_USERNAME` and `SITE_PASSWORD`
   - Redeploy the site

### Method B: CLI Deployment

1. **Install Netlify CLI**:
   ```bash
   npm install -g netlify-cli
   ```

2. **Login**:
   ```bash
   netlify login
   ```

3. **Deploy**:
   ```bash
   netlify deploy --prod
   ```

4. **Set environment variables**:
   ```bash
   netlify env:set SITE_USERNAME "admin"
   netlify env:set SITE_PASSWORD "your-secure-password"
   ```

---

## Configuration Files

- **`netlify.toml`**: Build settings and edge function configuration
- **`runtime.txt`**: Python version for Netlify
- **`netlify/edge-functions/auth.ts`**: Password protection logic
- **`.gitignore`**: Excludes build artifacts

---

## Updating the Site

### After making changes:

1. **Regenerate pages** (if you modified scripts):
   ```bash
   venv/bin/python3 scripts/generate_pages.py
   ```

2. **Test locally**:
   ```bash
   mkdocs serve
   # or
   netlify dev
   ```

3. **Commit and push** (Git deployment):
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```
   
   Netlify will automatically rebuild and redeploy.

4. **Or redeploy via CLI**:
   ```bash
   netlify deploy --prod
   ```

---

## Custom Domain (Optional)

1. Go to Site Settings → Domain Management
2. Add your custom domain
3. Follow DNS configuration instructions
4. SSL certificate is automatically provisioned

---

## Troubleshooting

### Build fails on Netlify

- Check the build logs in Netlify dashboard
- Verify `requirements.txt` contains all dependencies
- Ensure Python version matches (`runtime.txt`)

### Password protection not working

- Verify environment variables are set: Site Settings → Environment Variables
- Check edge function logs in Netlify dashboard
- Clear browser cache and try again

### Changes not appearing

- Check if build succeeded in Netlify dashboard
- Hard refresh browser (Cmd+Shift+R / Ctrl+Shift+R)
- Verify you regenerated pages if you changed scripts

---

## Recommended Setup

For most use cases, I recommend:

1. **Deployment**: Git-based (automatic deploys on push)
2. **Password Protection**: Edge Functions with environment variables (free, secure)
3. **Updates**: Push to git, auto-deploys

This gives you a professional, secure, and free deployment pipeline!
