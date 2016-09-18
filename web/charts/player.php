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
        $sql = "select t.startDate, b.rating, l.rating, b.notOut, b.runs, t.ground, t.team1, t.team2, p.teams from ".$batBowl.$matchFormat."Innings b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId;   
    } else {
        $sql = "select t.startDate, b.rating, l.rating, b.notOut, b.runs, t.ground, t.team1, t.team2, p.country from ".$batBowl.$matchFormat."Innings b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId;
    }
} else if ($batBowl == "bowling") {    
    if ($matchFormat == "FT20") {
        $sql = "select t.startDate, b.rating, l.rating, b.runs, b.wkts, t.ground, t.team1, t.team2, p.teams from ".$batBowl.$matchFormat."Innings b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId;   
    } else {
        $sql = "select t.startDate, b.rating, l.rating, b.runs, b.wkts, t.ground, t.team1, t.team2, p.country from ".$batBowl.$matchFormat."Innings b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId;
    }
} else if ($batBowl == "allRound") {
    if ($matchFormat == "Test") {
        $sql = "select t.startDate, b.rating, l.rating, b.notOut1, b.runs1, b.notOut2, b.runs2, b.wkts1, b.bowlRuns1, b.wkts2, b.bowlRuns2, t.ground, t.team1, t.team2, p.country from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId;         
    } else {
        if ($matchFormat == "FT20") {
            $sql = "select t.startDate, b.rating, l.rating, b.notOut, b.runs, b.wkts, b.bowlRuns, t.ground, t.team1, t.team2, p.teams from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId;
        } else {
            $sql = "select t.startDate, b.rating, l.rating, b.notOut, b.runs, b.wkts, b.bowlRuns, t.ground, t.team1, t.team2, p.country from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId;
        }
    }
} else if ($batBowl == "fielding") {
    if ($matchFormat == "FT20") {
        $sql = "select t.startDate, b.rating, l.rating, b.catches, b.droppedCatches, b.greatCatches, t.ground, t.team1, t.team2, p.teams from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId;
    } else {
        $sql = "select t.startDate, b.rating, l.rating, b.catches, b.droppedCatches, b.greatCatches, t.ground, t.team1, t.team2, p.country from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId;
    }
} else if ($batBowl == "winShares") {   
    if ($matchFormat == "FT20") {
        $sql = "select t.startDate, b.totalAdjWS, l.totalRating, b.battingAdjWS, b.bowlingAdjWS, b.fieldingAdjWS, t.ground, t.team1, t.team2, p.teams from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId;
    } else {
        $sql = "select t.startDate, b.totalAdjWS, l.totalRating, b.battingAdjWS, b.bowlingAdjWS, b.fieldingAdjWS, t.ground, t.team1, t.team2, p.country from ".$batBowl.$matchFormat."Match b, ".$batBowl.$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId;
    }
}
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");

$table = array();
$table['cols'] = array(
                        array('id' => "", 'label' => 'Match Date', 'pattern' => "", 'type' => 'string'),
                        array('id' => "", 'label' => 'Innings Rating', 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'type' => 'string', 'p' => array('role' => 'tooltip', 'html' => true)),
                        array('id' => "", 'label' => 'Current Rating', 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'type' => 'string', 'p' => array('role' => 'tooltip', 'html' => true))    
                    );

