# TrustVault – Secure Document Sharing with Audit Trail

## Project Overview

TrustVault is a secure document-sharing web application developed using Python and Flask. It allows users to upload, encrypt, download, and share documents with other registered users.

The application uses AES-GCM encryption to protect uploaded files and maintains an audit trail of important document activities.

## Key Features

- User registration and secure login.
- Admin and user roles.
- Secure document upload and download.
- AES-GCM file encryption and decryption.
- Support for PDF, TXT, and DOCX files.
- Document sharing through registered user email addresses.
- Viewer and Editor permissions.
- Revoke document access.
- Document integrity and tamper detection.
- Audit logs for document activities.
- Admin dashboard to view all registered users and uploaded documents.
- Admin-only dashboard access.

## Technologies Used

- **Frontend:** HTML, CSS
- **Backend:** Python, Flask
- **Database:** SQLite
- **ORM:** Flask-SQLAlchemy
- **Authentication:** Flask-Login
- **Encryption:** AES-GCM (Cryptography library)
- **Version Control:** Git and GitHub

## Project Structure

```text
TrustVault/
│
├── app/
│   ├── auth/
│   ├── templates/
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   └── admin_dashboard.html
│   ├── __init__.py
│   ├── models.py
│   ├── documents.py
│   ├── encryption.py
│   ├── permissions.py
│   └── audit.py
│
├── private_storage/
├── instance/
├── venv/
├── config.py
├── run.py
├── .env
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd TrustVault
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF cryptography python-dotenv
```

Install any additional dependencies listed in requirements.txt if present.

### 5. Configure environment variables

Create a `.env` file in the project root.

```env
SECRET_KEY=your_secret_key
ENCRYPTION_KEY=your_64_character_hex_key
```

Generate your own secure keys. Do not share or upload the `.env` file.

### 6. Run the application

```bash
python run.py
```

Open your browser:

```text
http://127.0.0.1:5000
```

## Security Implementation

- Uploaded documents are encrypted using AES-GCM.
- Encryption keys are stored in environment variables.
- Authentication protects user-specific pages.
- Document permissions control access.
- Only document owners can share or revoke access.
- Unauthorized downloads are denied.
- AES-GCM authentication detects modified encrypted files.
- Audit logs record document activities and access results.
- Admin routes restrict access to administrator accounts.

## User Roles

**Admin**
- View registered users.
- View all uploaded documents.
- View document owners and upload dates.
- Access the admin dashboard.

**User**
- Upload and download documents.
- Share documents with registered users.
- Receive shared documents.
- Access documents according to assigned permissions.

## Testing

The following features have been tested:

- User registration and login.
- Document upload and download.
- File encryption and decryption.
- Empty-file validation.
- File extension validation.
- Tamper detection.
- Document sharing.
- Permission revocation.
- Unauthorized download rejection.
- Audit logging.
- Admin dashboard access restrictions.

## Future Enhancements

- Cloud storage integration.
- Email notifications for shared documents.
- Advanced document search.
- Improved administrator management.
- Additional security monitoring.

## Author

**Sujatha Pilli**

B.Tech – Computer Science and Engineering

RISE Krishna Sai Prakasam Group of Institutions

Expected Graduation: 2027
