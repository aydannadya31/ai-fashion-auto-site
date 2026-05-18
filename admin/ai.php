<h2>AI Prompt Kuralları</h2>

<form method="post" action="save_ai.php">

<div class="card">

<h3>MODEL_FEATURES</h3>
<input name="MODEL_FEATURES">

<h3>CLOTHING_FEATURES</h3>
<input name="CLOTHING_FEATURES">

<h3>EDITORIAL_ENVIRONMENT</h3>
<input name="EDITORIAL_ENVIRONMENT">

<h3>TECHNICAL_TAGS</h3>
<input name="TECHNICAL_TAGS">

<br><br>
<button>Kaydet</button>

</div>

</form>

<div class="card">
<h3>Mevcut Kurallar</h3>

<?php
$data=json_decode(file_get_contents("../ai_rules.json"),true);

foreach($data as $k=>$v){
echo "<b>$k</b>: $v<br>";
}
?>

</div>
