<?php
// DB + Session
$host = "localhost";
$user = "root";
$pass = "";
$db   = "watch_store";

$conn = new mysqli($host, $user, $pass, $db);
if ($conn->connect_error) { die("Database connection failed: " . $conn->connect_error); }
$conn->set_charset("utf8mb4");

session_start();
if (!isset($_SESSION['cart'])) { $_SESSION['cart'] = []; } // id => qty

function cart_count() { return array_sum($_SESSION['cart']); }
?>