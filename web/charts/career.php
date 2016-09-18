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

if ($matchFormat == "Test") {
    if ($batBowl == "batting") {
	$xValMod = array("average"=>"Average", "runs"=>"Runs", "strikeRate"=>"Strike Rate", "fifties"=>"Fifties", "hundreds"=>"Hundreds", "rating"=>"Rating", "innings"=>"Innings", "tests"=>"Tests");
	$yValMod = array("strikeRate"=>"Strike Rate", "average"=>"Average", "runs"=>"Runs", "fifties"=>"Fifties", "hundreds"=>"Hundreds", "rating"=>"Rating", "innings"=>"Innings", "tests"=>"Tests");
    } else if ($batBowl == "bowling") {
	$xValMod = array("average"=>"Average", "runs"=>"Runs", "strikeRate"=>"Strike Rate", "balls"=>"Balls", "wickets"=>"Wickets", "econRate"=>"Econ Rate", "fiveWkts"=>"Five Wkts", "tenWkts"=>"Ten Wkts", "rating"=>"Rating", "innings"=>"Innings", "tests"=>"Tests");
	$yValMod = array("strikeRate"=>"Strike Rate", "average"=>"Average", "runs"=>"Runs", "balls"=>"Balls", "wickets"=>"Wickets", "econRate"=>"Econ Rate", "fiveWkts"=>"Five Wkts", "tenWkts"=>"Ten Wkts", "rating"=>"Rating", "innings"=>"Innings", "tests"=>"Tests");
    } else if ($batBowl == "allRound") {
	$xValMod = array("battingAverage"=>"Batting Average", "bowlingAverage"=>"Bowling Average", "runs"=>"Runs", "wickets"=>"Wickets", "hundreds"=>"Hundreds", "fiveWkts"=>"Five Wkts", "hundredFiveWkts"=>"Hundred Runs + Five Wkts", "rating"=>"Rating", "tests"=>"Tests");
	$yValMod = array("bowlingAverage"=>"Bowling Average", "battingAverage"=>"Batting Average", "runs"=>"Runs", "wickets"=>"Wickets", "hundreds"=>"Hundreds", "fiveWkts"=>"Five Wkts", "hundredFiveWkts"=>"Hundred Runs  + Five Wkts", "rating"=>"Rating", "tests"=>"Tests");
    } else if ($batBowl == "team") {
	$xValMod = array("wins"=>"Wins", "losses"=>"Losses", "draws"=>"Draws", "winPct"=>"Win %", "rating"=>"Rating", "tests"=>"Tests");
	$yValMod = array("losses"=>"Losses", "wins"=>"Wins", "draws"=>"Draws", "winPct"=>"Win %", "rating"=>"Rating", "tests"=>"Tests");
    }
} else if ($matchFormat == "ODI" || $matchFormat == "T20I" || $matchFormat == "FT20") {
    if ($batBowl == "batting") {
	$xValMod = array("average"=>"Average", "runs"=>"Runs", "strikeRate"=>"Strike Rate", "fifties"=>"Fifties", "hundreds"=>"Hundreds", "rating"=>"Rating", "innings"=>"Innings");
	$yValMod = array("strikeRate"=>"Strike Rate", "average"=>"Average", "runs"=>"Runs", "fifties"=>"Fifties", "hundreds"=>"Hundreds", "rating"=>"Rating", "innings"=>"Innings");
    } else if ($batBowl == "bowling") {
	$xValMod = array("average"=>"Average", "runs"=>"Runs", "strikeRate"=>"Strike Rate", "balls"=>"Balls", "wickets"=>"Wickets", "econRate"=>"Econ Rate", "fiveWkts"=>"Five Wkts", "threeWkts"=>"Three Wkts", "rating"=>"Rating", "innings"=>"Innings");
	$yValMod = array("strikeRate"=>"Strike Rate", "average"=>"Average", "runs"=>"Runs", "balls"=>"Balls", "wickets"=>"Wickets", "econRate"=>"Econ Rate", "fiveWkts"=>"Five Wkts", "threeWkts"=>"Three Wkts", "rating"=>"Rating", "innings"=>"Innings");
    } else if ($batBowl == "allRound") {
	if ($matchFormat == "ODI") {
	    $xValMod = array("battingAverage"=>"Batting Average", "bowlingAverage"=>"Bowling Average", "runs"=>"Runs", "wickets"=>"Wickets", "fifties"=>"Fifties", "threeWkts"=>"Three Wkts", "fiftyThreeWkts"=>"Fifty Runs + Three Wkts", "rating"=>"Rating", "odis"=>"ODIs");
	    $yValMod = array("bowlingAverage"=>"Bowling Average", "battingAverage"=>"Batting Average", "runs"=>"Runs", "wickets"=>"Wickets", "fifties"=>"Fifties", "threeWkts"=>"Five Wkts", "fiftyThreeWkts"=>"Fifty Runs + Three Wkts", "rating"=>"Rating", "odis"=>"ODIs");   
	} else if ($matchFormat == "T20I") {
	    $xValMod = array("battingAverage"=>"Batting Average", "bowlingAverage"=>"Bowling Average", "runs"=>"Runs", "wickets"=>"Wickets", "fifties"=>"Fifties", "threeWkts"=>"Three Wkts", "thirtyTwoWkts"=>"Thirty Runs + Two Wkts", "rating"=>"Rating", "t20is"=>"T20Is");
	    $yValMod = array("bowlingAverage"=>"Bowling Average", "battingAverage"=>"Batting Average", "runs"=>"Runs", "wickets"=>"Wickets", "fifties"=>"Fifties", "threeWkts"=>"Five Wkts", "thirtyTwoWkts"=>"Thirty Runs + Two Wkts", "rating"=>"Rating", "t20is"=>"T20Is");   
	} else if ($matchFormat == "FT20") {
	    $xValMod = array("battingAverage"=>"Batting Average", "bowlingAverage"=>"Bowling Average", "runs"=>"Runs", "wickets"=>"Wickets", "fifties"=>"Fifties", "threeWkts"=>"Three Wkts", "thirtyTwoWkts"=>"Thirty Runs + Two Wkts", "rating"=>"Rating", "ft20s"=>"FT20s");
	    $yValMod = array("bowlingAverage"=>"Bowling Average", "battingAverage"=>"Batting Average", "runs"=>"Runs", "wickets"=>"Wickets", "fifties"=>"Fifties", "threeWkts"=>"Five Wkts", "thirtyTwoWkts"=>"Thirty Runs + Two Wkts", "rating"=>"Rating", "ft20s"=>"FT20s");   
	}
    }  else if ($batBowl == "team") {
	if ($matchFormat == "ODI") {
	    $xValMod = array("wins"=>"Wins", "losses"=>"Losses", "draws"=>"Draws", "winPct"=>"Win %", "rating"=>"Rating", "odis"=>"ODIs");
	    $yValMod = array("losses"=>"Losses", "wins"=>"Wins", "draws"=>"Draws", "winPct"=>"Win %", "rating"=>"Rating", "odis"=>"ODIs");
	} else if ($matchFormat == "T20I") {
	    $xValMod = array("wins"=>"Wins", "losses"=>"Losses", "draws"=>"Draws", "winPct"=>"Win %", "rating"=>"Rating", "t20is"=>"T20Is");
	    $yValMod = array("losses"=>"Losses", "wins"=>"Wins", "draws"=>"Draws", "winPct"=>"Win %", "rating"=>"Rating", "t20is"=>"T20Is");
	} else if ($matchFormat == "FT20") {
	    $xValMod = array("wins"=>"Wins", "losses"=>"Losses", "draws"=>"Draws", "winPct"=>"Win %", "rating"=>"Rating", "ft20s"=>"FT20s");
	    $yValMod = array("losses"=>"Losses", "wins"=>"Wins", "draws"=>"Draws", "winPct"=>"Win %", "rating"=>"Rating", "ft20s"=>"FT20s");
	}
    }
}

