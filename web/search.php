<?php

$searchTerm = $_GET["search"];

$db = new SQLite3('ccr.db');
$sql = "select playerId, count(playerId) from playerInfo where player like \"%".$searchTerm."%\"";
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");
$res = $result->fetchArray(SQLITE3_NUM);
$multiplePlayers = false;

if (!empty($res)) {
    if ($res[1] == 1) {
	$playerId = $res[0];
	header("Location: player.php?playerId=".$playerId."&matchFormat=Test");
	die();
    } else if ($res[1] > 1) {
	$multiplePlayers = true;
    }
}

if ($multiplePlayers == false) {
    $sql = "select distinct team from teamTestOverall where team like '%".$searchTerm."%'";
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    $res = $result->fetchArray(SQLITE3_NUM);
    if (!empty($res)) {
	if (!strstr($res[0], "XI")) {
	    $team = $res[0];
	    header("Location: team.php?team=".$team."&matchFormat=Test");
	    die();
	}
    }
}
$db->close();

if ($multiplePlayers == false) {
    $db = new SQLite3('ccrODI.db');
    $sql = "select playerId, count(playerId) from playerInfo where player like '%".$searchTerm."%'";
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    $res = $result->fetchArray(SQLITE3_NUM);

    if (!empty($res)) {
	if ($res[1] == 1) {
	    $playerId = $res[0];
	    header("Location: player.php?playerId=".$playerId."&matchFormat=ODI");
	    die();
	} else if ($res[1] > 1) {
	    $multiplePlayers = true;
	}
    }

    $sql = "select distinct team from teamODIOverall where team like '%".$searchTerm."%'";
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    $res = $result->fetchArray(SQLITE3_NUM);

    if (!empty($res)) {
	if (!strstr($res[0], "XI")) {
	    $team = $res[0];
	    header("Location: team.php?team=".$team."&matchFormat=ODI");
	    die();
	}
    }
    $db->close();
}

if ($multiplePlayers == false) {
    $db = new SQLite3('ccrT20I.db');
    $sql = "select playerId, count(playerId) from playerInfo where player like '%".$searchTerm."%'";
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    $res = $result->fetchArray(SQLITE3_NUM);

    if (!empty($res)) {
	if ($res[1] == 1) {
	    $playerId = $res[0];
	    header("Location: player.php?playerId=".$playerId."&matchFormat=T20I");
	    die();
	}
    }

    $sql = "select distinct team from teamT20IOverall where team like '%".$searchTerm."%'";
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    $res = $result->fetchArray(SQLITE3_NUM);

    if (!empty($res)) {
	if (!strstr($res[0], "XI")) {
	    $team = $res[0];
	    header("Location: team.php?team=".$team."&matchFormat=T20I");
	    die();
	}
    }
    $db->close();
}

if ($multiplePlayers == false) {
    $db = new SQLite3('ccrFT20.db');
    $sql = "select playerId, count(playerId) from playerInfo where player like '%".$searchTerm."%'";
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    $res = $result->fetchArray(SQLITE3_NUM);

    if (!empty($res)) {
	if ($res[1] == 1) {
	    $playerId = $res[0];
	    header("Location: player.php?playerId=".$playerId."&matchFormat=FT20");
	    die();
	}
    }

    $sql = "select distinct team from teamFT20Overall where team like '%".$searchTerm."%'";
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    $res = $result->fetchArray(SQLITE3_NUM);

    if (!empty($res)) {
	if (!strstr($res[0], "XI")) {
	    $team = $res[0];
	    header("Location: team.php?team=".$team."&matchFormat=FT20");
	    die();
	}
    }
    $db->close();
}
?>

<html>
<head>
    <title>cricrate | Search</title>
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
                    <li><a href="cricinsight.php"><b>cricinsight</b></a></li>
		                <li><a href="cricodds.php"><b>cricodds <span class="label label-warning">new</span></b></a></li>
                    <li><a href="about.php">About</a></li>
                </ul>
                <div class="twitter navbar-text pull-right"><a href="https://twitter.com/cricrate" class="twitter-follow-button" data-show-count="false" data-show-screen-name="false">Follow @cricrate</a></div>
                <div class="fb-like navbar-text pull-right" data-href="https://www.facebook.com/cricrate" data-layout="button" data-action="like" data-show-faces="true" data-share="false"></div>
            </div>
        </div>
    </nav>

    <div class="container">
    <div class="panel panel-default">
    <div class="panel-body">
<?php

echo "<h2><b>Search Results</b></h2><br/>";

$searchTerm = $_GET["search"];

$db = new SQLite3('ccr.db');
$sql = "select distinct team from teamTestOverall where team like \"%".$searchTerm."%\"";
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");

$teamCount = 0;
$teamsFound = array();
echo "<h4><b>Teams</b></h4><br/>";
echo "<ul>";
while($res = $result->fetchArray(SQLITE3_NUM)) {
    if (!strstr($res[0], "XI")) {
	echo "<li><a href=\"team.php?team=".$res[0]."\"><img src=\"images/".$res[0].".png\" alt=\"$res[0]\" style='border:1px solid #A9A9A9'/></a>&nbsp;&nbsp;&nbsp;<a href=\"team.php?team=".$res[0]."\">".$res[0]."</a></li>";
	$teamsFound[$res[0]] = 1;
	$teamCount++;
    }
}
$db->close();

