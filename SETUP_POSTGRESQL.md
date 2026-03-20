# PostgreSQL Installation and Setup Guide for Windows

## Step 1: Install PostgreSQL

### Option A: Using Chocolatey (Recommended)
```powershell
# Run PowerShell as Administrator
choco install postgresql -y --params '/Password:postgres'
```

### Option B: Download Installer
1. Go to https://www.postgresql.org/download/windows/
2. Download PostgreSQL 15+ installer
3. Run installer with default settings (save password as "postgres")
4. Ensure "Stack Builder" is unchecked at the end

### Option C: Using WSL (Windows Subsystem for Linux)
```bash
wsl
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

---

## Step 2: Verify Installation

After installation, add PostgreSQL to PATH (if not automatic):

```powershell
# Find PostgreSQL bin directory
$env:Path += ";C:\Program Files\PostgreSQL\15\bin"

# Test connection
psql --version
```

---

## Step 3: Create Database and Apply Schema

Once PostgreSQL is installed, run these commands:

```powershell
# Create the database
psql -U postgres -c "CREATE DATABASE oims_dev ENCODING 'UTF8';"

# Apply schema
psql -U postgres -d oims_dev -f Backend\Database\init.sql

# Verify
psql -U postgres -d oims_dev -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"
```

---

## Alternative: Use Entity Framework Core Migrations

If using .NET backend:

```powershell
cd Backend

# Install EF Core tools (if not installed)
dotnet tool install --global dotnet-ef

# Create and apply migrations
dotnet ef migrations add InitialCreate
dotnet ef database update
```

---

## Connection String

Make sure your `appsettings.json` has:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Port=5432;Database=oims_dev;Username=postgres;Password=postgres"
  }
}
```

---

## Quick Test

```powershell
# Connect interactively to test
psql -U postgres -d oims_dev

# Inside psql, try:
SELECT * FROM "Users" LIMIT 1;
\dt                    # List tables
\q                     # Quit
```
