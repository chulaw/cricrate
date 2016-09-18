<?php    

$playerId1 = $_GET["playerId1"];
$playerId2 = $_GET["playerId2"];
$playerId3 = $_GET["playerId3"];
$playerId4 = $_GET["playerId4"];
$playerId5 = $_GET["playerId5"];
$batBowl = $_GET["batBowl"];
$matchFormat = $_GET["matchFormat"];
$matchFormatLower = strtolower($matchFormat);

if ($matchFormat == "Test") {
    $db = new SQLite3("../ccr.db");   
} else {
    $db = new SQLite3("../ccr".$matchFormat.".db");   
}

date_default_timezone_set('America/New_York');
$time = strtotime("-2 year", time());
$startDate = date("Ymd", $time);

if ($batBowl == "batting") {
    if ($matchFormat == "FT20") {
        $sql1 = "select l.rating, t.startDate, b.notOut, b.runs, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId1." and l.startDate>".$startDate;
        $sql2 = "select l.rating, t.startDate, b.notOut, b.runs, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId2." and l.startDate>".$startDate;
        $sql3 = "select l.rating, t.startDate, b.notOut, b.runs, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId3." and l.startDate>".$startDate;
        $sql4 = "select l.rating, t.startDate, b.notOut, b.runs, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId4." and l.startDate>".$startDate;
        $sql5 = "select l.rating, t.startDate, b.notOut, b.runs, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId5." and l.startDate>".$startDate;
    } else {
        $sql1 = "select l.rating, t.startDate, b.notOut, b.runs, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId1." and l.startDate>".$startDate;
        $sql2 = "select l.rating, t.startDate, b.notOut, b.runs, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId2." and l.startDate>".$startDate;
        $sql3 = "select l.rating, t.startDate, b.notOut, b.runs, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId3." and l.startDate>".$startDate;
        $sql4 = "select l.rating, t.startDate, b.notOut, b.runs, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId4." and l.startDate>".$startDate;
        $sql5 = "select l.rating, t.startDate, b.notOut, b.runs, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId5." and l.startDate>".$startDate;
    }    
} else if ($batBowl == "bowling") {
    if ($matchFormat == "FT20") {
        $sql1 = "select l.rating, t.startDate, b.runs, b.wkts, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId1." and l.startDate>".$startDate;
        $sql2 = "select l.rating, t.startDate, b.runs, b.wkts, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId2." and l.startDate>".$startDate;
        $sql3 = "select l.rating, t.startDate, b.runs, b.wkts, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId3." and l.startDate>".$startDate;
        $sql4 = "select l.rating, t.startDate, b.runs, b.wkts, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId4." and l.startDate>".$startDate;
        $sql5 = "select l.rating, t.startDate, b.runs, b.wkts, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId5." and l.startDate>".$startDate;
    } else {
        $sql1 = "select l.rating, t.startDate, b.runs, b.wkts, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId1." and l.startDate>".$startDate;
        $sql2 = "select l.rating, t.startDate, b.runs, b.wkts, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId2." and l.startDate>".$startDate;
        $sql3 = "select l.rating, t.startDate, b.runs, b.wkts, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId3." and l.startDate>".$startDate;
        $sql4 = "select l.rating, t.startDate, b.runs, b.wkts, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId4." and l.startDate>".$startDate;
        $sql5 = "select l.rating, t.startDate, b.runs, b.wkts, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId5." and l.startDate>".$startDate;
    }
} else if ($batBowl == "allRound") {
    if ($matchFormat == "FT20") {
        $sql1 = "select l.rating, t.startDate, b.notOut, b.runs, b.wkts, b.bowlRuns, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Match b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId1." and l.startDate>".$startDate;
        $sql2 = "select l.rating, t.startDate, b.notOut, b.runs, b.wkts, b.bowlRuns, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Match b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId2." and l.startDate>".$startDate;
        $sql3 = "select l.rating, t.startDate, b.notOut, b.runs, b.wkts, b.bowlRuns, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Match b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId3." and l.startDate>".$startDate;
        $sql4 = "select l.rating, t.startDate, b.notOut, b.runs, b.wkts, b.bowlRuns, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Match b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId4." and l.startDate>".$startDate;
        $sql5 = "select l.rating, t.startDate, b.notOut, b.runs, b.wkts, b.bowlRuns, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Match b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId5." and l.startDate>".$startDate;
    } else if ($matchFormat == "Test") {
        $sql1 = "select l.rating, t.startDate, b.runs1, b.runs2, b.wkts1, b.bowlRuns1, b.wkts2, b.bowlRuns2, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Match b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId1." and l.startDate>".$startDate;
        $sql2 = "select l.rating, t.startDate, b.runs1, b.runs2, b.wkts1, b.bowlRuns1, b.wkts2, b.bowlRuns2, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Match b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId2." and l.startDate>".$startDate;
        $sql3 = "select l.rating, t.startDate, b.runs1, b.runs2, b.wkts1, b.bowlRuns1, b.wkts2, b.bowlRuns2, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Match b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId3." and l.startDate>".$startDate;
        $sql4 = "select l.rating, t.startDate, b.runs1, b.runs2, b.wkts1, b.bowlRuns1, b.wkts2, b.bowlRuns2, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Match b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId4." and l.startDate>".$startDate;
        $sql5 = "select l.rating, t.startDate, b.runs1, b.runs2, b.wkts1, b.bowlRuns1, b.wkts2, b.bowlRuns2, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Match b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId5." and l.startDate>".$startDate;
    } else {
        $sql1 = "select l.rating, t.startDate, b.notOut, b.runs, b.wkts, b.bowlRuns, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Match b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId1." and l.startDate>".$startDate;
        $sql2 = "select l.rating, t.startDate, b.notOut, b.runs, b.wkts, b.bowlRuns, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Match b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId2." and l.startDate>".$startDate;
        $sql3 = "select l.rating, t.startDate, b.notOut, b.runs, b.wkts, b.bowlRuns, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Match b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId3." and l.startDate>".$startDate;
        $sql4 = "select l.rating, t.startDate, b.notOut, b.runs, b.wkts, b.bowlRuns, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Match b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId4." and l.startDate>".$startDate;
        $sql5 = "select l.rating, t.startDate, b.notOut, b.runs, b.wkts, b.bowlRuns, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Match b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId5." and l.startDate>".$startDate;
    }
} else {
    $sql1 = "select l.rating, t.startDate, t.ground, t.team1, t.team2 from ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t where l.team=\"".$playerId1."\" and l.startDate=t.startDate and l.startDate>".$startDate;
    $sql2 = "select l.rating, t.startDate, t.ground, t.team1, t.team2 from ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t where l.team=\"".$playerId2."\" and l.startDate=t.startDate and l.startDate>".$startDate;
    $sql3 = "select l.rating, t.startDate, t.ground, t.team1, t.team2 from ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t where l.team=\"".$playerId3."\" and l.startDate=t.startDate and l.startDate>".$startDate;
    $sql4 = "select l.rating, t.startDate, t.ground, t.team1, t.team2 from ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t where l.team=\"".$playerId4."\" and l.startDate=t.startDate and l.startDate>".$startDate;
    $sql5 = "select l.rating, t.startDate, t.ground, t.team1, t.team2 from ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t where l.team=\"".$playerId5."\" and l.startDate=t.startDate and l.startDate>".$startDate;
}

