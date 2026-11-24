<?php
include 'shared.php';
$id = (int) ($_GET['id'] ?? 0);
$order = $conn->query("SELECT * FROM orders WHERE id = $id")->fetch_assoc();
if (!$order) {
  echo "<div style='padding:2rem'>Order not found.</div>";
  exit;
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <title>Order Success — ChronoLuxe</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>

<body>
  <?php include 'navbar.php'; ?>
  <div class="container py-5 text-center">
    <div class="card p-5 mx-auto" style="max-width:640px">
      <h2 class="text-success">✅ Order Successful</h2>
      <p class="mt-2">Thanks, <strong><?php echo htmlspecialchars($order['name']); ?></strong>!</p>
      <p class="mb-1">Order ID: <strong>#<?php echo $order['id']; ?></strong></p>
      <p>Total: <strong>$<?php echo number_format($order['total'], 2); ?></strong></p>
      <p class="small">A confirmation will be sent to <?php echo htmlspecialchars($order['email']); ?>.</p>
      <a href="home.php" class="btn btn-dark mt-3">Back to Home</a>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>

</html>