$db = new SQLite3('ccrODI.db');
$sql = "select distinct team from teamODIOverall where team like \"%".$searchTerm."%\"";
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");
while($res = $result->fetchArray(SQLITE3_NUM)) {
    if (array_key_exists($res[0], $teamsFound) || strstr($res[0], "XI")) {
	continue;
    }
    echo "<li><a href=\"team.php?team=".$res[0]."\"><img src=\"images/".$res[0].".png\" alt=\"$res[0]\" style='border:1px solid #A9A9A9'/></a>&nbsp;&nbsp;&nbsp;<a href=\"team.php?team=".$res[0]."\">".$res[0]."</a></li>";
    $teamsFound[$res[0]] = 1;
    $teamCount++;
}
$db->close();

$db = new SQLite3('ccrT20I.db');
$sql = "select distinct team from teamT20IOverall where team like \"%".$searchTerm."%\"";
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");
while($res = $result->fetchArray(SQLITE3_NUM)) {
    if (array_key_exists($res[0], $teamsFound) || strstr($res[0], "XI")) {
	continue;
    }
    echo "<li><a href=\"team.php?team=".$res[0]."\"><img src=\"images/".$res[0].".png\" alt=\"$res[0]\" style='border:1px solid #A9A9A9'/></a>&nbsp;&nbsp;&nbsp;<a href=\"team.php?team=".$res[0]."\">".$res[0]."</a></li>";
    $teamsFound[$res[0]] = 1;
    $teamCount++;
}
$db->close();

$db = new SQLite3('ccrFT20.db');
$sql = "select distinct team from teamFT20Overall where team like \"%".$searchTerm."%\"";
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");
while($res = $result->fetchArray(SQLITE3_NUM)) {
    if (array_key_exists($res[0], $teamsFound) || strstr($res[0], "XI")) {
	continue;
    }
    echo "<li><a href=\"team.php?team=".$res[0]."\">".$res[0]."</a></li>";
    $teamsFound[$res[0]] = 1;
    $teamCount++;
}
$db->close();
echo "</ul>";
echo "</ul>";

if ($teamCount == 0) {
    echo "No matching team found.";
}

echo "<br/><br/><h4><b>Players</b></h4><br/>";
$db = new SQLite3('ccr.db');
$sql = "select playerId, player, country from playerInfo where player like \"%".$searchTerm."%\"";
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");

$playerCount = 0;
$playersFound = array();
echo "<ul>";
while($res = $result->fetchArray(SQLITE3_NUM)) {
    echo "<li><img src=\"images/".$res[2].".png\" alt=\"$res[2]\" style='border:1px solid #A9A9A9'/>&nbsp;&nbsp;&nbsp;<a href=\"player.php?playerId=".$res[0]."\">".str_replace("Sir ","",$res[1])."</a></li>";
    $playersFound[$res[0]] = 1;
    $playerCount++;
}

$db = new SQLite3('ccrODI.db');
$sql = "select playerId, player, country from playerInfo where player like \"%".$searchTerm."%\"";
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");

while($res = $result->fetchArray(SQLITE3_NUM)) {
    if (array_key_exists($res[0], $playersFound)) {
	continue;
    }
    echo "<li><img src=\"images/".$res[2].".png\" alt=\"$res[2]\" style='border:1px solid #A9A9A9'/>&nbsp;&nbsp;&nbsp;<a href=\"player.php?playerId=".$res[0]."\">".str_replace("Sir ","",$res[1])."</a></li>";
    $playersFound[$res[0]] = 1;
    $playerCount++;
}
$db->close();

$db = new SQLite3('ccrT20I.db');
$sql = "select playerId, player, country from playerInfo where player like \"%".$searchTerm."%\"";
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");

while($res = $result->fetchArray(SQLITE3_NUM)) {
    if (array_key_exists($res[0], $playersFound)) {
	continue;
    }
    echo "<li><img src=\"images/".$res[2].".png\" alt=\"$res[2]\" style='border:1px solid #A9A9A9'/>&nbsp;&nbsp;&nbsp;<a href=\"player.php?playerId=".$res[0]."\">".str_replace("Sir ","",$res[1])."</a></li>";
    $playersFound[$res[0]] = 1;
    $playerCount++;
}
$db->close();

$db = new SQLite3('ccrFT20.db');
$sql = "select playerId, player from playerInfo where player like \"%".$searchTerm."%\"";
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");

while($res = $result->fetchArray(SQLITE3_NUM)) {
    if (array_key_exists($res[0], $playersFound)) {
	continue;
    }
    echo "<li><a href=\"player.php?playerId=".$res[0]."\">".str_replace("Sir ","",$res[1])."</a></li>";
    $playersFound[$res[0]] = 1;
    $playerCount++;
}
$db->close();
echo "</ul>";

if ($playerCount == 0) {
    echo "No matching player found.<br/><br/>";
}
echo "</div>";
?>
</div>
</div>
</div>
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