$result1 = $db->query($sql1);
if (!$result1) die("Cannot execute query.");
$result2 = $db->query($sql2);	
if (!$result2) die("Cannot execute query.");
$result3 = $db->query($sql3);	
if (!$result2) die("Cannot execute query.");
$result4 = $db->query($sql4);	
if (!$result2) die("Cannot execute query.");
$result5 = $db->query($sql5);	
if (!$result2) die("Cannot execute query.");

$k = 0;
$live1 = array();
$dates1 = array();
$runs1 = array();
$ground1 = array();
$opposition1 = array();
$live2 = array();
$dates2 = array();
$runs2 = array();
$ground2 = array();
$opposition2 = array();
$live3 = array();
$dates3 = array();
$runs3 = array();
$ground3 = array();
$opposition3 = array();
$live4 = array();
$dates4 = array();
$runs4 = array();
$ground4 = array();
$opposition4 = array();
$live5 = array();
$dates5 = array();
$runs5 = array();
$ground5 = array();
$opposition5 = array();
$dateRating1 = array();
$dateRating2 = array();
$dateRating3 = array();
$dateRating4 = array();
$dateRating5 = array();
$allDates = array();
while($res1 = $result1->fetchArray(SQLITE3_NUM)) {
    if (array_key_exists($res1[1], $dateRating1)) {
        array_push($dates1, $res1[1]+1);
        $dateRating1[($res1[1]+1)] = round($res1[0], 0);
        array_push($allDates, $res1[1]+1);
    } else {
        array_push($dates1, $res1[1]);
        $dateRating1[$res1[1]] = round($res1[0], 0);
        array_push($allDates, $res1[1]);
    }        
    if ($batBowl == "allRound") {
        if ($matchFormat == "Test") {
            $runs = $res1[2] + $res1[3];
            $wkts = $res1[4] + $res1[6];
            $bowlRuns = $res1[5] + $res1[7];
            $runsMod = $runs . ", " . $wkts."/".$bowlRuns;
            $ground = $res1[8];
            $team1 = $res1[9];
            $team2 = $res1[10];
            $country = $res1[11];
        } else {
            $no = $res1[2];
            if ($no == 1) {
                $runsMod = $res1[3]."*";
            } else {
                $runsMod = $res1[3];
            } 
            $wkts = $res1[4];
            $bowlRuns = $res1[5];
            $runsMod = $runsMod . ", " . $wkts."/".$bowlRuns;
            $ground = $res1[6];
            $team1 = $res1[7];
            $team2 = $res1[8];
            $country = $res1[9];
        }
    } else if ($batBowl == "team") {
        $ground = $res1[2];
        $team1 = $res1[3];
        $team2 = $res1[4];
        $runsMod = "";
    } else {
        $no = $res1[2];
        $runs = $res1[3];
        $ground = $res1[4];
        $team1 = $res1[5];
        $team2 = $res1[6];
        $country = $res1[7];   
    }
    
    if ($batBowl == "batting") {
        if ($no == 1) {
            $runsMod = $res1[3]."*";
        } else {
            $runsMod = $res1[3];
        }    
    } else if ($batBowl == "bowling") {
        $runsMod = $runs."/".$no; # use batting vars
    }
    
    array_push($runs1, $runsMod);
    array_push($ground1, $ground);
    
    if ($batBowl == "team") {
        if ($team1 == $playerId1) {
            $opposition = $team2;
        } else {
            $opposition = $team1;
        }  
    } else {
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
    }
    
    array_push($opposition1, $opposition);
}

