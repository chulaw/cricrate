<!DOCTYPE html>
<html>
<head>
    <?php    
        $matchId = $_GET["matchId"];
        $matchFormat = $_GET["matchFormat"];  
        echo "<title>cricrate | $matchFormat #".$matchId."</title>";
    ?>
    <link rel="icon" href="images/cricrate.png" /> 
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link type="text/css" href="style.css" />
    <link href="css/bootstrap.css" rel="stylesheet">
    <link href="css/jquery-ui.css" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="style.css" />
    <script src="//code.jquery.com/jquery-1.12.0.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
    <script type="text/javascript">
    $(function() {        
        jQuery.get('searchSuggest.txt', function(data) {
            var autoSuggest = data.split('\n');
            $( "#search" ).autocomplete({
                source: autoSuggest,
                minLength: 3,
            });
        });            
      });
    </script>
</head>    
<body>
    <nav class="navbar navbar-default navbar-static-top">
        <div class="container-fluid">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="index.php"><b>cricrate</b></a>
            </div>        
            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <form class="navbar-form navbar-right" role="search"  name="input" action="search.php" method="get">
                    <div class="form-group">
                        <div class="ui-front ui-widget">
                            <input id="search" type="text" class="form-control" placeholder="Search" name="search">
                        </div>
                    </div>                
                    <button type="submit" class="btn btn-default">Submit</button>
                </form>
                <ul class="nav navbar-nav navbar">
                    <li><a href="index.php">Home</a></li>
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Team <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="methodology.php?matchFormat=Test&disc=Team"><b>Test</b></a></li>
                            <li><a href="current.php?matchFormat=Test&disc=Team">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=Test&disc=Team">&nbsp;&nbsp;Overall</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=ODI&disc=Team"><b>ODI</b></a></li>
                            <li><a href="current.php?matchFormat=ODI&disc=Team">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=ODI&disc=Team">&nbsp;&nbsp;Overall</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=T20I&disc=Team"><b>T20I</b></a></li>
                            <li><a href="current.php?matchFormat=T20I&disc=Team">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=T20I&disc=Team">&nbsp;&nbsp;Overall</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=Team"><b>FT20</b></a></li>
                            <li><a href="current.php?matchFormat=FT20&disc=Team">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=FT20&disc=Team">&nbsp;&nbsp;Overall</a></li>
                        </ul>
                    </li>
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Batting <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="methodology.php?matchFormat=Test&disc=Batting"><b>Test</b></a></li>
                            <li><a href="current.php?matchFormat=Test&disc=Batting">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=Test&disc=Batting">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=Test&disc=Batting">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=ODI&disc=Batting"><b>ODI</b></a></li>
                            <li><a href="current.php?matchFormat=ODI&disc=Batting">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=ODI&disc=Batting">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=ODI&disc=Batting">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=T20I&disc=Batting"><b>T20I</b></a></li>
                            <li><a href="current.php?matchFormat=T20I&disc=Batting">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=T20I&disc=Batting">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=T20I&disc=Batting">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=Batting"><b>FT20</b></a></li>
                            <li><a href="current.php?matchFormat=FT20&disc=Batting">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=FT20&disc=Batting">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=FT20&disc=Batting">&nbsp;&nbsp;Performances</a></li>
                        </ul>
                    </li>
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Bowling <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="methodology.php?matchFormat=Test&disc=Bowling"><b>Test</b></a></li>
                            <li><a href="current.php?matchFormat=Test&disc=Bowling">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=Test&disc=Bowling">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=Test&disc=Bowling">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=ODI&disc=Bowling"><b>ODI</b></a></li>
                            <li><a href="current.php?matchFormat=ODI&disc=Bowling">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=ODI&disc=Bowling">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=ODI&disc=Bowling">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=T20I&disc=Bowling"><b>T20I</b></a></li>
                            <li><a href="current.php?matchFormat=T20I&disc=Bowling">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=T20I&disc=Bowling">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=T20I&disc=Bowling">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=Bowling"><b>FT20</b></a></li>
                            <li><a href="current.php?matchFormat=FT20&disc=Bowling">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=FT20&disc=Bowling">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=FT20&disc=Bowling">&nbsp;&nbsp;Performances</a></li>
                        </ul>
                    </li>
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">All-Round <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="methodology.php?matchFormat=Test&disc=All-Round"><b>Test</b></a></li>
                            <li><a href="current.php?matchFormat=Test&disc=All-Round">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=Test&disc=All-Round">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=Test&disc=All-Round">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=ODI&disc=All-Round"><b>ODI</b></a></li>
                            <li><a href="current.php?matchFormat=ODI&disc=All-Round">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=ODI&disc=All-Round">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=ODI&disc=All-Round">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=T20I&disc=All-Round"><b>T20I</b></a></li>
                            <li><a href="current.php?matchFormat=T20I&disc=All-Round">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=T20I&disc=All-Round">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=T20I&disc=All-Round">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=All-Round"><b>FT20</b></a></li>
                            <li><a href="current.php?matchFormat=FT20&disc=All-Round">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=FT20&disc=All-Round">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=FT20&disc=All-Round">&nbsp;&nbsp;Performances</a></li>
                        </ul>
                    </li>
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Fielding <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="methodology.php?matchFormat=Test&disc=Fielding"><b>Test</b></a></li>
                            <li><a href="current.php?matchFormat=Test&disc=Fielding">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=Test&disc=Fielding">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=Test&disc=Fielding">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=ODI&disc=Fielding"><b>ODI</b></a></li>
                            <li><a href="current.php?matchFormat=ODI&disc=Fielding">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=ODI&disc=Fielding">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=ODI&disc=Fielding">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=Fielding"><b>FT20</b></a></li>
                            <li><a href="current.php?matchFormat=FT20&disc=Fielding">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=FT20&disc=Fielding">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=FT20&disc=Fielding">&nbsp;&nbsp;Performances</a></li>
                        </ul>
                    </li>
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Win Shares <span class="caret"></span></a>
                        <ul class="dropdown-menu">                  
                            <li><a href="methodology.php?matchFormat=ODI&disc=Win Shares"><b>ODI</b></a></li>
                            <li><a href="current.php?matchFormat=ODI&disc=Win Shares">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=ODI&disc=Win Shares">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=ODI&disc=Win Shares">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=Win Shares"><b>FT20</b></a></li>
                            <li><a href="current.php?matchFormat=FT20&disc=Win Shares">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=FT20&disc=Win Shares">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=FT20&disc=Win Shares">&nbsp;&nbsp;Performances</a></li>
                        </ul>
                    </li>
                    <li><a href="cricinsight.php"><b>cricinsight <span class="label label-warning">new</span></b></a></li>
                    <li><a href="about.php">About</a></li>
                </ul>
                <div class="twitter navbar-text pull-right"><a href="https://twitter.com/cricrate" class="twitter-follow-button" data-show-count="false" data-show-screen-name="false">Follow @cricrate</a></div>
                <div class="fb-like navbar-text pull-right" data-href="https://www.facebook.com/cricrate" data-layout="button" data-action="like" data-show-faces="true" data-share="false"></div>
            </div>
        </div>
    </nav>
    
