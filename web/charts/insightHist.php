<?php    

$histVal = $_GET["histVal"];
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

if ($batBowl == "batting") {
    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	$histValMod = array("average"=>"Average", "runs"=>"Runs", "strikeRate"=>"Strike Rate", "fifties"=>"Fifties", "hundreds"=>"Hundreds", "rating"=>"Rating", "innings"=>"Innings");
    } else {
	$histValMod = array("runs"=>"Runs", "strikeRate"=>"Strike Rate", "balls"=>"Balls", "rating"=>"Rating");
    }    
} else if ($batBowl == "bowling") {
    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	$histValMod = array("average"=>"Average", "runs"=>"Runs", "strikeRate"=>"Strike Rate", "balls"=>"Balls", "wickets"=>"Wickets", "econRate"=>"Econ Rate", "rating"=>"Rating", "innings"=>"Innings");	
    } else {
	$histValMod = array("wickets"=>"Wickets", "runs"=>"Runs", "balls"=>"Balls", "rating"=>"Rating");
    }      
} else if ($batBowl == "allRound") {
    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {	    	
	$histValMod = array("battingAverage"=>"Batting Average", "bowlingAverage"=>"Bowling Average", "runs"=>"Runs", "wickets"=>"Wickets", "rating"=>"Rating", "matches"=>"Matches");
    } else {
	$histValMod = array("rating"=>"Rating", "runs"=>"Runs", "wickets"=>"Wickets");
    }    
} else if ($batBowl == "fielding") {
    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {	    	
	$histValMod = array("dropRate"=>"Drop Rate", "catches"=>"Catches", "droppedCatches"=>"Dropped Catches", "greatCatches"=>"Great Catches", "directHits"=>"Direct Hits", "runsSaved"=>"Runs Saved", "rating"=>"Rating", "innings"=>"Innings");
    } else {
	$histValMod = array("catches"=>"Catches", "droppedCatches"=>"Dropped Catches", "greatCatches"=>"Great Catches", "directHits"=>"Direct Hits", "runsSaved"=>"Runs Saved", "rating"=>"Rating");
    }    
} else if ($batBowl == "winShares") {
    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	$histValMod = array("battingWSAvg"=>"Batting WSAvg", "bowlingWSAvg"=>"Bowling WSAvg", "totalWSAvg"=>"Total WSAvg", "fieldingWSAvg"=>"Fielding WSAvg", "innings"=>"Innings");
    } else {
	$histValMod = array("battingWS"=>"Batting WS", "bowlingWS"=>"Bowling WS", "totalWS"=>"Total WS", "fieldingWS"=>"Fielding WS");
    }	
} else if ($batBowl == "team") {
    $histValMod = array("wins"=>"Wins", "losses"=>"Losses", "draws"=>"Draws", "winPct"=>"Win %", "rating"=>"Rating", "tests"=>"Tests");
}