while($res2 = $result2->fetchArray(SQLITE3_NUM)) {
    if (array_key_exists($res2[1], $dateRating2)) {
        array_push($dates2, $res2[1]+1);
        $dateRating2[($res2[1]+1)] = round($res2[0], 0);
        array_push($allDates, $res2[1]+1);
    } else {
        array_push($dates2, $res2[1]);
        $dateRating2[$res2[1]] = round($res2[0], 0);
        array_push($allDates, $res2[1]);
    }    
    if ($batBowl == "allRound") {
        if ($matchFormat == "Test") {
            $runs = $res2[2] + $res2[3];
            $wkts = $res2[4] + $res2[6];
            $bowlRuns = $res2[5] + $res2[7];
            $runsMod = $runs . ", " . $wkts."/".$bowlRuns;
            $ground = $res2[8];
            $team1 = $res2[9];
            $team2 = $res2[10];
            $country = $res2[11];
        } else {
            $no = $res2[2];
            if ($no == 1) {
                $runsMod = $res2[3]."*";
            } else {
                $runsMod = $res2[3];
            } 
            $wkts = $res2[4];
            $bowlRuns = $res2[5];
            $runsMod = $runsMod . ", " . $wkts."/".$bowlRuns;
            $ground = $res2[6];
            $team1 = $res2[7];
            $team2 = $res2[8];
            $country = $res2[9];
        }
    } else if ($batBowl == "team") {
        $ground = $res2[2];
        $team1 = $res2[3];
        $team2 = $res2[4];
        $runsMod = "";
    } else {
        $no = $res2[2];
        $runs = $res2[3];
        $ground = $res2[4];
        $team1 = $res2[5];
        $team2 = $res2[6];
        $country = $res2[7];   
    } 
    
    if ($batBowl == "batting") {
        if ($no == 1) {
            $runsMod = $res2[3]."*";
        } else {
            $runsMod = $res2[3];
        }    
    } else if ($batBowl == "bowling") {
        $runsMod = $runs."/".$no; # use batting vars
    }
    array_push($runs2, $runsMod);
    array_push($ground2, $ground);
    
    if ($batBowl == "team") {
        if ($team1 == $playerId1) {
            $opposition = $team2;
        } else {
            $opposition = $team1;
        }  
    } else {
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
    }
    array_push($opposition2, $opposition);
}

