<?php    

$playerId1 = $_GET["playerId1"];
$playerId2 = $_GET["playerId2"];
$batBowl = $_GET["batBowl"];
$matchFormat = $_GET["matchFormat"];
$inningsDate = $_GET["inningsDate"];
$matchFormatLower = strtolower($matchFormat);

if ($matchFormat == "Test") {
    $db = new SQLite3("../ccr.db");   
} else {
    $db = new SQLite3("../ccr".$matchFormat.".db");   
}
if ($batBowl == "batting") {
    if ($matchFormat == "FT20") {
        $sql1 = "select l.rating, t.startDate, b.notOut, b.runs, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId1." order by t.startDate asc";
        $sql2 = "select l.rating, t.startDate, b.notOut, b.runs, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId2." order by t.startDate asc";
    } else {
        $sql1 = "select l.rating, t.startDate, b.notOut, b.runs, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId1." order by t.startDate asc";
        $sql2 = "select l.rating, t.startDate, b.notOut, b.runs, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId2." order by t.startDate asc";
    }    
} else if ($batBowl == "bowling") {
    if ($matchFormat == "FT20") {
        $sql1 = "select l.rating, t.startDate, b.runs, b.wkts, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId1." order by t.startDate asc";
        $sql2 = "select l.rating, t.startDate, b.runs, b.wkts, t.ground, t.team1, t.team2, p.teams from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId2." order by t.startDate asc";
    } else {
        $sql1 = "select l.rating, t.startDate, b.runs, b.wkts, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId1." order by t.startDate asc";
        $sql2 = "select l.rating, t.startDate, b.runs, b.wkts, t.ground, t.team1, t.team2, p.country from ".$batBowl."".$matchFormat."Innings b, ".$batBowl."".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId2." order by t.startDate asc";
    }
} else if ($batBowl == "allRound") {
    if ($matchFormat == "Test") {
        $sql1 = "select l.rating, t.startDate, b.notOut1, b.runs1, b.notOut2, b.runs2, b.wkts1, b.bowlRuns1, b.wkts2, b.bowlRuns2, t.ground, t.team1, t.team2, p.country from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId1." order by t.startDate asc";
        $sql2 = "select l.rating, t.startDate, b.notOut1, b.runs1, b.notOut2, b.runs2, b.wkts1, b.bowlRuns1, b.wkts2, b.bowlRuns2, t.ground, t.team1, t.team2, p.country from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId2." order by t.startDate asc";         
    } else {
        if ($matchFormat == "FT20") {
            $sql1 = "select l.rating, t.startDate, b.notOut, b.runs, b.wkts, b.bowlRuns, t.ground, t.team1, t.team2, p.teams from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId1." order by t.startDate asc";
            $sql2 = "select l.rating, t.startDate, b.notOut, b.runs, b.wkts, b.bowlRuns, t.ground, t.team1, t.team2, p.teams from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId2." order by t.startDate asc";
        } else {
            $sql1 = "select l.rating, t.startDate, b.notOut, b.runs, b.wkts, b.bowlRuns, t.ground, t.team1, t.team2, p.country from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId1." order by t.startDate asc";
            $sql2 = "select l.rating, t.startDate, b.notOut, b.runs, b.wkts, b.bowlRuns, t.ground, t.team1, t.team2, p.country from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId2." order by t.startDate asc";
        }
    }
} else if ($batBowl == "fielding") {
    if ($matchFormat == "FT20") {
        $sql1 = "select l.rating, t.startDate, b.catches, b.droppedCatches, b.greatCatches, t.ground, t.team1, t.team2, p.teams from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId1." order by t.startDate asc";
        $sql2 = "select l.rating, t.startDate, b.catches, b.droppedCatches, b.greatCatches, t.ground, t.team1, t.team2, p.teams from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId2." order by t.startDate asc";
    } else {
        $sql1 = "select l.rating, t.startDate, b.catches, b.droppedCatches, b.greatCatches, t.ground, t.team1, t.team2, p.country from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId1." order by t.startDate asc";
        $sql2 = "select l.rating, t.startDate, b.catches, b.droppedCatches, b.greatCatches, t.ground, t.team1, t.team2, p.country from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId2." order by t.startDate asc";
    }    
} else if ($batBowl == "winShares") {
    if ($matchFormat == "FT20") {
        $sql1 = "select l.totalRating, t.startDate, b.battingAdjWS, b.bowlingAdjWS, b.fieldingAdjWS, t.ground, t.team1, t.team2, p.teams from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId1." order by t.startDate asc";
        $sql2 = "select l.totalRating, t.startDate, b.battingAdjWS, b.bowlingAdjWS, b.fieldingAdjWS, t.ground, t.team1, t.team2, p.teams from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId2." order by t.startDate asc";
    } else {
        $sql1 = "select l.totalRating, t.startDate, b.battingAdjWS, b.bowlingAdjWS, b.fieldingAdjWS, t.ground, t.team1, t.team2, p.country from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId1." order by t.startDate asc";
        $sql2 = "select l.totalRating, t.startDate, b.battingAdjWS, b.bowlingAdjWS, b.fieldingAdjWS, t.ground, t.team1, t.team2, p.country from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId2." order by t.startDate asc";
    }    
}