if ($batBowl == "batting") {
    if ($groupBy == "Player") {
	$sql = "select b.player, (sum(b.runs) * 1.0/(count(b.innings)-sum(b.notOut))) as average, (sum(b.runs) * 100 / sum(b.balls)) as strikeRate, sum(b.runs) as sumRuns, avg(b.rating) as avgRtg, count(b.innings) as numInn, (count(b.innings)-sum(b.notOut)) as sumNonNOInn from batting".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by b.playerId $resultQualFilter";
    } else if ($groupBy == "Ground") {
	$sql = "select t.ground, (sum(b.runs) * 1.0/(count(b.innings)-sum(b.notOut))) as average, (sum(b.runs) * 100 / sum(b.balls)) as strikeRate, sum(b.runs) as sumRuns, avg(b.rating) as avgRtg, count(b.innings) as numInn, (count(b.innings)-sum(b.notOut)) as sumNonNOInn from batting".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by t.ground $resultQualFilter";
    }  else if ($groupBy == "Opposition") {
	$sql = "select (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, (sum(b.runs) * 1.0/(count(b.innings)-sum(b.notOut))) as average, (sum(b.runs) * 100 / sum(b.balls)) as strikeRate, sum(b.runs) as sumRuns, avg(b.rating) as avgRtg, count(b.innings) as numInn, (count(b.innings)-sum(b.notOut)) as sumNonNOInn from batting".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by opposition $resultQualFilter";
    } else {
	$sql = "select b.player, b.runs as sumRuns, (b.runs * 100 / b.balls) as strikeRate, b.balls, b.rating as avgRtg from batting".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter $resultQualFilter limit 5000";     
    }
} else if ($batBowl == "bowling") {
    if ($groupBy == "Player") {
	$sql = "select b.player, (sum(b.runs) * 1.0 / sum(b.wkts)) as average, (sum(b.balls) * 1.0 / sum(b.wkts)) as strikeRate, (sum(b.runs) * 6.0 / sum(b.balls)) as econRate, sum(b.balls) as sumBalls, sum(b.runs) as sumRuns, sum(b.wkts) as sumWkts, avg(b.rating) as avgRtg, count(b.innings) as numInn from bowling".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by b.playerId $resultQualFilter";
    } else if ($groupBy == "Ground") {
	$sql = "select t.ground, (sum(b.runs) * 1.0 / sum(b.wkts)) as average, (sum(b.balls) * 1.0 / sum(b.wkts)) as strikeRate, (sum(b.runs) * 6.0 / sum(b.balls)) as econRate, sum(b.balls) as sumBalls, sum(b.runs) as sumRuns, sum(b.wkts) as sumWkts, avg(b.rating) as avgRtg, count(b.innings) as numInn from bowling".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by t.ground $resultQualFilter";
    }  else if ($groupBy == "Opposition") {
	$sql = "select (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, (sum(b.runs) * 1.0 / sum(b.wkts)) as average, (sum(b.balls) * 1.0 / sum(b.wkts)) as strikeRate, (sum(b.runs) * 6.0 / sum(b.balls)) as econRate, sum(b.balls) as sumBalls, sum(b.runs) as sumRuns, sum(b.wkts) as sumWkts, avg(b.rating) as avgRtg, count(b.innings) as numInn from bowling".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by opposition $resultQualFilter";
    } else {
	$sql = "select b.player, b.wkts as sumWkts, b.balls as sumBalls, b.runs as sumRuns, b.rating as avgRtg from bowling".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter $resultQualFilter limit 5000";
    }    
} else if ($batBowl == "allRound") {
    if ($matchFormat == "Test") {
	if ($groupBy == "Player") {
	    $sql = "select a.player, (sum(a.runs1) + sum(a.runs2)) as sumRuns, (sum(a.runs1) + sum(a.runs2)) * 1.0/(count(a.runs1) + count(a.runs2) - sum(a.notOut1) - sum(a.notOut2)) as battingAverage, (sum(a.wkts1) + sum(a.wkts2)) as sumWkts, (sum(a.bowlRuns1)+sum(a.bowlRuns2)) * 1.0 / (sum(a.wkts1)+sum(a.wkts2)) as bowlingAverage, avg(a.rating) as avgRtg, count(a.".$matchFormatLower."Id) as numMat from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by a.playerId $resultQualFilter";
	} else if ($groupBy == "Ground") {
	    $sql = "select t.ground, (sum(a.runs1) + sum(a.runs2)) as sumRuns, (sum(a.runs1) + sum(a.runs2)) * 1.0/(count(a.runs1) + count(a.runs2) - sum(a.notOut1) - sum(a.notOut2)) as battingAverage, (sum(a.wkts1) + sum(a.wkts2)) as sumWkts, (sum(a.bowlRuns1)+sum(a.bowlRuns2)) * 1.0 / (sum(a.wkts1)+sum(a.wkts2)) as bowlingAverage, avg(a.rating) as avgRtg, count(a.".$matchFormatLower."Id) as numMat from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by t.ground $resultQualFilter";
	} else if ($groupBy == "Opposition") {
	    $sql = "select (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, (sum(a.runs1) + sum(a.runs2)) as sumRuns, (sum(a.runs1) + sum(a.runs2)) * 1.0/(count(a.runs1) + count(a.runs2) - sum(a.notOut1) - sum(a.notOut2)) as battingAverage, (sum(a.wkts1) + sum(a.wkts2)) as sumWkts, (sum(a.bowlRuns1)+sum(a.bowlRuns2)) * 1.0 / (sum(a.wkts1)+sum(a.wkts2)) as bowlingAverage, avg(a.rating) as avgRtg, count(a.".$matchFormatLower."Id) as numMat, ".$countryTeams." from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by opposition $resultQualFilter";
	} else {
	    $sql = "select a.player, a.runs1, a.notOut1, a.runs2, a.notOut2, a.wkts1, a.bowlRuns1, a.wkts2, a.bowlRuns2, a.rating as avgRtg, (a.runs1+a.runs2) as sumRuns, (a.wkts1+a.wkts2) as sumWkts from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter $resultQualFilter limit 5000";
	}
    } else {
	if ($groupBy == "Player") {
	    $sql = "select a.player, sum(a.runs) as sumRuns, sum(a.runs) * 1.0/(count(a.runs) - sum(a.notOut)) as battingAverage, sum(a.wkts) as sumWkts, (sum(a.bowlRuns) * 1.0 / sum(a.wkts)) as bowlingAverage, avg(a.rating) as avgRtg, count(a.".$matchFormatLower."Id) as numMat, ".$countryTeams." from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by a.playerId $resultQualFilter";
	} else if ($groupBy == "Ground") {
	    $sql = "select t.ground, sum(a.runs) as sumRuns, sum(a.runs) * 1.0/(count(a.runs) - sum(a.notOut)) as battingAverage, sum(a.wkts) as sumWkts, (sum(a.bowlRuns) * 1.0 / sum(a.wkts)) as bowlingAverage, avg(a.rating) as avgRtg, count(a.".$matchFormatLower."Id) as numMat, ".$countryTeams." from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by t.ground $resultQualFilter";
	} else if ($groupBy == "Opposition") {
	    $sql = "select (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, sum(a.runs) as sumRuns, sum(a.runs) * 1.0/(count(a.runs) - sum(a.notOut)) as battingAverage, sum(a.wkts) as sumWkts, (sum(a.bowlRuns) * 1.0 / sum(a.wkts)) as bowlingAverage, avg(a.rating) as avgRtg, count(a.".$matchFormatLower."Id) as numMat from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by opposition $resultQualFilter";
	} else {
	    $sql = "select a.player, a.runs as sumRuns, a.notOut, a.wkts as sumWkts, a.bowlRuns, a.rating as avgRtg from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter $resultQualFilter limit 5000";
	}
    }
} else if ($batBowl == "fielding") {
    if ($groupBy == "Player") {
	$sql = "select a.player, sum(a.catches) as sumCatches, sum(a.droppedCatches) as droppedCatches, (sum(a.droppedCatches) * 1.0 / (sum(a.droppedCatches) + sum(a.catches))) as dropRate, sum(a.greatCatches) as sumGreatCatches, sum(a.directHits) as sumDirectHits, sum(a.runsSaved) as sumRunsSaved, avg(a.rating) avgRtg, count(t.".$matchFormatLower."Id) as numInn from fielding".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate  $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by a.playerId $resultQualFilter";
    } else if ($groupBy == "Ground") {
	$sql = "select t.ground, sum(a.catches) as sumCatches, sum(a.droppedCatches) as droppedCatches, (sum(a.droppedCatches) * 1.0 / (sum(a.droppedCatches) + sum(a.catches))) as dropRate, sum(a.greatCatches) as sumGreatCatches, sum(a.directHits) as sumDirectHits, sum(a.runsSaved) as sumRunsSaved, avg(a.rating) avgRtg, count(t.".$matchFormatLower."Id) as numInn from fielding".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate  $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by t.ground $resultQualFilter";
    }  else if ($groupBy == "Opposition") {
	$sql = "select (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, sum(a.catches) as sumCatches, sum(a.droppedCatches) as droppedCatches, (sum(a.droppedCatches) * 1.0 / (sum(a.droppedCatches) + sum(a.catches))) as dropRate, sum(a.greatCatches) as sumGreatCatches, sum(a.directHits) as sumDirectHits, sum(a.runsSaved) as sumRunsSaved, avg(a.rating) avgRtg, count(t.".$matchFormatLower."Id) as numInn from fielding".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate  $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by opposition $resultQualFilter";
    } else {
	$sql = "select a.player, a.catches as sumCatches, a.droppedCatches as droppedCatches, a.greatCatches as sumGreatCatches, a.directHits as sumDirectHits, a.runsSaved as sumRunsSaved, a.rating as avgRtg from fielding".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter $resultQualFilter limit 5000";
    }
} else if ($batBowl == "winShares") {
    if ($groupBy == "Player") {
	$sql = "select a.player, avg(a.battingAdjWS) as avgBattingWS, avg(a.bowlingAdjWS) as avgBowlingWS, avg(a.fieldingAdjWS) as avgFieldingWS, avg(a.totalAdjWS) as avgRtg, count(t.".$matchFormatLower."Id) as numInn from winShares".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by a.playerId $resultQualFilter";
    } else if ($groupBy == "Ground") {
	$sql = "select t.ground, avg(a.battingAdjWS) as avgBattingWS, avg(a.bowlingAdjWS) as avgBowlingWS, avg(a.fieldingAdjWS) as avgFieldingWS, avg(a.totalAdjWS) as avgRtg, count(t.".$matchFormatLower."Id) as numInn from winShares".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by t.ground $resultQualFilter";
    }  else if ($groupBy == "Opposition") {
	$sql = "select (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, avg(a.battingAdjWS) as avgBattingWS, avg(a.bowlingAdjWS) as avgBowlingWS, avg(a.fieldingAdjWS) as avgFieldingWS, avg(a.totalAdjWS) as avgRtg, count(t.".$matchFormatLower."Id) as numInn from winShares".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter group by opposition $resultQualFilter";
    } else {
	$sql = "select a.player, a.battingAdjWS as avgBattingWS, a.bowlingAdjWS as avgBowlingWS, a.fieldingAdjWS as avgFieldingWS, a.totalAdjWS as avgRtg from winShares".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $batFieldFirstFilter $homeAwayFilter $hostFilter $groundFilter $inningsFilter $resultQualFilter limit 5000";
    }
}

