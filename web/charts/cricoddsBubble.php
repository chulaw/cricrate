<?php

date_default_timezone_set("America/New_York");
$matchFormat = $_GET["matchFormat"];
$inn = $_GET["inn"];
$runs = $_GET["runs"];
$overs = $_GET["overs"];
$wkts = $_GET["wkts"];
$matchFormatLower = strtolower($matchFormat);

if ($matchFormat == "ODI") {
  $startDate = "19710000";
} else if ($matchFormat == "T20") {
  $startDate = "20050000";
}
$endDate = "20999999";

if (isset($_GET['startDate'])) {
  if ($_GET['startDate'] != "") {
    if (strpos($_GET['startDate'], "-") == false) {
      $startDate = $_GET['startDate'];
    } else {
      $startDates = explode("-", $_GET['startDate']);
      $startDate = $startDates[0].$startDates[1].$startDates[2];
    }
  }
}

if (isset($_GET['endDate'])) {
  if ($_GET['endDate'] != "") {
    if (strpos($_GET['endDate'], "-") == false) {
      $endDate = $_GET['endDate'];
    } else {
      $endDates = explode("-", $_GET['endDate']);
      $endDate = $endDates[0].$endDates[1].$endDates[2];
    }
  }
}

if ($matchFormat == "ODI") {
  $db = new SQLite3("../ccrODI.db");
} elseif ($matchFormat == "T20") {
  $db = new SQLite3("../ccrT20I.db");
}

if (strpos($overs, ".")) {
  $oversBalls = explode(".", $overs);
  $ballsRem = $oversBalls[0] * 6 + $oversBalls[1];
} else {
  $ballsRem = $overs * 6;
}

if ($matchFormat == "ODI") {
  if ($inn == 1) {
    if ($runs == 0) {
      $sql = 'select o.'.$matchFormatLower.'Id, o.runs, o.overs, o.runRate, o.wkts, o.teamBat, t.team1, t.team2, t.ground, t.startDate, o.result from overComparisonODI o, '.$matchFormatLower.'Info t where o.'.$matchFormatLower.'Id=t.'.$matchFormatLower.'Id and o.innings=1 and t.startDate>='.$startDate.' and t.startDate<='.$endDate.' and o.overs>='.($overs-1).' and o.overs<'.($overs+1).' and o.runs<=1 and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1);
    } else {
      $sql = 'select o.'.$matchFormatLower.'Id, o.runs, o.overs, o.runRate, o.wkts, o.teamBat, t.team1, t.team2, t.ground, t.startDate, o.result from overComparisonODI o, '.$matchFormatLower.'Info t where o.'.$matchFormatLower.'Id=t.'.$matchFormatLower.'Id and o.innings=1 and t.startDate>='.$startDate.' and t.startDate<='.$endDate.' and o.overs>='.($overs-1).' and o.overs<'.($overs+1).' and o.runs<='.($runs*1.1).' and o.runs>'.($runs*0.9).' and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1);
    }
  } else if ($inn == 2) {
    if ($ballsRem < 60) {
      $sql = 'select o.'.$matchFormatLower.'Id, o.runsReq, o.ballsRem, o.reqRate, o.wkts, o.teamBat, t.team1, t.team2, t.ground, t.startDate, o.result from overComparisonODI o, '.$matchFormatLower.'Info t where o.'.$matchFormatLower.'Id=t.'.$matchFormatLower.'Id and o.innings=2 and t.startDate>='.$startDate.' and t.startDate<='.$endDate.' and o.ballsRem>'.($ballsRem*0.75).' and o.ballsRem<='.($ballsRem*1.25).' and o.runsReq<'.($runs*1.25).' and o.runsReq>='.($runs*0.75).' and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1);
    } else {
      $sql = 'select o.'.$matchFormatLower.'Id, o.runsReq, o.ballsRem, o.reqRate, o.wkts, o.teamBat, t.team1, t.team2, t.ground, t.startDate, o.result from overComparisonODI o, '.$matchFormatLower.'Info t where o.'.$matchFormatLower.'Id=t.'.$matchFormatLower.'Id and o.innings=2 and t.startDate>='.$startDate.' and t.startDate<='.$endDate.' and o.ballsRem>'.($ballsRem*0.9).' and o.ballsRem<='.($ballsRem*1.1).' and o.runsReq<'.($runs*1.1).' and o.runsReq>='.($runs*0.9).' and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1);
    }
  }
} else {
  if ($inn == 1) {
    if ($runs == 0) {
      $sql = 'select o.'.$matchFormatLower.'Id, o.runs, o.overs, o.runRate, o.wkts, o.teamBat, o.result from overComparison o where o.innings=1 and o.overs>='.($overs-1).' and o.overs<'.($overs+1).' and o.runs<=1 and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1);
    } else {
      $sql = 'select o.'.$matchFormatLower.'Id, o.runs, o.overs, o.runRate, o.wkts, o.teamBat, o.result from overComparison o where o.innings=1 and o.overs>='.($overs-1).' and o.overs<'.($overs+1).' and o.runs<='.($runs*1.1).' and o.runs>'.($runs*0.9).' and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1);
    }
  } else if ($inn == 2) {
    if ($ballsRem < 60) {
      $sql = 'select o.'.$matchFormatLower.'Id, o.runsReq, o.ballsRem, o.reqRate, o.wkts, o.teamBat, o.result from overComparison o where o.innings=2 and o.ballsRem>'.($ballsRem*0.75).' and o.ballsRem<='.($ballsRem*1.25).' and o.runsReq<'.($runs*1.25).' and o.runsReq>='.($runs*0.75).' and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1);
    } else {
      $sql = 'select o.'.$matchFormatLower.'Id, o.runsReq, o.ballsRem, o.reqRate, o.wkts, o.teamBat, o.result from overComparison o where o.innings=2 and o.ballsRem>'.($ballsRem*0.9).' and o.ballsRem<='.($ballsRem*1.1).' and o.runsReq<'.($runs*1.1).' and o.runsReq>='.($runs*0.9).' and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1);
    }
  }
}
//echo $sql;
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");