$spanDates = split("-", $span);
$startSpan = $spanDates[0]."0000";
$endSpan = $spanDates[1]."9999";
if ($batBowl == "team") {
    $sql = "select ".$xVal.",".$yVal.",team, team, rating from ".$batBowl."".$matchFormat."Overall where span='".$span."' order by rating desc";
} else {
    if ($matchFormat == "FT20") {
        $sql = "select c.".$xVal.",c.".$yVal.",c.player,p.teams,c.rating from ".$batBowl."".$matchFormat."Career c, playerInfo p where p.playerId=c.playerId and ((c.startDate+c.endDate)/2)>".$startSpan." and ((c.startDate+c.endDate)/2)<=".$endSpan." order by rating desc limit 500";
    } else {
        if ($team == "All teams") {
            $sql = "select c.".$xVal.",c.".$yVal.",c.player,p.country,c.rating from ".$batBowl."".$matchFormat."Career c, playerInfo p where p.playerId=c.playerId and ((c.startDate+c.endDate)/2)>".$startSpan." and ((c.startDate+c.endDate)/2)<=".$endSpan." order by rating desc limit 500";
        } else {
            $sql = "select c.".$xVal.",c.".$yVal.",c.player,p.country,c.rating from ".$batBowl."".$matchFormat."Career c, playerInfo p where p.playerId=c.playerId and ((c.startDate+c.endDate)/2)>".$startSpan." and ((c.startDate+c.endDate)/2)<=".$endSpan." and p.country='".$team."' order by rating desc limit 100";
        }      
    }    
}

$result = $db->query($sql);
if (!$result) die("Cannot execute query.");

$k = 0;
$xVals = array();
$yVals = array();
$players = array();
$teams = array();
$ratings = array();
while($res = $result->fetchArray(SQLITE3_NUM)) {
    $roundXKey = 0;
    $roundYKey = 0;
    if ($xVal == "average" || $xVal == "strikeRate" || $xVal == "econRate" || $xVal == "battingAverage" || $xVal == "bowlingAverage" || $xVal == "winPct") {
        $roundXKey = 2;
    }
    if ($yVal == "average" || $yVal == "strikeRate" || $yVal == "econRate" || $yVal == "battingAverage" || $yVal == "bowlingAverage" || $yVal == "winPct") {
        $roundYKey = 2;
    }
    array_push($xVals, round($res[0], $roundXKey));
    array_push($yVals, round($res[1], $roundYKey));
    array_push($players, $res[2]);
    $teamMod = $res[3];
    if ($matchFormat == "FT20") {
        $fTeams = explode(",", $teamMod);
        $teamMod = trim($fTeams[0]);
    }
    array_push($teams, $teamMod);
    array_push($ratings, round($res[4], 0));
}

$table = array();
$table['cols'] = array(
                        array('id' => "", 'label' => "Player", 'pattern' => "", 'type' => 'string'),
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