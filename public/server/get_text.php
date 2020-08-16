<?php
header("Access-Control-Allow-Origin: *");
include "config.php";
$dataPath = $config['dataPath'];

$path = $dataPath . "Text_Store/combined/";

$latest_ctime = 0;
$text_file = '';

$d = dir($path);
while (false !== ($entry = $d->read())) {
    $filepath = "{$path}/{$entry}";
    // could do also other checks than just checking whether the entry is a file
    if (is_file($filepath) && filectime($filepath) > $latest_ctime) {
        $latest_ctime = filectime($filepath);
        $text_file = $entry;
    }
}


$text = file_get_contents($dataPath . 'Text_Store/combined/' . $text_file);
$sentences = explode("\n\n", $text);
array_pop($sentences);
echo json_encode($sentences);

