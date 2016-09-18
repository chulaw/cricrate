<?php    

$xVal = $_GET["xVal"];
$yVal = $_GET["yVal"];
$batBowl = $_GET["batBowl"];
$matchFormat = $_GET["matchFormat"];
$matchFormatLower = strtolower($matchFormat);

if ($matchFormat == "Test") {
    $db = new SQLite3("../ccr.db");   
} else {
    $db = new SQLite3("../ccr".$matchFormat.".db");   
}

$playerFilter = "";    
if(isset($_GET['player']) ) {
    $player = $_GET['player'];	
    if ($player != "All") {	
	if ($batBowl != "allRound" and $batBowl != "fielding") {
	    $playerFilter = "and b.player='".$player."'";
	} else {
	    $playerFilter = "and a.player='".$player."'";
	}
    }
}  

if(isset($_GET['league'])) {    
   $league = $_GET['league'];
} else {
   $league = "";
}

$leagueFilter = "";
$leagueTeams = array (
		array('Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad', 'Rajasthan Royals', 'Mumbai Indians', 'Kolkata Knight Riders', 'Deccan Chargers', 'Kochi Tuskers Kerala', 'Pune Warriors', 'Rising Pune Supergiants', 'Gujarat Lions'),
		array('Melbourne Stars', 'Melbourne Renegades', 'Sydney Sixers', 'Sydney Thunder', 'Hobart Hurricanes', 'Adelaide Strikers', 'Brisbane Heat', 'Perth Scorchers'),
		array('Barbados Tridents', 'St Lucia Zouks', 'Guyana Amazon Warriors', 'Trinidad & Tobago Red Steel', 'Antigua Hawksbills', 'Jamaica Tallawahs', 'Trinidad & Tobago Red Steel', 'St Kitts and Nevis Patriots')
	    );
if (isset($_GET['league']) ) {
    $league = $_GET['league'];
    if ($league != "All" and $league != "") {
	$leagueFilter = "and t.team1 in (";
	if ($league == "IPL") {
	    $leagueTeamKey = 0;
	} elseif ($league == "BBL") {
	    $leagueTeamKey = 1;
	} elseif ($league == "CPL") {
	    $leagueTeamKey = 2;
	}
	
	$teams = $leagueTeams[$leagueTeamKey];
	foreach($teams as $team) {    
	    $leagueFilter .= "'".$team."',";
	}
	$leagueFilter .= "'') ";
    }	
}
    
$countryTeams = "p.country";
if ($matchFormat == "FT20") {
   $countryTeams = "p.teams";
}

$teamFilter = "";    
if( isset($_GET['teams']) ) {
    $teamFilter = "and ".$countryTeams." in (";
    foreach($_GET['teams'] as $team) {    
	$teamFilter .= "'".$team."',";
    }
    $teamFilter .= "'') ";
}

$oppFilter = "";    
if( isset($_GET['oppositions']) ) {
    $oppFilter1 = "and ((t.team1 in (";
    $oppFilter2 = "or (t.team2 in (";
    foreach($_GET['oppositions'] as $opp) {    
	$oppFilter1 .= "'".$opp."',";
	$oppFilter2 .= "'".$opp."',";
    }
    $oppFilter1 .= "'') and t.team2=".$countryTeams.")";
    $oppFilter2 .= "'') and t.team1=".$countryTeams."))";    
    $oppFilter = $oppFilter1.$oppFilter2;
}

$matchTypeFilter = "";
if (isset($_GET['matchType']) ) {
    $matchType = $_GET['matchType'];
    if ($matchType != "Any" and $matchType != "") {	    
	if ($matchType == "Knockout") {
	    $matchTypeFilter = "and t.series like '%final%'";
	} elseif ($matchType == "World Cup") {
	    if ($matchFormat == "T20I") {
		$matchTypeFilter = "and t.series like '%World%'";
	    } else {
	       $matchTypeFilter = "and t.series like '%World Cup%'";
	    }
	}
    }	
}

$winLossFilter = "";    
if( isset($_GET['winLoss']) ) {
    $winLossFilter = "and b.result in (";
    foreach($_GET['winLoss'] as $matchResult) {
	$winLossFilter .= $matchResult.",";
    }
    $winLossFilter .= "'') ";
}    

$homeAwayFilter = "";    
if (isset($_GET['homeAway']) ) {
    $homeAway = $_GET['homeAway'];
    if ($homeAway != 2) {	
	$homeAwayFilter = "and b.homeAway=".$homeAway." ";
    }
}

$hostFilter = "";    
if( isset($_GET['hosts']) ) {
    $hostFilter = "and t.location in (";
    foreach($_GET['hosts'] as $host) {    
	$hostFilter .= "'".$host."',";
    }
    $hostFilter .= "'') ";
}

$batFieldFirstFilter = "";    
if (isset($_GET['batFieldFirst']) ) {
    $batFieldFirst = $_GET['batFieldFirst'];
    if ($batFieldFirst == "Batting") {
	$batFieldFirstFilter = "and d.innings=1 and d.batTeam=p.country";
    } elseif ($batFieldFirst == "Fielding") {
	$batFieldFirstFilter = "and d.innings=1 and d.bowlTeam=p.country";
    } elseif ($batFieldFirst == "Either") {
	$batFieldFirstFilter = "and d.innings=1";
    }
}   

