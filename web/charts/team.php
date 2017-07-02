<?php

$team = $_GET["team"];
$matchFormat = $_GET["matchFormat"];
$disc = $_GET["disc"];
$matchFormatLower = strtolower($matchFormat);

if ($matchFormat == "Test") {
    $db = new SQLite3("../ccr.db");
} else {
    $db = new SQLite3("../ccr".$matchFormat.".db");
}
if ($disc == "Team") {
  if ($matchFormat == "FT20") {
      $sql = "select startDate, rating, opposition, ground, result from team".$matchFormat."Live where team='".$team."'";
  } else {
      $sql = "select startDate, rating, opposition, location, result from team".$matchFormat."Live where team='".$team."'";
  }
} else {
  $sql = "select startDate, rating, playerList from team".$disc.$matchFormat."Live where team='".$team."'";
}

$result = $db->query($sql);
if (!$result) die("Cannot execute query.");

$table = array();
$table['cols'] = array(
                        array('id' => "", 'label' => 'Match Date', 'pattern' => "", 'type' => 'string'),
                        array('id' => "", 'label' => 'Current Rating', 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'type' => 'string', 'p' => array('role' => 'tooltip', 'html' => true))
                    );

$rows = array();
while($res = $result->fetchArray(SQLITE3_NUM)) {
    $dateMod = substr($res[0], 0, 4)."-".substr($res[0], 4, 2)."-".substr($res[0], 6, 2);
    $currRating = round($res[1], 0);
    $temp = array();
    $temp[] = array('v' => $dateMod);
    $temp[] = array('v' => $currRating);

    if ($disc == "Team") {
      $opposition = $res[2];
      $location = $res[3];
      $winLoss = $res[4];
      if ($winLoss == $team) {
          $winLoss = "Win";
      } elseif ($winLoss == $opposition) {
          $winLoss = "Loss";
      } else {
          if ($matchFormat == "Test") {
              $winLoss = "Draw/Tie/NR";
          } else {
              $winLoss = "Tie/NR";
          }
      }

      if ($location == $team) {
          $location = "Home";
      } else {
          $location = "Away";
      }
      $details = "<div style=\"padding:5px 5px 5px 5px; font-size:11px;\">";
      if ($matchFormat == "FT20") {
          $details .= "Opposition: <b>$opposition</b><br/>";
      } else {
          $details .= "Opposition: <img src=\"images/".$opposition.".png\" border=1px/><br/>";
      }
      $details .= "Result: <b>$winLoss</b><br/>";
      if ($matchFormat == "FT20") {
          $details .= "Ground: <b>$location</b><br/>";
      } else {
          $details .= "Location: <b>$location</b><br/>";
      }
    } else {
      $playerList = $res[2];
      $details = "<div style=\"padding:5px 5px 5px 5px; font-size:11px;\">";
      $details .= "$disc List: <b>$playerList</b><br/>";
    }

    $details .= "Date: <b>$dateMod</b><br/>";
    $details .= "Current Rating: <b>$currRating</b></div>";
    $temp[] = array('v' => $details);
    $rows[] = array('c' => $temp);
}

$table['rows'] = $rows;
$jsonTable = json_encode($table);
echo $jsonTable;
?>
