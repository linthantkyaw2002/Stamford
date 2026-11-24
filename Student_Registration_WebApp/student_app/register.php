<?php
// register.php — Student Registration Form
require_once __DIR__ . '/config.php';
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Student Registration</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="topbar">
    <div class="container">
      <h1>Student Registration</h1>
      <nav>
        <a href="register.php" class="active">Register</a>
        <a href="students.php">Students</a>
      </nav>
    </div>
  </header>

  <main class="container card">
    <h2>Register a Student</h2>
    <p class="muted">Fields marked with <span class="req">*</span> are required.</p>

    <form action="save.php" method="post" novalidate>
      <div class="grid">
        <div class="field">
          <label for="student_id">Student ID <span class="req">*</span></label>
          <input type="text" id="student_id" name="student_id" required maxlength="20" placeholder="e.g., ST12345">
        </div>

        <div class="field">
          <label for="first_name">First Name <span class="req">*</span></label>
          <input type="text" id="first_name" name="first_name" required maxlength="50">
        </div>

        <div class="field">
          <label for="last_name">Last Name <span class="req">*</span></label>
          <input type="text" id="last_name" name="last_name" required maxlength="50">
        </div>

        <div class="field">
          <label for="email">Email <span class="req">*</span></label>
          <input type="email" id="email" name="email" required maxlength="100" placeholder="name@example.com">
        </div>

        <div class="field">
          <label for="phone">Phone</label>
          <input type="text" id="phone" name="phone" maxlength="20" placeholder="+66 8x-xxx-xxxx">
        </div>

        <div class="field">
          <label for="program">Program <span class="req">*</span></label>
          <input type="text" id="program" name="program" required maxlength="100" placeholder="e.g., BSc IT">
        </div>

        <div class="field">
          <label for="year_level">Year Level (1–4) <span class="req">*</span></label>
          <select id="year_level" name="year_level" required>
            <option value="">-- Select --</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
          </select>
        </div>
      </div>

      <div class="field">
        <label for="notes">Notes (optional)</label>
        <textarea id="notes" name="notes" rows="5" maxlength="2000" placeholder="Additional information..."></textarea>
      </div>

      <div class="actions">
        <button type="submit" class="btn">Save</button>
        <a href="students.php" class="btn ghost">View Students</a>
      </div>
    </form>
  </main>

  <footer class="footer">
    <div class="container">
      <small>&copy; <?= date('Y') ?> Student Registration App</small>
    </div>
  </footer>
</body>
</html>
