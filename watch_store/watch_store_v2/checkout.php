<?php
include 'shared.php';
if (empty($_SESSION['cart'])) {
  header("Location: category.php");
  exit;
}

$total = 0;
$ids = implode(',', array_map('intval', array_keys($_SESSION['cart'])));
$res = $conn->query("SELECT id, name, price FROM products WHERE id IN ($ids)");
$prods = [];
while ($p = $res->fetch_assoc()) {
  $prods[(int) $p['id']] = $p;
}
foreach ($_SESSION['cart'] as $pid => $qty) {
  $total += (float) $prods[$pid]['price'] * (int) $qty;
}

if (isset($_POST['submit'])) {
  $name = $conn->real_escape_string($_POST['name']);
  $email = $conn->real_escape_string($_POST['email']);
  $address = $conn->real_escape_string($_POST['address']);
  $conn->query("INSERT INTO orders (name, email, address, total) VALUES ('$name', '$email', '$address', '$total')");
  $order_id = $conn->insert_id;
  foreach ($_SESSION['cart'] as $pid => $qty) {
    $pid = (int) $pid;
    $qty = (int) $qty;
    $conn->query("INSERT INTO order_items (order_id, product_id, quantity) VALUES ($order_id, $pid, $qty)");
  }
  $_SESSION['cart'] = [];
  header("Location: success.php?id=" . $order_id);
  exit;
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <title>Checkout — ChronoLuxe</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>

<body>
  <?php include 'navbar.php'; ?>
  <div class="container py-4">
    <h2 class="mb-3">Checkout</h2>
    <div class="row g-4">
      <div class="col-md-6">
        <form method="post" class="card p-4">
          <div class="mb-3"><label class="form-label">Full Name</label><input type="text" name="name"
              class="form-control" required></div>
          <div class="mb-3"><label class="form-label">Email</label><input type="email" name="email" class="form-control"
              required></div>
          <div class="mb-3"><label class="form-label">Address</label><textarea name="address" class="form-control"
              rows="3" required></textarea></div>
          <button class="btn btn-success w-100" name="submit">Confirm & Buy</button>
        </form>
      </div>
      <div class="col-md-6">
        <div class="card p-4 h-100">
          <h5 class="mb-3">Order Summary</h5>
          <ul class="list-group list-group-flush">
            <?php foreach ($_SESSION['cart'] as $pid => $qty): ?>
              <li class="checkout-list list-group-item bg-transparent d-flex justify-content-between align-items-center"
                style="color: aliceblue;">
                <span><?php echo htmlspecialchars($prods[$pid]['name']); ?> × <?php echo (int) $qty; ?></span>
                <span>$<?php echo number_format($prods[$pid]['price'] * $qty, 2); ?></span>
              </li>
            <?php endforeach; ?>
          </ul>
          <div class="d-flex justify-content-between align-items-center mt-3">
            <strong>Total</strong><strong>$<?php echo number_format($total, 2); ?></strong>
          </div>
        </div>
      </div>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>

</html>