<?php
header("Access-Control-Allow-Origin: *");
include "config.php";

$hostname = $config['hostname'];
$username = $config['username'];
$dbname = $config['dbname'];
$password = $config['password'];
$usrtable2 = $config['usrtable2'];
$columnname2 = $config['columnname2'];
$usrtable3= $config['usrtable3'];
$columnname3 = $config['columnname3'];
$usrtable4 = $config['usrtable4'];
$columnname4 = $config['columnname4'];
$columnname5 = $config['columnname5'];
$c=[];
$d=[];
$s=[];

$vfd = $config['vfd'];
if ($vfd == null) {
    $vfd = "/";
}

$con = mysqli_connect($hostname, $username, $password);
mysqli_select_db($con, $dbname);
$query1 = "select $columnname2 from $usrtable2";
$result1 = mysqli_query($con, $query1);
$query2 = "select $columnname3 from $usrtable3";
$result2 = mysqli_query($con, $query2);
$query3 = "select $columnname4 from $usrtable4";
$result3 = mysqli_query($con, $query3);
$query4= "select $columnname5 from $usrtable4";
$result4 = mysqli_query($con, $query4);


if ($result3) {
    while ($row = mysqli_fetch_array($result3)) {
        $sent[] = $row["$columnname4"];
    }
}

$doc=[];
$corp=[];
$docid=[];
$corpid=[];


if ($result4) {
    while ($row = mysqli_fetch_array($result4)) {
        $sentids[] = $row["$columnname5"];
    }

    foreach($sentids as $item) {
    

    $query5="select idDocument,documentEntry from `view_sentence` where idSentence=$item";


    $result5 = mysqli_query($con, $query5);
    if($result5)
    {
        while ($row = mysqli_fetch_array($result5)) {
        $docs[] = $row["documentEntry"];
        $docids[] = $row["idDocument"]; 
        }
        foreach($docs as $x)
        {
        array_push($doc,$x);
        }
        foreach($docids as $x)
        {
        array_push($docid,$x);
        }
    }
    $query6="select idCorpus,corpusEntry from `view_sentence` where  idSentence='$item'";
    $result6 = mysqli_query($con, $query6);
    if($result6)
    {
        while ($row = mysqli_fetch_array($result6)) {
        $corps[] = $row["corpusEntry"];
        $corpids[] = $row["idCorpus"];
        }
        foreach($corps as $x)
        {
        array_push($corp,$x);
        }
        foreach($corpids as $x)
        {
        array_push($corpid,$x);
        }
    }
}
}

$doc=array_unique($doc);
$corp=array_unique($corp);
$docid=array_unique($docid);
$corpid=array_unique($corpid);

$vals=array($corp,$doc,$sent,$corpid,$docid);
echo json_encode($vals);
?>