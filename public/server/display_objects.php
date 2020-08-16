<?php
$filepath= 'objects.png';
header('Content-type: image/jpeg');
echo file_get_contents($filepath);
?>