$groundFilter = "";    
if ($_GET['ground'] != "All") {
    $ground = $_GET['ground'];
    $groundFilter = "and t.ground='".$ground."'";
}    

$inningsFilter = "";    
if( isset($_GET['innings']) ) {
    $inningsFilter = "and b.innings in (";    
    foreach($_GET['innings'] as $inn) {
	$inningsFilter .= $inn.",";
    }
    $inningsFilter .= "'') ";
}

if ($matchFormat == "Test") {
    $startDate = "18770000";
} else if ($matchFormat == "ODI") {
    $startDate = "19710000";
} else if ($matchFormat == "T20I") {
    $startDate = "20050000";
} else if ($matchFormat == "FT20") {
    $startDate = "20080000";
}
$endDate = "20999999";    
if ($_GET['startDate'] != "") {
    if (strpos($_GET['startDate'], "-") == false) {
	$startDate = $_GET['startDate'];
    } else {
	$startDates = explode("-", $_GET['startDate']);
	$startDate = $startDates[0].$startDates[1].$startDates[2];
    }
}

if ($_GET['endDate'] != "") {
    if (strpos($_GET['endDate'], "-") == false) {
	$endDate = $_GET['endDate'];
    } else {
	$endDates = explode("-", $_GET['endDate']);
	$endDate = $endDates[0].$endDates[1].$endDates[2];
    }
}    

$groupBy = "Player";
if( isset($_GET['groupBy']) ) {
    $groupBy = $_GET['groupBy'];
}

$resultQualFilter = "";    
if( isset($_GET['resultQual']) ) {
    $resultQual = $_GET['resultQual'];
    $resultQualFrom = $_GET['resultQualFrom'];
    $resultQualTo = $_GET['resultQualTo'];
    
    if ($resultQual == "Innings played") {	
	if ($resultQualFrom != "") {
	    $resultQualFilter = "having numInn>=".$resultQualFrom." ";
	}
	
	if ($resultQualTo != "") {
	    if ($resultQualFrom != "") {
		$resultQualFilter .= "and";
	    } else {
		$resultQualFilter .= "having";
	    }
	    $resultQualFilter .= " numInn<=".$resultQualTo." ";
	}
    } else if ($resultQual == "Matches played") {	
	if ($resultQualFrom != "") {
	    $resultQualFilter = "having numMat>=".$resultQualFrom." ";
	}
	
	if ($resultQualTo != "") {
	    if ($resultQualFrom != "") {
		$resultQualFilter .= "and";
	    } else {
		$resultQualFilter .= "having";
	    }
	    $resultQualFilter .= " numMat<=".$resultQualTo." ";
	}
    } else if ($resultQual == "Runs scored") {
	if ($resultQualFrom != "") {
	    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
		$resultQualFilter = "having sumRuns>=".$resultQualFrom." ";   
	    } else {
		$resultQualFilter = "and sumRuns>=".$resultQualFrom." ";
	    }		
	}
	
	if ($resultQualTo != "") {
	    if ($resultQualFrom != "") {
		$resultQualFilter .= "and";
	    } else {
		if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
		    $resultQualFilter .= "having";
		} else {
		    $resultQualFilter .= "and";
		}		    
	    }
	    $resultQualFilter .= " sumRuns<=".$resultQualTo." ";
	}
    } else if ($resultQual == "Wickets taken") {
	if ($resultQualFrom != "") {
	    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
		$resultQualFilter = "having sumWkts>=".$resultQualFrom." ";   
	    } else {
		$resultQualFilter = "and sumWkts>=".$resultQualFrom." ";
	    }
	}
	
	if ($resultQualTo != "") {
	    if ($resultQualFrom != "") {
		$resultQualFilter .= "and";
	    } else {
		if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
		    $resultQualFilter .= "having";
		} else {
		    $resultQualFilter .= "and";
		}
	    }
	    $resultQualFilter .= " sumWkts<=".$resultQualTo." ";
	}
    } else if ($resultQual == "Catches taken") {
	if ($resultQualFrom != "") {
	    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
		$resultQualFilter = "having sumCatches>=".$resultQualFrom." ";   
	    } else {
		$resultQualFilter = "and sumCatches>=".$resultQualFrom." ";
	    }
	}
	
	if ($resultQualTo != "") {
	    if ($resultQualFrom != "") {
		$resultQualFilter .= "and";
	    } else {
		if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
		    $resultQualFilter .= "having";
		} else {
		    $resultQualFilter .= "and";
		}
	    }
	    $resultQualFilter .= " sumCatches<=".$resultQualTo." ";
	}
    } else if ($resultQual == "Rated" || $resultQual == "Total WSAvg" || $resultQual == "Total WS") {
	if ($resultQualFrom != "") {
	    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
		$resultQualFilter = "having avgRtg>=".$resultQualFrom." ";   
	    } else {
		$resultQualFilter = "and avgRtg>=".$resultQualFrom." ";
	    }
	}
	
	if ($resultQualTo != "") {
	    if ($resultQualFrom != "") {
		$resultQualFilter .= "and";
	    } else {
		if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
		    $resultQualFilter .= "having";
		} else {
		    $resultQualFilter .= "and";
		}
	    }
	    $resultQualFilter .= " avgRtg<=".$resultQualTo." ";
	}
    }
}

