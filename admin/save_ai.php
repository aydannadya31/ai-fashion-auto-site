<?php

$file="../ai_rules.json";

$data=json_decode(@file_get_contents($file),true);

foreach($_POST as $key=>$value){

if(trim($value)!=""){
$data[$key]=$value; // eskiyi ez
}

}

file_put_contents($file,json_encode($data,JSON_PRETTY_PRINT));

header("Location:index.php?page=ai");
