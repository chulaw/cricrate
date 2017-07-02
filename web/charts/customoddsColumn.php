<?php

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
      $sql = 'select avg(o.runRate), avg(o.result) from overComparisonODI o, odiInfo t where o.odiId = t.odiId and o.innings=1 and t.startDate>='.$startDate.' and t.startDate<='.$endDate.' and o.overs>='.($overs-1).' and o.overs<'.($overs+1).' and o.runs<=1 and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1).' group by o.odiId';
    } else {
      $sql = 'select avg(o.runRate), avg(o.result) from overComparisonODI o, odiInfo t where o.odiId = t.odiId and o.innings=1 and t.startDate>='.$startDate.' and t.startDate<='.$endDate.' and o.overs>='.($overs-1).' and o.overs<'.($overs+1).' and o.runs<='.($runs*1.1).' and o.runs>'.($runs*0.9).' and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1).' group by o.odiId';
    }
  } else if ($inn == 2) {
    if ($ballsRem < 60) {
      $sql = 'select avg(o.reqRate), avg(o.result) from overComparisonODI o, odiInfo t where o.odiId = t.odiId and o.innings=2 and t.startDate>='.$startDate.' and t.startDate<='.$endDate.' and o.ballsRem>'.($ballsRem*0.75).' and o.ballsRem<='.($ballsRem*1.25).' and o.runsReq<'.($runs*1.25).' and o.runsReq>='.($runs*0.75).' and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1).' group by o.odiId';
    } else {
      $sql = 'select avg(o.reqRate), avg(o.result) from overComparisonODI o, odiInfo t where o.odiId = t.odiId and o.innings=2 and t.startDate>='.$startDate.' and t.startDate<='.$endDate.' and o.ballsRem>'.($ballsRem*0.9).' and o.ballsRem<='.($ballsRem*1.1).' and o.runsReq<'.($runs*1.1).' and o.runsReq>='.($runs*0.9).' and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1).' group by o.odiId';
    }
  }
} else {
  if ($inn == 1) {
    if ($runs == 0) {
      $sql = 'select avg(runRate), avg(result) from overComparison where innings=1 and overs>='.($overs-1).' and overs<'.($overs+1).' and runs<=1 and wkts>='.($wkts-1).' and wkts<='.($wkts+1).' group by ocId';
    } else {
      $sql = 'select avg(runRate), avg(result) from overComparison where innings=1 and overs>='.($overs-1).' and overs<'.($overs+1).' and runs<='.($runs*1.1).' and runs>'.($runs*0.9).' and wkts>='.($wkts-1).' and wkts<='.($wkts+1).' group by ocId';
    }
  } else if ($inn == 2) {
    if ($ballsRem < 60) {
      $sql = 'select avg(reqRate), avg(result) from overComparison where innings=2 and ballsRem>'.($ballsRem*0.75).' and ballsRem<='.($ballsRem*1.25).' and runsReq<'.($runs*1.25).' and runsReq>='.($runs*0.75).' and wkts>='.($wkts-1).' and wkts<='.($wkts+1).' group by ocId';
    } else {
      $sql = 'select avg(reqRate), avg(result) from overComparison where innings=2 and ballsRem>'.($ballsRem*0.9).' and ballsRem<='.($ballsRem*1.1).' and runsReq<'.($runs*1.1).' and runsReq>='.($runs*0.9).' and wkts>='.($wkts-1).' and wkts<='.($wkts+1).' group by ocId';
    }
  }
}
// echo $sql;
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");

$wins = array();
$losses = array();
while($res = $result->fetchArray(SQLITE3_NUM)) {
  $rrRound = "".round($res[0], 1)."";

  if (array_key_exists($rrRound, $wins)) {
    if ($res[1] == 2) {
      $wins[$rrRound] = $wins[$rrRound] + 1;
    }
  } else {
    if ($res[1] == 2) {
      $wins[$rrRound] = 1;
    } else {
      $wins[$rrRound] = 0;
    }
  }


  if (array_key_exists($rrRound, $losses)) {
    if ($res[1] == 0) {
      $losses[$rrRound] = $losses[$rrRound] + 1;
    }
  } else {
    if ($res[1] == 0) {
      $losses[$rrRound] = 1;
    } else {
      $losses[$rrRound] = 0;
    }
  }
}

$rr = array();
$winCounts = array();
$lossCounts = array();
foreach($wins as $rrRound => $count) {
    array_push($rr, $rrRound);
    array_push($winCounts, $count);
    array_push($lossCounts, $losses[$rrRound]);
}

$table = array();
$table['cols'] = array(
                        array('id' => "", 'label' => "Run Rate", 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'label' => "Win Count", 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'label' => "Loss Count", 'pattern' => "", 'type' => 'number'),
                    );

$rows = array();

for ($i = 0; $i < count($rr); $i++) {
    $temp = array();
    $temp[] = array('v' => $rr[$i]);
    $temp[] = array('v' => $winCounts[$i]);
    $temp[] = array('v' => $lossCounts[$i]);
    $rows[] = array('c' => $temp);
}

$table['rows'] = $rows;
$jsonTable = json_encode($table);
echo $jsonTable;
?>
