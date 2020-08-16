<?php

header("Access-Control-Allow-Origin: *");
include "config.php";
require '../vendor/autoload.php';

use thiagoalessio\TesseractOCR\TesseractOCR;

include_once('../vendor/james-heinrich/getid3/getid3/getid3.php');

$hostname = $config['hostname'];
$username = $config['username'];
$dbname = $config['dbname'];
$password = $config['password'];
$pathtable = $config['pathtable'];
$pathcolumn = $config['pathcolumn'];
$dataPath = $config['dataPath'];

$con = mysqli_connect($hostname, $username, $password);
mysqli_select_db($con, $dbname);
$query = "select $pathcolumn from $pathtable";
$result = mysqli_query($con, $query);

$getID3 = new getID3;
$target_dir = $dataPath . "Video_Store/full/";

$val1 = $_POST["n1"]; // upload from web (1) or computer (2)
$val2 = $_POST["n2"]; // if download was ok
$file = $_POST["n3"]; // file URL
$l = $_POST["n4"]; // language
$c = $_POST["n5"]; // corpus
$d = $_POST["n6"]; // document
$tb1 = $_POST["n7"];
$tb2 = $_POST["n8"];
$tb3 = $_POST["n9"];

//val1=1 means file download from URL
if ($val1 == "1") {
    if ($val2 == "1") {

        $ffmpeg = FFMpeg\FFMpeg::create(array(
            'ffmpeg.binaries' => $config['ffmpeg.binaries'],
            'ffprobe.binaries' => $config['ffprobe.binaries'],
            'timeout' => 3600, // The timeout for the underlying process
            'ffmpeg.threads' => 12, // The number of threads that FFMpeg should use
        ), @$logger);
        $url = $_POST["n3"];


        parse_str(parse_url($url, PHP_URL_QUERY), $vars);
        $vid = $vars['v'];

        if ($vid) {
            parse_str(file_get_contents("http://youtube.com/get_video_info?video_id=" . $vid), $info); //decode the data

            $videoData = json_decode($info['player_response'], true);
            $videoDetails = $videoData['videoDetails'];
            $streamingData = $videoData['streamingData'];
            $streamingDataFormats = $streamingData['formats'];
//set video title 
            $video_title = $videoDetails["title"];


            $video = $streamingDataFormats[1]['url'];
            $shaval = sha1($video_title);

            $fileName = $shaval . '.mp4';
            $target_dir = $dataPath . "Video_Store/full/";
            $target_file = $target_dir . $fileName;

            $uploadOk = 1;

            if ($result) {
                while ($row = mysqli_fetch_array($result)) {
                    if ($row["$pathcolumn"] == $target_file) {
                        echo nl2br("Sorry, file already exists.\r\n");
                        $uploadOk = 0;
                        break;
                    }
                }
            }

            if ($uploadOk == 1) {
                $query1 = "select idDocument from document where entry='$d'";
                $result1 = mysqli_query($con, $query1);
                $id = 0;
                while ($row = mysqli_fetch_array($result1)) {
                    $id = $row["idDocument"];
                    break;
                }

                file_put_contents($target_file, fopen($video, 'r'));

                $getID3 = new getID3;
                $file = $getID3->analyze($target_file);

                $width = $file['video']['resolution_x'];
                $height = $file['video']['resolution_y'];

                $size = "small";
                if ($width > 240 and $height > 180) {
                    $size = "large";
                }

                $path = $dataPath . "Images_Store/thumbs/$size/";
                $name = "$shaval.jpeg";

                $video = $ffmpeg->open($target_file);

                $video->frame(FFMpeg\Coordinate\TimeCode::fromSeconds(5))->save($path . $name);
// Set the formats
                $output_format = new FFMpeg\Format\Audio\Flac(); // Here you choose your output format
                $output_format->setAudioCodec("flac");
                $target_dir2 = $dataPath . "Audio_Store/audio/";
                $target_file2 = $target_dir2 . $shaval . ".flac";
                $video->save($output_format, $target_file2);

                $client = new \GuzzleHttp\Client([
                    'base_uri' => 'https://stream.watsonplatform.net/'
                ]);

                $audio = fopen($target_file2, 'r');
                $resp = $client->request('POST', 'speech-to-text/api/v1/recognize?end_of_phrase_silence_time=1.0&split_transcript_at_phrase_end=true&speaker_labels=true', [
                    'auth' => ['apikey', '0J34Y-yMVfdnaZpxdEwc8c-FoRPrpeTXcOOsxYM6lLls'],
                    'headers' => [
                        'Content-Type' => 'audio/flac',
                    ],
                    'body' => $audio
                ]);

                $transcript = $resp->getBody();
                $target_dir1 = $dataPath . "Text_Store/transcripts/";
                $target_file1 = $target_dir1 . $shaval . ".txt";
                $myfile = fopen($target_file1, "w");
                fwrite($myfile, $transcript);
                fclose($myfile);

                echo nl2br("Audio Transcripts generated.\r\n");

                $ffprobe = FFMpeg\FFProbe::create();

                $target_dir3 = $dataPath . "Text_Store/subtitles/";
                $target_file3 = $target_dir3 . $shaval . ".srt";
                $dur = $ffprobe
                    ->streams($target_file)
                    ->videos()
                    ->first()
                    ->get('duration');

                $fr = $ffprobe
                    ->streams($target_file)
                    ->videos()
                    ->first()
                    ->get('r_frame_rate');

                $dur = floor($dur) * 60;
                $fr = round($fr) / 1000;
                $n = round($dur / $fr);
                $fr = round($dur / $n);
                $framerate = '1/' . $fr;

                $mp4Format = new FFMpeg\Format\Video\X264('libmp3lame', 'libx264');

                $val = "";

                if ($n < 100)
                    $val = "02";
                elseif ($n < 1000)
                    $val = "03";
                else
                    $val = "06";

                $dir = "/tmp/{$shaval}";

                if (is_dir($dir)) {
                    rrmdir($dir);
                }
                mkdir($dir, 0777);

                $cmd = $config['ffmpeg.binaries'] . " -i {$target_file} -vf fps=1/5 {$dir}/img%{$val}d.jpg";
                exec($cmd);

                $files = array_diff(scandir($dir), ['..', '.']);

                $subtitle_file = fopen($dataPath . "Text_Store/subtitles/{$shaval}.srt", "w");
                asort($files);
                foreach ($files as $file) {
                    $full_path = $dir . '/' . $file;
                    $tesseract = new TesseractOCR($full_path);
                    $text = $tesseract->run();
                    fwrite($subtitle_file, $text);
                }
                fclose($subtitle_file);

                echo nl2br("Subtitles extracted.\r\n");

                $json = file_get_contents($target_file1);

//Decode JSON
                $json_data = json_decode($json, true);

                $results = $json_data["results"];

                $parsed_transcript = [];
                $i = -1;

                foreach ($results as $key => $value) {
                    $i = $i + 1;
                    $det1 = $results[$key];
                    $alternatives = $det1["alternatives"];

                    $det2 = $alternatives[0];
                    $transcript = $det2["transcript"];
                    $timestamps = $det2["timestamps"];


                    $num = count($timestamps);
                    $start_time = $timestamps[0][1];
                    $end_time = $timestamps[$num - 1][2];

                    $parsed_transcript[$i][0] = $start_time;
                    $parsed_transcript[$i][1] = $transcript;
                    $parsed_transcript[$i][2] = $end_time;
                }


                $subtitles = file_get_contents($dataPath . "./Text_Store/subtitles/{$shaval}.srt");
                $subtitles = str_replace("\n", " ", $subtitles);
                $subtitles = str_replace("‘", "'", $subtitles);

                $sub_ar = explode(" ", $subtitles);
                $p = $dataPath . "Text_Store/combined/{$shaval}.txt";
                $combined_file = fopen($p, "w");


                foreach ($parsed_transcript as $key => $value) {
                    $tr = $parsed_transcript[$key][1];
                    $tr_ar = explode(' ', $tr);
                    $cnt = count($tr_ar);

                    for ($x = 0; $x <= $cnt - 2; $x++) {
                        $flag = 0;
                        $cnt1 = count($sub_ar);

                        for ($y = 0; $y <= $cnt1 - 2; $y++) {
                            if ($tr_ar[$x] === strtolower($sub_ar[$y]) && $tr_ar[$x + 1] === strtolower($sub_ar[$y + 1]) && $tr_ar[$x + 2] === strtolower($sub_ar[$y + 2])) {
                                $first = $tr_ar[$x];
                                $val = 0;
                                for ($k = $x; $k <= $cnt - 2; $k++) {
                                    if ($tr_ar[$k] === $sub_ar[$y + $k - $x] || $tr_ar[$k + 1] === $sub_ar[$y + $k - $x + 1] || $tr_ar[$k] === $sub_ar[$y + $k - $x + 1]) {
                                        if ($tr_ar[$k] === $sub_ar[$y + $k - $x + 1]) {
                                            $inserted = array($sub_ar[$y + $k - $x]);

                                            array_splice($tr_ar, $k, 0, $inserted);

                                        } else
                                            $tr_ar[$k] = $sub_ar[$y + $k - $x];
                                    } else {
                                        $val = 1;
                                        break;
                                    }

                                    if ($tr_ar[$k] === $tr_ar[$k + 1])
                                        unset($arr1[$k]);
                                }
                                if ($val === 1)
                                    $tr_ar[$k] = $sub_ar[$y + $k - $x];
                                else {
                                    $tr_ar[$k] = $sub_ar[$y + $k - $x + 1];
                                }

                                $flag = 1;
                                break;
                            }
                        }
                        if ($flag === 1)
                            break;
                    }

                    $parsed_transcript[$key][1] = implode(' ', $tr_ar);
                    fwrite($combined_file, $parsed_transcript[$key][0] . "\n" . $parsed_transcript[$key][1] . "\n" . $parsed_transcript[$key][2] . "\n\n");
                }

                echo nl2br("Alignments Done.\r\n");

                $sql = "insert into $pathtable (audioPath,visualPath,alignPath,idDocument) values ('$target_file2','$target_file','$p',$id)";
                if ($con->query($sql) === TRUE) {
                    echo nl2br("New record created successfully\r\n");
                } else {
                    echo nl2br("Error: " . $sql . "<br>" . $con->error . "\r\n");
                }
                echo nl2br("Youtube Video Download finished! Now check the file\r\n");

                echo nl2br("Return to Home Page\r\n");
            } else {
                echo nl2br("There was a problem in downloading the file.\r\n");
                echo nl2br("Return to Home Page\r\n");
            }
        }
    } else if ($val2 == "0") {
        ?>
        <script>
            alert("Sorry, the file cannot be uploaded. Please Try again.");
            // if everything is ok, try to upload file
        </script>
        <?php
    }
} //val1=2 means file upload from computer
else if ($val1 == "2") {
    if ($val2 == "1") {
        $ffmpeg = FFMpeg\FFMpeg::create(array(
            'ffmpeg.binaries' => $config['ffmpeg.binaries'],
            'ffprobe.binaries' => $config['ffprobe.binaries'],
            'timeout' => 3600, // The timeout for the underlying process
            'ffmpeg.threads' => 12, // The number of threads that FFMpeg should use
        ), @$logger);
        $getID3 = new getID3;
        $cur_dir = getcwd();
        $target_dir = $dataPath . "/Video_Store/full/";
        $filename = $_POST["n3"];
        $f = fopen($filename, "r");
        $info = pathinfo($_POST['n3']);
        $ext = $info['extension']; // get the extension of the file
        $shaval = sha1($filename);
        $newname = $shaval . "." . $ext;
        $target_file = $target_dir . $newname;
        $uploadOk = 1;
        $err = '';
// Check if file already exists
        if ($result) {
            while ($row = mysqli_fetch_array($result)) {
                if ($row["$pathcolumn"] == $target_file) {
                    $err = nl2br("Sorry, file already exists.\r\n");
                    $uploadOk = 0;
                    break;
                }
            }
        }

// Check if file meets minimum size constraints
        $VIDEO_MIN_WIDTH = 720;
        if ($tb1 !== 0) {
            $VIDEO_MIN_WIDTH = $tb1;
        }
        $VIDEO_MIN_HEIGHT = 480;
        if ($tb2 !== 0) {
            $VIDEO_MIN_HEIGHT = $tb2;
        }

        $file = $getID3->analyze($filename);
        if (isset($file['video'])) {
            $val = 0;
            $width = $file['video']['resolution_x'];
            $height = $file['video']['resolution_y'];
            if ($height < $VIDEO_MIN_HEIGHT) {
                $err = nl2br("File height is less than MIN_HEIGHT=480, height of video is:" . $height . "\r\n");
                $uploadOk = 0;
            }
            if ($width < $VIDEO_MIN_WIDTH) {
                $err = nl2br("File width is less than MIN_WIDTH=720, width of video is:" . $width . "\r\n");
                $uploadOk = 0;
            }
        } else {
            $uploadOk = 0;
        }


// Check if $uploadOk is set to 0 by an error
        if ($uploadOk == 0) {
            ?>
            <script>
                alert("Sorry, the file cannot be uploaded. Please Try again.");
                // if everything is ok, try to upload file
            </script>

            <?php
        } else {
            $query1 = "select idDocument from document where entry='$d'";
            $result1 = mysqli_query($con, $query1);
            $id = 0;
            while ($row = mysqli_fetch_array($result1)) {
                $id = $row["idDocument"];
                break;
            }


            $width = $file['video']['resolution_x'];
            $height = $file['video']['resolution_y'];

            $size = "small";
            if ($width > 240 and $height > 180) {
                $size = "large";
            }

            ?>
            <p>Return to Home Page:</p>
            <?php
            if ($uploadOk == 1) {
                if (copy($filename, $target_file)) {
                    echo nl2br("The file " . basename($newname) . " has been uploaded.\r\n");

                    $path = $dataPath . "Images_Store/thumbs/$size/";
                    $name = "$shaval.jpeg";
                    $video = $ffmpeg->open($target_file);
                    if ($ext !== 'mp4') {
                        $mp4Format = new FFMpeg\Format\Video\X264('libmp3lame', 'libx264');
                        $new = $target_dir . $shaval . '.mp4';
                        $video->save($mp4Format, $new);
                        $video = $ffmpeg->open($new);
                        unlink($target_file);
                    }


                    $video->frame(FFMpeg\Coordinate\TimeCode::fromSeconds(5))->save($path . $name);

// Set the formats
                    $output_format = new FFMpeg\Format\Audio\Flac(); // Here you choose your output format
                    $output_format->setAudioCodec("flac");
                    $target_dir2 = $dataPath . "Audio_Store/audio/";
                    $target_file2 = $target_dir2 . $shaval . ".flac";
                    $video->save($output_format, $target_file2);

                    $client = new \GuzzleHttp\Client([
                        'base_uri' => 'https://stream.watsonplatform.net/'
                    ]);

                    $audio = fopen($target_file2, 'r');;
                    $resp = $client->request('POST', 'speech-to-text/api/v1/recognize?end_of_phrase_silence_time=2.0&split_transcript_at_phrase_end=true&speaker_labels=true', [
                        'auth' => ['apikey', '0J34Y-yMVfdnaZpxdEwc8c-FoRPrpeTXcOOsxYM6lLls'],
                        'headers' => [
                            'Content-Type' => 'audio/flac',
                        ],
                        'body' => $audio
                    ]);

                    $transcript = $resp->getBody();
                    $target_dir1 = $dataPath . "Text_Store/transcripts/";
                    $target_file1 = $target_dir1 . $shaval . ".txt";
                    $myfile = fopen($target_file1, "w");
                    fwrite($myfile, $transcript);
                    fclose($myfile);

                    echo nl2br("Audio Transcripts generated.\r\n");

                    $ffprobe = FFMpeg\FFProbe::create();

                    $target_dir3 = $dataPath . "Text_Store/subtitles/";
                    $target_file3 = $target_dir3 . $shaval . ".srt";
                    $dur = $ffprobe
                        ->streams($target_file)
                        ->videos()
                        ->first()
                        ->get('duration');

                    $fr = $ffprobe
                        ->streams($target_file)
                        ->videos()
                        ->first()
                        ->get('r_frame_rate');

                    $dur = floor($dur) * 60;
                    $fr = round($fr) / 1000;
                    $n = round($dur / $fr);
                    $fr = round($dur / $n);
                    $framerate = '1/' . $fr;


                    $val = "";

                    if ($n < 100)
                        $val = "02";
                    elseif ($n < 1000)
                        $val = "03";
                    else
                        $val = "06";

                    $dir = "/tmp/{$shaval}";
                    if (is_dir($dir)) {
                        rrmdir($dir);
                    }
                    mkdir($dir, 0777);


                    $cmd = $config['ffmpeg.binaries'] . " -i {$target_file} -vf fps=1/5 {$dir}/img%{$val}d.jpg";
                    exec($cmd);

                    $files = array_diff(scandir($dir), ['..', '.']);

                    $subtitle_file = fopen($dataPath . "Text_Store/subtitles/{$shaval}.srt", "w");
                    asort($files);
                    foreach ($files as $file) {
                        $full_path = $dir . '/' . $file;
                        $tesseract = new TesseractOCR($full_path);
                        $text = $tesseract->run();
                        fwrite($subtitle_file, $text);
                    }
                    fclose($subtitle_file);

                    echo nl2br("Subtitles extracted.\r\n");

                    $json = file_get_contents($target_file1);

//Decode JSON
                    $json_data = json_decode($json, true);

                    $results = $json_data["results"];

                    $parsed_transcript = [];
                    $i = -1;

                    foreach ($results as $key => $value) {
                        $i = $i + 1;
                        $det1 = $results[$key];
                        $alternatives = $det1["alternatives"];

                        $det2 = $alternatives[0];
                        $transcript = $det2["transcript"];
                        $timestamps = $det2["timestamps"];


                        $num = count($timestamps);
                        $start_time = $timestamps[0][1];
                        $end_time = $timestamps[$num - 1][2];

                        $parsed_transcript[$i][0] = $start_time;
                        $parsed_transcript[$i][1] = $transcript;
                        $parsed_transcript[$i][2] = $end_time;
                    }


                    $subtitles = file_get_contents("./Text_Store/subtitles/{$shaval}.srt");
                    $subtitles = str_replace("\n", " ", $subtitles);
                    $subtitles = str_replace("‘", "'", $subtitles);

                    $sub_ar = explode(" ", $subtitles);
                    $p = $dataPath . "Text_Store/combined/{$shaval}.txt";
                    $combined_file = fopen($p, "w");


                    foreach ($parsed_transcript as $key => $value) {
                        $tr = $parsed_transcript[$key][1];
                        $tr_ar = explode(' ', $tr);
                        $cnt = count($tr_ar);

                        for ($x = 0; $x <= $cnt - 2; $x++) {
                            $flag = 0;
                            $cnt1 = count($sub_ar);

                            for ($y = 0; $y <= $cnt1 - 2; $y++) {
                                if ($tr_ar[$x] === strtolower($sub_ar[$y]) && $tr_ar[$x + 1] === strtolower($sub_ar[$y + 1]) && $tr_ar[$x + 2] === strtolower($sub_ar[$y + 2])) {
                                    $first = $tr_ar[$x];
                                    $val = 0;
                                    for ($k = $x; $k <= $cnt - 2; $k++) {
                                        if ($tr_ar[$k] === $sub_ar[$y + $k - $x] || $tr_ar[$k + 1] === $sub_ar[$y + $k - $x + 1] || $tr_ar[$k] === $sub_ar[$y + $k - $x + 1]) {
                                            if ($tr_ar[$k] === $sub_ar[$y + $k - $x + 1]) {
                                                $inserted = array($sub_ar[$y + $k - $x]);
                                                array_splice($tr_ar, $k, 0, $inserted);

                                            } else
                                                $tr_ar[$k] = $sub_ar[$y + $k - $x];
                                        } else {
                                            $val = 1;
                                            break;
                                        }

                                        if ($tr_ar[$k] === $tr_ar[$k + 1])
                                            unset($arr1[$k]);
                                    }
                                    if ($val === 1)
                                        $tr_ar[$k] = $sub_ar[$y + $k - $x];
                                    else {
                                        $tr_ar[$k] = $sub_ar[$y + $k - $x + 1];
                                    }

                                    $flag = 1;
                                    break;
                                }
                            }
                            if ($flag === 1)
                                break;
                        }

                        $parsed_transcript[$key][1] = implode(' ', $tr_ar);
                        fwrite($combined_file, $parsed_transcript[$key][0] . "\n" . $parsed_transcript[$key][1] . "\n" . $parsed_transcript[$key][2] . "\n\n");
                    }

                    echo nl2br("Alignments Done.\r\n");

                    $sql = "insert into $pathtable (audioPath,visualPath,alignPath,idDocument) values ('$target_file2','$target_file','$p',$id)";
                    if ($con->query($sql) === TRUE) {
                        echo nl2br("New record created successfully\r\n");
                    } else {
                        echo nl2br("Error: " . $sql . "<br>" . $con->error . "\r\n");
                    }
                }
            } else {
                echo nl2br("Sorry, there was an error uploading your file. {$err}\r\n");
            }
        }
    } else if ($val2 == "0") {
        echo nl2br("The file could not be uploaded. Return to home page.\r\n");
    }
}

function rrmdir($dir)
{
    if (is_dir($dir)) {
        $objects = scandir($dir);
        foreach ($objects as $object) {
            if ($object != "." && $object != "..") {
                if (filetype($dir . "/" . $object) == "dir") rrmdir($dir . "/" . $object); else unlink($dir . "/" . $object);
            }
        }
        reset($objects);
        rmdir($dir);
    }
}