<?php

$matchFormatLower = strtolower($matchFormat);
$dbName = "ccr.db";
if ($matchFormat == "ODI") {
    $dbName = "ccrODI.db";
} elseif ($matchFormat == "T20I") {
    $dbName = "ccrT20I.db";
} elseif ($matchFormat == "FT20") {
    $dbName = "ccrFT20.db";
}
$db = new SQLite3($dbName);
if ($matchFormat == "Test" || $matchFormat == "ODI") {
    $sql = "select startDate, team1, team2, season, ground, result, margin, series, ballsPerOver from ".$matchFormatLower."Info where ".$matchFormatLower."Id=".$matchId;   
} else {
    $sql = "select startDate, team1, team2, season, ground, result, margin, series from ".$matchFormatLower."Info where ".$matchFormatLower."Id=".$matchId;   
} 
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");
$res = $result->fetchArray(SQLITE3_NUM);

function inningsTable($db, $matchId, $innings, $bpo, $batInnNum, $target, $matchFormat) {
    $matchFormatLower = strtolower($matchFormat);
    $sql = "select batTeam, bowlTeam, extras, runs, balls, minutes, wickets, inningsEndDetail from details".$matchFormat."Innings where ".$matchFormatLower."Id=".$matchId." and innings=".$innings;
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    $det = $result->fetchArray(SQLITE3_NUM);    

    $sql = "select playerId, player, dismissalInfo, runs, minutes, balls, fours, sixes, rating from batting".$matchFormat."Innings where ".$matchFormatLower."Id=".$matchId." and innings=".$innings." order by position asc";
    $result = $db->query($sql);    
    if (!$result) die("Cannot execute query.");
    echo "<table class=\"table\" id=\"battingTable\">";
    echo "<thead><tr>";
    if ($batInnNum == 1) {
        if ($matchFormat == "FT20") {
            echo "<th><a href=\"team.php?team=".$det[0]."&matchFormat=$matchFormat\"><b>".$det[0]."</a> 1st Innings</b></th>";
        } else {
            echo "<th><a href=\"team.php?team=".$det[0]."&matchFormat=$matchFormat\"><img src=\"images/".$det[0].".png\" alt=\"".$det[0]."\" border=1px/></a>&nbsp; <b>".$det[0]." 1st Innings</b></th>";   
        }	
    } else {
	if ($innings == 4) {
	    echo "<th><a href=\"team.php?team=".$det[0]."&matchFormat=$matchFormat\"><img src=\"images/".$det[0].".png\" alt=\"".$det[0]."\" border=1px/></a>&nbsp; <b>".$det[0]." 2nd Innings</b> (Target: ".$target." runs)</th>";
	} else {
            if ($matchFormat == "FT20") {
                echo "<th><a href=\"team.php?team=".$det[0]."&matchFormat=$matchFormat\"><b>".$det[0]."</a> 2nd Innings</b></th>";
            } else {
                echo "<th><a href=\"team.php?team=".$det[0]."&matchFormat=$matchFormat\"><img src=\"images/".$det[0].".png\" alt=\"".$det[0]."\" border=1px/></a>&nbsp; <b>".$det[0]." 2nd Innings</b></th>";
            }
	}	
    }
    echo "<th></th>";
    echo "<th>R</th>";
    echo "<th>M</th>";
    echo "<th>B</th>";
    echo "<th>4</th>"; 
    echo "<th>6</th>";
    echo "<th>SR</th>";
    echo "<th>Rating</th>";    
    echo "</tr></thead>";
    while($batInn = $result->fetchArray(SQLITE3_NUM)) {
	echo "<tr>";
	for ($j = 0; $j < $result->numColumns(); $j++) {
	    if ($j == 0) { # batsman info
		echo "<td><a href=\"player.php?playerId=".$batInn[0]."&matchFormat=".$matchFormat."&disc=Batting\">".str_replace("Sir ","",$batInn[1])."</a></td>";
		$j++;
	    } elseif ($j == 2) { # dismissal info		 
		echo "<td>".str_replace("â€","",$batInn[2])."</td>";
	    } elseif ($j == 3) { # runs
		echo "<td><b>".$batInn[3]."</b></td>";
	    } elseif ($j == 7) { # sixes + sr
		echo "<td>".$batInn[7]."</td>";
		if ($batInn[5] > 0) {
		    $sr = 100 * $batInn[3] / $batInn[5];		    
		    echo "<td>".number_format(round($sr, 2), 2)."</td>";
		} else {
		    echo "<td></td>";
		}
	    } elseif ($j == 8) { # rating
		echo "<td><b>".round($batInn[8], 0)."</b></td>";
	    } else {
		echo "<td>$batInn[$j]</td>";
	    }        
	}	
	echo "</tr>";
    }    
    $balls = $det[4] % $bpo;
    $overs = ($det[4]-$balls) / $bpo;
    if ($det[5] > 0) {
	$mins = $det[5];
    } else {
	$mins = "";
    } 
    if ($bpo == 6) {
	$totOvers = $overs.".".$balls;
    } else {
	$totOvers = $overs.".".$balls."x".$bpo;
    }
    if ($det[4] > 0) {
	$totEcon = 6 * $det[3] / $det[4];
	$totEconHtml = number_format(round($totEcon, 2), 2)." rpo";
    } else {
	$totEconHtml = "";
    }
    echo "<tr><td>Extras</td><td></td><td>".$det[2]."</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>"; #extras
    echo "<tr><td><b>Total</b></td><td>".$det[7].", ".$totOvers." overs, $totEconHtml</td><td><b>".$det[3]."</b></td><td>".$mins."</td><td></td><td></td><td></td><td></td><td></td></tr>";
    echo "</table>";
    
    $sql = "select wicket, runs, player, balls from fow".$matchFormat."Innings where ".$matchFormatLower."Id=".$matchId." and innings=".$innings;
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    
    echo "<div id='fowScorecard'><b>Fall of wickets</b><br/>";
    $fowInfo = "";
    $fowCount = 0;
    while($fow = $result->fetchArray(SQLITE3_NUM)) {	
	$fowInfo .= $fow[0]."-".$fow[1]." (".$fow[2];
	if (!empty($fow[3])) {
	    $balls = $fow[3] % $bpo;
	    $overs = ($fow[3]-$balls) / $bpo;
	    if ($bpo == 6) {
		$fowOvers = $overs.".".$balls;
	    } else {
		$fowOvers = $overs.".".$balls."x".$bpo;
	    }
	    $fowInfo .= ", ".$fowOvers." ov), ";
	} else {
	    $fowInfo .= "), ";
	}
	$fowCount++;
    }
    echo substr($fowInfo, 0, -2);
    echo "</div><br/>";

    $sql = "select playerId, player, balls, maidens, runs, wkts, rating from bowling".$matchFormat."Innings where ".$matchFormatLower."Id=".$matchId." and innings=".$innings." order by position asc";
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    echo "<table class=\"table\" id=\"bowlingTable\">";
    echo "<thead><tr>";
    echo "<th>Bowling</th>";
    echo "<th>O</th>";
    echo "<th>M</th>";
    echo "<th>R</th>";
    echo "<th>W</th>";
    echo "<th>Econ</th>";     
    echo "<th>Rating</th>";    
    echo "</tr></thead>";
    while($bowlInn = $result->fetchArray(SQLITE3_NUM)) {
	echo "<tr>";
	for ($j = 0; $j < $result->numColumns(); $j++) {
	    if ($j == 0) { # bowler info
		echo "<td><a href=\"player.php?playerId=".$bowlInn[0]."&matchFormat=".$matchFormat."&disc=Bowling\">".str_replace("Sir ","",$bowlInn[1])."</a></td>";
		$j++;
	    } elseif ($j == 2) { # overs
                $balls = $bowlInn[2] % $bpo;
                $overs = ($bowlInn[2]-$balls) / $bpo;
                if ($bpo == 6) {
                    echo "<td>".$overs.".".$balls."</td>";
                } else {
                    echo "<td>".$overs.".".$balls."x".$bpo."</td>";
                }
	    } elseif ($j == 5) { # runs + econ
		echo "<td>".$bowlInn[5]."</td>";
		if ($bowlInn[2] > 0) {
		    $econ = 6 * $bowlInn[4] / $bowlInn[2];
		    echo "<td>".number_format(round($econ, 2), 2)."</td>";
		} else {
		    echo "<td></td>";
		}		
	    } elseif ($j == 6) { # rating
		echo "<td><b>".round($bowlInn[6], 0)."</b></td>";
	    } else {
		echo "<td>$bowlInn[$j]</td>";
	    }        
	}	
	echo "</tr>";
    }
    echo "</table><br/>";
}