$result1 = $db->query($sql1);
if (!$result1) die("Cannot execute query.");
$result2 = $db->query($sql2);	
if (!$result2) die("Cannot execute query.");

$k = 0;
$innings = array();
$live1 = array();
$dates1 = array();
$runs1 = array();
$wkts1 = array();
$ground1 = array();
$opposition1 = array();
$live2 = array();
$dates2 = array();
$runs2 = array();
$wkts2 = array();
$ground2 = array();
$opposition2 = array();
$dateRating1 = array();
$dateRating2 = array();
$allDates = array();
$liveDate1 = array();
$liveDate2 = array();
$lastDate1 = 0;
$lastDate2 = 0;
$grtCat1 = array();
$grtCat2 = array();
if ($batBowl == "allRound") {
    while($res1 = $result1->fetchArray(SQLITE3_NUM)) {
        $k++;
        array_push($innings, $k);    
        array_push($live1, round($res1[0], 0));
        
        if (array_key_exists($res1[1], $dateRating1)) {
            array_push($dates1, $res1[1]+1);
            $dateRating1[($res1[1]+1)] = round($res1[0], 0);
            array_push($allDates, $res1[1]+1);
            $lastDate1 = $res1[1]+1;
        } else {
            array_push($dates1, $res1[1]);
            $dateRating1[$res1[1]] = round($res1[0], 0);
            array_push($allDates, $res1[1]);
            $lastDate1 = $res1[1];
        }
        if ($matchFormat == "Test") {
            $no1 = $res1[2];
            $run1 = $res1[3];
            $no2 = $res1[4];
            $run2 = $res1[5];
            $wkt1 = $res1[6];
            $bowlRuns1 = $res1[7];
            $wkt2 = $res1[8];
            $bowlRuns2 = $res1[9];
            $ground = $res1[10];
            $team1 = $res1[11];
            $team2 = $res1[12];
            $country = $res1[13];
        } else {
            $no = $res1[2];
            $runs = $res1[3];
            $wkts = $res1[4];
            $bowlRuns = $res1[5];
            $ground = $res1[6];
            $team1 = $res1[7];
            $team2 = $res1[8];
            $country = $res1[9];
        }             
        
        $runsMod = "";
        $wktsMod = "";
        if ($matchFormat == "Test") {
            if ($run1 != "") {
                if ($no1 == 1) {
                    $runsMod = $run1."*";
                } else {
                    $runsMod = $run1;
                }   
            } else {
                $runsMod = "-";
            }
            
            if ($run2 != "") {
                if ($no2 == 1) {
                    $runsMod = $runsMod. " & " . $run2."*";
                } else {
                    $runsMod = $runsMod. " & " . $run2;
                }
            } else {
                $runsMod = $runsMod. " & " . "-";
            }
            
            if ($wkt1 != "" and $bowlRuns1 != "") {
                $wktsMod = $wkt1."/".$bowlRuns1;
            } else {
                $wktsMod = "-";
            }
            
            if ($wkt2 != "" and $bowlRuns2 != "") {
                $wktsMod = $wktsMod. " & " . $wkt2."/".$bowlRuns2;
            } else {
                $wktsMod = $wktsMod. " & " . "-";
            }
        } else {
            if ($no == 1) {
                $runsMod = $runs."*";
            } else {
                $runsMod = $runs;
            }
            
            if ($wkts != "" and $bowlRuns != "") {
                $wktsMod = $wkts."/".$bowlRuns;
            } 
        }
        
        array_push($runs1, $runsMod);
        array_push($wkts1, $wktsMod);
        array_push($ground1, $ground);
        
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
        array_push($opposition1, $opposition);
    }
    
    $l = 0;
    while($res2 = $result2->fetchArray(SQLITE3_NUM)) {
        $l++;
        if ($l > $k) {
            array_push($innings, $l);    
        }
        array_push($live2, round($res2[0], 0));
        
        if (array_key_exists($res2[1], $dateRating2)) {
            array_push($dates2, $res2[1]+1);
            $dateRating2[($res2[1]+1)] = round($res2[0], 0);
            array_push($allDates, $res2[1]+1);
            $lastDate2 = $res2[1]+1;
        } else {
            array_push($dates2, $res2[1]);
            $dateRating2[$res2[1]] = round($res2[0], 0);
            array_push($allDates, $res2[1]);
            $lastDate2 = $res2[1];
        }
        if ($matchFormat == "Test") {
            $no1 = $res2[2];
            $run1 = $res2[3];
            $no2 = $res2[4];
            $run2 = $res2[5];
            $wkt1 = $res2[6];
            $bowlRuns1 = $res2[7];
            $wkt2 = $res2[8];
            $bowlRuns2 = $res2[9];
            $ground = $res2[10];
            $team1 = $res2[11];
            $team2 = $res2[12];
            $country = $res2[13];
        } else {
            $no = $res2[2];
            $runs = $res2[3];
            $wkts = $res2[4];
            $bowlRuns = $res2[5];
            $ground = $res2[6];
            $team1 = $res2[7];
            $team2 = $res2[8];
            $country = $res2[9];
        } 
        
        $runsMod = "";
        $wktsMod = "";
        if ($matchFormat == "Test") {
            if ($run1 != "") {
                if ($no1 == 1) {
                    $runsMod = $run1."*";
                } else {
                    $runsMod = $run1;
                }   
            } else {
                $runsMod = "-";
            }
            
            if ($run2 != "") {
                if ($no2 == 1) {
                    $runsMod = $runsMod. " & " . $run2."*";
                } else {
                    $runsMod = $runsMod. " & " . $run2;
                }
            } else {
                $runsMod = $runsMod. " & " . "-";
            }
            
            if ($wkt1 != "" and $bowlRuns1 != "") {
                $wktsMod = $wkt1."/".$bowlRuns1;
            } else {
                $wktsMod = "-";
            }
            
            if ($wkt2 != "" and $bowlRuns2 != "") {
                $wktsMod = $wktsMod. " & " . $wkt2."/".$bowlRuns2;
            } else {
                $wktsMod = $wktsMod. " & " . "-";
            }
        } else {
            if ($no == 1) {
                $runsMod = $runs."*";
            } else {
                $runsMod = $runs;
            }
            
            if ($wkts != "" and $bowlRuns != "") {
                $wktsMod = $wkts."/".$bowlRuns;
            } 
        }
        
        array_push($runs2, $runsMod);
        array_push($wkts2, $wktsMod);
        array_push($ground2, $ground);
        
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
        array_push($opposition2, $opposition);
    }
} else if ($batBowl == "fielding") {
    while($res1 = $result1->fetchArray(SQLITE3_NUM)) {        
        $k++;
        array_push($innings, $k);    
        array_push($live1, round($res1[0], 0));
        
        if (array_key_exists($res1[1], $dateRating1)) {
            array_push($dates1, $res1[1]+1);
            $dateRating1[($res1[1]+1)] = round($res1[0], 0);
            array_push($allDates, $res1[1]+1);
            $lastDate1 = $res1[1]+1;
        } else {
            array_push($dates1, $res1[1]);
            $dateRating1[$res1[1]] = round($res1[0], 0);
            array_push($allDates, $res1[1]);
            $lastDate1 = $res1[1];
        }
        $cat = $res1[2];
        $drop = $res1[3];
        $grtCat = $res1[4];        
        $ground = $res1[5];
        $team1 = $res1[6];
        $team2 = $res1[7];
        $country = $res1[8];
        
        array_push($runs1, $cat);
        array_push($wkts1, $drop);
        array_push($grtCat1, $grtCat);        
        array_push($ground1, $ground);
        
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
        array_push($opposition1, $opposition);                
    }
    
    $l = 0;
    while($res2 = $result2->fetchArray(SQLITE3_NUM)) {
        $l++;
        if ($l > $k) {
            array_push($innings, $l);    
        }
        array_push($live2, round($res2[0], 0));
        
        if (array_key_exists($res2[1], $dateRating2)) {
            array_push($dates2, $res2[1]+1);
            $dateRating2[($res2[1]+1)] = round($res2[0], 0);
            array_push($allDates, $res2[1]+1);
            $lastDate2 = $res2[1]+1;
        } else {
            array_push($dates2, $res2[1]);
            $dateRating2[$res2[1]] = round($res2[0], 0);
            array_push($allDates, $res2[1]);
            $lastDate2 = $res2[1];
        }        
        $cat = $res2[2];
        $drop = $res2[3];
        $grtCat = $res2[4];        
        $ground = $res2[5];
        $team1 = $res2[6];
        $team2 = $res2[7];
        $country = $res2[8];
        
        array_push($runs2, $cat);
        array_push($wkts2, $drop);
        array_push($grtCat2, $grtCat);        
        array_push($ground2, $ground);
        
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
        array_push($opposition2, $opposition);
    }
}  else if ($batBowl == "winShares") {
    while($res1 = $result1->fetchArray(SQLITE3_NUM)) {        
        $k++;
        array_push($innings, $k);    
        array_push($live1, round($res1[0], 3));
        
        if (array_key_exists($res1[1], $dateRating1)) {
            array_push($dates1, $res1[1]+1);
            $dateRating1[($res1[1]+1)] = round($res1[0], 3);
            array_push($allDates, $res1[1]+1);
            $lastDate1 = $res1[1]+1;
        } else {
            array_push($dates1, $res1[1]);
            $dateRating1[$res1[1]] = round($res1[0], 3);
            array_push($allDates, $res1[1]);
            $lastDate1 = $res1[1];
        }
        $bat = round($res1[2], 3);
        $bowl = round($res1[3], 3);
        $field = round($res1[4], 3);   
        $ground = $res1[5];
        $team1 = $res1[6];
        $team2 = $res1[7];
        $country = $res1[8];
        
        array_push($runs1, $bat);
        array_push($wkts1, $bowl);
        array_push($grtCat1, $field);        
        array_push($ground1, $ground);
        
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
        array_push($opposition1, $opposition);                
    }
    
    $l = 0;
    while($res2 = $result2->fetchArray(SQLITE3_NUM)) {
        $l++;
        if ($l > $k) {
            array_push($innings, $l);    
        }
        array_push($live2, round($res2[0], 3));
        
        if (array_key_exists($res2[1], $dateRating2)) {
            array_push($dates2, $res2[1]+1);
            $dateRating2[($res2[1]+1)] = round($res2[0], 3);
            array_push($allDates, $res2[1]+1);
            $lastDate2 = $res2[1]+1;
        } else {
            array_push($dates2, $res2[1]);
            $dateRating2[$res2[1]] = round($res2[0], 3);
            array_push($allDates, $res2[1]);
            $lastDate2 = $res2[1];
        }        
        $bat = round($res2[2], 3);
        $bowl = round($res2[3], 3);
        $field = round($res2[4], 3);    
        $ground = $res2[5];
        $team1 = $res2[6];
        $team2 = $res2[7];
        $country = $res2[8];
        
        array_push($runs2, $bat);
        array_push($wkts2, $bowl);
        array_push($grtCat2, $field);        
        array_push($ground2, $ground);
        
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
        array_push($opposition2, $opposition);
    }
} else {
    while($res1 = $result1->fetchArray(SQLITE3_NUM)) {
        $k++;
        array_push($innings, $k);    
        array_push($live1, round($res1[0], 0));
        
        if (array_key_exists($res1[1], $dateRating1)) {
            array_push($dates1, $res1[1]+1);
            $dateRating1[($res1[1]+1)] = round($res1[0], 0);
            array_push($allDates, $res1[1]+1);
            $lastDate1 = $res1[1]+1;
        } else {
            array_push($dates1, $res1[1]);
            $dateRating1[$res1[1]] = round($res1[0], 0);
            array_push($allDates, $res1[1]);
            $lastDate1 = $res1[1];
        }        
        $no = $res1[2];
        $runs = $res1[3];
        $ground = $res1[4];
        $team1 = $res1[5];
        $team2 = $res1[6];
        $country = $res1[7];
        
        if ($batBowl == "batting") {
            if ($no == 1) {
                $runsMod = $res1[3]."*";
            } else {
                $runsMod = $res1[3];
            }    
        } else {
            $runsMod = $runs."/".$no; # use batting vars
        }
        
        array_push($runs1, $runsMod);
        array_push($ground1, $ground);
        
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
        array_push($opposition1, $opposition);
    }
    
    $l = 0;
    while($res2 = $result2->fetchArray(SQLITE3_NUM)) {
        $l++;
        if ($l > $k) {
            array_push($innings, $l);    
        }
        array_push($live2, round($res2[0], 0));
        
        if (array_key_exists($res2[1], $dateRating2)) {
            array_push($dates2, $res2[1]+1);
            $dateRating2[($res2[1]+1)] = round($res2[0], 0);
            array_push($allDates, $res2[1]+1);
            $lastDate2 = $res2[1]+1;
        } else {
            array_push($dates2, $res2[1]);
            $dateRating2[$res2[1]] = round($res2[0], 0);
            array_push($allDates, $res2[1]);
            $lastDate2 = $res2[1];
        }
        $no = $res2[2];
        $runs = $res2[3];
        $ground = $res2[4];
        $team1 = $res2[5];
        $team2 = $res2[6];
        $country = $res2[7];
        
        if ($batBowl == "batting") {
            if ($no == 1) {
                $runsMod = $res2[3]."*";
            } else {
                $runsMod = $res2[3];
            }    
        } else {
            $runsMod = $runs."/".$no; # use batting vars
        }
        array_push($runs2, $runsMod);
        array_push($ground2, $ground);
        
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
        array_push($opposition2, $opposition);
    }
}

