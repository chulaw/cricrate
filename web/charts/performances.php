<?php    

$xVal = $_GET["xVal"];
$yVal = $_GET["yVal"];
$batBowl = $_GET["batBowl"];
$matchFormat = $_GET["matchFormat"];
$matchFormatLower = strtolower($matchFormat);
$span = $_GET["span"];
$team = $_GET["team"];

if ($matchFormat == "Test") {
    $db = new SQLite3("../ccr.db");   
} else {
    $db = new SQLite3("../ccr".$matchFormat.".db");   
}

$innMat = "Innings";
if ($batBowl == "allRound" || $batBowl == "fielding" || $batBowl == "winShares") {
    $innMat = "Match";
}

$countryTeams = "p.country";
if ($matchFormat == "FT20") {
   $countryTeams = "p.teams";
}

$spanDates = split("-", $span);
$startSpan = $spanDates[0]."0000";
$endSpan = $spanDates[1]."9999";
if ($team == "All teams") {
    $sql = "select c.".$xVal.",c.".$yVal.",c.player, ".$countryTeams.", t.ground, t.startDate from ".$batBowl.$matchFormat.$innMat." c, ".$matchFormatLower."Info t, playerInfo p where c.".$matchFormatLower."Id=t.".$matchFormatLower."Id and c.playerId=p.playerId and t.startDate>$startSpan and t.startDate<$endSpan order by c.rating desc limit 1000";
} else {
    $sql = "select c.".$xVal.",c.".$yVal.",c.player, ".$countryTeams.", t.ground, t.startDate from ".$batBowl.$matchFormat.$innMat." c, ".$matchFormatLower."Info t, playerInfo p where c.".$matchFormatLower."Id=t.".$matchFormatLower."Id and c.playerId=p.playerId and t.startDate>$startSpan and t.startDate<$endSpan and ".$countryTeams."='".$team."' order by c.rating desc limit 500";
}   

$result = $db->query($sql);
if (!$result) die("Cannot execute query.");

$k = 0;
$xVals = array();
$yVals = array();
$players = array();
$countries = array();
$grounds = array();
$dates = array();
while($res = $result->fetchArray(SQLITE3_NUM)) {
    array_push($xVals, $res[0]);
    array_push($yVals, $res[1]);
    array_push($players, str_replace(" ","&nbsp;",$res[2]));    
    array_push($countries, $res[3]);
    array_push($grounds, $res[4]);
    $dateMod = substr($res[5], 0, 4)."-".substr($res[5], 4, 2)."-".substr($res[5], 6, 2);
    array_push($dates, $dateMod);
}

$table = array();
$table['cols'] = array(
                        array('id' => "", 'label' => $xVal, 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'label' => $yVal, 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'type' => 'string', 'p' => array('role' => 'tooltip', 'html' => true)),                        
                    );

$rows = array();

for ($i = 0; $i < count($xVals); $i++) {    
    $temp = array();
    $temp[] = array('v' => $xVals[$i]);
    $temp[] = array('v' => $yVals[$i]);
    $tooltip = "<div style=\"padding:5px 5px 5px 5px; font-size:11px;\">Player: <b>".$players[$i]."</b><br/>";
    if ($matchFormat == "FT20") {
        $tooltip .= "Team: <b>".$countries[$i]."</b><br/>";
    } else {
        $tooltip .= "Team: <img src=\"images/".$countries[$i].".png\" border=1px/><br/>";
    }
    $tooltip .= "Ground: <b>$grounds[$i]</b><br/>";
    $tooltip .= "Date: <b>$dates[$i]</b><br/></div>";
    $temp[] = array('v' => $tooltip);    
    $rows[] = array('c' => $temp);  
} 

$table['rows'] = $rows;
$jsonTable = json_encode($table);
echo $jsonTable;
?>