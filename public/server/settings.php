<?php
header("Access-Control-Allow-Origin: *");
require '../vendor/autoload.php';
$tb1 = $_POST["tb1"];
$tb2 = $_POST["tb2"];
$cb = $_POST["cb"];
echo nl2br($tb1 . "\n");
echo nl2br($tb2 . "\n");
echo nl2br($cb . "\n");
