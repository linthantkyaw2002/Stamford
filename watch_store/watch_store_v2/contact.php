<?php include 'shared.php'; ?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Contact — ChronoLuxe</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <?php include 'navbar.php'; ?>
  <div class="container py-5">
    <h2 class="text-center mb-4" style="color:#30AE80">Contact Us</h2>
    <div class="row justify-content-center">
      <div class="col-md-6">
        <form class="card p-4">
          <div class="mb-3"><label class="form-label">Your Name</label><input type="text" class="form-control" required></div>
          <div class="mb-3"><label class="form-label">Email Address</label><input type="email" class="form-control" required></div>
          <div class="mb-3"><label class="form-label">Message</label><textarea class="form-control" rows="4" required></textarea></div>
          <button type="submit" class="btn btn-success w-100">Send Message</button>
        </form>
      </div>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>