<?php
include 'shared.php';

/* CART ACTIONS */
if (isset($_POST['add'])) {
  $id = (int)($_POST['id'] ?? 0);
  if ($id > 0) {
    $_SESSION['cart'][$id] = ($_SESSION['cart'][$id] ?? 0) + 1;
  }
  header("Location: cart.php"); exit;
}

if (isset($_POST['update'])) {
  foreach ($_POST['qty'] ?? [] as $pid => $qty) {
    $pid = (int)$pid; $qty = max(0, (int)$qty);
    if ($qty === 0) unset($_SESSION['cart'][$pid]);
    else $_SESSION['cart'][$pid] = $qty;
  }
}

if (isset($_GET['remove'])) {
  $rid = (int)$_GET['remove'];
  unset($_SESSION['cart'][$rid]);
  header("Location: cart.php"); exit;
}

/* BUILD LINES */
$items = []; $total = 0;
if (!empty($_SESSION['cart'])) {
  $ids = implode(',', array_map('intval', array_keys($_SESSION['cart'])));
  $res = $conn->query("SELECT * FROM products WHERE id IN ($ids)");
  while ($p = $res->fetch_assoc()) {
    $pid = (int)$p['id'];
    $qty = (int)($_SESSION['cart'][$pid] ?? 0);
    if ($qty <= 0) continue;
    $line = $qty * (float)$p['price'];
    $items[] = ['id'=>$pid,'name'=>$p['name'],'brand'=>$p['brand'],'image'=>$p['image'],'price'=>$p['price'],'qty'=>$qty,'line'=>$line];
    $total += $line;
  }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Your Cart — ChronoLuxe</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <?php include 'navbar.php'; ?>
  <div class="container py-4">
    <h2 class="mb-3">Your Cart</h2>
    <?php if (empty($items)): ?>
      <div class="alert alert-dark">Your cart is empty.</div>
      <a href="category.php" class="btn btn-success">Browse Watches</a>
    <?php else: ?>
      <form method="post">
        <div class="table-responsive">
          <table class="table align-middle text-center">
            <thead>
              <tr><th class="text-start">Product</th><th>Brand</th><th>Price</th><th width="120">Qty</th><th>Subtotal</th><th></th></tr>
            </thead>
            <tbody>
              <?php foreach ($items as $it): ?>
              <tr>
                <td class="text-start">
                  <img src="<?php echo htmlspecialchars($it['image']); ?>" width="60" class="me-2 rounded"> 
                  <?php echo htmlspecialchars($it['name']); ?>
                </td>
                <td><?php echo htmlspecialchars($it['brand']); ?></td>
                <td>$<?php echo number_format($it['price'],2); ?></td>
                <td><input class="form-control form-control-sm text-center" type="number" name="qty[<?php echo (int)$it['id']; ?>]" value="<?php echo (int)$it['qty']; ?>" min="0"></td>
                <td>$<?php echo number_format($it['line'],2); ?></td>
                <td><a class="btn btn-sm btn-outline-danger" href="cart.php?remove=<?php echo (int)$it['id']; ?>">Remove</a></td>
              </tr>
              <?php endforeach; ?>
            </tbody>
          </table>
        </div>
        <div class="d-flex justify-content-between align-items-center mt-2">
          <button name="update" class="btn btn-outline-light">Update Cart</button>
          <div class="fs-5">Total: <strong>$<?php echo number_format($total,2); ?></strong></div>
        </div>
      </form>
      <div class="text-end mt-3">
        <a href="checkout.php" class="btn btn-success px-4">Proceed to Checkout</a>
      </div>
    <?php endif; ?>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>