$allDates = array_unique($allDates);
sort($allDates);

$lastLive1 = null;
$lastLive2 = null;
for ($x = 0; $x < count($allDates); $x++) {
    $matchD = $allDates[$x];
    if (array_key_exists($matchD, $dateRating1)) {
        array_push($liveDate1, $dateRating1[$matchD]);
        $lastLive1 = $dateRating1[$matchD];
    } else if ($matchD <= $lastDate1) {
        array_push($liveDate1, $lastLive1);   
    } else {
        array_push($liveDate1, null);   
    }
    
    if (array_key_exists($matchD, $dateRating2)) {
        array_push($liveDate2, $dateRating2[$matchD]);
        $lastLive2 = $dateRating2[$matchD];
    } else if ($matchD <= $lastDate2) {
        array_push($liveDate2, $lastLive2);   
    } else {
        array_push($liveDate2, null);   
    }
}

$table = array();
if ($inningsDate == "Inning") {
    $table['cols'] = array(
                        array('id' => "", 'label' => 'Inning', 'pattern' => "", 'type' => 'string'),
                        array('id' => "", 'label' => 'Current Rating 1', 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'type' => 'string', 'p' => array('role' => 'tooltip', 'html' => true)),
                        array('id' => "", 'label' => 'Current Rating 2', 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'type' => 'string', 'p' => array('role' => 'tooltip', 'html' => true))    
                    );

    $rows = array();
    for ($x = 0; $x < count($innings); $x++) {
        $temp = array();
        $temp[] = array('v' => $innings[$x]);
        if ($x < count($live1)) {
            $temp[] = array('v' => $live1[$x]);        
            $details1 = "<div style=\"padding:5px 5px 5px 5px; font-size:11px;\">";
            if ($batBowl == "batting") {
                $details1 .= "Runs: <b>".$runs1[$x]."</b><br/>";   
            } else if ($batBowl == "bowling") {
                $details1 .= "Wkts: <b>".$runs1[$x]."</b><br/>";   
            } else if ($batBowl == "allRound") {
                $details1 .= "Runs: <b>".$runs1[$x]."</b><br/>";   
                $details1 .= "Wkts: <b>".$wkts1[$x]."</b><br/>";   
            } else if ($batBowl == "fielding") {
                $details1 .= "Catches: <b>".$runs1[$x]."</b><br/>";
                $details1 .= "Drops: <b>".$wkts1[$x]."</b><br/>";
                $details1 .= "GreatCatches: <b>".$grtCat1[$x]."</b><br/>";   
            } else if ($batBowl == "winShares") {
                $details1 .= "Bat: <b>".$runs1[$x]."</b><br/>";
                $details1 .= "Bowl: <b>".$wkts1[$x]."</b><br/>";
                $details1 .= "Field: <b>".$grtCat1[$x]."</b><br/>";   
            }
            if ($matchFormat == "FT20") {
                $details1 .= "Opposition: <b>".$opposition1[$x]."</b><br/>";
            } else {
                $details1 .= "Opposition: <img src=\"images/".$opposition1[$x].".png\" border=1px/><br/>";
            }
            $details1 .= "Ground: <b>".$ground1[$x]."</b><br/>";
            $dateMod = substr($dates1[$x], 0, 4)."-".substr($dates1[$x], 4, 2)."-".substr($dates1[$x], 6, 2);
            $details1 .= "Date: <b>".$dateMod."</b><br/>";
            $details1 .= "Current Rating: <b>".$live1[$x]."</b></div>";
        } else {
            $temp[] = array('v' => null);
            $details1 = "";
        }
        $temp[] = array('v' => $details1);
        
        if ($x < count($live2)) {
            $temp[] = array('v' => $live2[$x]);
            $details2 = "<div style=\"padding:5px 5px 5px 5px; font-size:11px;\">";
            if ($batBowl == "batting") {
                $details2 .= "Runs: <b>".$runs2[$x]."</b><br/>";   
            } else if ($batBowl == "bowling") {
                $details2 .= "Wkts: <b>".$runs2[$x]."</b><br/>";   
            } else if ($batBowl == "allRound") {
                $details2 .= "Runs: <b>".$runs2[$x]."</b><br/>";   
                $details2 .= "Wkts: <b>".$wkts2[$x]."</b><br/>";   
            } else if ($batBowl == "fielding") {
                $details2 .= "Catches: <b>".$runs2[$x]."</b><br/>";
                $details2 .= "Drops: <b>".$wkts2[$x]."</b><br/>";
                $details2 .= "GreatCatches: <b>".$grtCat2[$x]."</b><br/>";   
            } else if ($batBowl == "winShares") {
                $details2 .= "Bat: <b>".$runs2[$x]."</b><br/>";
                $details2 .= "Bowl: <b>".$wkts2[$x]."</b><br/>";
                $details2 .= "Field: <b>".$grtCat2[$x]."</b><br/>";   
            }        
            if ($matchFormat == "FT20") {
                $details2 .= "Opposition: <b>".$opposition2[$x]."</b><br/>";
            } else {
                $details2 .= "Opposition: <img src=\"images/".$opposition2[$x].".png\" border=1px/><br/>";
            }
            $details2 .= "Ground: <b>".$ground2[$x]."</b><br/>";
            $dateMod = substr($dates2[$x], 0, 4)."-".substr($dates2[$x], 4, 2)."-".substr($dates2[$x], 6, 2);
            $details2 .= "Date: <b>".$dateMod."</b><br/>";
            $details2 .= "Current Rating: <b>".$live2[$x]."</b></div>";            
        } else {
            $temp[] = array('v' => null);
            $details2 = "";
        }
        $temp[] = array('v' => $details2);
        $rows[] = array('c' => $temp);  
    } 
} else {
    $table['cols'] = array(
                        array('id' => "", 'label' => 'Date', 'pattern' => "", 'type' => 'string'),
                        array('id' => "", 'label' => 'Current Rating 1', 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'type' => 'string', 'p' => array('role' => 'tooltip', 'html' => true)),
                        array('id' => "", 'label' => 'Current Rating 2', 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'type' => 'string', 'p' => array('role' => 'tooltip', 'html' => true))    
                    );

    $rows = array();
    $y1 = 0;
    $y2 = 0;
    for ($x = 0; $x < count($allDates); $x++) {    
        $temp = array();
        $dateMod = substr($allDates[$x], 0, 4)."-".substr($allDates[$x], 4, 2)."-".substr($allDates[$x], 6, 2);
        $temp[] = array('v' => $dateMod);
        
        $temp[] = array('v' => $liveDate1[$x]);
        if (array_key_exists($allDates[$x], $dateRating1) and $x < count($liveDate1)) {
            $details1 = "<div style=\"padding:5px 5px 5px 5px; font-size:11px;\">";
            if ($batBowl == "batting") {
                $details1 .= "Runs: <b>".$runs1[$y1]."</b><br/>";   
            } else if ($batBowl == "bowling") {
                $details1 .= "Wkts: <b>".$runs1[$y1]."</b><br/>";   
            } else if ($batBowl == "allRound") {
                $details1 .= "Runs: <b>".$runs1[$y1]."</b><br/>";   
                $details1 .= "Wkts: <b>".$wkts1[$y1]."</b><br/>";   
            } else if ($batBowl == "fielding") {
                $details1 .= "Catches: <b>".$runs1[$y1]."</b><br/>";
                $details1 .= "Drops: <b>".$wkts1[$y1]."</b><br/>";
                $details1 .= "GreatCatches: <b>".$grtCat1[$y1]."</b><br/>";   
            } else if ($batBowl == "winShares") {
                $details1 .= "Bat: <b>".$runs1[$y1]."</b><br/>";
                $details1 .= "Bowl: <b>".$wkts1[$y1]."</b><br/>";
                $details1 .= "Field: <b>".$grtCat1[$y1]."</b><br/>";   
            }      
            if ($matchFormat == "FT20") {
                $details1 .= "Opposition: <b>".$opposition1[$y1]."</b><br/>";
            } else {
                $details1 .= "Opposition: <img src=\"../../images/".$opposition1[$y1].".png\" border=1px/><br/>";
            }
            $details1 .= "Ground: <b>".$ground1[$y1]."</b><br/>";
            $details1 .= "Date: <b>".$dateMod."</b><br/>";
            $details1 .= "Current Rating: <b>".$liveDate1[$x]."</b></div>";
            $y1 = $y1 + 1;
        } else {        
            $details1 = " ";
        }
        $temp[] = array('v' => $details1);
    
    
        $temp[] = array('v' => $liveDate2[$x]);
        if (array_key_exists($allDates[$x], $dateRating2) and $x < count($liveDate2)) {        
            $details2 = "<div style=\"padding:5px 5px 5px 5px; font-size:11px;\">";
            if ($batBowl == "batting") {
                $details2 .= "Runs: <b>".$runs2[$y2]."</b><br/>";   
            } else if ($batBowl == "bowling") {
                $details2 .= "Wkts: <b>".$runs2[$y2]."</b><br/>";   
            } else if ($batBowl == "allRound") {
                $details2 .= "Runs: <b>".$runs2[$y2]."</b><br/>";   
                $details2 .= "Wkts: <b>".$wkts2[$y2]."</b><br/>";   
            } else if ($batBowl == "fielding") {
                $details2 .= "Catches: <b>".$runs2[$y2]."</b><br/>";
                $details2 .= "Drops: <b>".$wkts2[$y2]."</b><br/>";
                $details2 .= "GreatCatches: <b>".$grtCat2[$y2]."</b><br/>";   
            } else if ($batBowl == "winShares") {
                $details2 .= "Bat: <b>".$runs2[$y2]."</b><br/>";
                $details2 .= "Bowl: <b>".$wkts2[$y2]."</b><br/>";
                $details2 .= "Field: <b>".$grtCat2[$y2]."</b><br/>";   
            }     
            if ($matchFormat == "FT20") {
                $details2 .= "Opposition: <b>".$opposition2[$y2]."</b><br/>";
            } else {
                $details2 .= "Opposition: <img src=\"../../images/".$opposition2[$y2].".png\" border=1px/><br/>";
            }
            $details2 .= "Ground: <b>".$ground2[$y2]."</b><br/>";
            $details2 .= "Date: <b>".$dateMod."</b><br/>";
            $details2 .= "Current Rating: <b>".$liveDate2[$x]."</b></div>";
            $y2 = $y2 + 1;
        } else {
            $details2 = " ";
        }
        $temp[] = array('v' => $details2);
        $rows[] = array('c' => $temp);
    }
}

$table['rows'] = $rows;
$jsonTable = json_encode($table);
echo $jsonTable;
?>