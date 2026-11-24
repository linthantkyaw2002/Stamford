<?php include 'shared.php'; ?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ChronoLuxe — Category</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <?php include 'navbar.php'; ?>
  <div class="container py-4">
    <div class="d-flex flex-wrap justify-content-between align-items-center mb-3">
      <h2 class="m-0">Watches</h2>
      <form class="d-flex" method="get" action="category.php">
        <input class="form-control me-2" type="search" name="q" placeholder="Search by name or brand" value="<?php echo htmlspecialchars($_GET['q'] ?? ''); ?>">
        <button class="btn btn-success" type="submit">Search</button>
      </form>
    </div>
    <div class="row g-4">
      <?php
        $q = trim($_GET['q'] ?? '');
        if ($q !== '') {
          $safe = $conn->real_escape_string($q);
          $sql = "SELECT * FROM products WHERE name LIKE '%$safe%' OR brand LIKE '%$safe%' ORDER BY id DESC";
        } else {
          $sql = "SELECT * FROM products ORDER BY id DESC";
        }
        $result = $conn->query($sql);
        while ($row = $result->fetch_assoc()):
      ?>
      <div class="col-12 col-sm-6 col-md-4 col-lg-3">
        <div class="card h-100 text-center">
          <img src="<?php echo htmlspecialchars($row['image']); ?>" class="card-img-top" alt="">
          <div class="card-body d-flex flex-column">
            <span class="badge badge-brand align-self-start mb-2"><?php echo htmlspecialchars($row['brand']); ?></span>
            <h6 class="card-title"><?php echo htmlspecialchars($row['name']); ?></h6>
            <div class="mt-auto">
              <p class="price mb-3">$<?php echo number_format($row['price'], 2); ?></p>
              <form action="cart.php" method="POST">
                <input type="hidden" name="id" value="<?php echo (int)$row['id']; ?>">
                <button type="submit" name="add" class="btn btn-success w-100">Add to Cart</button>
              </form>
            </div>
          </div>
        </div>
      </div>
      <?php endwhile; ?>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>