while($res3 = $result3->fetchArray(SQLITE3_NUM)) {
    if (array_key_exists($res3[1], $dateRating3)) {
        array_push($dates3, $res3[1]+1);
        $dateRating3[($res3[1]+1)] = round($res3[0], 0);
        array_push($allDates, $res3[1]+1);
    } else {
        array_push($dates3, $res3[1]);
        $dateRating3[$res3[1]] = round($res3[0], 0);
        array_push($allDates, $res3[1]);
    } 
    if ($batBowl == "allRound") {
        if ($matchFormat == "Test") {
            $runs = $res3[2] + $res3[3];
            $wkts = $res3[4] + $res3[6];
            $bowlRuns = $res3[5] + $res3[7];
            $runsMod = $runs . ", " . $wkts."/".$bowlRuns;
            $ground = $res3[8];
            $team1 = $res3[9];
            $team2 = $res3[10];
            $country = $res3[11];
        } else {
            $no = $res3[2];
            if ($no == 1) {
                $runsMod = $res3[3]."*";
            } else {
                $runsMod = $res3[3];
            } 
            $wkts = $res3[4];
            $bowlRuns = $res3[5];
            $runsMod = $runsMod . ", " . $wkts."/".$bowlRuns;
            $ground = $res3[6];
            $team1 = $res3[7];
            $team2 = $res3[8];
            $country = $res3[9];
        }
    } else if ($batBowl == "team") {
        $ground = $res3[2];
        $team1 = $res3[3];
        $team2 = $res3[4];
        $runsMod = "";
    } else {
        $no = $res3[2];
        $runs = $res3[3];
        $ground = $res3[4];
        $team1 = $res3[5];
        $team2 = $res3[6];
        $country = $res3[7];   
    } 
    
    if ($batBowl == "batting") {
        if ($no == 1) {
            $runsMod = $res3[3]."*";
        } else {
            $runsMod = $res3[3];
        }    
    } else if ($batBowl == "bowling") {
        $runsMod = $runs."/".$no; # use batting vars
    }
    array_push($runs3, $runsMod);
    array_push($ground3, $ground);
    
    if ($batBowl == "team") {
        if ($team1 == $playerId1) {
            $opposition = $team2;
        } else {
            $opposition = $team1;
        }  
    } else {
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
    }
    array_push($opposition3, $opposition);
}

while($res4 = $result4->fetchArray(SQLITE3_NUM)) {
    if (array_key_exists($res4[1], $dateRating4)) {
        array_push($dates4, $res4[1]+1);
        $dateRating4[($res4[1]+1)] = round($res4[0], 0);
        array_push($allDates, $res4[1]+1);
    } else {
        array_push($dates4, $res4[1]);
        $dateRating4[$res4[1]] = round($res4[0], 0);
        array_push($allDates, $res4[1]);
    } 
    if ($batBowl == "allRound") {
        if ($matchFormat == "Test") {
            $runs = $res4[2] + $res4[3];
            $wkts = $res4[4] + $res4[6];
            $bowlRuns = $res4[5] + $res4[7];
            $runsMod = $runs . ", " . $wkts."/".$bowlRuns;
            $ground = $res4[8];
            $team1 = $res4[9];
            $team2 = $res4[10];
            $country = $res4[11];
        } else {
            $no = $res4[2];
            if ($no == 1) {
                $runsMod = $res4[3]."*";
            } else {
                $runsMod = $res4[3];
            } 
            $wkts = $res4[4];
            $bowlRuns = $res4[5];
            $runsMod = $runsMod . ", " . $wkts."/".$bowlRuns;
            $ground = $res4[6];
            $team1 = $res4[7];
            $team2 = $res4[8];
            $country = $res4[9];
        }  
    } else if ($batBowl == "team") {
        $ground = $res4[2];
        $team1 = $res4[3];
        $team2 = $res4[4];
        $runsMod = "";
    } else {
        $no = $res4[2];
        $runs = $res4[3];
        $ground = $res4[4];
        $team1 = $res4[5];
        $team2 = $res4[6];
        $country = $res4[7];   
    } 
    
    if ($batBowl == "batting") {
        if ($no == 1) {
            $runsMod = $res4[3]."*";
        } else {
            $runsMod = $res4[3];
        }    
    } else if ($batBowl == "bowling") {
        $runsMod = $runs."/".$no; # use batting vars
    }
    array_push($runs4, $runsMod);
    array_push($ground4, $ground);
    
    if ($batBowl == "team") {
        if ($team1 == $playerId1) {
            $opposition = $team2;
        } else {
            $opposition = $team1;
        }  
    } else {
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
    }
    array_push($opposition4, $opposition);
}

