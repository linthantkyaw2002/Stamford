<?php require_once 'shared.php'; ?>
<nav class="navbar navbar-expand-lg navbar-dark bg-black border-bottom border-dark sticky-top">
  <div class="container">
    <a class="navbar-brand fw-bold" href="home.php"><span style="color:#30AE80;">Chrono</span>Luxe</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navMenu">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item"><a href="home.php" class="nav-link">Home</a></li>
        <li class="nav-item"><a href="category.php" class="nav-link">Category</a></li>
        <li class="nav-item"><a href="about.php" class="nav-link">About</a></li>
        <li class="nav-item"><a href="contact.php" class="nav-link">Contact</a></li>
        <li class="nav-item">
          <a href="cart.php" class="nav-link">🛒 Cart (<?php echo cart_count(); ?>)</a>
        </li>
      </ul>
    </div>
  </div>
</nav>