# Hugo Blog Automation

This document explains the automated dependency management and security monitoring for your Hugo blog.

## 🤖 **What's Automated**

Your blog uses **Renovate Bot** for dependency management and **Security Audit** for continuous monitoring.

### **Renovate Bot**

- ✅ **Hugo version updates** (auto-merge minor/patch, manual review for major)
- ✅ **GitHub Actions updates** (auto-merge)
- ✅ **Beautiful Hugo theme updates** (manual review)
- ✅ **Dependency dashboard** in GitHub Issues
- ✅ **Scheduled updates** every Monday at 6 AM (São Paulo time)
- ✅ **Smart auto-merge** for safe updates

### **Security Monitoring**

- ✅ **Daily security scans**
- ✅ **Hugo version security assessment**
- ✅ **Theme maintenance monitoring**
- ✅ **Secret scanning** with TruffleHog
- ✅ **Security headers validation**
- ✅ **Automatic alerts** for high-risk findings

## 🚀 **Setup**

### 1. Install Renovate GitHub App

Visit https://github.com/apps/renovate and install it on your repository.

### 2. Commit the Configuration

```bash
git add renovate.json .github/workflows/security-audit.yml docs/AUTOMATION_SETUP.md
git commit -m "feat: add automated dependency management and security monitoring"
git push
```

### 3. Wait for First Dashboard

Renovate will create a "Dependency Dashboard" issue in your repository within a few minutes.

## 📋 **How It Works**

### **Weekly Dependency Updates**

Every Monday at 6 AM (São Paulo time), Renovate:

1. Checks for new Hugo releases
2. Checks for GitHub Actions updates
3. Checks for Beautiful Hugo theme updates
4. Creates PRs for any updates found
5. Auto-merges safe updates (minor/patch versions)
6. Requests manual review for major updates

### **Daily Security Monitoring**

Every day at 2 AM UTC, Security Audit:

1. Scans for Hugo version security risks
2. Monitors theme maintenance status
3. Scans for exposed secrets
4. Validates security headers
5. Creates GitHub issues for high-risk findings
6. Uploads detailed security reports

## 🔧 **Configuration Files**

### `renovate.json`

Main configuration for dependency updates:

- **Schedule**: Monday mornings
- **Auto-merge**: Minor and patch updates
- **Manual review**: Major updates
- **Rate limiting**: Max 2 PRs per hour, 3 concurrent

### `.github/workflows/security-audit.yml`

Security monitoring workflow:

- **Frequency**: Daily
- **Scans**: Hugo versions, theme age, secrets, headers
- **Alerts**: Automatic issue creation for high risks

## 📈 **Monitoring**

### **What to Watch**

1. **Dependency Dashboard** - GitHub issue created by Renovate
2. **Security Audit Reports** - Uploaded as workflow artifacts
3. **Automated PRs** - Review and merge dependency updates
4. **Security Issues** - Automatically created for high-risk findings

### **Regular Tasks**

- **Weekly**: Review and merge dependency PRs
- **Monthly**: Check security audit reports
- **As needed**: Test major Hugo updates before merging

## 🎯 **Benefits**

With this automation, your blog gets:

- ✅ **Always up-to-date dependencies**
- ✅ **Proactive security monitoring**
- ✅ **Minimal manual maintenance**
- ✅ **Early warning for security issues**
- ✅ **Consistent update process**
- ✅ **Detailed change tracking**

## 🚨 **Troubleshooting**

### **Renovate Issues**

- Check if GitHub App is installed and has repository access
- Review Renovate logs in the dependency dashboard issue
- Verify `renovate.json` syntax

### **Security Audit Issues**

- Check GitHub Actions logs for detailed error messages
- Ensure workflow has proper permissions
- Verify security headers file exists at `static/_headers`

### **Getting Help**

- GitHub Actions logs provide detailed error information
- Renovate documentation: https://docs.renovatebot.com/
- Hugo documentation: https://gohugo.io/documentation/

Your Hugo blog will stay secure and current with minimal manual intervention!