while($res5 = $result5->fetchArray(SQLITE3_NUM)) {
    if (array_key_exists($res5[1], $dateRating5)) {
        array_push($dates5, $res5[1]+1);
        $dateRating5[($res5[1]+1)] = round($res5[0], 0);
        array_push($allDates, $res5[1]+1);
    } else {
        array_push($dates5, $res5[1]);
        $dateRating5[$res5[1]] = round($res5[0], 0);
        array_push($allDates, $res5[1]);
    }    
    if ($batBowl == "allRound") {
        if ($matchFormat == "Test") {
            $runs = $res5[2] + $res5[3];
            $wkts = $res5[4] + $res5[6];
            $bowlRuns = $res5[5] + $res5[7];
            $runsMod = $runs . ", " . $wkts."/".$bowlRuns;
            $ground = $res5[8];
            $team1 = $res5[9];
            $team2 = $res5[10];
            $country = $res5[11];
        } else {
            $no = $res5[2];
            if ($no == 1) {
                $runsMod = $res5[3]."*";
            } else {
                $runsMod = $res5[3];
            } 
            $wkts = $res5[4];
            $bowlRuns = $res5[5];
            $runsMod = $runsMod . ", " . $wkts."/".$bowlRuns;
            $ground = $res5[6];
            $team1 = $res5[7];
            $team2 = $res5[8];
            $country = $res5[9];
        } 
    } else if ($batBowl == "team") {
        $ground = $res5[2];
        $team1 = $res5[3];
        $team2 = $res5[4];
        $runsMod = "";
    } else {
        $no = $res5[2];
        $runs = $res5[3];
        $ground = $res5[4];
        $team1 = $res5[5];
        $team2 = $res5[6];
        $country = $res5[7];   
    } 
    
    if ($batBowl == "batting") {
        if ($no == 1) {
            $runsMod = $res5[3]."*";
        } else {
            $runsMod = $res5[3];
        }    
    } else if ($batBowl == "bowling") {
        $runsMod = $runs."/".$no; # use batting vars
    }
    array_push($runs5, $runsMod);
    array_push($ground5, $ground);
    
    if ($batBowl == "team") {
        if ($team1 == $playerId1) {
            $opposition = $team2;
        } else {
            $opposition = $team1;
        }  
    } else {
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
    }
    array_push($opposition5, $opposition);
}

$allDates = array_unique($allDates);
sort($allDates);

$lastLive1 = null;
$lastLive2 = null;
$lastLive3 = null;
$lastLive4 = null;
$lastLive5 = null;
for ($x = 0; $x < count($allDates); $x++) {
    $matchD = $allDates[$x];
    if (array_key_exists($matchD, $dateRating1)) {
        array_push($live1, $dateRating1[$matchD]);
        $lastLive1 = $dateRating1[$matchD];
    } else {
        array_push($live1, $lastLive1);   
    }
    
    if (array_key_exists($matchD, $dateRating2)) {
        array_push($live2, $dateRating2[$matchD]);
        $lastLive2 = $dateRating2[$matchD];
    } else {
        array_push($live2, $lastLive2);   
    }
    
    if (array_key_exists($matchD, $dateRating3)) {
        array_push($live3, $dateRating3[$matchD]);
        $lastLive3 = $dateRating3[$matchD];
    } else {
        array_push($live3, $lastLive3);   
    }
    
    if (array_key_exists($matchD, $dateRating4)) {
        array_push($live4, $dateRating4[$matchD]);
        $lastLive4 = $dateRating4[$matchD];
    } else {
        array_push($live4, $lastLive4);   
    }
    
    if (array_key_exists($matchD, $dateRating5)) {
        array_push($live5, $dateRating5[$matchD]);
        $lastLive5 = $dateRating5[$matchD];
    } else {
        array_push($live5, $lastLive5);   
    }
}