$xValSql = "";
$yValSql = "";
if ($batBowl == "batting") {
    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	$xValMod = array("average"=>"Average", "runs"=>"Runs", "strikeRate"=>"Strike Rate", "fifties"=>"Fifties", "hundreds"=>"Hundreds", "rating"=>"Rating", "innings"=>"Innings");
	$yValMod = array("strikeRate"=>"Strike Rate", "average"=>"Average", "runs"=>"Runs", "fifties"=>"Fifties", "hundreds"=>"Hundreds", "rating"=>"Rating", "innings"=>"Innings");	
    } else {
	$xValMod = array("runs"=>"Runs", "strikeRate"=>"Strike Rate", "balls"=>"Balls", "rating"=>"Rating");
	$yValMod = array("strikeRate"=>"Strike Rate", "runs"=>"Runs", "balls"=>"Balls", "rating"=>"Rating");
    }
} else if ($batBowl == "bowling") {
    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	$xValMod = array("average"=>"Average", "runs"=>"Runs", "strikeRate"=>"Strike Rate", "balls"=>"Balls", "wickets"=>"Wickets", "econRate"=>"Econ Rate", "rating"=>"Rating", "innings"=>"Innings");
	$yValMod = array("strikeRate"=>"Strike Rate", "average"=>"Average", "runs"=>"Runs", "balls"=>"Balls", "wickets"=>"Wickets", "econRate"=>"Econ Rate", "rating"=>"Rating", "innings"=>"Innings");
    } else {
	$xValMod = array("wickets"=>"Wickets", "runs"=>"Runs", "balls"=>"Balls", "rating"=>"Rating");
	$yValMod = array("runs"=>"Runs", "wickets"=>"Wickets", "balls"=>"Balls", "rating"=>"Rating");
    }     
} else if ($batBowl == "allRound") {
    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {	    
	$xValMod = array("battingAverage"=>"Batting Average", "bowlingAverage"=>"Bowling Average", "runs"=>"Runs", "wickets"=>"Wickets", "rating"=>"Rating", "matches"=>"Matches");
	$yValMod = array("bowlingAverage"=>"Bowling Average", "battingAverage"=>"Batting Average", "runs"=>"Runs", "wickets"=>"Wickets", "rating"=>"Rating", "matches"=>"Matches");
    } else {
	$xValMod = array("runs"=>"Runs", "wickets"=>"Wickets", "rating"=>"Rating");
	$yValMod = array("wickets"=>"Wickets", "runs"=>"Runs", "rating"=>"Rating");
    }
} else if ($batBowl == "fielding") {
    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	$xValMod = array("catches"=>"Catches", "droppedCatches"=>"Dropped Catches", "dropRate"=>"Drop Rate", "greatCatches"=>"Great Catches", "directHits"=>"Direct Hits", "runsSaved"=>"Runs Saved", "rating"=>"Rating", "innings"=>"Innings");
	$yValMod = array("droppedCatches"=>"Dropped Catches", "catches"=>"catches", "dropRate"=>"Drop Rate", "greatCatches"=>"Great Catches", "directHits"=>"Direct Hits", "runsSaved"=>"Runs Saved", "rating"=>"Rating", "innings"=>"Innings");		
    } else {
	$xValMod = array("catches"=>"Catches", "droppedCatches"=>"Dropped Catches", "greatCatches"=>"Great Catches", "directHits"=>"Direct Hits", "runsSaved"=>"Runs Saved", "rating"=>"Rating");
	$yValMod = array("droppedCatches"=>"Dropped Catches", "catches"=>"catches", "greatCatches"=>"Great Catches", "directHits"=>"Direct Hits", "runsSaved"=>"Runs Saved", "rating"=>"Rating");
    }	
} else if ($batBowl == "winShares") {
    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	$xValMod = array("battingWSAvg"=>"Batting WSAvg", "bowlingWSAvg"=>"Bowling WSAvg", "totalWSAvg"=>"Total WSAvg", "fieldingWSAvg"=>"Fielding WSAvg", "innings"=>"Innings");
	$yValMod = array("bowlingWSAvg"=>"Bowling WSAvg", "battingWSAvg"=>"Batting WSAvg", "totalWSAvg"=>"Total WSAvg", "fieldingWSAvg"=>"Fielding WSAvg", "innings"=>"Innings");
    } else {
	$xValMod = array("battingWS"=>"Batting WS", "bowlingWS"=>"Bowling WS", "totalWS"=>"Total WS", "fieldingWS"=>"Fielding WS");
	$yValMod = array("bowlingWS"=>"Bowling WS", "battingWS"=>"Batting WS", "totalWS"=>"Total WS", "fieldingWS"=>"Fielding WS");
    }	
} else if ($batBowl == "team") {
    $xValMod = array("wins"=>"Wins", "losses"=>"Losses", "draws"=>"Draws", "winPct"=>"Win %", "rating"=>"Rating", "tests"=>"Tests");
    $yValMod = array("losses"=>"Losses", "wins"=>"Wins", "draws"=>"Draws", "winPct"=>"Win %", "rating"=>"Rating", "tests"=>"Tests");
}