//echo $sql;
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");

$k = 0;
$players = array();
$histVals = array();
$teams = array();
$ratings = array();
while($res = $result->fetchArray(SQLITE3_NUM)) {        
    $histKey = 1;
    $roundHistKey = 0;
    if ($batBowl == "batting") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	    if ($res[6] == 0) { continue; }
	    if ($histVal == "average") {
		$histKey = 1;
		$roundHistKey = 2;
	    } else if ($histVal == "strikeRate") {
		$histKey = 2;
		$roundHistKey = 2;
	    } else if ($histVal == "runs") {
		$histKey = 3;
		$roundHistKey = 0;
	    } else if ($histVal == "rating") {
		$histKey = 4;
		$roundHistKey = 0;
	    } else if ($histVal == "innings") {
		$histKey = 5;
		$roundHistKey = 0;
	    }
	} else {
	    if ($histVal == "runs") {
		$histKey = 1;
		$roundHistKey = 0;
	    } else if ($histVal == "strikeRate") {
		$histKey = 2;
		$roundHistKey = 2;
	    } else if ($histVal == "balls") {
		$histKey = 3;
		$roundHistKey = 0;
	    } else if ($histVal == "rating") {
		$histKey = 4;
		$roundHistKey = 0;
	    }
	}
    } else if ($batBowl == "bowling") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	    if ($res[6] == 0) { continue; }
	    if ($histVal == "average") {
		$histKey = 1;
		$roundHistKey = 2;
	    } else if ($histVal == "strikeRate") {
		$histKey = 2;
		$roundHistKey = 1;
	    } else if ($histVal == "econRate") {
		$histKey = 3;
		$roundHistKey = 2;
	    } else if ($histVal == "balls") {
		$histKey = 4;
		$roundHistKey = 0;
	    } else if ($histVal == "runs") {
		$histKey = 5;
		$roundHistKey = 0;
	    } else if ($histVal == "wickets") {
		$histKey = 6;
		$roundHistKey = 0;
	    } else if ($histVal == "rating") {
		$histKey = 7;
		$roundHistKey = 0;
	    } else if ($histVal == "innings") {
		$histKey = 8;
		$roundHistKey = 0;
	    }
	} else {
	    if ($histVal == "wickets") {
		$histKey = 1;
		$roundHistKey = 0;
	    } else if ($histVal == "balls") {
		$histKey = 2;
		$roundHistKey = 0;
	    } else if ($histVal == "runs") {
		$histKey = 3;
		$roundHistKey = 0;
	    } else if ($histVal == "rating") {
		$histKey = 4;
		$roundHistKey = 0;
	    }
	}
    } else if ($batBowl == "allRound") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	    if ($res[2] == 0 || $res[4] == 0) { continue; }
	    if ($histVal == "battingAverage") {
		$histKey = 2;
		$roundHistKey = 2;
	    } else if ($histVal == "bowlingAverage") {
		$histKey = 4;
		$roundHistKey = 2;
	    } else if ($histVal == "runs") {
		$histKey = 1;
		$roundHistKey = 0;
	    } else if ($histVal == "wickets") {
		$histKey = 3;
		$roundHistKey = 0;
	    } else if ($histVal == "rating") {
		$histKey = 5;
		$roundHistKey = 0;
	    } else if ($histVal == "matches") {
		$histKey = 6;
		$roundHistKey = 0;
	    }
	} else {
	    if ($matchFormat == "Test") {
		if ($histVal == "wickets") {
		    $histKey = 11;
		    $roundHistKey = 0;
		} else if ($histVal == "runs") {
		    $histKey = 10;
		    $roundHistKey = 0;
		} else if ($histVal == "rating") {
		    $histKey = 9;
		    $roundHistKey = 0;
		}
	    } else {
		if ($histVal == "wickets") {
		    $histKey = 3;
		    $roundHistKey = 0;
		} else if ($histVal == "runs") {
		    $histKey = 1;
		    $roundHistKey = 0;
		} else if ($histVal == "rating") {
		    $histKey = 5;
		    $roundHistKey = 0;
		}
	    }	    
	}
    } else if ($batBowl == "fielding") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	    if ($res[1] == 0) { continue; }
	    if ($histVal == "dropRate") {
		$histKey = 3;
		$roundHistKey = 2;
	    } else if ($histVal == "catches") {
		$histKey = 1;
		$roundHistKey = 0;
	    } else if ($histVal == "droppedCatches") {
		$histKey = 2;
		$roundHistKey = 0;
	    } else if ($histVal == "greatCatches") {
		$histKey = 4;
		$roundHistKey = 0;
	    } else if ($histVal == "directHits") {
		$histKey = 5;
		$roundHistKey = 0;
	    } else if ($histVal == "runsSaved") {
		$histKey = 6;
		$roundHistKey = 0;
	    } else if ($histVal == "rating") {
		$histKey = 7;
		$roundHistKey = 0;
	    } else if ($histVal == "innings") {
		$histKey = 8;
		$roundHistKey = 0;
	    }
	} else {
	    if ($histVal == "catches") {
		$histKey = 1;
		$roundHistKey = 0;
	    } else if ($histVal == "droppedCatches") {
		$histKey = 2;
		$roundHistKey = 0;
	    } else if ($histVal == "greatCatches") {
		$histKey = 3;
		$roundHistKey = 0;
	    } else if ($histVal == "directHits") {
		$histKey = 4;
		$roundHistKey = 0;
	    } else if ($histVal == "runsSaved") {
		$histKey = 5;
		$roundHistKey = 0;
	    } else if ($histVal == "rating") {
		$histKey = 6;
		$roundHistKey = 0;
	    }
	}
    } else if ($batBowl == "winShares") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	    if ($histVal == "battingWSAvg") {
		$histKey = 1;
		$roundHistKey = 3;
	    } else if ($histVal == "bowlingWSAvg") {
		$histKey = 2;
		$roundHistKey = 3;
	    } else if ($histVal == "fieldingWSAvg") {
		$histKey = 3;
		$roundHistKey = 3;
	    } else if ($histVal == "totalWSAvg") {
		$histKey = 4;
		$roundHistKey = 3;
	    } else if ($histVal == "innings") {
		$histKey = 5;
		$roundHistKey = 0;
	    }
	} else {
	    if ($histVal == "battingWS") {
		$histKey = 1;
		$roundHistKey = 3;
	    } else if ($histVal == "bowlingWS") {
		$histKey = 2;
		$roundHistKey = 3;
	    } else if ($histVal == "fieldingWS") {
		$histKey = 3;
		$roundHistKey = 3;
	    } else if ($histVal == "totalWS") {
		$histKey = 4;
		$roundHistKey = 3;
	    }
	}
    }
        
    array_push($players, $res[0]);
    array_push($histVals, round($res[$histKey], $roundHistKey));
}

$table = array();
$table['cols'] = array(
                        array('id' => "", 'label' => "Player/Ground/Opposition", 'pattern' => "", 'type' => 'string'),
                        array('id' => "", 'label' => $histValMod[$histVal], 'pattern' => "", 'type' => 'number'),                      
                    );

$rows = array();

for ($i = 0; $i < count($histVals); $i++) {
    $temp = array();
    $temp[] = array('v' => $players[$i]);
    $temp[] = array('v' => $histVals[$i]);
    $rows[] = array('c' => $temp);  
} 

$table['rows'] = $rows;
$jsonTable = json_encode($table);
echo $jsonTable;
?>