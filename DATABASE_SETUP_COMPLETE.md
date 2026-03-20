# Database Integration Verification Report

## System Status ✅

### Services Running
- **Backend**: .NET 9.0 Core (Port 5000) - Running
- **Frontend**: React/Vite (Port 5173) - Running  
- **Database**: PostgreSQL 18 (localhost:5432) - Connected
- **Database Name**: oims_dev
- **Database User**: postgres

### Database Tables (6 Total)
```
✅ Applications     (uuid Id, uuid StudentId, uuid ListingId, Status tracking)
✅ AuditLogs        (Audit trail for all operations)
✅ IdempotencyKeys  (Duplicate request prevention)
✅ Listings         (Job postings from companies)
✅ Users            (User profiles with role-specific fields)
✅ __EFMigrationsHistory (EF Core tracking)
```

## Users Table Schema
| Column | Type | Purpose |
|--------|------|---------|
| Id | uuid | Primary key |
| Email | varchar | Login username |
| FirstName | varchar | User first name |
| LastName | varchar | User last name |
| PasswordHash | varchar | Hashed password |
| Role | varchar | student/adviser/company/admin |
| Status | varchar | active/inactive/suspended |
| University | varchar | (For advisers) |
| School | varchar | (For advisers/students) |
| Program | varchar | (For advisers/students) |
| StudentId | varchar | (For students) |
| EmployeeId | varchar | (For advisers) |
| AdviserId | uuid | (For students, links to adviser) |
| RequiredHours | int | (For students) |
| CompletedHours | int | (For students) |
| CreatedAt | timestamp | Record creation time |
| UpdatedAt | timestamp | Record update time |

## Listings Table Schema
| Column | Type | Purpose |
|--------|------|---------|
| Id | uuid | Primary key |
| Title | varchar | Job title |
| Description | text | Detailed description |
| Requirements | text | Job requirements |
| CompanyId | uuid | FK to Users (company) |
| Location | varchar | Work location |
| Salary | numeric | Salary offered |
| Type | varchar | on-site/remote/hybrid |
| RequiredHours | numeric | Required internship hours |
| IsActive | boolean | Is listing open for applications |
| PostedAt | timestamp | When posted |
| ClosedAt | timestamp | When closed |
| CreatedAt | timestamp | Record creation |
| UpdatedAt | timestamp | Record update |

## Applications Table Schema
| Column | Type | Purpose |
|--------|------|---------|
| Id | uuid | Primary key |
| StudentId | uuid | FK to Users (student) |
| ListingId | uuid | FK to Listings |
| CompanyId | uuid | FK to Users (company) - denormalized |
| Status | varchar | pending/reviewed/accepted/rejected/withdrawn |
| Feedback | text | Feedback from reviewer |
| CreatedAt | timestamp | Application date |
| UpdatedAt | timestamp | Last update |

## API Endpoints - Ready to Use

### Authentication (No Auth Required)
- POST /api/auth/register - Register new user (student/adviser/company)
- POST /api/auth/login - Login and get JWT token
- POST /api/auth/refresh - Refresh access token
- POST /api/auth/logout - Logout

### User Management (Requires Auth)
- GET /api/user/me - Get current user
- GET /api/user/{id} - Get user by ID
- PUT /api/user/{id} - Update user profile
- DELETE /api/user/{id} - Deactivate user

### Listings (Requires Auth)
- GET /api/listing - List all active job postings
- GET /api/listing/{id} - Get listing details
- POST /api/listing - Create listing (company only)
- PUT /api/listing/{id} - Update listing (owner only)
- DELETE /api/listing/{id} - Close listing

### Applications (Requires Auth)
- GET /api/application - List applications (filtered by user role)
- GET /api/application/{id} - Get application details
- POST /api/application - Submit application
- PUT /api/application/{id}/status - Update status (adviser/admin only)
- PUT /api/application/{id}/progress - Update progress (student/adviser/admin)

## Data Persistence ✅

**How it works:**
1. User registers through frontend (http://localhost:5173)
2. Frontend sends JSON to backend (http://localhost:5000/api/auth/register)
3. Backend validates and saves to PostgreSQL oims_dev database
4. Data persists immediately - automatically saved to Users table
5. Frontend can query via /api/user/me to verify saved data

**Verification via PostgreSQL:**
```bash
# Check registered users
psql -h localhost -U postgres -d oims_dev
=> SELECT "Email", "FirstName", "Role" FROM "Users";

# Check job postings
=> SELECT "Title", "Location" FROM "Listings";

# Check applications
=> SELECT * FROM "Applications";
```

## Configuration Details

### CORS Setup (Available Ports)
- http://localhost:5173 (Vite dev server)
- http://localhost:5174 (Fallback)
- http://localhost:3000 (Production)

### JWT Authentication
- Access Token: 15 minutes
- Refresh Token: 7 days (in HttpOnly cookie)
- Token stored in localStorage as: `ojt_session_token`

### Database Connection
- Host: localhost
- Port: 5432
- Database: oims_dev
- User: postgres
- Password: postgres
- Connection String: `Server=localhost;Port=5432;Database=oims_dev;User Id=postgres;Password=postgres;`

## Testing Checklist

To test the full system:

1. **Register a Test Account**
   - Visit http://localhost:5173
   - Click Register
   - Fill in form (adviser: needs @usjr.edu.ph email)
   - Submit

2. **Verify in Database**
   ```bash
   psql -h localhost -U postgres -d oims_dev
   => SELECT "Email", "Role" FROM "Users" WHERE "Email" = 'youremail@example.com';
   ```
   Expected: Your account appears in Users table

3. **Login**
   - Use registered email and password
   - Frontend redirects to your dashboard

4. **Verify Token Storage**
   - Open Browser DevTools → Application → LocalStorage
   - Check `ojt_session_token` exists

5. **Create Listing (if Company)**
   - Navigate to listings panel
   - Create new job posting
   - Verify in database: `SELECT * FROM "Listings";`

6. **Apply (if Student)**
   - Browse listings
   - Click Apply
   - Check database: `SELECT * FROM "Applications";`

7. **Update Status (if Adviser)**
   - View applications
   - Update status to "accepted"
   - Database updates automatically

## Important Notes

✅ **Automatic Persistence**: All changes save to PostgreSQL automatically
✅ **Case-Insensitive JSON**: API accepts both camelCase and PascalCase
✅ **Role-Based Access**: Each API endpoint validates user role
✅ **Audit Trail**: All actions logged to AuditLogs table
✅ **Data Relationships**: Proper foreign keys prevent orphaned data

⚠️ **For pgAdmin 4 Access**: If you need visual data browsing:
- Alternative 1: Use psql command line (recommended)
- Alternative 2: Install DBeaver (free, open-source GUI)
- Alternative 3: Use VS Code PostgreSQL extension

Generated: $(date)