if ($batBowl == "batting") {
    if ($groupBy == "Player") {
	$sql = "select b.player, (sum(b.runs) * 1.0/(count(b.innings)-sum(b.notOut))) as average, (sum(b.runs) * 100.0 / sum(b.balls)) as strikeRate, sum(b.runs) as sumRuns, avg(b.rating) as avgRtg, count(b.innings) as numInn, ".$countryTeams.", (count(b.innings)-sum(b.notOut)) as sumNonNOInn from batting".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by b.playerId $resultQualFilter";
    } else if ($groupBy == "Ground") {
	$sql = "select t.ground, (sum(b.runs) * 1.0/(count(b.innings)-sum(b.notOut))) as average, (sum(b.runs) * 100.0 / sum(b.balls)) as strikeRate, sum(b.runs) as sumRuns, avg(b.rating) as avgRtg, count(b.innings) as numInn, t.location, (count(b.innings)-sum(b.notOut)) as sumNonNOInn from batting".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by t.ground $resultQualFilter";
    } else if ($groupBy == "Opposition") {
	$sql = "select (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, (sum(b.runs) * 1.0/(count(b.innings)-sum(b.notOut))) as average, (sum(b.runs) * 100.0 / sum(b.balls)) as strikeRate, sum(b.runs) as sumRuns, avg(b.rating) as avgRtg, count(b.innings) as numInn, t.location, (count(b.innings)-sum(b.notOut)) as sumNonNOInn from batting".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by opposition $resultQualFilter";
    } else {
	$sql = "select b.player, b.runs as sumRuns, (b.runs * 100.0 / b.balls) as strikeRate, b.balls, b.rating as avgRtg, ".$countryTeams.", t.team1, t.team2, t.ground, t.startDate, t.".$matchFormatLower."Id from batting".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter $resultQualFilter limit 5000";     
    }
} else if ($batBowl == "bowling") {
    if ($groupBy == "Player") {
	$sql = "select b.player, (sum(b.runs) * 1.0 / sum(b.wkts)) as average, (sum(b.balls) * 1.0 / sum(b.wkts)) as strikeRate, (sum(b.runs) * 6.0 / sum(b.balls)) as econRate, sum(b.balls) as sumBalls, sum(b.runs) as sumRuns, sum(b.wkts) as sumWkts, avg(b.rating) as avgRtg, count(b.innings) as numInn, ".$countryTeams." from bowling".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by b.playerId $resultQualFilter";
    } else if ($groupBy == "Ground") {
	$sql = "select t.ground, (sum(b.runs) * 1.0 / sum(b.wkts)) as average, (sum(b.balls) * 1.0 / sum(b.wkts)) as strikeRate, (sum(b.runs) * 6.0 / sum(b.balls)) as econRate, sum(b.balls) as sumBalls, sum(b.runs) as sumRuns, sum(b.wkts) as sumWkts, avg(b.rating) as avgRtg, count(b.innings) as numInn, t.location from bowling".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by t.ground $resultQualFilter";
    } else if ($groupBy == "Opposition") {
	$sql = "select (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, (sum(b.runs) * 1.0 / sum(b.wkts)) as average, (sum(b.balls) * 1.0 / sum(b.wkts)) as strikeRate, (sum(b.runs) * 6.0 / sum(b.balls)) as econRate, sum(b.balls) as sumBalls, sum(b.runs) as sumRuns, sum(b.wkts) as sumWkts, avg(b.rating) as avgRtg, count(b.innings) as numInn, t.location from bowling".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by opposition $resultQualFilter";
    } else {
	$sql = "select b.player, b.wkts as sumWkts, b.balls as sumBalls, b.runs as sumRuns, b.rating as avgRtg, ".$countryTeams.", t.team1, t.team2, t.ground, t.startDate, t.".$matchFormatLower."Id from bowling".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter $resultQualFilter limit 5000";
    }
} else if ($batBowl == "allRound") {
    if ($matchFormat == "Test") {
	if ($groupBy == "Player") {
	    $sql = "select a.player, (sum(a.runs1) + sum(a.runs2)) as sumRuns, (sum(a.runs1) + sum(a.runs2)) * 1.0/(count(a.runs1) + count(a.runs2) - sum(a.notOut1) - sum(a.notOut2)) as battingAverage, (sum(a.wkts1) + sum(a.wkts2)) as sumWkts, (sum(a.bowlRuns1)+sum(a.bowlRuns2)) * 1.0 / (sum(a.wkts1)+sum(a.wkts2)) as bowlingAverage, avg(a.rating) as avgRtg, count(a.".$matchFormatLower."Id) as numMat, ".$countryTeams." from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by a.playerId $resultQualFilter";
	} else if ($groupBy == "Ground") {
	    $sql = "select t.ground, (sum(a.runs1) + sum(a.runs2)) as sumRuns, (sum(a.runs1) + sum(a.runs2)) * 1.0/(count(a.runs1) + count(a.runs2) - sum(a.notOut1) - sum(a.notOut2)) as battingAverage, (sum(a.wkts1) + sum(a.wkts2)) as sumWkts, (sum(a.bowlRuns1)+sum(a.bowlRuns2)) * 1.0 / (sum(a.wkts1)+sum(a.wkts2)) as bowlingAverage, avg(a.rating) as avgRtg, count(a.".$matchFormatLower."Id) as numMat, t.location from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by t.ground $resultQualFilter";
	} else if ($groupBy == "Opposition") {
	    $sql = "select (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, (sum(a.runs1) + sum(a.runs2)) as sumRuns, (sum(a.runs1) + sum(a.runs2)) * 1.0/(count(a.runs1) + count(a.runs2) - sum(a.notOut1) - sum(a.notOut2)) as battingAverage, (sum(a.wkts1) + sum(a.wkts2)) as sumWkts, (sum(a.bowlRuns1)+sum(a.bowlRuns2)) * 1.0 / (sum(a.wkts1)+sum(a.wkts2)) as bowlingAverage, avg(a.rating) as avgRtg, count(a.".$matchFormatLower."Id) as numMat, t.location from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by opposition $resultQualFilter";
	} else {
	    $sql = "select a.player, a.runs1, a.notOut1, a.runs2, a.notOut2, a.wkts1, a.bowlRuns1, a.wkts2, a.bowlRuns2, a.rating as avgRtg, ".$countryTeams.", t.team1, t.team2, t.ground, t.startDate, t.".$matchFormatLower."Id, (a.runs1+a.runs2) as sumRuns, (a.wkts1+a.wkts2) as sumWkts from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter $resultQualFilter limit 5000";
	}
    } else {
	if ($groupBy == "Player") {
	    $sql = "select a.player, sum(a.runs) as sumRuns, sum(a.runs) * 1.0/(count(a.runs) - sum(a.notOut)) as battingAverage, sum(a.wkts) as sumWkts, (sum(a.bowlRuns) * 1.0 / sum(a.wkts)) as bowlingAverage, avg(a.rating) as avgRtg, count(a.".$matchFormatLower."Id) as numMat, ".$countryTeams." from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by a.playerId $resultQualFilter";
	} else if ($groupBy == "Ground") {
	    $sql = "select t.ground, sum(a.runs) as sumRuns, sum(a.runs) * 1.0/(count(a.runs) - sum(a.notOut)) as battingAverage, sum(a.wkts) as sumWkts, (sum(a.bowlRuns) * 1.0 / sum(a.wkts)) as bowlingAverage, avg(a.rating) as avgRtg, count(a.".$matchFormatLower."Id) as numMat, t.location from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by t.ground $resultQualFilter";
	} else if ($groupBy == "Opposition") {
	    $sql = "select (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, sum(a.runs) as sumRuns, sum(a.runs) * 1.0/(count(a.runs) - sum(a.notOut)) as battingAverage, sum(a.wkts) as sumWkts, (sum(a.bowlRuns) * 1.0 / sum(a.wkts)) as bowlingAverage, avg(a.rating) as avgRtg, count(a.".$matchFormatLower."Id) as numMat, t.location from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by opposition $resultQualFilter";
	} else {
	    $sql = "select a.player, a.runs as sumRuns, a.notOut, a.wkts as sumWkts, a.bowlRuns, a.rating as avgRtg, ".$countryTeams.", t.team1, t.team2, t.ground, t.startDate, t.".$matchFormatLower."Id from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter $resultQualFilter limit 5000";
	}
    }
} else if ($batBowl == "fielding") {   
    if ($groupBy == "Player") {
	$sql = "select a.player, sum(a.catches) as sumCatches, sum(a.droppedCatches) as droppedCatches, (sum(a.droppedCatches) * 1.0 / (sum(a.droppedCatches) + sum(a.catches))) as dropRate, sum(a.greatCatches) as sumGreatCatches, sum(a.directHits) as sumDirectHits, sum(a.runsSaved) as sumRunsSaved, avg(a.rating) avgRtg, count(t.".$matchFormatLower."Id) as numInn, ".$countryTeams." from fielding".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate  $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by a.playerId $resultQualFilter";
    } else if ($groupBy == "Ground") {
	$sql = "select t.ground, sum(a.catches) as sumCatches, sum(a.droppedCatches) as droppedCatches, (sum(a.droppedCatches) * 1.0 / (sum(a.droppedCatches) + sum(a.catches))) as dropRate, sum(a.greatCatches) as sumGreatCatches, sum(a.directHits) as sumDirectHits, sum(a.runsSaved) as sumRunsSaved, avg(a.rating) avgRtg, count(t.".$matchFormatLower."Id) as numInn, t.location from fielding".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate  $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by t.ground $resultQualFilter";
    } else if ($groupBy == "Opposition") {
	$sql = "select (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, sum(a.catches) as sumCatches, sum(a.droppedCatches) as droppedCatches, (sum(a.droppedCatches) * 1.0 / (sum(a.droppedCatches) + sum(a.catches))) as dropRate, sum(a.greatCatches) as sumGreatCatches, sum(a.directHits) as sumDirectHits, sum(a.runsSaved) as sumRunsSaved, avg(a.rating) avgRtg, count(t.".$matchFormatLower."Id) as numInn, t.location from fielding".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate  $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by opposition $resultQualFilter";
    } else {
	$sql = "select a.player, a.catches as sumCatches, a.droppedCatches as droppedCatches, a.greatCatches as sumGreatCatches, a.directHits as sumDirectHits, a.runsSaved as sumRunsSaved, a.rating as avgRtg, ".$countryTeams.", t.team1, t.team2, t.ground, t.startDate, t.".$matchFormatLower."Id from fielding".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter $resultQualFilter limit 5000";
    }
} else if ($batBowl == "winShares") {    
    if ($groupBy == "Player") {
	$sql = "select a.player, avg(a.battingAdjWS) as avgBattingWS, avg(a.bowlingAdjWS) as avgBowlingWS, avg(a.fieldingAdjWS) as avgFieldingWS, avg(a.totalAdjWS) as avgRtg, count(t.".$matchFormatLower."Id) as numInn, ".$countryTeams." from winShares".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by a.playerId $resultQualFilter";
    } else if ($groupBy == "Ground") {
	$sql = "select t.ground, avg(a.battingAdjWS) as avgBattingWS, avg(a.bowlingAdjWS) as avgBowlingWS, avg(a.fieldingAdjWS) as avgFieldingWS, avg(a.totalAdjWS) as avgRtg, count(t.".$matchFormatLower."Id) as numInn, t.location from winShares".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by t.ground $resultQualFilter";
    } else if ($groupBy == "Opposition") {
	$sql = "select (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, avg(a.battingAdjWS) as avgBattingWS, avg(a.bowlingAdjWS) as avgBowlingWS, avg(a.fieldingAdjWS) as avgFieldingWS, avg(a.totalAdjWS) as avgRtg, count(t.".$matchFormatLower."Id) as numInn, t.location from winShares".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by opposition $resultQualFilter";
    } else {
	$sql = "select a.player, a.battingAdjWS as avgBattingWS, a.bowlingAdjWS as avgBowlingWS, a.fieldingAdjWS as avgFieldingWS, a.totalAdjWS as avgRtg, ".$countryTeams.", t.team1, t.team2, t.ground, t.startDate, t.".$matchFormatLower."Id from winShares".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter $resultQualFilter limit 5000";
    }
}

