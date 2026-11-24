<?php
// save.php — Handles POST from register.php, validates & inserts.
require_once __DIR__ . '/config.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: register.php');
    exit;
}

// Collect + basic trim
$student_id = trim($_POST['student_id'] ?? '');
$first_name = trim($_POST['first_name'] ?? '');
$last_name  = trim($_POST['last_name'] ?? '');
$email      = trim($_POST['email'] ?? '');
$phone      = trim($_POST['phone'] ?? '');
$program    = trim($_POST['program'] ?? '');
$year_level = trim($_POST['year_level'] ?? '');
$notes      = trim($_POST['notes'] ?? '');

// Validate
$errors = [];

if ($student_id === '')   $errors[] = 'Student ID is required.';
if ($first_name === '')   $errors[] = 'First name is required.';
if ($last_name === '')    $errors[] = 'Last name is required.';
if ($program === '')      $errors[] = 'Program is required.';

if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors[] = 'A valid email is required.';
}

$year_num = filter_var($year_level, FILTER_VALIDATE_INT, ['options' => ['min_range' => 1, 'max_range' => 4]]);
if ($year_num === false) {
    $errors[] = 'Year level must be an integer between 1 and 4.';
}

if ($errors) {
    http_response_code(400);
    ?>
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Validation Errors</title>
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <main class="container card">
            <h2>Fix the following errors</h2>
            <ul class="errors">
                <?php foreach ($errors as $err): ?>
                    <li><?= e($err) ?></li>
                <?php endforeach; ?>
            </ul>
            <div class="actions">
                <a class="btn" href="register.php">Back to form</a>
            </div>
            <section class="card muted">
                <h3>Your submitted values</h3>
                <dl class="kv">
                    <dt>Student ID</dt><dd><?= e($student_id) ?></dd>
                    <dt>First Name</dt><dd><?= e($first_name) ?></dd>
                    <dt>Last Name</dt><dd><?= e($last_name) ?></dd>
                    <dt>Email</dt><dd><?= e($email) ?></dd>
                    <dt>Phone</dt><dd><?= e($phone) ?></dd>
                    <dt>Program</dt><dd><?= e($program) ?></dd>
                    <dt>Year</dt><dd><?= e($year_level) ?></dd>
                    <dt>Notes</dt><dd><?= nl2br(e($notes)) ?></dd>
                </dl>
            </section>
        </main>
    </body>
    </html>
    <?php
    exit;
}

// Insert
try {
    $stmt = $pdo->prepare("
        INSERT INTO students 
            (student_id, first_name, last_name, email, phone, program, year_level, notes)
        VALUES 
            (:student_id, :first_name, :last_name, :email, :phone, :program, :year_level, :notes)
    ");
    $stmt->execute([
        ':student_id' => $student_id,
        ':first_name' => $first_name,
        ':last_name'  => $last_name,
        ':email'      => $email,
        ':phone'      => $phone,
        ':program'    => $program,
        ':year_level' => $year_num,
        ':notes'      => $notes,
    ]);
} catch (PDOException $e) {
    // Handle duplicate student_id gracefully
    if ((int)$e->getCode() === 23000) {
        $msg = 'Student ID already exists. Please use a different ID.';
    } else {
        $msg = 'An error occurred while saving. Please try again.';
    }
    http_response_code(400);
    ?>
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Save Error</title>
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <main class="container card">
            <h2>Could not save your submission</h2>
            <p class="danger"><?= e($msg) ?></p>
            <div class="actions">
                <a class="btn" href="register.php">Back to form</a>
            </div>
        </main>
    </body>
    </html>
    <?php
    exit;
}

// Success page
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Registration Successful</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <main class="container card">
    <h2>Registration Successful 🎉</h2>
    <p>Your record has been saved.</p>

    <section class="card">
      <h3>Summary</h3>
      <dl class="kv">
        <dt>Student ID</dt><dd><?= e($student_id) ?></dd>
        <dt>Name</dt><dd><?= e($first_name) . ' ' . e($last_name) ?></dd>
        <dt>Email</dt><dd><?= e($email) ?></dd>
        <dt>Phone</dt><dd><?= e($phone) ?></dd>
        <dt>Program</dt><dd><?= e($program) ?></dd>
        <dt>Year</dt><dd><?= e((string)$year_num) ?></dd>
        <dt>Notes</dt><dd><?= nl2br(e($notes)) ?></dd>
      </dl>
    </section>

    <div class="actions">
      <a href="register.php" class="btn">Register another</a>
      <a href="students.php" class="btn ghost">View all students</a>
    </div>
  </main>
</body>
</html>