$rows = array();
if ($batBowl == "allRound") {
    while($res = $result->fetchArray(SQLITE3_NUM)) {    
        $dateMod = substr($res[0], 0, 4)."-".substr($res[0], 4, 2)."-".substr($res[0], 6, 2);
        $innRating = round($res[1], 0);
        $currRating = round($res[2], 0);
        if ($matchFormat == "Test") {
            $no1 = $res[3];
            $runs1 = $res[4];
            $no2 = $res[5];
            $runs2 = $res[6];
            $wkts1 = $res[7];
            $bowlRuns1 = $res[8];
            $wkts2 = $res[9];
            $bowlRuns2 = $res[10];
            $ground = $res[11];
            $team1 = $res[12];
            $team2 = $res[13];
            $country = $res[14];
        } else {
            $no = $res[3];
            $runs = $res[4];
            $wkts = $res[5];
            $bowlRuns = $res[6];
            $ground = $res[7];
            $team1 = $res[8];
            $team2 = $res[9];
            $country = $res[10];
        }        
        
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
        
        $runsMod = "";
        $wktsMod = "";
        if ($matchFormat == "Test") {
            if ($runs1 != "") {
                if ($no1 == 1) {
                    $runsMod = $runs1."*";
                } else {
                    $runsMod = $runs1;
                }   
            } else {
                $runsMod = "-";
            }
            
            if ($runs2 != "") {
                if ($no2 == 1) {
                    $runsMod = $runsMod. " & " . $runs2."*";
                } else {
                    $runsMod = $runsMod. " & " . $runs2;
                }
            } else {
                $runsMod = $runsMod. " & " . "-";
            }
            
            if ($wkts1 != "" and $bowlRuns1 != "") {
                $wktsMod = $wkts1."/".$bowlRuns1;
            } else {
                $wktsMod = "-";
            }
            
            if ($wkts2 != "" and $bowlRuns2 != "") {
                $wktsMod = $wktsMod. " & " . $wkts2."/".$bowlRuns2;
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
        
        $details = "<div style=\"padding:5px 5px 5px 5px; font-size:11px;\">";   
        $details .= "Runs: <b>".$runsMod."</b><br/>";   
        $details .= "Wkts: <b>".$wktsMod."</b><br/>";   

        if ($matchFormat == "FT20") {
            $details .= "Opposition: <b>$opposition</b><br/>";
        } else {
            $details .= "Opposition: <img src=\"images/".$opposition.".png\" border=1px/><br/>";
        }
        $details .= "Ground: <b>$ground</b><br/>";
        $details .= "Date: <b>$dateMod</b><br/>";
        $details .= "Match Rating: <b>$innRating</b><br/>";
        $details .= "Current Rating: <b>$currRating</b></div>";
        $temp[] = array('v' => $details);
        $temp[] = array('v' => $currRating);
        $temp[] = array('v' => $details);
        $rows[] = array('c' => $temp);
    }
} else if ($batBowl == "fielding") {
    while($res = $result->fetchArray(SQLITE3_NUM)) {    
        $dateMod = substr($res[0], 0, 4)."-".substr($res[0], 4, 2)."-".substr($res[0], 6, 2);
        $innRating = round($res[1], 0);
        $currRating = round($res[2], 0);
        $cat = $res[3];
        $drop = $res[4];
        $grtCat = $res[5];        
        $ground = $res[6];
        $team1 = $res[7];
        $team2 = $res[8];
        $country = $res[9];
        
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
        
        $details = "<div style=\"padding:5px 5px 5px 5px; font-size:11px;\">";   
        $details .= "Catches: <b>".$cat."</b><br/>";
        $details .= "Drops: <b>".$drop."</b><br/>";
        $details .= "GreatCatches: <b>".$grtCat."</b><br/>";        

        if ($matchFormat == "FT20") {
            $details .= "Opposition: <b>$opposition</b><br/>";
        } else {
            $details .= "Opposition: <img src=\"images/".$opposition.".png\" border=1px/><br/>";
        }
        $details .= "Ground: <b>$ground</b><br/>";
        $details .= "Date: <b>$dateMod</b><br/>";
        $details .= "Match Rating: <b>$innRating</b><br/>";
        $details .= "Current Rating: <b>$currRating</b></div>";
        $temp[] = array('v' => $details);
        $temp[] = array('v' => $currRating);
        $temp[] = array('v' => $details);
        $rows[] = array('c' => $temp);
    }
}  else if ($batBowl == "winShares") {
    while($res = $result->fetchArray(SQLITE3_NUM)) {    
        $dateMod = substr($res[0], 0, 4)."-".substr($res[0], 4, 2)."-".substr($res[0], 6, 2);
        $innRating = round($res[1], 3);
        $currRating = round($res[2], 3);
        $bat = round($res[3], 3);
        $bowl = round($res[4], 3);
        $field = round($res[5], 3);
        $ground = $res[6];
        $team1 = $res[7];
        $team2 = $res[8];
        $country = $res[9];
        
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
        
        $details = "<div style=\"padding:5px 5px 5px 5px; font-size:11px;\">";   
        $details .= "Bat: <b>".$bat."</b><br/>";
        $details .= "Bowl: <b>".$bowl."</b><br/>";
        $details .= "Field: <b>".$field."</b><br/>";        

        if ($matchFormat == "FT20") {
            $details .= "Opposition: <b>$opposition</b><br/>";
        } else {
            $details .= "Opposition: <img src=\"images/".$opposition.".png\" border=1px/><br/>";
        }
        $details .= "Ground: <b>$ground</b><br/>";
        $details .= "Date: <b>$dateMod</b><br/>";
        $details .= "Match Rating: <b>$innRating</b><br/>";
        $details .= "Current Rating: <b>$currRating</b></div>";
        $temp[] = array('v' => $details);
        $temp[] = array('v' => $currRating);
        $temp[] = array('v' => $details);
        $rows[] = array('c' => $temp);
    }
} else {
    while($res = $result->fetchArray(SQLITE3_NUM)) {    
        $dateMod = substr($res[0], 0, 4)."-".substr($res[0], 4, 2)."-".substr($res[0], 6, 2);
        $innRating = round($res[1], 0);
        $currRating = round($res[2], 0);
        $no = $res[3];
        $runs = $res[4];
        $ground = str_replace(" ","&nbsp;",$res[5]);
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
        $temp[] = array('v' => $details);
        $temp[] = array('v' => $currRating);
        $temp[] = array('v' => $details);
        $rows[] = array('c' => $temp);
    }
}


$table['rows'] = $rows;
$jsonTable = json_encode($table);
echo $jsonTable;
?>