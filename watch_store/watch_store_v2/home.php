<?php include 'shared.php'; ?>
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <title>ChronoLuxe — Home</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>

<body>
  <?php include 'navbar.php'; ?>
  <section class="hero">
    <div class="container">
      <h1 class="display-5" style="color:#30AE80">Timeless Luxury. Modern Precision.</h1>
      <p class="mt-3">Discover curated timepieces from Rolex, Omega, Seiko, Tag Heuer and more.</p>
      <a href="category.php" class="btn btn-success btn-lg mt-4 px-4">Shop Collection</a>
    </div>
  </section>
  <div class="container pb-5">
    <div class="row g-4">
      <div class="col-md-4">
        <div class="card p-4 h-100">
          <h5>Authentic Brands</h5>
          <p class="mb-0">Only verified models from world‑class houses.</p>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card p-4 h-100">
          <h5>Secure Checkout</h5>
          <p class="mb-0">Frictionless order flow with confirmation.</p>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card p-4 h-100">
          <h5>Fast Support</h5>
          <p class="mb-0">Questions? Reach us via the contact page.</p>
        </div>
      </div>
    </div>
  </div>
  <footer class="footer text-center py-4">© <?php echo date('Y'); ?> ChronoLuxe</footer>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>

</html>