$dates = array();
$matchIds = array();
$rr = array();
$results = array();
if ($matchFormat == "ODI") {
  while($res = $result->fetchArray(SQLITE3_NUM)) {
    if ($res[10] == 2) {
      $dateMod = substr($res[9], 0, 4)."-".substr($res[9], 4, 2)."-".substr($res[9], 6, 2);
      array_push($dates, $dateMod);
      array_push($matchIds, $res[0]);
      array_push($rr, round($res[3], 2));
      array_push($results, "Win");
    }
  }

  while($res = $result->fetchArray(SQLITE3_NUM)) {
    if ($res[10] == 0) {
      $dateMod = substr($res[9], 0, 4)."-".substr($res[9], 4, 2)."-".substr($res[9], 6, 2);
      array_push($dates, $dateMod);
      array_push($matchIds, $res[0]);
      array_push($rr, round($res[3], 2));
      array_push($results, "Loss");
    }
  }

  while($res = $result->fetchArray(SQLITE3_NUM)) {
    if ($res[10] == 1) {
      $dateMod = substr($res[9], 0, 4)."-".substr($res[9], 4, 2)."-".substr($res[9], 6, 2);
      array_push($dates, $dateMod);
      array_push($matchIds, $res[0]);
      array_push($rr, round($res[3], 2));
      array_push($results, "Tie/NR");
    }
  }
} else {
  while($res = $result->fetchArray(SQLITE3_NUM)) {
    if ($res[6] == 2) {
      array_push($dates, "");
      array_push($matchIds, $res[0]);
      array_push($rr, round($res[3], 2));
      array_push($results, "Win");
    }
  }

  while($res = $result->fetchArray(SQLITE3_NUM)) {
    if ($res[6] == 0) {
      array_push($dates, "");
      array_push($matchIds, $res[0]);
      array_push($rr, round($res[3], 2));
      array_push($results, "Loss");
    }
  }

  while($res = $result->fetchArray(SQLITE3_NUM)) {
    if ($res[6] == 1) {
      array_push($dates, "");
      array_push($matchIds, $res[0]);
      array_push($rr, round($res[3], 2));
      array_push($results, "Tie/NR");
    }
  }
}

$table = array();
$table['cols'] = array(
                        array('id' => "", 'label' => "Date", 'pattern' => "", 'type' => 'string'),
                        array('id' => "", 'label' => "Match #", 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'label' => "Run Rate", 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'label' => "Result", 'pattern' => "", 'type' => 'string'),
                    );

$rows = array();

for ($i = 0; $i < count($matchIds); $i++) {
    $temp = array();
    $temp[] = array('v' => $dates[$i]);
    $temp[] = array('v' => $matchIds[$i]);
    $temp[] = array('v' => $rr[$i]);
    $temp[] = array('v' => $results[$i]);
    $rows[] = array('c' => $temp);
}

$table['rows'] = $rows;
$jsonTable = json_encode($table);
echo $jsonTable;
?>
