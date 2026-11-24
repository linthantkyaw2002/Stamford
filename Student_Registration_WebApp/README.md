# Student Registration Web Application

A database-driven student registration application built with **PHP, MySQL, HTML, and CSS**. It provides a straightforward workflow for registering students, reviewing saved records, and finding students using search and filters.

Developed as part of **ITE220** coursework, this project focuses on server-side form handling, relational database integration, and foundational web application security.

## Features

- **Student registration:** Capture student ID, name, email, phone number, academic program, year level (1–4), and optional notes.
- **Server-side validation:** Check required fields, email format, and permitted year levels before storing records.
- **Duplicate ID handling:** Enforce unique student IDs in MySQL and display a user-friendly error when an ID already exists.
- **Registration confirmation:** Display the details of a successfully saved registration.
- **Student directory:** View saved registrations in a table ordered by creation date (newest first).
- **Search and filters:** Search by student ID, first name, last name, or email; filter by academic program and year level.
- **Responsive dark interface:** Two-column registration layout on larger screens, single-column layout on smaller screens, and a horizontally scrollable student table.

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | HTML5, CSS3 |
| Backend | PHP |
| Database | MySQL |
| Database access | PHP Data Objects (PDO) |
| Local development | XAMPP (Apache + MySQL) |

## Application Flow

```text
index.php
    |
    v
register.php  -- POST form -->  save.php
    |                             |
    |                             +-- Validate submitted fields
    |                             +-- Insert record with PDO
    |                             +-- Show error or confirmation
    |
    +-------------------------+
                              v
                         students.php
                              |
                              +-- Search by ID / name / email
                              +-- Filter by program / year
                              +-- Display matching records

config.php: Shared database connection and HTML escaping helper
schema.sql: Database and students table definition
```

## Getting Started

### Prerequisites

- PHP with the `pdo_mysql` extension enabled
- MySQL server
- Apache or another web server configured to execute PHP

**XAMPP** is one convenient way to run Apache, PHP, and MySQL locally.

### 1. Download the project

Clone the repository or download it as a ZIP, then place the project folder inside your web server's document root.

Typical XAMPP locations:

- **Windows:** `C:\xampp\htdocs\student_app`
- **macOS:** `/Applications/XAMPP/xamppfiles/htdocs/student_app`

The folder name `student_app` is used in the URLs below; adjust the URL if you use a different folder name.

### 2. Start Apache and MySQL

Open the XAMPP Control Panel or Manager and start **Apache** and **MySQL**.

### 3. Create the database

Import `schema.sql` using **phpMyAdmin**, or run it from the MySQL command line:

```bash
mysql -u root -p < schema.sql
```

The script creates the `student_db` database and its `students` table if they do not already exist.

### 4. Configure the database connection

Open `config.php` and update the connection values for your local MySQL installation:

```php
const DB_HOST = '127.0.0.1';
const DB_NAME = 'student_db';
const DB_USER = 'root';
const DB_PASS = '';
```

> **Security note:** The empty password above is a common XAMPP development default, not a production recommendation. Use an appropriately restricted database account and secure configuration for deployment. Do not commit real database passwords to a public repository.

### 5. Open the application

Visit:

```text
http://localhost/student_app/
```

`index.php` redirects to `register.php`. To view the directory directly, open:

```text
http://localhost/student_app/students.php
```

## Database Schema

The application uses one MySQL table: `students`.

| Column | Type | Purpose |
| --- | --- | --- |
| `id` | `INT` | Auto-incrementing primary key |
| `student_id` | `VARCHAR(20)` | Required, unique student identifier |
| `first_name` | `VARCHAR(50)` | Required first name |
| `last_name` | `VARCHAR(50)` | Required last name |
| `email` | `VARCHAR(100)` | Required email address |
| `phone` | `VARCHAR(20)` | Optional phone number |
| `program` | `VARCHAR(100)` | Required academic program |
| `year_level` | `TINYINT` | Required value between 1 and 4 |
| `notes` | `TEXT` | Optional additional information |
| `created_at` | `TIMESTAMP` | Automatically recorded creation timestamp |

The schema includes a `UNIQUE` constraint on `student_id` and a `CHECK` constraint restricting `year_level` to values from 1 through 4.

## Project Structure

```text
student_app/
├── index.php                       # Redirects to the registration page
├── register.php                    # Student registration form
├── save.php                        # POST processing, validation, and insertion
├── students.php                    # Student directory with search and filters
├── config.php                      # Shared PDO connection and escaping helper
├── schema.sql                      # Database and table creation script
├── styles.css                      # Responsive dark-themed UI
├── Student_Registration_Report.docx # Original coursework report
└── README.md                        # Project documentation
```

## Implementation Details

### Registration and validation

`register.php` collects student information and sends it to `save.php` through an HTTP `POST` request. The backend trims submitted values and checks required fields, valid email syntax, and a year level between 1 and 4. Failed validation produces an error page; successful insertion produces a confirmation page.

### Database access

`config.php` centralizes the MySQL connection using PDO, with exception-based error handling and UTF-8 (`utf8mb4`) character encoding. `save.php` uses a prepared `INSERT` statement with bound parameters rather than concatenating user values into SQL.

### Student search

`students.php` builds a query using the supplied search term and optional program and year filters. Results are displayed newest first. The program filter is populated from program values already stored in the database.

### Output encoding and error handling

The shared `e()` helper wraps `htmlspecialchars()` to encode user-provided content before it is written into HTML. Notes are encoded before line breaks are rendered. The registration flow also handles duplicate student IDs with a readable error message, without exposing database exception details to the user.

## Scope and Limitations

This version implements **Create** and **Read** operations; **Update** and **Delete** have not yet been implemented. It is a local/coursework application, not a production-ready student information system. There is currently no user authentication or authorization, CSRF protection, or pagination. The registration form uses server-side validation; its HTML `novalidate` attribute disables the browser's built-in form validation.

## Possible Improvements

- Add editing and deletion of existing student records.
- Add authentication and role-based access control to protect student information.
- Implement CSRF protection and stronger form validation.
- Add pagination for larger student datasets.
- Move database credentials to environment-based configuration.
- Add automated tests for registration, validation, and search behavior.

## Project Context

**Course:** ITE220  
**Project type:** Academic web application  
**Focus areas:** PHP backend development, MySQL, form validation, database queries, and secure HTML output

The accompanying `Student_Registration_Report.docx` includes an original project walkthrough and screenshots of the registration form, success page, and student directory.
