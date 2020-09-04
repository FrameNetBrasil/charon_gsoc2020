<?php
header("Access-Control-Allow-Origin: *");
require '../vendor/autoload.php';
include "config.php";
$dataPath = $config['dataPath'];

$filename = $dataPath . "Text_Store/combined/";
$content = file_get_contents($filename);
 var_dump($content);


echo nl2br("Sentences have been uploaded to database successfully!\n Return to Homepage\n");
