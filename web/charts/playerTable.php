<?php    

$playerId = $_GET["playerId"];
$batBowl = $_GET["batBowl"];
$matchFormat = $_GET["matchFormat"];
$matchFormatLower = strtolower($matchFormat);

if ($matchFormat == "Test") {
    $db = new SQLite3("../ccr.db");   
} else {
    $db = new SQLite3("../ccr".$matchFormat.".db");   
}
if ($batBowl == "batting") {
    if ($matchFormat == "FT20") {
        $sql = "select t.startDate, b.rating, l.rating, b.notOut, b.runs, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId;   
    } else {
        $sql = "select t.startDate, b.rating, l.rating, b.notOut, b.runs, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId;
    }
} else {    
    if ($matchFormat == "FT20") {
        $sql = "select t.startDate, b.rating, l.rating, b.runs, b.wkts, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId;   
    } else {
        $sql = "select t.startDate, b.rating, l.rating, b.runs, b.wkts, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId;
    }
}
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");

$table = array();
$table['cols'] = array(
                        array('id' => "", 'label' => 'Match Date', 'pattern' => "", 'type' => 'string'),
                        array('id' => "", 'label' => 'Innings Rating', 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'label' => 'Current Rating', 'pattern' => "", 'type' => 'number'),
                    );

$rows = array();  
while($res = $result->fetchArray(SQLITE3_NUM)) {    
    $dateMod = substr($res[0], 0, 4)."-".substr($res[0], 4, 2)."-".substr($res[0], 6, 2);
    $innRating = round($res[1], 0);
    $currRating = round($res[2], 0);
    $no = $res[3];
    $runs = $res[4];
    $ground = $res[5];
    $team1 = $res[6];
    $team2 = $res[7];
    $country = $res[8];
    $temp = array();
    $temp[] = array('v' => $dateMod);
    $temp[] = array('v' => $innRating);
    
    if ($matchFormat == "FT20") {
        if (strrpos($country, $team1) === false) {
            $opposition = $team1;
        } else {
            $opposition = $team2;
        }
    } else {
        if ($team1 == $country) {
            $opposition = $team2;
        } else {
            $opposition = $team1;
        }        
    }        
    
    if ($batBowl == "batting") {
        if ($no == 1) {
            $runsMod = $runs."*";
        } else {
            $runsMod = $runs;
        }    
    } else {
        $runsMod = $runs."/".$no; # use batting vars
    }

    $details = "<div style=\"padding:5px 5px 5px 5px; font-size:11px;\">";   
    if ($batBowl == "batting") {
        $details .= "Runs: <b>".$runsMod."</b><br/>";   
    } else {
        $details .= "Wkts: <b>".$runsMod."</b><br/>";   
    }    
    if ($matchFormat == "FT20") {
        $details .= "Opposition: <b>$opposition</b><br/>";
    } else {
        $details .= "Opposition: <img src=\"images/".$opposition.".png\" border=1px/><br/>";
    }
    $details .= "Ground: <b>$ground</b><br/>";
    $details .= "Date: <b>$dateMod</b><br/>";
    $details .= "Innings Rating: <b>$innRating</b><br/>";
    $details .= "Current Rating: <b>$currRating</b></div>";
    //$temp[] = array('v' => $details);
    $temp[] = array('v' => $currRating);
    //$temp[] = array('v' => $details);
    $rows[] = array('c' => $temp);
}

$table['rows'] = $rows;
$jsonTable = json_encode($table);
echo $jsonTable;
?>