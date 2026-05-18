<?php

if(isset($_GET["single"])){
unlink("../uploads/".$_GET["single"]);
header("Location:index.php?page=gallery");
exit;
}

if(isset($_POST["delete"])){

foreach($_POST["delete"] as $file){
unlink("../uploads/".$file);
}

}

header("Location:index.php?page=gallery");