//echo $sql;
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");

$k = 0;
$xVals = array();
$yVals = array();
$players = array();
$teams = array();
$ratings = array();
while($res = $result->fetchArray(SQLITE3_NUM)) {        
    $xKey = 1;
    $yKey = 2;
    $roundXKey = 0;
    $roundYKey = 0;
    $teamKey = 6;
    $ratingKey = 4; 
    if ($batBowl == "batting") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	    if ($res[7] == 0) { continue; }
	    $teamKey = 6;
	    $ratingKey = 4; 
	    if ($xVal == "average") {
		$xKey = 1;
		$roundXKey = 2;
	    } else if ($xVal == "strikeRate") {
		$xKey = 2;
		$roundXKey = 2;
	    } else if ($xVal == "runs") {
		$xKey = 3;
		$roundXKey = 0;
	    } else if ($xVal == "rating") {
		$xKey = 4;
		$roundXKey = 0;
	    } else if ($xVal == "innings") {
		$xKey = 5;
		$roundXKey = 0;
	    }
	    
	    if ($yVal == "average") {
		$yKey = 1;
		$roundYKey = 2;
	    } else if ($yVal == "strikeRate") {
		$yKey = 2;
		$roundYKey = 2;
	    } else if ($yVal == "runs") {
		$yKey = 3;
		$roundYKey = 0;
	    } else if ($yVal == "rating") {
		$yKey = 4;
		$roundYKey = 0;
	    } else if ($yVal == "innings") {
		$yKey = 5;
		$roundYKey = 0;
	    }
	} else {
	    $teamKey = 5;
	    $ratingKey = 4; 
	    if ($xVal == "runs") {
		$xKey = 1;
		$roundXKey = 0;
	    } else if ($xVal == "strikeRate") {
		$xKey = 2;
		$roundXKey = 2;
	    } else if ($xVal == "balls") {
		$xKey = 3;
		$roundXKey = 0;
	    } else if ($xVal == "rating") {
		$xKey = 4;
		$roundXKey = 0;
	    }
	    
	    if ($yVal == "runs") {
		$yKey = 1;
		$roundYKey = 0;
	    } else if ($yVal == "strikeRate") {
		$yKey = 2;
		$roundYKey = 2;
	    } else if ($yVal == "balls") {
		$yKey = 3;
		$roundYKey = 0;
	    } else if ($yVal == "rating") {
		$yKey = 4;
		$roundYKey = 0;
	    }
	}
    } else if ($batBowl == "bowling") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	    if ($res[6] == 0) { continue; }
	    $teamKey = 9;
	    $ratingKey = 7; 
	    if ($xVal == "average") {
		$xKey = 1;
		$roundXKey = 2;
	    } else if ($xVal == "strikeRate") {
		$xKey = 2;
		$roundXKey = 2;
	    } else if ($xVal == "econRate") {
		$xKey = 3;
		$roundXKey = 1;
	    } else if ($xVal == "balls") {
		$xKey = 4;
		$roundXKey = 0;
	    } else if ($xVal == "runs") {
		$xKey = 5;
		$roundXKey = 0;
	    } else if ($xVal == "wickets") {
		$xKey = 6;
		$roundXKey = 0;
	    } else if ($xVal == "rating") {
		$xKey = 7;
		$roundXKey = 0;
	    } else if ($xVal == "innings") {
		$xKey = 8;
		$roundXKey = 0;
	    }
	    
	    if ($yVal == "average") {
		$yKey = 1;
		$roundYKey = 2;
	    } else if ($yVal == "strikeRate") {
		$yKey = 2;
		$roundYKey = 2;
	    } else if ($yVal == "econRate") {
		$yKey = 3;
		$roundYKey = 1;
	    } else if ($yVal == "balls") {
		$yKey = 4;
		$roundYKey = 0;
	    } else if ($yVal == "runs") {
		$yKey = 5;
		$roundYKey = 0;
	    } else if ($yVal == "wickets") {
		$yKey = 6;
		$roundYKey = 0;
	    } else if ($yVal == "rating") {
		$yKey = 7;
		$roundYKey = 0;
	    } else if ($yVal == "innings") {
		$yKey = 8;
		$roundYKey = 0;
	    }
	} else {
	    $teamKey = 5;
	    $ratingKey = 4; 
	    if ($xVal == "wickets") {
		$xKey = 1;
		$roundXKey = 0;
	    } else if ($xVal == "balls") {
		$xKey = 2;
		$roundXKey = 0;
	    } else if ($xVal == "runs") {
		$xKey = 3;
		$roundXKey = 0;
	    } else if ($xVal == "rating") {
		$xKey = 4;
		$roundXKey = 0;
	    }	    
	    
	    if ($yVal == "wickets") {
		$yKey = 1;
		$roundYKey = 0;
	    } else if ($yVal == "balls") {
		$yKey = 2;
		$roundYKey = 0;
	    } else if ($yVal == "runs") {
		$yKey = 3;
		$roundYKey = 0;
	    } else if ($yVal == "rating") {
		$yKey = 4;
		$roundYKey = 0;
	    }
	}
    } else if ($batBowl == "allRound") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	    if ($res[2] == 0 || $res[4] == 0) { continue; }
	    $teamKey = 7;
	    $ratingKey = 5; 
	    if ($xVal == "runs") {
		$xKey = 1;
		$roundXKey = 0;
	    } else if ($xVal == "battingAverage") {
		$xKey = 2;
		$roundXKey = 2;
	    } else if ($xVal == "wickets") {
		$xKey = 3;
		$roundXKey = 0;
	    } else if ($xVal == "bowlingAverage") {
		$xKey = 4;
		$roundXKey = 2;
	    } else if ($xVal == "rating") {
		$xKey = 5;
		$roundXKey = 0;
	    } else if ($xVal == "matches") {
		$xKey = 6;
		$roundXKey = 0;
	    }
	    
	    if ($yVal == "runs") {
		$yKey = 1;
		$roundYKey = 0;
	    } else if ($yVal == "battingAverage") {
		$yKey = 2;
		$roundYKey = 2;
	    } else if ($yVal == "wickets") {
		$yKey = 3;
		$roundYKey = 0;
	    } else if ($yVal == "bowlingAverage") {
		$yKey = 4;
		$roundYKey = 2;
	    } else if ($yVal == "rating") {
		$yKey = 5;
		$roundYKey = 0;
	    } else if ($yVal == "matches") {
		$yKey = 6;
		$roundYKey = 0;
	    }
	} else {
	    if ($matchFormat == "Test") {
		$teamKey = 10;
		$ratingKey = 9; 
		if ($xVal == "runs") {
		    $xKey = 16;
		    $roundXKey = 0;
		} else if ($xVal == "wickets") {
		    $xKey = 17;
		    $roundXKey = 0;
		} else if ($xVal == "rating") {
		    $xKey = 9;
		    $roundXKey = 0;
		}	    
		
		if ($yVal == "runs") {
		    $yKey = 16;
		    $roundYKey = 0;
		} else if ($yVal == "wickets") {
		    $yKey = 17;
		    $roundYKey = 0;
		} else if ($yVal == "rating") {
		    $yKey = 9;
		    $roundYKey = 0;
		}
	    } else {
		$teamKey = 6;
		$ratingKey = 5; 
		if ($xVal == "runs") {
		    $xKey = 1;
		    $roundXKey = 0;
		} else if ($xVal == "wickets") {
		    $xKey = 3;
		    $roundXKey = 0;
		} else if ($xVal == "rating") {
		    $xKey = 5;
		    $roundXKey = 0;
		}	    
		
		if ($yVal == "runs") {
		    $yKey = 1;
		    $roundYKey = 0;
		} else if ($yVal == "wickets") {
		    $yKey = 3;
		    $roundYKey = 0;
		} else if ($yVal == "rating") {
		    $yKey = 5;
		    $roundYKey = 0;
		}
	    }	    
	}
    } else if ($batBowl == "fielding") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	    if ($res[1] == 0) { continue; }
	    $teamKey = 9;
	    $ratingKey = 7;
	    if ($xVal == "dropRate") {
		$xKey = 3;
		$roundXKey = 2;
	    } else if ($xVal == "catches") {
		$xKey = 1;
		$roundXKey = 0;
	    } else if ($xVal == "droppedCatches") {
		$xKey = 2;
		$roundXKey = 0;
	    } else if ($xVal == "greatCatches") {
		$xKey = 4;
		$roundXKey = 0;
	    } else if ($xVal == "directHits") {
		$xKey = 5;
		$roundXKey = 0;
	    } else if ($xVal == "runsSaved") {
		$xKey = 6;
		$roundXKey = 0;
	    } else if ($xVal == "rating") {
		$xKey = 7;
		$roundXKey = 0;
	    } else if ($xVal == "innings") {
		$xKey = 8;
		$roundXKey = 0;
	    }
	    
	    if ($yVal == "dropRate") {
		$yKey = 3;
		$roundYKey = 2;
	    } else if ($yVal == "catches") {
		$yKey = 1;
		$roundYKey = 0;
	    } else if ($yVal == "droppedCatches") {
		$yKey = 2;
		$roundYKey = 0;
	    } else if ($yVal == "greatCatches") {
		$yKey = 4;
		$roundYKey = 0;
	    } else if ($yVal == "directHits") {
		$yKey = 5;
		$roundYKey = 0;
	    } else if ($yVal == "runsSaved") {
		$yKey = 6;
		$roundYKey = 0;
	    } else if ($yVal == "rating") {
		$yKey = 7;
		$roundYKey = 0;
	    } else if ($yVal == "innings") {
		$yKey = 8;
		$roundYKey = 0;
	    }
	} else {
	    $teamKey = 7;
	    $ratingKey = 6; 
	    if ($xVal == "catches") {
		$xKey = 1;
		$roundXKey = 0;
	    } else if ($xVal == "droppedCatches") {
		$xKey = 2;
		$roundXKey = 0;
	    } else if ($xVal == "greatCatches") {
		$xKey = 3;
		$roundXKey = 0;
	    } else if ($xVal == "directHits") {
		$xKey = 4;
		$roundXKey = 0;
	    } else if ($xVal == "runsSaved") {
		$xKey = 5;
		$roundXKey = 0;
	    } else if ($xVal == "rating") {
		$xKey = 6;
		$roundXKey = 0;
	    }
	    
	    if ($yVal == "catches") {
		$yKey = 1;
		$roundYKey = 0;
	    } else if ($yVal == "droppedCatches") {
		$yKey = 2;
		$roundYKey = 0;
	    } else if ($yVal == "greatCatches") {
		$yKey = 3;
		$roundYKey = 0;
	    } else if ($yVal == "directHits") {
		$yKey = 4;
		$roundYKey = 0;
	    } else if ($yVal == "runsSaved") {
		$yKey = 5;
		$roundYKey = 0;
	    } else if ($yVal == "rating") {
		$yKey = 6;
		$roundYKey = 0;
	    }
	}
    } else if ($batBowl == "winShares") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	    $teamKey = 6;
	    $ratingKey = 4;
	    if ($xVal == "battingWSAvg") {
		$xKey = 1;
		$roundXKey = 3;
	    } else if ($xVal == "bowlingWSAvg") {
		$xKey = 2;
		$roundXKey = 3;
	    } else if ($xVal == "fieldingWSAvg") {
		$xKey = 3;
		$roundXKey = 3;
	    } else if ($xVal == "totalWSAvg") {
		$xKey = 4;
		$roundXKey = 3;
	    } else if ($xVal == "innings") {
		$xKey = 5;
		$roundXKey = 0;
	    }
	    
	    if ($yVal == "battingWSAvg") {
		$yKey = 1;
		$roundYKey = 3;
	    } else if ($yVal == "bowlingWSAvg") {
		$yKey = 2;
		$roundYKey = 3;
	    } else if ($yVal == "fieldingWSAvg") {
		$yKey = 3;
		$roundYKey = 3;
	    } else if ($yVal == "totalWSAvg") {
		$yKey = 4;
		$roundYKey = 3;
	    } else if ($yVal == "innings") {
		$yKey = 5;
		$roundYKey = 0;
	    }
	} else {
	    $teamKey = 5;
	    $ratingKey = 4; 
	    if ($xVal == "battingWS") {
		$xKey = 1;
		$roundXKey = 3;
	    } else if ($xVal == "bowlingWS") {
		$xKey = 2;
		$roundXKey = 3;
	    } else if ($xVal == "fieldingWS") {
		$xKey = 3;
		$roundXKey = 3;
	    } else if ($xVal == "totalWS") {
		$xKey = 4;
		$roundXKey = 3;
	    }
	    
	    if ($yVal == "battingWS") {
		$yKey = 1;
		$roundYKey = 3;
	    } else if ($yVal == "bowlingWS") {
		$yKey = 2;
		$roundYKey = 3;
	    } else if ($yVal == "fieldingWS") {
		$yKey = 3;
		$roundYKey = 3;
	    } else if ($yVal == "totalWS") {
		$yKey = 4;
		$roundYKey = 3;
	    }
	}
    }
    
    array_push($players, $res[0]);
    array_push($xVals, round($res[$xKey], $roundXKey));
    array_push($yVals, round($res[$yKey], $roundYKey));
    $teamMod = $res[$teamKey];
    if ($matchFormat == "FT20") {
        $fTeams = explode(",", $teamMod);
        $teamMod = trim($fTeams[0]);
    }
    if ($groupBy == "Opposition") {
	array_push($teams, $res[0]);
    } else {
	array_push($teams, $teamMod);
    }    
    array_push($ratings, round($res[$ratingKey], 0));
}

$table = array();
$table['cols'] = array(
                        array('id' => "", 'label' => "Player/Ground/Opposition", 'pattern' => "", 'type' => 'string'),
                        array('id' => "", 'label' => $xValMod[$xVal], 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'label' => $yValMod[$yVal], 'pattern' => "", 'type' => 'number'),
                        array('id' => "", 'label' => "Team", 'pattern' => "", 'type' => 'string'),
                        array('id' => "", 'label' => "Rating", 'pattern' => "", 'type' => 'number'),			
                    );

$rows = array();

for ($i = 0; $i < count($xVals); $i++) {    
    $temp = array();
    $temp[] = array('v' => $players[$i]);
    $temp[] = array('v' => $xVals[$i]);
    $temp[] = array('v' => $yVals[$i]);
    $temp[] = array('v' => $teams[$i]);
    $temp[] = array('v' => $ratings[$i]);    
    $rows[] = array('c' => $temp);  
} 

$table['rows'] = $rows;
$jsonTable = json_encode($table);
echo $jsonTable;
?>