$table = array();
$table['cols'] = array(
                        array('id' => "", 'label' => 'Date', 'pattern' => "", 'type' => 'string'),
                        array('id' => "", 'label' => 'Current Rating 1', 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'type' => 'string', 'p' => array('role' => 'tooltip', 'html' => true)),
                        array('id' => "", 'label' => 'Current Rating 2', 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'type' => 'string', 'p' => array('role' => 'tooltip', 'html' => true)),
                        array('id' => "", 'label' => 'Current Rating 3', 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'type' => 'string', 'p' => array('role' => 'tooltip', 'html' => true)),
                        array('id' => "", 'label' => 'Current Rating 4', 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'type' => 'string', 'p' => array('role' => 'tooltip', 'html' => true)),
                        array('id' => "", 'label' => 'Current Rating 5', 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'type' => 'string', 'p' => array('role' => 'tooltip', 'html' => true))    
                    );

$rows = array();
$y1 = 0;
$y2 = 0;
$y3 = 0;
$y4 = 0;
$y5 = 0;
$time1y = strtotime("-1 year", time());
$date1y = date("Ymd", $time1y);

for ($x = 0; $x < count($allDates); $x++) {
    if ($allDates[$x] < $date1y) {
        continue;
    }
    $temp = array();
    $dateMod = substr($allDates[$x], 0, 4)."-".substr($allDates[$x], 4, 2)."-".substr($allDates[$x], 6, 2);
    $temp[] = array('v' => $dateMod);
    
    $temp[] = array('v' => $live1[$x]);
    if (array_key_exists($allDates[$x], $dateRating1) and $x < count($live1)) {
        $details1 = "<div style=\"padding:5px 5px 5px 5px; font-size:11px;\">";
        if ($batBowl == "batting") {
            $details1 .= "Runs: <b>".$runs1[$y1]."</b><br/>";   
        } else if ($batBowl == "bowling") {
            $details1 .= "Wkts: <b>".$runs1[$y1]."</b><br/>";   
        } else if ($batBowl == "allRound") {
            $details1 .= "Match: <b>".$runs1[$y1]."</b><br/>";   
        } else {
            $details1 .= "";
        }
        if ($matchFormat == "FT20") {
            $details1 .= "Opposition: <b>".$opposition1[$y1]."</b><br/>";
        } else {
            $details1 .= "Opposition: <img src=\"../../images/".$opposition1[$y1].".png\" border=1px/><br/>";
        }
        $details1 .= "Ground: <b>".$ground1[$y1]."</b><br/>";
        $details1 .= "Date: <b>".$dateMod."</b><br/>";
        $details1 .= "Current Rating: <b>".$live1[$x]."</b></div>";
        $y1 = $y1 + 1;
    } else {        
        $details1 = " ";
    }
    $temp[] = array('v' => $details1);
    
    $temp[] = array('v' => $live2[$x]);
    if (array_key_exists($allDates[$x], $dateRating2) and $x < count($live2)) {        
        $details2 = "<div style=\"padding:5px 5px 5px 5px; font-size:11px;\">";
        if ($batBowl == "batting") {
            $details2 .= "Runs: <b>".$runs2[$y2]."</b><br/>";   
        } else if ($batBowl == "bowling") {
            $details2 .= "Wkts: <b>".$runs2[$y2]."</b><br/>";   
        }  else if ($batBowl == "allRound") {
            $details1 .= "Match: <b>".$runs2[$y2]."</b><br/>";   
        } else {
            $details1 .= "";
        }
        if ($matchFormat == "FT20") {
            $details2 .= "Opposition: <b>".$opposition2[$y2]."</b><br/>";
        } else {
            $details2 .= "Opposition: <img src=\"../../images/".$opposition2[$y2].".png\" border=1px/><br/>";
        }
        $details2 .= "Ground: <b>".$ground2[$y2]."</b><br/>";
        $details2 .= "Date: <b>".$dateMod."</b><br/>";
        $details2 .= "Current Rating: <b>".$live2[$x]."</b></div>";
        $y2 = $y2 + 1;
    } else {
        $details2 = " ";
    }
    $temp[] = array('v' => $details2);
    
    $temp[] = array('v' => $live3[$x]);
    if (array_key_exists($allDates[$x], $dateRating3) and $x < count($live3)) {
        $details3 = "<div style=\"padding:5px 5px 5px 5px; font-size:11px;\">";
        if ($batBowl == "batting") {
            $details3 .= "Runs: <b>".$runs3[$y3]."</b><br/>";   
        } else if ($batBowl == "bowling") {
            $details3 .= "Wkts: <b>".$runs3[$y3]."</b><br/>";   
        } else if ($batBowl == "allRound") {
            $details1 .= "Match: <b>".$runs3[$y3]."</b><br/>";   
        } else {
            $details1 .= "";
        }
        if ($matchFormat == "FT20") {
            $details3 .= "Opposition: <b>".$opposition3[$y3]."</b><br/>";
        } else {
            $details3 .= "Opposition: <img src=\"../../images/".$opposition3[$y3].".png\" border=1px/><br/>";
        }
        $details3 .= "Ground: <b>".$ground3[$y3]."</b><br/>";
        $details3 .= "Date: <b>".$dateMod."</b><br/>";
        $details3 .= "Current Rating: <b>".$live3[$x]."</b></div>";
        $y3 = $y3 + 1;
    } else {
        $details3 = " ";
    }
    $temp[] = array('v' => $details3);
    
    $temp[] = array('v' => $live4[$x]);
    if (array_key_exists($allDates[$x], $dateRating4) and $x < count($live4)) {        
        $details4 = "<div style=\"padding:5px 5px 5px 5px; font-size:11px;\">";
        if ($batBowl == "batting") {
            $details4 .= "Runs: <b>".$runs4[$y4]."</b><br/>";   
        } else if ($batBowl == "bowling") {
            $details4 .= "Wkts: <b>".$runs4[$y4]."</b><br/>";   
        } else if ($batBowl == "allRound") {
            $details1 .= "Match: <b>".$runs4[$y4]."</b><br/>";   
        } else {
            $details1 .= "";
        }
        if ($matchFormat == "FT20") {
            $details4 .= "Opposition: <b>".$opposition4[$y4]."</b><br/>";
        } else {
            $details4 .= "Opposition: <img src=\"../../images/".$opposition4[$y4].".png\" border=1px/><br/>";
        }
        $details4 .= "Ground: <b>".$ground4[$y4]."</b><br/>";
        $details4 .= "Date: <b>".$dateMod."</b><br/>";
        $details4 .= "Current Rating: <b>".$live4[$x]."</b></div>";
        $y4 = $y4 + 1;
    } else {
        $details4 = " ";
    }
    $temp[] = array('v' => $details4);
    
    $temp[] = array('v' => $live5[$x]);
    if (array_key_exists($allDates[$x], $dateRating5) and $x < count($live5)) {            
        $details5 = "<div style=\"padding:5px 5px 5px 5px; font-size:11px;\">";
        if ($batBowl == "batting") {
            $details5 .= "Runs: <b>".$runs5[$y5]."</b><br/>";   
        } else if ($batBowl == "bowling") {
            $details5 .= "Wkts: <b>".$runs5[$y5]."</b><br/>";   
        } else if ($batBowl == "allRound") {
            $details1 .= "Match: <b>".$runs5[$y5]."</b><br/>";   
        } else {
            $details1 .= "";
        }
        if ($matchFormat == "FT20") {
            $details5 .= "Opposition: <b>".$opposition5[$y5]."</b><br/>";
        } else {
            $details5 .= "Opposition: <img src=\"../../images/".$opposition5[$y5].".png\" border=1px/><br/>";
        }
        $details5 .= "Ground: <b>".$ground5[$y5]."</b><br/>";
        $details5 .= "Date: <b>".$dateMod."</b><br/>";
        $details5 .= "Current Rating: <b>".$live5[$x]."</b></div>";
        $y5 = $y5 + 1;        
    } else {
        $details5 = " ";
    }
    $temp[] = array('v' => $details5);
    
    $rows[] = array('c' => $temp);  
} 

$table['rows'] = $rows;
$jsonTable = json_encode($table);
echo $jsonTable;
?>