<?php

$match = $_GET["match"];

$csvFile = file('https://s3-eu-west-1.amazonaws.com/cricrate/liveOdds.csv');
$data = [];
$overs = [];
$oversAdj = [];
$betOdds = [];
$crOdds = [];
$crMLOdds = [];
$inn1stOvers = 0;
$inns = [];
$runsReqs = [];
$wkts = [];
$runRates = [];
# set max first innings overs
foreach ($csvFile as $line) {
    $data = str_getcsv($line);
    $dateTime = explode(" ", $data[0]);
    $matchDate = $dateTime[0];
    $matchFormat = $data[1];
    $team1 = $data[2];
    $team2 = $data[3];
    $inn = $data[4];
    $matchSt = $matchDate . ": " . $team1 . " vs " . $team2 . " " . $matchFormat;
    if ($inn == 2) {
        $matchSt = $matchDate . ": " . $team2 . " vs " . $team1 . " " . $matchFormat;
    }
    if ($match == $matchSt) {
      $ov = $data[7];
      if ($inn == 1 && $ov > $inn1stOvers) {
        $inn1stOvers = $ov;
      }
    }
}

foreach ($csvFile as $line) {
    $data = str_getcsv($line);
    $dateTime = explode(" ", $data[0]);
    $matchDate = $dateTime[0];
    $matchFormat = $data[1];
    $team1 = $data[2];
    $team2 = $data[3];
    $inn = $data[4];
    $matchSt = $matchDate . ": " . $team1 . " vs " . $team2 . " " . $matchFormat;
    if ($inn == 2) {
        $matchSt = $matchDate . ": " . $team2 . " vs " . $team1 . " " . $matchFormat;
    }
    if ($match == $matchSt) {
      $runsReq = $data[5];
      $wkt = $data[6];
      $ov = $data[7];
      $runRate = $data[8];
      $betO = $data[9];
      $crO = $data[10];
      $crMLO = $data[11];
      if ($inn == 2) {
        $inn2ndOvers = $inn1stOvers + $ov;
        array_push($oversAdj, $inn2ndOvers);
        $crOdds[$inn2ndOvers] = 100 - $crO;
        $crMLOdds[$inn2ndOvers] = 100 - $crMLO;
        $betOdds[$inn2ndOvers] = 100 - $betO;
        $overs[$inn2ndOvers] = $ov;
        $inns[$inn2ndOvers] = $inn;
        $runsReqs[$inn2ndOvers] = $runsReq;
        $wkts[$inn2ndOvers] = $wkt;
        $runRates[$inn2ndOvers] = $runRate;
       } else {
        array_push($oversAdj, $ov);
        $crOdds[$ov] = $crO;
        $crMLOdds[$ov] = $crMLO;
        $betOdds[$ov] = $betO;
        $overs[$ov] = $ov;
        $inns[$ov] = $inn;
        $runsReqs[$ov] = $runsReq;
        $wkts[$ov] = $wkt;
        $runRates[$ov] = $runRate;
      }
    }
}

sort($oversAdj);

$table = array();
$table['cols'] = array(
                        array('id' => "", 'label' => 'Overs', 'pattern' => "", 'type' => 'string'),
                        array('id' => "", 'label' => 'Betting Odds', 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'type' => 'string', 'p' => array('role' => 'tooltip', 'html' => true)),
                        array('id' => "", 'label' => 'Cricrate Base Odds', 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'type' => 'string', 'p' => array('role' => 'tooltip', 'html' => true)),
                        array('id' => "", 'label' => 'Cricrate ML Odds', 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'type' => 'string', 'p' => array('role' => 'tooltip', 'html' => true)),
                    );

$rows = array();
foreach ($oversAdj as $k => $x) {
    $temp = array();
    $temp[] = array('v' => $x);
    $temp[] = array('v' => $betOdds[$x]);
    $details = "<div style=\"padding:5px 5px 5px 5px; font-size:11px;\">";
    $details .= "Innings: <b>".$inns[$x]."</b><br/>";
    if ($inns[$x] == 1) {
      $details .= "Runs: <b>".$runsReqs[$x]."</b><br/>";
    } else {
      $details .= "Runs Required: <b>".$runsReqs[$x]."</b><br/>";
    }
    $details .= "Wkts: <b>".$wkts[$x]."</b><br/>";
    $balls = round($overs[$x] * 6);
    $actualBalls = $balls % 6;
    $actualOvers = ($balls - $actualBalls) / 6;
    if ($actualBalls > 0) {
      $details .= "Overs: <b>".$actualOvers.".".$actualBalls."</b><br/>";
    } else {
      $details .= "Overs: <b>".$actualOvers."</b><br/>";
    }
    if ($inns[$x] == 1) {
      $details .= "Run Rate: <b>".$runRates[$x]."</b><br/>";
    } else {
      $details .= "Req Rate: <b>".$runRates[$x]."</b><br/>";
    }

    $details1 = $details;
    $details2 = $details;
    $details3 = $details;
    $details1 .= "Betting Site Odds: <b>".$betOdds[$x]."</b><br/>";
    $details1 .= "</div>";
    $details2 .= "cricrate Base Odds: <b>".$crOdds[$x]."</b><br/>";
    $details2 .= "</div>";
    $details3 .= "cricrate ML Odds: <b>".$crMLOdds[$x]."</b><br/>";
    $details3 .= "</div>";
    $temp[] = array('v' => $details1);
    $temp[] = array('v' => $crOdds[$x]);
    $temp[] = array('v' => $details2);
    $temp[] = array('v' => $crMLOdds[$x]);
    $temp[] = array('v' => $details3);
    $rows[] = array('c' => $temp);
}

$table['rows'] = $rows;
$jsonTable = json_encode($table);
echo $jsonTable;
?>
