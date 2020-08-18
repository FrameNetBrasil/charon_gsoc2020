<?php
header("Access-Control-Allow-Origin: *");
include "config.php";

$hostname = $config['hostname'];
$username = $config['username'];
$dbname = $config['dbname'];
$password = $config['password'];
$usrtable1 = $config['usrtable1'];
$columnname1 = $config['columnname1'];
$usrtable2 = $config['usrtable2'];
$columnname2 = $config['columnname2'];
$usrtable3 = $config['usrtable3'];
$columnname3 = $config['columnname3'];
$l = [];
$c = [];
$d = [];

//$vfd = $config['vfd'];
//if ($vfd == null) {
//    $vfd = "/";
//}

$con = mysqli_connect($hostname, $username, $password);
mysqli_select_db($con, $dbname);
$query1 = "select $columnname1 from $usrtable1";
$result1 = mysqli_query($con, $query1);
$query2 = "select $columnname2 from $usrtable2";
$result2 = mysqli_query($con, $query2);
$query3 = "select $columnname3 from $usrtable3";
$result3 = mysqli_query($con, $query3);

if ($result1) {
    while ($row = mysqli_fetch_array($result1)) {
        $lang[] = $row["$columnname1"];
    }
}

if ($result2) {
    while ($row = mysqli_fetch_array($result2)) {
        $corp[] = $row["$columnname2"];
    }
}

if ($result3) {
    while ($row = mysqli_fetch_array($result3)) {
        $doc[] = $row["$columnname3"];
    }
}

$vals = array($lang, $corp, $doc);
echo json_encode($vals);
