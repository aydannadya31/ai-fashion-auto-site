<?php
session_start();
if(!isset($_SESSION["admin"])) exit("Giriş yok");
?>

<link rel="stylesheet" href="style.css">

<div class="sidebar">
<h2>ADMIN</h2>

<a href="?page=gallery">Galeriler</a>
<a href="?page=ai">AI Kuralları</a>

</div>

<a class="logout" href="logout.php">ÇIKIŞ</a>

<div class="main">

<?php
$page=$_GET["page"]??"gallery";
include $page.".php";
?>

</div>
