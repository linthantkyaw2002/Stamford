<?php
// students.php — Lists all records with search & filters.
require_once __DIR__ . '/config.php';

$q = trim($_GET['q'] ?? '');
$program = trim($_GET['program'] ?? '');
$year = trim($_GET['year'] ?? '');

$where = [];
$params = [];

if ($q !== '') {
    $where[] = "(student_id LIKE :q OR first_name LIKE :q OR last_name LIKE :q OR email LIKE :q)";
    $params[':q'] = '%' . $q . '%';
}
if ($program !== '') {
    $where[] = "program = :program";
    $params[':program'] = $program;
}
if ($year !== '') {
    $yearInt = filter_var($year, FILTER_VALIDATE_INT, ['options' => ['min_range' => 1, 'max_range' => 4]]);
    if ($yearInt !== false) {
        $where[] = "year_level = :year";
        $params[':year'] = $yearInt;
    }
}

$sql = "SELECT * FROM students";
if ($where) {
    $sql .= " WHERE " . implode(" AND ", $where);
}
$sql .= " ORDER BY created_at DESC";

$stmt = $pdo->prepare($sql);
$stmt->execute($params);
$rows = $stmt->fetchAll();

// Distinct programs for filter dropdown
$progStmt = $pdo->query("SELECT DISTINCT program FROM students ORDER BY program ASC");
$programs = $progStmt->fetchAll(PDO::FETCH_COLUMN);
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Students</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="topbar">
    <div class="container">
      <h1>Students</h1>
      <nav>
        <a href="register.php">Register</a>
        <a href="students.php" class="active">Students</a>
      </nav>
    </div>
  </header>

  <main class="container">
    <section class="card">
      <form class="filters" method="get" action="students.php">
        <input type="text" name="q" value="<?= e($q) ?>" placeholder="Search by ID, name, or email…">
        <select name="program">
          <option value="">All programs</option>
          <?php foreach ($programs as $p): ?>
            <option value="<?= e($p) ?>" <?= $program === $p ? 'selected' : '' ?>><?= e($p) ?></option>
          <?php endforeach; ?>
        </select>
        <select name="year">
          <option value="">All years</option>
          <?php for ($i=1; $i<=4; $i++): ?>
            <option value="<?= $i ?>" <?= ((string)$year === (string)$i) ? 'selected' : '' ?>>Year <?= $i ?></option>
          <?php endfor; ?>
        </select>
        <button class="btn" type="submit">Apply</button>
        <a class="btn ghost" href="students.php">Reset</a>
      </form>
    </section>

    <section class="card">
      <div class="table-info">
        <strong><?= count($rows) ?></strong> record(s) found
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Student ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Program</th>
              <th>Year</th>
              <th>Notes</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            <?php if (!$rows): ?>
              <tr><td colspan="8" class="muted center">No records found.</td></tr>
            <?php else: ?>
              <?php foreach ($rows as $r): ?>
                <tr>
                  <td><?= e($r['student_id']) ?></td>
                  <td><?= e($r['first_name'] . ' ' . $r['last_name']) ?></td>
                  <td><?= e($r['email']) ?></td>
                  <td><?= e($r['phone']) ?></td>
                  <td><?= e($r['program']) ?></td>
                  <td><?= e((string)$r['year_level']) ?></td>
                  <td><?= nl2br(e($r['notes'])) ?></td>
                  <td><?= e($r['created_at']) ?></td>
                </tr>
              <?php endforeach; ?>
            <?php endif; ?>
          </tbody>
        </table>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="container">
      <small>&copy; <?= date('Y') ?> Student Registration App</small>
    </div>
  </footer>
</body>
</html>