echo "<div class=\"panel panel-inverse\">";
echo "<div class=\"panel-body\">";

if ($res[0] > 0) {
    echo "<h2><b>".$res[7].", ".$res[3]."</b></h2>";
    echo "<h4>$matchFormat #".$matchId.", <a href=\"team.php?team=".$res[1]."&matchFormat=$matchFormat\">".$res[1]."</a> v <a href=\"team.php?team=".$res[2]."&matchFormat=$matchFormat\">".$res[2]."</a> at ".$res[4].", ".substr($res[0], 0, 4)."-".substr($res[0], 4, 2)."-".substr($res[0], 6, 2)."</h4>";
    if ($res[5] == "Draw") {
	echo "<h4>Match drawn</h4>";   
    } else if ($res[5] == "Tie/NR") {
        echo "<h4>Tie/No Result</h4>";   
    } else {
	$margin = str_replace("inns &","an innings and",$res[6]);    
	echo "<h4>".$res[5]." won by ".$margin."</h4>";   
    }
    if ($matchFormat == "Test" || $matchFormat == "ODI") {
        $bpo = $res[8];   
    } else {
        $bpo = 6;   
    }
    $sql = "select distinct innings, batTeam, bowlTeam, runs from details".$matchFormat."Innings where ".$matchFormatLower."Id=".$matchId." order by innings asc";
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    
    $batTeamInns = array();
    $cumRuns = array();
    $target = "";    
    while($inns = $result->fetchArray(SQLITE3_NUM)) {
        if ($matchFormat == "Test") {
            if ($inns[0] == 4) {
                $target = 1 + $cumRuns[$inns[2]] - $cumRuns[$inns[1]];
            }
            if (array_key_exists($inns[1], $batTeamInns)) {
                $batTeamInns[$inns[1]]++;
                $cumRuns[$inns[1]] = $cumRuns[$inns[1]] + $inns[3];
            } else {
                $batTeamInns[$inns[1]] = 1;
                $cumRuns[$inns[1]] = $inns[3];
            }                    
        } else {
            if ($target == "") {
                $target = 1 + $inns[1];
            }
            $batTeamInns[$inns[1]] = 1;
        }                    
	
        if ($inns[0] == 1 || $inns[0] == 3) {
            echo "<div class=\"row\">";
            echo "<ul class=\"list-group\">";
        }            
        echo "<div class=\"col-lg-6\">";
        echo "<li class=\"list-group-item\">";
	inningsTable($db, $matchId, $inns[0], $bpo, $batTeamInns[$inns[1]], $target, $matchFormat);
        echo "</li>";
        echo "</div>";        
        if ($inns[0] == 2 || $inns[0] == 4) {
            echo "</ul>";
            echo "</div>";
        }
    }
} else {
    echo "<h2><b>Scorecard not found.</b></h2>";
}
echo "</div>";
echo "</div>";
?>
<div id="fb-root"></div>    
<div class="navbar navbar-default navbar-fixed-bottom">
    <div class="container">
	<p class="navbar-text">© 2014-<?php date_default_timezone_set('America/New_York'); echo date('Y'); ?> by cricrate. All rights reserved.</p>                        
    </div>
</div>    
<script>(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.5";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));</script>
<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');</script>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-50384653-1', 'auto');
  ga('send', 'pageview');

</script>
</body>
</html>