<?php
header("Access-Control-Allow-Origin: *");
require '../vendor/autoload.php';
include "config.php";
$dataPath = $config['dataPath'];

if (isset($_FILES['custom'])) {
    $file_name = $_FILES['custom']['name'];
    $file_size = $_FILES['custom']['size'];
    $file_tmp = $_FILES['custom']['tmp_name'];
    $file_type = $_FILES['custom']['type'];

    if (move_uploaded_file($file_tmp, $dataPath .  "Text_Store/combined/" . $file_name)) {
        echo nl2br("Sentences have been uploaded successfully!\n Return to Homepage\n");
    } else {
        echo nl2br("There were errors while uploading. Please Try Again.\n Return to Homepage\n");
    }
}
