<h2>Galeriler</h2>

<form method="post" action="delete.php">

<div class="gallery">

<?php
$files=glob("../uploads/*");

foreach($files as $file){

$name=basename($file);
$date=date("d.m.Y H:i",filectime($file));

echo "
<div class='gallery-item'>
<img src='$file'>

<div class='meta'>
$name<br>
$date
</div>

<input type='checkbox' name='delete[]' value='$name'>
<br>

<button formaction='delete.php?single=$name'>Sil</button>

</div>";
}
?>

</div>

<br>
<button>Seçilenleri Sil</button>
</form>
