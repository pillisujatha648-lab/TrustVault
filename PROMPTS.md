# TrustVault – AI Prompts and Corrections

## 1. Encryption Verification

**AI assistance:** Helped implement AES-GCM encryption for uploaded documents.

**Problem discovered:** Some files had an `.encrypted` extension but were actually stored without encryption. This caused decryption failures during downloads.

**My correction:** I inspected the stored files, created and ran a migration script, and used a verification script to check that existing files were encrypted correctly.

**Testing:** Verified all five existing files and tested tamper detection.

## 2. Login and User Roles

**AI assistance:** Helped implement user authentication and separate Admin and User dashboards.

**Problem discovered:** Some login attempts failed, and role-based redirection needed correction.

**My correction:** I checked the authentication logic, user roles and password verification. I also used the admin password reset process to restore admin login.

**Testing:** Tested admin and normal user login separately and confirmed that each opened the correct dashboard.

## 3. GitHub and Deployment

**AI assistance:** Helped with Git commands and deployment to Render.

**Problem discovered:** I encountered GitHub connection errors and repository naming issues.

**My correction:** I retried the Git push after the connection problem and corrected the repository name and link.

**Testing:** Confirmed that code was pushed to GitHub and the Render deployment became live.

## 4. What I Learned

I learned that AI-generated code should not be accepted without testing. I checked the actual application behaviour, investigated errors, corrected problems and verified important security features myself.
