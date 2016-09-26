<!DOCTYPE html>
<?php

if(isset($_GET['matchFormat'])) {
   $matchFormat = $_GET['matchFormat'];
} else {
   $matchFormat = "Test";
}
if(isset($_GET['disc'])) {
   $disc = $_GET['disc'];
} else {
   $disc = "Batting";
}

?>
<html>
<head>
    <title>cricrate | Methodology - <?php echo($matchFormat." ".$disc); ?></title>
    <link rel="icon" href="images/cricrate.png" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="css/bootstrap.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.10.11/css/dataTables.bootstrap.min.css" rel="stylesheet">
    <link href="css/jquery-ui.css" rel="stylesheet">
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script src="//code.jquery.com/jquery-1.12.0.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.11/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.11/js/dataTables.bootstrap.min.js"></script>
    <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
    <link rel="stylesheet" type="text/css" href="style.css" />
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

    submitForms = function(){
	    window.document.selectForm.submit();
	}

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
		    <?php if ($disc == "Team") { echo "<li class=\"active\">"; } else { echo "<li class=\"dropdown\">"; } ?>
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Team <span class="caret"></span></a>
                        <ul class="dropdown-menu">
			    <?php if ($disc == "Team" && $matchFormat == "Test") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=Test&disc=Team\"><b>Test</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=Test&disc=Team\"><b>Test</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=Test&disc=Team">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=Test&disc=Team">&nbsp;&nbsp;Overall</a></li>
                            <li role="separator" class="divider"></li>
			    <?php if ($disc == "Team" && $matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=ODI&disc=Team\"><b>ODI</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=ODI&disc=Team\"><b>ODI</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=ODI&disc=Team">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=ODI&disc=Team">&nbsp;&nbsp;Overall</a></li>
                            <li role="separator" class="divider"></li>
			    <?php if ($disc == "Team" && $matchFormat == "T20I") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=T20I&disc=Team\"><b>T20I</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=T20I&disc=Team\"><b>T20I</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=T20I&disc=Team">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=T20I&disc=Team">&nbsp;&nbsp;Overall</a></li>
                            <li role="separator" class="divider"></li>
			    <?php if ($disc == "Team" && $matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=FT20&disc=Team\"><b>FT20</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=FT20&disc=Team\"><b>FT20</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=FT20&disc=Team">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=FT20&disc=Team">&nbsp;&nbsp;Overall</a></li>
                        </ul>
                    </li>
                    <?php if ($disc == "Batting") { echo "<li class=\"active\">"; } else { echo "<li class=\"dropdown\">"; } ?>
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Batting <span class="caret"></span></a>
                        <ul class="dropdown-menu">
			    <?php if ($disc == "Batting" && $matchFormat == "Test") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=Test&disc=Batting\"><b>Test</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=Test&disc=Batting\"><b>Test</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=Test&disc=Batting">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=Test&disc=Batting">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=Test&disc=Batting">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <?php if ($disc == "Batting" && $matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=ODI&disc=Batting\"><b>ODI</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=ODI&disc=Batting\"><b>ODI</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=ODI&disc=Batting">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=ODI&disc=Batting">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=ODI&disc=Batting">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <?php if ($disc == "Batting" && $matchFormat == "T20I") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=T20I&disc=Batting\"><b>T20I</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=T20I&disc=Batting\"><b>T20I</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=T20I&disc=Batting">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=T20I&disc=Batting">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=T20I&disc=Batting">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <?php if ($disc == "Batting" && $matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=FT20&disc=Batting\"><b>FT20</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=FT20&disc=Batting\"><b>FT20</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=FT20&disc=Batting">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=FT20&disc=Batting">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=FT20&disc=Batting">&nbsp;&nbsp;Performances</a></li>
                        </ul>
                    </li>
                    <?php if ($disc == "Bowling") { echo "<li class=\"active\">"; } else { echo "<li class=\"dropdown\">"; } ?>
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Bowling <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <?php if ($disc == "Bowling" && $matchFormat == "Test") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=Test&disc=Bowling\"><b>Test</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=Test&disc=Bowling\"><b>Test</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=Test&disc=Bowling">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=Test&disc=Bowling">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=Test&disc=Bowling">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <?php if ($disc == "Bowling" && $matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=ODI&disc=Bowling\"><b>ODI</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=ODI&disc=Bowling\"><b>ODI</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=ODI&disc=Bowling">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=ODI&disc=Bowling">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=ODI&disc=Bowling">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <?php if ($disc == "Bowling" && $matchFormat == "T20I") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=T20I&disc=Bowling\"><b>T20I</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=T20I&disc=Bowling\"><b>T20I</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=T20I&disc=Bowling">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=T20I&disc=Bowling">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=T20I&disc=Bowling">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <?php if ($disc == "Bowling" && $matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=FT20&disc=Bowling\"><b>FT20</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=FT20&disc=Bowling\"><b>FT20</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=FT20&disc=Bowling">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=FT20&disc=Bowling">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=FT20&disc=Bowling">&nbsp;&nbsp;Performances</a></li>
                        </ul>
                    </li>
                    <?php if ($disc == "All-Round") { echo "<li class=\"active\">"; } else { echo "<li class=\"dropdown\">"; } ?>
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">All-Round <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <?php if ($disc == "All-Round" && $matchFormat == "Test") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=Test&disc=All-Round\"><b>Test</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=Test&disc=All-Round\"><b>Test</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=Test&disc=All-Round">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=Test&disc=All-Round">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=Test&disc=All-Round">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <?php if ($disc == "All-Round" && $matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=ODI&disc=All-Round\"><b>ODI</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=ODI&disc=All-Round\"><b>ODI</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=ODI&disc=All-Round">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=ODI&disc=All-Round">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=ODI&disc=All-Round">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <?php if ($disc == "All-Round" && $matchFormat == "T20I") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=T20I&disc=All-Round\"><b>T20I</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=T20I&disc=All-Round\"><b>T20I</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=T20I&disc=All-Round">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=T20I&disc=All-Round">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=T20I&disc=All-Round">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <?php if ($disc == "All-Round" && $matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=FT20&disc=All-Round\"><b>FT20</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=FT20&disc=All-Round\"><b>FT20</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=FT20&disc=All-Round">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=FT20&disc=All-Round">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=FT20&disc=All-Round">&nbsp;&nbsp;Performances</a></li>
                        </ul>
                    </li>
                    <?php if ($disc == "Fielding") { echo "<li class=\"active\">"; } else { echo "<li class=\"dropdown\">"; } ?>
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Fielding <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <?php if ($disc == "Fielding" && $matchFormat == "Test") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=Test&disc=Fielding\"><b>Test</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=Test&disc=Fielding\"><b>Test</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=Test&disc=Fielding">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=Test&disc=Fielding">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=Test&disc=Fielding">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <?php if ($disc == "Fielding" && $matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=ODI&disc=Fielding\"><b>ODI</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=ODI&disc=Fielding\"><b>ODI</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=ODI&disc=Fielding">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=ODI&disc=Fielding">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=ODI&disc=Fielding">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <?php if ($disc == "Fielding" && $matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=FT20&disc=Fielding\"><b>FT20</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=FT20&disc=Fielding\"><b>FT20</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=FT20&disc=Fielding">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=FT20&disc=Fielding">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=FT20&disc=Fielding">&nbsp;&nbsp;Performances</a></li>
                        </ul>
                    </li>
                    <?php if ($disc == "Win Shares") { echo "<li class=\"active\">"; } else { echo "<li class=\"dropdown\">"; } ?>
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Win Shares <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <?php if ($disc == "Win Shares" && $matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=ODI&disc=Win Shares\"><b>ODI</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=ODI&disc=Win Shares\"><b>ODI</b></a></li>"; } ?>
                            <li><a href="current.php?matchFormat=ODI&disc=Win Shares">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=ODI&disc=Win Shares">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=ODI&disc=Win Shares">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <?php if ($disc == "Win Shares" && $matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"methodology.php?matchFormat=FT20&disc=Win Shares\"><b>FT20</b><span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"methodology.php?matchFormat=FT20&disc=Win Shares\"><b>FT20</b></a></li>"; } ?>
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
<?php

echo "<div class=\"panel panel-inverse\">";
echo "<div class=\"panel-body\">";
echo "<div class=\"col-lg-6\">";
echo "<h2><b>Methodology</b></h2>";
echo "<form class=\"form-inline\" role=\"form\" name=\"selectForm\" method=\"get\" action=\"methodology.php\">";
echo "<div class=\"form-group\">";
echo "<select class=\"form-control\" name=\"matchFormat\" onChange=\"submitForms()\">";
$matchFormats = array("Test", "ODI", "T20I", "FT20");
if(isset($_GET['matchFormat'])) {
     $matchFormat = $_GET['matchFormat'];
     foreach ($matchFormats as $mf) {
       if ($matchFormat == $mf) {
	   echo "<option selected=\"selected\" value=\"$mf\">$mf</option>";
       } else {
	   echo "<option value=\"$mf\">$mf</option>";
       }
   }
} else {
   $count = 0;
   foreach ($matchFormats as $mf) {
       if ($count == 0) {
	   echo "<option selected=\"selected\" value=\"$mf\">$mf</option>";
	   $matchFormat = $mf;
       } else {
	   echo "<option value=\"$mf\">$mf</option>";
       }
       $count = $count + 1;
   }
}
echo "</select>";
echo "</div>";

echo "<div class=\"form-group\">";
echo "<select class=\"form-control\" name=\"disc\" onChange=\"submitForms()\">";
$discs = array("Batting", "Bowling", "All-Round", "Team", "Fielding", "Win Shares");
if(isset($_GET['disc'])) {
   $disc = $_GET['disc'];
   foreach ($discs as $dc) {
       if ($disc == $dc) {
	   echo "<option selected=\"selected\" value=\"$dc\">$dc</option>";
       } else {
	   echo "<option value=\"$dc\">$dc</option>";
       }
   }
} else {
   $count = 0;
   foreach ($discs as $dc) {
       if ($count == 0) {
	   echo "<option selected=\"selected\" value=\"$dc\">$dc</option>";
	   $disc = $dc;
       } else {
	   echo "<option value=\"$dc\">$dc</option>";
       }
       $count = $count + 1;
   }
}
echo "</select>";
echo "</div>";
echo "</form>";

if ($disc == "Fielding" && ($matchFormat != "Test" && $matchFormat != "ODI" && $matchFormat != "FT20")) {
    $matchFormat = "ODI";
}

if ($disc == "Win Shares" && ($matchFormat != "ODI" && $matchFormat != "FT20")) {
   $matchFormat = "ODI";
}

$disciplineLower = strtolower($disc);
$startYear = 1877;
if ($matchFormat == "Test" && $disc == "Fielding") {
    $startYear = 2005;
} else if ($matchFormat == "ODI") {
    if ($disc == "Fielding" || $disc == "Win Shares") {
	$startYear = 2005;
    } else {
	$startYear = 1971;
    }
} else if ($matchFormat == "T20I") {
    $startYear = 2005;
}

echo "<ul class=\"list-group\">";
echo "<br/><br/>";
echo "<li class=\"list-group-item\">";
echo "<h4><b>Data</b></h4>";
if ($matchFormat == "FT20") {
    echo "<ul>";
    echo "<li>The following franchises are considered:</li>";
    echo "<ul><li>IPL (Indian Premier League, from 2008)</li>";
    echo "<li>BBL (Big Bash League, from 2011)</li>";
    echo "<li>CPL (Caribbean Premier League, from 2013)</li>";
    echo "</ul><br/>";
    echo "<li>The IPL is taken as the standard of quality franchise T20 cricket, so only leagues that relatively match its quality with siginificant international player presence are considered.</li><br/>";
    echo "<li>$matchFormat scorecards are parsed to rate every $disciplineLower performance. Scorecard information is sourced to generate an accurate assessment of each player's performance.</li><br/>";
    echo "<li>Match results are used to generate team ratings. Fielding performances are evaluated by parsing detailed text commentary. Win shares are calculated by attributing over-by-over team match odds changes to the appropriate player.</li><br/>";
} else {
    echo "<br/><ul>";
    echo "<li>$matchFormat scorecards from $startYear to date are parsed to rate every $disciplineLower performance.</li><br/>";
    echo "<li>Scorecard information is sourced to generate an accurate assessment of each player's performance.</li><br/>";
    echo "<li>Match results are used to generate team ratings.</li><br/>";
    echo "<li>Fielding performances are evaluated by parsing detailed text commentary.</li><br/>";
    echo "<li>Win shares are calculated by attributing over-by-over team match odds changes to the appropriate player.</li><br/>";
}
echo "</ul>";
echo "</li>";
echo "<li class=\"list-group-item\">";
echo "<h4><b>Ratings</b></h4>";
echo "<br/><ul>";
if ($matchFormat == "Test") {
    if ($disc == "Batting") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Top $matchFormat Batsmen</b></a>:<br/> This is evaluated using a weighted average of a batsman's performances. More weight is given to recent performances with past performances diminishing in value with time. Unestablished batsmen that have played less than 20 innings are penalized to avoid cases where a few highly rated innings can catapult a newer batsman to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat Batting Careers</b></a>:<br/> This evaluates overall careers by calculating the average performance rating of each batsman, with a bonus given to career longevity (where playing the most number of years while missing the least percentage of matches gets the most credit) and a penalty for careers of less than 40 matches (increasing penalty for lower matches played).</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat Batting Performances</b></a>:<br/> This is a list of the highest rated batting performances calculated using the factors detailed here.</li>";
    } else if ($disc == "Bowling") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Top $matchFormat Bowlers</b></a>:<br/> This is evaluated using a weighted average of a bowler's performances. More weight is given to recent performances with past performances diminishing in value with time. Unestablished bowlers that have played less than 20 innings are penalized to avoid cases where a few highly rated innings can catapult a newer bowler to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat Bowling Careers</b></a>:<br/> This evaluates overall careers by calculating the average performance rating of each bowler, with a bonus given to career longevity (where playing the most number of years while missing the least percentage of matches gets the most credit) and a penalty for careers of less than 40 matches (increasing penalty for lower matches played).</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat Bowling Performances</b></a>:<br/> This is a list of the highest rated bowling performances calculated using the factors given below.</li>";
    } else if ($disc == "All-Round") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Top $matchFormat All-Rounders</b></a>:<br/> This is evaluated using a weighted average of a player's all-round performances. More weight is given to recent performances with past performances diminishing in value with time. Unestablished players that have played less than 10 matches are penalized to avoid cases where a few highly rated matches can catapult a newer player to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat All-Round Careers</b></a>:<br/> This evaluates overall careers by calculating the average match all-round rating of each player, with a bonus given to career longevity (where playing the most number of years while missing the least percentage of matches gets the most credit) and a penalty for careers of less than 40 matches (increasing penalty for lower matches played). An additional bonus is added based on the player's batting average - bowling average ratio.</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat All-Round Performances</b></a>:<br/> This is a list of the highest rated all-round performances.</li>";
    } else if ($disc == "Fielding") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Best/Worst $matchFormat Fielders</b></a>:<br/> This is evaluated using a weighted average of a player's fielding performances. More weight is given to recent performances with past performances diminishing in value with time. Unestablished players that have played less than 10 matches are penalized to avoid cases where a few highly rated matches can catapult a newer player to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best/Worst $matchFormat Fielding Careers</b></a>:<br/> This evaluates overall careers by calculating the average match fielding rating of each player, with a bonus given to career longevity (where playing the most number of years while missing the least percentage of matches gets the most credit) and a penalty for careers of less than 40 matches (increasing penalty for lower matches played). An additional bonus is added based on the player's drop rate (percentage of catches dropped).</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best/Worst $matchFormat Fielding Performances</b></a>:<br/> This is a list of the highest and lowest rated fielding performances.</li>";
    } else if ($disc == "Team") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current $matchFormat $disc Rankings</b></a>:<br/> This is evaluated using a weighted average of a team's match results. More weight is given to recent performances with past performances diminishing in value with time. A higher rated team loses more points for losing to a lower rated team, and vice versa. Each team starts at 100 points and moves higher on wins and lower on losses. Ties will slightly reduce the higher rated team's rating while slightly increasing the lower team's rating.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>$matchFormat $disc Careers</b></a>:<br/> This evaluates overall team ratings by calculating the average team current rating, with a bonus given to more matches played and a penalty for teams that have played less than 100 matches (increasing penalty for lower matches played).</li><br/>";
    }
    echo "</ul><br/>";
    echo "</li></ul>";
    echo "</div>";
    echo "<div class=\"col-lg-6\">";
    if ($disc == "All-Round" || $disc == "Fielding" || $disc == "Win Shares") {
	echo "<br/><br/><br/><br/><br/><br/><br/>";
    }
    if ($disc != "Team") {
	echo "<ul class=\"list-group\">";
        echo "<li class=\"list-group-item\">";
	echo "<h4><b>Performance Factors</b></h4>";
    }
    echo "<br/><ul>";
    if ($disc == "Batting") {
	echo "<li><b>Runs scored</b>: This is the most significant factor. It values runs linearly upto 200, then each additional run becomes less valuable than the last. This is because scores in excess of 200 are pursued mainly as personal milestones and does not always line up with the team objective.</li><br/>";
	echo "<li><b>Not out</b>: This factor comes into play significantly when a batsman completes an innings below his expected innings rating without being dismissed. The overall rating is adjusted to assume an average innings rating (using his current batting rating) if lower than average and adds a diminishing bonus if the rating is already above average.</li><br/>";
	echo "<li><b>Percentage of total</b>: Moderate factor that considers the percentage of team runs scored by the batsman. Diminishing returns for scores above 250 to avoid skewing the innings ratings excessively just from runs scored.</li><br/>";
	echo "<li><b>Bowling quality</b>: Major factor that considers the current rating of the bowling attack (adjusted by the percentage of overs bowled by each bowler). Adds increased value to more significant innings to avoid rewarding low scores against good attacks.</li><br/>";
	echo "<li><b>Point of entry</b>: This factor rewards significant innings made after coming into the crease at difficult situations. This rewards a batsman who makes a significant contribution after coming to the crease at 50/4 over another that makes the same contribution from 100/1.</li><br/>";
	echo "<li><b>Wickets at crease</b>: This evaluates how a batsman handled the pressure of losing partners on the other end. An opening batsman that makes a significant contribution while carrying his bat through the innings gets the highest value. The credit receieved decreases with batting position of the wickets fallen.</li><br/>";
	echo "<li><b>Support</b>: Compares the percentage of team runs made with the next highest player. Gives credit for making the team's highest score with little support from others.</li><br/>";
	echo "<li><b>Strike rate</b>: Minor factor that adds a small bonus based on the strike rate of the innings weighted by the number of runs scored. For innings with no balls faced data, the minutes played percentage or the innings run rate is used to estimate the strike rate.</li><br/>";
	echo "<li><b>Location</b>: This is a minor factor that adds a bonus to significant innings completed away from home.</li><br/>";
	echo "<li><b>Match status</b>: This factor rewards match-winning or match-savings innings made under pressure in the second innings. Significant contributions under pressure in successful fourth innings run chases get the highest value.</li><br/>";
	echo "<li><b>Result</b>: This factor recognizes significant contributions made in wins and draws. Positive results against higher rated teams are rewarded more than against lower rated teams, using the current rating at the time of the match of the opposition team.</li><br/>";
	echo "<li><b>Close match</b>: Rewards significant contributions made in close wins in terms of wickets or runs left. Recognizes performances that are remembered for delivering under pressure.</li><br/>";
	echo "<li><b>Milestone</b>: Minor factor that adds a bonus to innings that reach significant landmarks such as 100, 200 or 300 runs scored.</li><br/>";
    } else if ($disc == "Bowling") {
	echo "<li><b>Wickets per run</b><br/> This is a major factor that gives the highest value to a high number of wickets taken with the least runs conceded. By tieing the factor with runs conceded this avoids rewarding wickets taken after conceding a significant number of runs.</li><br/>";
	echo "<li><b>Wickets per ball</b><br/> This is also a major factor that gives the highest value to a high number of wickets taken with the least number of balls bowled. This rewards strike bowlers that are very valuable in test matches.</li><br/>";
	echo "<li><b>Economy</b><br/> Minor factor that rewards bowling a long spell of tight bowling where only a few runs are scored. This is to distinguish between bowling innings where a bowler bowls well for long periods with no reward but keeps the pressure.</li><br/>";
	echo "<li><b>Wickets quality</b><br/> Major factor that considers the total current batting rating of the batsmen dismissed. This factor is adjusted by the runs conceded to avoid unduely rewarding expensive returns where a bowler dismisses a quality batsman after he has already done significant damage.</li><br/>";
	echo "<li><b>Batting quality</b><br/> Moderate factor that considers the current rating of the batting line-up faced. Adds increasing value to more significant bowling performances to avoid rewarding unsuccessful and expensive returns against good batsmen.</li><br/>";
	echo "<li><b>Incomplete innings</b><br/> This factor comes into play significantly in incomplete innings (< 75 total overs bowled). If the bowler has bowled less that 15 overs, it is deemed an incomplete performance where he did not get the opportunity to make an impact. In these cases, the bowler's current bowling rating overrides the innings performance to avoid unduely penalizing the performance. This functions similarly to a batsman being not out at the end of an innings.</li><br/>";
	echo "<li><b>Location</b><br/> This is a minor factor that adds a bonus to significant performances completed away from home.</li><br/>";
	echo "<li><b>Match status</b><br/> This factor rewards match-winning or match-savings performances made under pressure in the second innings. Significant contributions in successful fourth innings defenses get the highest value.</li><br/>";
	echo "<li><b>Result</b><br/> This factor recognizes significant contributions made in wins and draws. Positive results against higher rated teams are rewarded more than against lower rated teams, using the current rating at the time of the match of the opposition team.</li><br/>";
	echo "<li><b>Close match</b><br/> Rewards significant contributions made in close wins in terms of wickets or runs left. Recognizes performances that are remembered for delivering under pressure.</li><br/>";
	echo "<li><b>Milestone</b><br/> Minor factor that adds a bonus to bowling performances with at least 5 dismissals.</li><br/>";
    } else if ($disc == "All-Round") {
	echo "<li>All-round performances are rated by multiplying a player's total batting rating with the total bowling rating of a match.</li></br>";
	echo "<li>Performances in just one discipline are automatically nullified with this method and only true all-round performances are rewarded.</li><br/>";
	echo "<li>Check <a href=\"methodology.php?matchFormat=$matchFormat&disc=Batting\">here</a> for more detail on how batting performances are rated, and <a href=\"methodology.php?matchFormat=$matchFormat&disc=Bowling\">here</a> for bowling performance rating details.</li><br/>";
	echo "<li>In addition, a milestone factor is added for performances that involve a total of at least 100 runs and 5 wickets in a match.</li><br/>";
    }
} else if ($matchFormat == "ODI") {
    if ($disc == "Batting") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Top $matchFormat Batsmen</b></a>:<br/> This is evaluated using a weighted average of a batsman's performances. More weight is given to recent performances with past performances diminishing in value with time. Unestablished batsmen that have played less than 20 innings are penalized to avoid cases where a few highly rated innings can catapult a newer batsman to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat Batting Careers</b></a>:<br/> This evaluates overall careers by calculating the average performance rating of each batsman, with a bonus given to career longevity (where playing the most number of years while missing the least percentage of matches gets the most credit) and a penalty for careers of less than 100 matches (increasing penalty for lower matches played).</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat Batting Performances</b></a>:<br/> This is a list of the highest rated batting performances calculated using the factors detailed here.</li>";
    } else if ($disc == "Bowling") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Top $matchFormat Bowlers</b></a>:<br/> This is evaluated using a weighted average of a bowler's performances. More weight is given to recent performances with past performances diminishing in value with time. Unestablished bowlers that have played less than 20 innings are penalized to avoid cases where a few highly rated innings can catapult a newer bowler to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat Bowling Careers</b></a>:<br/> This evaluates overall careers by calculating the average performance rating of each bowler, with a bonus given to career longevity (where playing the most number of years while missing the least percentage of matches gets the most credit) and a penalty for careers of less than 100 matches (increasing penalty for lower matches played).</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat Bowling Performances</b></a>:<br/> This is a list of the highest rated bowling performances calculated using the factors given below.</li>";
    } else if ($disc == "All-Round") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Top $matchFormat All-Rounders</b></a>:<br/> This is evaluated using a weighted average of a player's all-round performances. More weight is given to recent performances with past performances diminishing in value with time. Unestablished players that have played less than 10 matches are penalized to avoid cases where a few highly rated matches can catapult a newer player to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat All-Round Careers</b></a>:<br/> This evaluates overall careers by calculating the average match all-round rating of each player, with a bonus given to career longevity (where playing the most number of years while missing the least percentage of matches gets the most credit) and a penalty for careers of less than 100 matches (increasing penalty for lower matches played). An additional bonus is added based on the player's batting average - bowling average ratio.</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat All-Round Performances</b></a>:<br/> This is a list of the highest rated all-round performances.</li>";
    } else if ($disc == "Fielding") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Best/Worst $matchFormat Fielders</b></a>:<br/> This is evaluated using a weighted average of a player's fielding performances. More weight is given to recent performances with past performances diminishing in value with time. Unestablished players that have played less than 10 matches are penalized to avoid cases where a few highly rated matches can catapult a newer player to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best/Worst $matchFormat Fielding Careers</b></a>:<br/> This evaluates overall careers by calculating the average match fielding rating of each player, with a bonus given to career longevity (where playing the most number of years while missing the least percentage of matches gets the most credit) and a penalty for careers of less than 100 matches (increasing penalty for lower matches played). An additional bonus is added based on the player's drop rate (percentage of catches dropped).</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best/Worst $matchFormat Fielding Performances</b></a>:<br/> This is a list of the highest and lowest rated fielding performances.</li>";
    } else if ($disc == "Win Shares") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Best/Worst $matchFormat Win Shares</b></a>:<br/> This is evaluated using a weighted average of a player's win shares. More weight is given to recent performances with past performances diminishing in value with time. Unestablished players that have played less than 20 matches are penalized to avoid cases where a few highly rated matches can catapult a newer player to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best/Worst $matchFormat Win Share Careers</b></a>:<br/> This evaluates overall careers by calculating the average match win shares of each player, with a bonus given to career longevity (where playing the most number of years while missing the least percentage of matches gets the most credit) and a penalty for careers of less than 100 matches (increasing penalty for lower matches played).</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best/Worst $matchFormat Win Share Performances</b></a>:<br/> This is a list of the highest and lowest rated win share match performances.</li>";
    } else if ($disc == "Team") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current $matchFormat $disc Rankings</b></a>:<br/> This is evaluated using a weighted average of a team's match results. More weight is given to recent performances with past performances diminishing in value with time. A higher rated team loses more points for losing to a lower rated team, and vice versa. Each team starts at 100 points and moves higher on wins and lower on losses. Ties will slightly reduce the higher rated team's rating while slightly increasing the lower team's rating.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>$matchFormat $disc Careers</b></a>:<br/> This evaluates overall team ratings by calculating the average team current rating, with a bonus given to more matches played and a penalty for teams that have played less than 100 matches (increasing penalty for lower matches played).</li><br/>";
    }
    echo "</ul><br/>";
    echo "</li></ul>";
    echo "</div>";
    echo "<div class=\"col-lg-6\">";
    if ($disc == "All-Round" || $disc == "Fielding" || $disc == "Win Shares") {
	echo "<br/><br/><br/><br/><br/><br/><br/>";
    }
    if ($disc != "Team") {
	echo "<ul class=\"list-group\">";
        echo "<li class=\"list-group-item\">";
	echo "<h4><b>Performance Factors</b></h4>";
    }
    echo "<br/><ul>";
    if ($disc == "Batting") {
	echo "<li><b>Runs + Strike rate</b>: This is the most significant factor - it multiplies the runs scored with a combination of the strike rate and the strike rate relative to the team's strike rate.</li><br/>";
	echo "<li><b>Not out</b>: This factor comes into play significantly when a batsman completes an innings below his expected innings rating without being dismissed. The overall rating is adjusted to assume an average innings rating (using his current batting rating) if lower than average and adds a diminishing bonus if the rating is already above average.</li><br/>";
	echo "<li><b>Percentage of total</b>: Moderate factor that considers the percentage of team runs scored by the batsman.</li><br/>";
	echo "<li><b>Bowling quality</b>: Major factor that considers the current rating of the bowling attack (adjusted by the percentage of overs bowled by each bowler). Adds increased value to more significant innings to avoid rewarding low scores against good attacks.</li><br/>";
	echo "<li><b>Point of entry</b>: This factor rewards significant innings made after coming into the crease at difficult situations. This rewards a batsman who makes a significant contribution after coming to the crease at 50/4 over another that makes the same contribution from 100/1.</li><br/>";
	echo "<li><b>Wickets at crease</b>: This evaluates how a batsman handled the pressure of losing partners on the other end. An opening batsman that makes a significant contribution while carrying his bat through the innings gets the highest value. The credit receieved decreases with batting position of the wickets fallen.</li><br/>";
	echo "<li><b>Location</b>: This is a minor factor that adds a bonus to significant innings completed away from home.</li><br/>";
	echo "<li><b>Match status</b>: This factor rewards contributions made in significant matches like finals. World cup knock-out matches are the most highly rewarded.</li><br/>";
	echo "<li><b>Result</b>: This factor recognizes significant contributions made in wins and ties. Positive results against higher rated teams are rewarded more than against lower rated teams, using the current rating at the time of the match of the opposition team.</li><br/>";
	echo "<li><b>Milestone</b>: Minor factor that adds a bonus to innings that reach the century landmark.</li><br/>";
	echo "<li><b>Rule changes</b>: ODI rule changes that generally favor batting such as fielding restrictions, power plays and duo new balls are taken into account by comparatively discounting more recent batting performances.</li><br/>";
    } else if ($disc == "Bowling") {
	echo "<li><b>Wickets per run</b><br/> This is a major factor that gives the highest value to a high number of wickets taken with the least runs conceded. By tieing the factor with runs conceded this avoids rewarding wickets taken after conceding a significant number of runs.</li><br/>";
	echo "<li><b>Economy</b><br/> Major factor in limited overs matches. This rewards lower economy rates compared to other's in the team as well in absolute terms. The value is scaled by the number of overs bowled.</li><br/>";
	echo "<li><b>Wickets per ball</b><br/> This factor gives the highest value to a high number of wickets taken with the least number of balls bowled - rewarding strike bowlers.</li><br/>";
	echo "<li><b>Wickets quality</b><br/> Major factor that considers the total current batting rating of the batsmen dismissed. This factor is adjusted by the runs conceded to avoid unduely rewarding expensive returns where a bowler dismisses a quality batsman after he has done damage.</li><br/>";
	echo "<li><b>Batting quality</b><br/> Major factor that considers the current rating of the batting line-up faced. Adds increasing value to more significant bowling performances to avoid rewarding unsuccessful and expensive returns against good batsmen.</li><br/>";
	echo "<li><b>Incomplete innings</b><br/> This factor comes into play significantly in incomplete innings (< 25 total overs bowled). If the bowler has bowled less that 5 overs, it is deemed an incomplete performance where he did not get the opportunity to make an impact. In these cases, the bowler's current bowling rating overrides the innings performance to avoid unduely penalizing the performance. This functions similarly to a batsman being not out at the end of an innings.</li><br/>";
	echo "<li><b>Location</b><br/> This is a minor factor that adds a bonus to significant performances completed away from home.</li><br/>";
	echo "<li><b>Match status</b><br/> This factor rewards contributions made in significant matches like finals. World cup knock-out matches are the most highly rewarded.</li><br/>";
	echo "<li><b>Result</b><br/> This factor recognizes significant contributions made in wins and ties. Positive results against higher rated teams are rewarded more than against lower rated teams, using the current rating at the time of the match of the opposition team.</li><br/>";
	echo "<li><b>Milestone</b><br/> Minor factor that adds a bonus to 5-wicket performances.</li><br/>";
	echo "<li><b>Rule changes</b><br/> ODI rule changes that generally favor batting such as fielding restrictions, power plays and duo new balls are taken into account by comparatively discounting past bowling performances.</li><br/>";
    } else if ($disc == "All-Round") {
	echo "<li>All-round performances are rated by multiplying a player's total batting rating with the total bowling rating of a match.</li></br>";
	echo "<li>Performances in just one discipline are automatically nullified with this method and only true all-round performances are rewarded.</li><br/>";
	echo "<li>Check <a href=\"methodology.php?matchFormat=$matchFormat&disc=Batting\">here</a> for more detail on how batting performances are rated, and <a href=\"methodology.php?matchFormat=$matchFormat&disc=Bowling\">here</a> for bowling performance rating details.</li><br/>";
	echo "<li>In addition, a milestone factor is added for performances that involve a total of at least 50 runs and 3 wickets in a match.</li><br/>";
    }
} else if ($matchFormat == "T20I") {
    if ($disc == "Batting") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Top $matchFormat Batsmen</b></a>:<br/> This is evaluated using a weighted average of a batsman's performances. More weight is given to recent performances with past performances diminishing in value with time. Unestablished batsmen that have played less than 20 innings are penalized to avoid cases where a few highly rated innings can catapult a newer batsman to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat Batting Careers</b></a>:<br/> This evaluates overall careers by calculating the average performance rating of each batsman, with a bonus given to career longevity and a penalty for careers of less than 20 matches (increasing penalty for lower matches played).</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat Batting Performances</b></a>:<br/> This is a list of the highest rated batting performances calculated using the factors detailed here.</li>";
    } else if ($disc == "Bowling") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Top $matchFormat Bowlers</b></a>:<br/> This is evaluated using a weighted average of a bowler's performances. More weight is given to recent performances with past performances diminishing in value with time. Unestablished bowlers that have played less than 20 innings are penalized to avoid cases where a few highly rated innings can catapult a newer bowler to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat Bowling Careers</b></a>:<br/> This evaluates overall careers by calculating the average performance rating of each bowler, with a bonus given to career longevity and a penalty for careers of less than 20 matches (increasing penalty for lower matches played).</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat Bowling Performances</b></a>:<br/> This is a list of the highest rated bowling performances calculated using the factors given below.</li>";
    } else if ($disc == "All-Round") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Top $matchFormat All-Rounders</b></a>:<br/> This is evaluated using a weighted average of a player's all-round performances. More weight is given to recent performances with past performances diminishing in value with time. Unestablished players that have played less than 10 matches are penalized to avoid cases where a few highly rated matches can catapult a newer player to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat All-Round Careers</b></a>:<br/> This evaluates overall careers by calculating the average match all-round rating of each player, with a bonus given to career longevity and a penalty for careers of less than 40 matches (increasing penalty for lower matches played). An additional bonus is added based on the player's batting average - bowling average ratio.</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat All-Round Performances</b></a>:<br/> This is a list of the highest rated all-round performances.</li>";
    } else if ($disc == "Fielding") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Best/Worst $matchFormat Fielders</b></a>:<br/> This is evaluated using a weighted average of a player's fielding performances. More weight is given to recent performances with past performances diminishing in value with time. Unestablished players that have played less than 10 matches are penalized to avoid cases where a few highly rated matches can catapult a newer player to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best/Worst $matchFormat Fielding Careers</b></a>:<br/> This evaluates overall careers by calculating the average match fielding rating of each player, with a bonus given to career longevity (where playing the most number of years while missing the least percentage of matches gets the most credit) and a penalty for careers of less than 100 matches (increasing penalty for lower matches played). An additional bonus is added based on the player's drop rate (percentage of catches dropped).</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best/Worst $matchFormat Fielding Performances</b></a>:<br/> This is a list of the highest and lowest rated fielding performances.</li>";
    } else if ($disc == "Win Shares") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Best/Worst $matchFormat Win Shares</b></a>:<br/> This is evaluated using a weighted average of a player's win shares. More weight is given to recent performances with past performances diminishing in value with time. Unestablished players that have played less than 20 matches are penalized to avoid cases where a few highly rated matches can catapult a newer player to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best/Worst $matchFormat Win Share Careers</b></a>:<br/> This evaluates overall careers by calculating the average match win shares of each player, with a bonus given to career longevity (where playing the most number of years while missing the least percentage of matches gets the most credit) and a penalty for careers of less than 100 matches (increasing penalty for lower matches played).</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best/Worst $matchFormat Win Share Performances</b></a>:<br/> This is a list of the highest and lowest rated win share match performances.</li>";
    } else if ($disc == "Team") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current $matchFormat $disc Rankings</b></a>:<br/> This is evaluated using a weighted average of a team's match results. More weight is given to recent performances with past performances diminishing in value with time. A higher rated team loses more points for losing to a lower rated team, and vice versa. Each team starts at 100 points and moves higher on wins and lower on losses. Ties will slightly reduce the higher rated team's rating while slightly increasing the lower team's rating.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>$matchFormat $disc Careers</b></a>:<br/> This evaluates overall team ratings by calculating the average team current rating, with a bonus given to more matches played and a penalty for teams that have played less than 20 matches (increasing penalty for lower matches played).</li><br/>";
    }
    echo "</ul><br/>";
    echo "</li></ul>";
    echo "</div>";
    echo "<div class=\"col-lg-6\">";
    if ($disc == "All-Round" || $disc == "Fielding" || $disc == "Win Shares" || $disc == "Batting") {
	echo "<br/><br/><br/><br/><br/><br/><br/>";
    }
    if ($disc != "Team") {
	echo "<ul class=\"list-group\">";
        echo "<li class=\"list-group-item\">";
	echo "<h4><b>Performance Factors</b></h4>";
    }
    echo "<br/><ul>";
    if ($disc == "Batting") {
	echo "<li><b>Runs + Strike rate</b>: This is the most significant factor - it multiplies the runs scored with the strike rate relative to the team's strike rate.</li><br/>";
	echo "<li><b>Not out</b>: This factor comes into play significantly when a batsman completes an innings below his expected innings rating without being dismissed. The overall rating is adjusted to assume an average innings rating (using his current batting rating) if lower than average and adds a diminishing bonus if the rating is already above average.</li><br/>";
	echo "<li><b>Percentage of total</b>: Moderate factor that considers the percentage of team runs scored by the batsman.</li><br/>";
	echo "<li><b>Bowling quality</b>: Major factor that considers the current rating of the bowling attack (adjusted by the percentage of overs bowled by each bowler). Adds increased value to more significant innings to avoid rewarding low scores against good attacks.</li><br/>";
	echo "<li><b>Location</b>: This is a minor factor that adds a bonus to significant innings completed away from home.</li><br/>";
	echo "<li><b>Match status</b>: This factor rewards contributions made in significant matches like finals. World cup knock-out matches are the most highly rewarded.</li><br/>";
	echo "<li><b>Result</b>: This factor recognizes significant contributions made in wins and ties. Positive results against higher rated teams are rewarded more than against lower rated teams, using the current rating at the time of the match of the opposition team.</li><br/>";
	echo "<li><b>Milestone</b>: Minor factor that adds a bonus to innings that reach the fifty landmark.</li><br/>";
    } else if ($disc == "Bowling") {
	echo "<li><b>Wickets per run</b><br/> This is a moderate factor that gives the highest value to a high number of wickets taken with the least runs conceded. By tieing the factor with runs conceded this avoids rewarding wickets taken after conceding a significant number of runs.</li><br/>";
	echo "<li><b>Economy</b><br/> Major factor in limited overs matches. This rewards lower economy rates compared to other's in the team as well in absolute terms. The value is scaled by the number of overs bowled. A bowler who is economical but doesn't pick up a wicket will get a higher rating than one who gets a few wickets but is expensive due to this factor.</li><br/>";
	echo "<li><b>Wickets quality</b><br/> This factor that considers the total current batting rating of the batsmen dismissed. This factor is adjusted by the runs conceded to avoid unduely rewarding expensive returns where a bowler dismisses a quality batsman after he has done damage.</li><br/>";
	echo "<li><b>Batting quality</b><br/> This factor that considers the current rating of the batting line-up faced. Adds increasing value to more significant bowling performances to avoid rewarding unsuccessful and expensive returns against good batsmen.</li><br/>";
	echo "<li><b>Incomplete innings</b><br/> This factor comes into play significantly in incomplete innings (< 10 total overs bowled). If the bowler has bowled less that 2 overs, it is deemed an incomplete performance where he did not get the opportunity to make an impact. In these cases, the bowler's current bowling rating overrides the innings performance to avoid unduely penalizing the performance. This functions similarly to a batsman being not out at the end of an innings.</li><br/>";
	echo "<li><b>Location</b><br/> This is a minor factor that adds a bonus to significant performances completed away from home.</li><br/>";
	echo "<li><b>Match status</b><br/> This factor rewards contributions made in significant matches like finals. World cup knock-out matches are the most highly rewarded.</li><br/>";
	echo "<li><b>Result</b><br/> This factor recognizes significant contributions made in wins and ties. Positive results against higher rated teams are rewarded more than against lower rated teams, using the current rating at the time of the match of the opposition team.</li><br/>";
	echo "<li><b>Milestone</b><br/> Minor factor that adds a bonus to 3-wicket performances.</li><br/>";
    } else if ($disc == "All-Round") {
	echo "<li>All-round performances are rated by multiplying a player's total batting rating with the total bowling rating of a match.</li></br>";
	echo "<li>Performances in just one discipline are automatically nullified with this method and only true all-round performances are rewarded.</li><br/>";
	echo "<li>Check <a href=\"methodology.php?matchFormat=$matchFormat&disc=Batting\">here</a> for more detail on how batting performances are rated, and <a href=\"methodology.php?matchFormat=$matchFormat&disc=Bowling\">here</a> for bowling performance rating details.</li><br/>";
	echo "<li>In addition, a milestone factor is added for performances that involve a total of at least 30 runs and 2 wickets in a match.</li><br/>";
    }
} else if ($matchFormat == "FT20") {
    if ($disc == "Batting") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Top $matchFormat Batsmen</b></a>:<br/> This is evaluated using a weighted average of a batsman's performances. More weight is given to recent performances with past performances diminishing in value with time. Unestablished batsmen that have played less than 20 innings are penalized to avoid cases where a few highly rated innings can catapult a newer batsman to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat Batting Careers</b></a>:<br/> This evaluates overall careers by calculating the average performance rating of each batsman, with a bonus given to career longevity and a penalty for careers of less than 20 matches (increasing penalty for lower matches played).</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat Batting Performances</b></a>:<br/> This is a list of the highest rated batting performances calculated using the factors detailed here.</li>";
    } else if ($disc == "Bowling") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Top $matchFormat Bowlers</b></a>:<br/> This is evaluated using a weighted average of a bowler's performances. More weight is given to recent performances with past performances diminishing in value with time. Unestablished bowlers that have played less than 20 innings are penalized to avoid cases where a few highly rated innings can catapult a newer bowler to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat Bowling Careers</b></a>:<br/> This evaluates overall careers by calculating the average performance rating of each bowler, with a bonus given to career longevity and a penalty for careers of less than 20 matches (increasing penalty for lower matches played).</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat Bowling Performances</b></a>:<br/> This is a list of the highest rated bowling performances calculated using the factors given below.</li>";
    } else if ($disc == "All-Round") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Top $matchFormat All-Rounders</b></a>:<br/> This is evaluated using a weighted average of a player's all-round performances. More weight is given to recent performances with past performances diminishing in value with time. Unestablished players that have played less than 10 matches are penalized to avoid cases where a few highly rated matches can catapult a newer player to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat All-Round Careers</b></a>:<br/> This evaluates overall careers by calculating the average match all-round rating of each player, with a bonus given to career longevity and a penalty for careers of less than 40 matches (increasing penalty for lower matches played). An additional bonus is added based on the player's batting average - bowling average ratio.</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best $matchFormat All-Round Performances</b></a>:<br/> This is a list of the highest rated all-round performances.</li>";
    } else if ($disc == "Fielding") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Best/Worst $matchFormat Fielders</b></a>:<br/> This is evaluated using a weighted average of a player's fielding performances. More weight is given to recent performances with past performances diminishing in value with time. Unestablished players that have played less than 10 matches are penalized to avoid cases where a few highly rated matches can catapult a newer player to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best/Worst $matchFormat Fielding Careers</b></a>:<br/> This evaluates overall careers by calculating the average match fielding rating of each player, with a bonus given to career longevity (where playing the most number of years while missing the least percentage of matches gets the most credit) and a penalty for careers of less than 100 matches (increasing penalty for lower matches played). An additional bonus is added based on the player's drop rate (percentage of catches dropped).</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best/Worst $matchFormat Fielding Performances</b></a>:<br/> This is a list of the highest and lowest rated fielding performances.</li>";
    } else if ($disc == "Win Shares") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current Best/Worst $matchFormat Win Shares</b></a>:<br/> This is evaluated using a weighted average of a player's win shares. More weight is given to recent performances with past performances diminishing in value with time. Unestablished players that have played less than 20 matches are penalized to avoid cases where a few highly rated matches can catapult a newer player to the top of the pile.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>Best/Worst $matchFormat Win Share Careers</b></a>:<br/> This evaluates overall careers by calculating the average match win shares of each player, with a bonus given to career longevity (where playing the most number of years while missing the least percentage of matches gets the most credit) and a penalty for careers of less than 100 matches (increasing penalty for lower matches played).</li><br/>";
	echo "<li><a href=\"performances.php?matchFormat=$matchFormat&disc=$disc\"><b>Best/Worst $matchFormat Win Share Performances</b></a>:<br/> This is a list of the highest and lowest rated win share match performances.</li>";
    } else if ($disc == "Team") {
	echo "<li><a href=\"current.php?matchFormat=$matchFormat&disc=$disc\"><b>Current $matchFormat $disc Rankings</b></a>:<br/> This is evaluated using a weighted average of a team's match results. More weight is given to recent performances with past performances diminishing in value with time. A higher rated team loses more points for losing to a lower rated team, and vice versa. Each team starts at 100 points and moves higher on wins and lower on losses. Ties will slightly reduce the higher rated team's rating while slightly increasing the lower team's rating.</li><br/>";
	echo "<li><a href=\"career.php?matchFormat=$matchFormat&disc=$disc\"><b>$matchFormat $disc Careers</b></a>:<br/> This evaluates overall team ratings by calculating the average team current rating, with a bonus given to more matches played and a penalty for teams that have played less than 20 matches (increasing penalty for lower matches played).</li><br/>";
    }
    echo "</ul><br/>";
    echo "</li></ul>";
    echo "</div>";
    echo "<div class=\"col-lg-6\">";
    if ($disc == "All-Round" || $disc == "Fielding" || $disc == "Win Shares" || $disc == "Batting") {
	echo "<br/><br/><br/><br/><br/><br/><br/>";
    } else if ($disc == "Bowling") {
	echo "<br/><br/><br/>";
    }
    if ($disc != "Team") {
	echo "<ul class=\"list-group\">";
        echo "<li class=\"list-group-item\">";
	echo "<h4><b>Performance Factors</b></h4>";
    }
    echo "<br/><ul>";
    if ($disc == "Batting") {
	echo "<li><b>Runs + Strike rate</b>: This is the most significant factor - it multiplies the runs scored with the strike rate relative to the team's strike rate.</li><br/>";
	echo "<li><b>Not out</b>: This factor comes into play significantly when a batsman completes an innings below his expected innings rating without being dismissed. The overall rating is adjusted to assume an average innings rating (using his current batting rating) if lower than average and adds a diminishing bonus if the rating is already above average.</li><br/>";
	echo "<li><b>Percentage of total</b>: Moderate factor that considers the percentage of team runs scored by the batsman.</li><br/>";
	echo "<li><b>Bowling quality</b>: Major factor that considers the current rating of the bowling attack (adjusted by the percentage of overs bowled by each bowler). Adds increased value to more significant innings to avoid rewarding low scores against good attacks.</li><br/>";
	echo "<li><b>Match status</b>: This factor rewards contributions made in significant matches like finals. League knock-out matches are the most highly rewarded.</li><br/>";
	echo "<li><b>Result</b>: This factor recognizes significant contributions made in wins and ties. Positive results against higher rated teams are rewarded more than against lower rated teams, using the current rating at the time of the match of the opposition team.</li><br/>";
	echo "<li><b>Milestone</b>: Minor factor that adds a bonus to innings that reach the fifty landmark.</li><br/>";
    } else if ($disc == "Bowling") {
	echo "<li><b>Wickets per run</b><br/> This is a moderate factor that gives the highest value to a high number of wickets taken with the least runs conceded. By tieing the factor with runs conceded this avoids rewarding wickets taken after conceding a significant number of runs.</li><br/>";
	echo "<li><b>Economy</b><br/> Major factor in limited overs matches. This rewards lower economy rates compared to other's in the team as well in absolute terms. The value is scaled by the number of overs bowled. A bowler who is economical but doesn't pick up a wicket will get a higher rating than one who gets a few wickets but is expensive due to this factor.</li><br/>";
	echo "<li><b>Wickets quality</b><br/> This factor that considers the total current batting rating of the batsmen dismissed. This factor is adjusted by the runs conceded to avoid unduely rewarding expensive returns where a bowler dismisses a quality batsman after he has done damage.</li><br/>";
	echo "<li><b>Batting quality</b><br/> This factor that considers the current rating of the batting line-up faced. Adds increasing value to more significant bowling performances to avoid rewarding unsuccessful and expensive returns against good batsmen.</li><br/>";
	echo "<li><b>Incomplete innings</b><br/> This factor comes into play significantly in incomplete innings (< 10 total overs bowled). If the bowler has bowled less that 2 overs, it is deemed an incomplete performance where he did not get the opportunity to make an impact. In these cases, the bowler's current bowling rating overrides the innings performance to avoid unduely penalizing the performance. This functions similarly to a batsman being not out at the end of an innings.</li><br/>";
	echo "<li><b>Match status</b><br/> This factor rewards contributions made in significant matches like finals. League knock-out matches are the most highly rewarded.</li><br/>";
	echo "<li><b>Result</b><br/> This factor recognizes significant contributions made in wins and ties. Positive results against higher rated teams are rewarded more than against lower rated teams, using the current rating at the time of the match of the opposition team.</li><br/>";
	echo "<li><b>Milestone</b><br/> Minor factor that adds a bonus to 3-wicket performances.</li><br/>";
    } else if ($disc == "All-Round") {
	echo "<li>All-round performances are rated by multiplying a player's total batting rating with the total bowling rating of a match.</li></br>";
	echo "<li>Performances in just one discipline are automatically nullified with this method and only true all-round performances are rewarded.</li><br/>";
	echo "<li>Check <a href=\"methodology.php?matchFormat=$matchFormat&disc=Batting\">here</a> for more detail on how batting performances are rated, and <a href=\"methodology.php?matchFormat=$matchFormat&disc=Bowling\">here</a> for bowling performance rating details.</li><br/>";
	echo "<li>In addition, a milestone factor is added for performances that involve a total of at least 30 runs and 2 wickets in a match.</li><br/>";
    }
}
if ($disc == "Fielding") {
    echo "<li><b>Catches</b><br/> Minor factor that credits regulation catches taken with the current rating of the relevant batsmen affecting the value. This is weighted to be 20 times as less important as great catches based on the frequency of regulation catches.</li><br/>";
    echo "<li><b>Dropped Catches</b><br/> Significant negative factor that increases the higher the current rating of the batsman dropped. If the chance was difficult and not expected to be taken, it is not considered a drop - this is assuming that the commentary explicits states that to be the case.</li><br/>";
    echo "<li><b>Direct Hits</b><br/> Major positive factor that credits the fielder with a direct hit to get a batsman run out. The current rating of the batsman involved affects the value.</li><br/>";
    echo "<li><b>Great Catches</b><br/> Major positive factor that credits the fielder with a great catch (if described as such in the commentary). The current rating of the batsman involved affects the value.</li><br/>";
    echo "<li><b>Runs Saved</b><br/> This factor attempts to parse out how many runs a fielder saves through ground fielding. If the commentary does not explicitly state the number of runs saved, an attempt is made to guess it based on the actual runs scored from the fielding event.</li><br/>";
    echo "<li><b>Missed Stumpings</b><br/> Major negative factor that only affects wicket-keepers. The current rating of the batsman is used to evaluate the value.</li><br/>";
} else if ($disc == "Win Shares") {
    echo "<li><b>Odds</b><br/> Over-by-over match odds are calculated by using similar historical match situations and the corresponding win/loss frequencies of those matches. For adjusted win-shares, the starting match odds are adjusted to factor the team strengths (Aus vs Afg will not be 50-50 but more like 75-25 favored to Australia for example).</li><br/>";
    echo "<li><b>Batting WS</b><br/> Batting Win Shares are attributed over-by-over based on the number of runs added by each batsman when win odds for the batting team increases, and the number of balls faced by the batsman when the win odds decrease. The likely win odds decrease when a batsman gets out is also attributed to the corresponding batsman.</li><br/>";
    echo "<li><b>Bowling WS</b><br/> Bowling Win Shares are attributed to the bowler over-by-over based on the win odds change for the bowling team. Fielding events such as dropped catches and missed stumpings are positively credited to the bowler since he created the chance while the odds change from a great catch is shared with the relevant fielder so the bowler does not get full credit.</li><br/>";
    echo "<li><b>Fielding WS</b><br/> Fielding Win Shares are attributed based on fielding events that affected the game. A direct hit or a great catch would be mainly attributed to the fielder instead of the bowler, and dropped catch is also considered as \"lost\" win odds.</li><br/>";
}
echo "</ul>";
if ($disc != "Team") {
    echo "</li></ul>";
}
echo "</div>";
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
