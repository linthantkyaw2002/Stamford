-- schema.sql — Database + table
-- Run these in your MySQL (e.g., via phpMyAdmin or mysql CLI).

-- 1) Create DB (you may choose a different name and update config.php)
CREATE DATABASE IF NOT EXISTS student_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE student_db;

-- 2) Create table
CREATE TABLE IF NOT EXISTS students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id VARCHAR(20) NOT NULL UNIQUE,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL,
  phone VARCHAR(20),
  program VARCHAR(100) NOT NULL,
  year_level TINYINT NOT NULL,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CHECK (year_level BETWEEN 1 AND 4)
);
