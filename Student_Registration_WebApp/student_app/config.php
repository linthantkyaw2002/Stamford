<?php
// config.php — DB connection (PDO) + helper
// --------------------------------------------------
// 1) Create a MySQL database (e.g., `student_db`)
// 2) Update DB_* constants below if needed.
// 3) Include this file from your PHP pages to use `$pdo`.
// --------------------------------------------------

declare(strict_types=1);

// XAMPP typical defaults: user 'root' with empty password.
const DB_HOST = '127.0.0.1';
const DB_NAME = 'student_db';
const DB_USER = 'root';
const DB_PASS = '';

$dsn = 'mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=utf8mb4';

try {
    $pdo = new PDO($dsn, DB_USER, DB_PASS, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);
} catch (PDOException $e) {
    // Never reveal full details in production.
    http_response_code(500);
    echo '<h1>Database connection failed.</h1>';
    exit;
}

// HTML escape helper (prevents XSS in output)
function e(?string $str): string {
    return htmlspecialchars($str ?? '', ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}
