<!DOCTYPE html>
<?php
session_start();
$playerId = $_GET["playerId"];

$matchFormat = "";
function getDefaultMatchFormat($db, $playerId, $mf, $matchFormat) {
    if ($matchFormat == "") {
	$sql = "select playerId from playerInfo where playerId=".$playerId;
        $result = $db->query($sql);
        if (!$result) die("Cannot execute query.");
        $res = $result->fetchArray(SQLITE3_NUM);

        if (!empty($res)) {
            $matchFormat = $mf;
        }
        $db->close();
    }
    return $matchFormat;
}

if(isset($_GET['matchFormat'])) {
   $matchFormat = $_GET['matchFormat'];
} else {
    $db = new SQLite3('ccr.db');
    $matchFormat = getDefaultMatchFormat($db, $playerId, "Test", $matchFormat);
    $db = new SQLite3('ccrODI.db');
    $matchFormat = getDefaultMatchFormat($db, $playerId, "ODI", $matchFormat);
    $db = new SQLite3('ccrT20I.db');
    $matchFormat = getDefaultMatchFormat($db, $playerId, "T20I", $matchFormat);
    $db = new SQLite3('ccrFT20.db');
    $matchFormat = getDefaultMatchFormat($db, $playerId, "FT20", $matchFormat);
}
if(isset($_GET['disc'])) {
   $disc = $_GET['disc'];
} else {
   $disc = "Batting";
}

if(isset($_SESSION['screen_width']) AND isset($_SESSION['screen_height'])){
} else if(isset($_REQUEST['width']) AND isset($_REQUEST['height'])) {
    $_SESSION['screen_width'] = $_REQUEST['width'];
    $_SESSION['screen_height'] = $_REQUEST['height'];
    header("Location: player.php?playerId=".$playerId."&matchFormat=".$matchFormat."&disc=".$disc);
} else {
    echo '<script type="text/javascript">window.location = "' . $_SERVER['PHP_SELF'] . '?playerId='.$playerId.'&matchFormat='.$matchFormat.'&disc='.$disc.'&width="+screen.width+"&height="+screen.height;</script>';
}

$player = "";
function getPlayerName($db, $playerId, $player) {
    if ($player == "") {
        $sql = "select player from playerInfo where playerId=".$playerId;
        $result = $db->query($sql);
        if (!$result) die("Cannot execute query.");
        $res = $result->fetchArray(SQLITE3_NUM);

        if (!empty($res)) {
            $player = $res[0];
        }
        $db->close();
    }
    return $player;
}

$db = new SQLite3('ccr.db');
$player = getPlayerName($db, $playerId, $player);
$db = new SQLite3('ccrODI.db');
$player = getPlayerName($db, $playerId, $player);
$db = new SQLite3('ccrT20I.db');
$player = getPlayerName($db, $playerId, $player);
$db = new SQLite3('ccrFT20.db');
$player = getPlayerName($db, $playerId, $player);
?>
<html>
<head>
    <?php echo "<title>cricrate | ".$player." - ".$matchFormat." ".$disc."</title>"; ?>
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

    var isMobile = false; //initiate as false
    // device detection
    if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent)
    || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))) isMobile = true;

    var chartWidth = screen.width * 0.375;
    var chartHeight = screen.height * 0.4;
    if (isMobile == true) {
	chartWidth = chartWidth * 2;
    }

    var player = <?php echo $_GET['playerId'] ?>;
    var matchFormat = <?php echo json_encode($matchFormat); ?>;
    var disc = <?php echo json_encode($disc); ?>;
    var batBowl = disc.toLowerCase();
    if (batBowl == "all-round") {
       batBowl = "allRound";
    } else if (batBowl == "win shares") {
       batBowl = "winShares";
    }

    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
	var jsonData = $.ajax({
	    url: "charts/player.php?playerId="+player+"&matchFormat="+matchFormat+"&batBowl="+batBowl,
	    dataType:"json",
	    async: false
	    }).responseText;

	// Create our data table out of JSON data loaded from server.
	var data = new google.visualization.DataTable(jsonData);
        var showEvery = parseInt(data.getNumberOfRows() / 7);

	var options = {
	    fontName: "Lucida Sans Unicode",
	    backgroundColor: {
			    backgroundColor: '#FFFFFF',
			    fill:'#FFFFFF'
			    },
	    bar: {
		groupWidth: '100%'
		},
	    legend: {
		    position: 'none',
		},
	    chartArea: {
		width: "85%",
		height: "80%",
		left: "10%",
		top: "5%"
		},
	    colors:['#2c518d','#ff3232'],
	    width: chartWidth,
	    height: chartHeight,
	    vAxis: {
		    title: "Rating",
		    format: 'decimal',
		    viewWindowMode: "maximized",
		    gridlines: {count: 12},
		    textStyle: {
				color: '#000000',
				fontSize: 11
				},
		    titleTextStyle: {
				    color: '#000000',
				    italic: "false",
				    }
		},
	    hAxis: {
                    showTextEvery: showEvery,
		    title: "Date",
		    slantedText: "false",
		    maxAlternation: 1,
		    textStyle: {
				color: '#000000',
				fontSize: 11
				},
		    titleTextStyle: {
				    color: '#000000',
				    italic: "false",
				    },
		    },
	    seriesType: "bars",
	    series: {1: {type: "area"}},
	    animation: {
			"startup": true,
			duration: 1000,
			easing: 'inAndOut',
			},
	    tooltip: {
		    textStyle: {
				fontSize: 11,
				color: '#000000',
				bold: 'true'
				},
		    isHtml: true
		    }
	};

	var chart = new google.visualization.ComboChart(document.getElementById('chart'));
	chart.draw(data, options);
    }

    $(document).ready(function() {
	$('#inningsTable').DataTable( {
        "lengthChange":   false,
	"pageLength": 18,
    } );
    } );

    submitForms = function(){
	    window.document.selectForm.submit();
	}

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
<?php

$playerFound = 0;
echo "<div class=\"panel panel-inverse\">";
echo "<div class=\"panel-body\">";
echo "<div class=\"row\">";
echo "<div class=\"col-lg-5\">";
if ($player != "") {
    if(isset($_GET['matchFormat'])) {
	$mf = $_GET['matchFormat'];
    } else {
	$mf = "Test";
    }
    if(isset($_GET['disc'])) {
	$dc = $_GET['disc'];
    } else {
	$dc = "Batting";
    }
    echo "<h2><b>".$player."&nbsp;&nbsp;&nbsp;<a id=\"playerCompareLink\" href=\"compare.php?playerId1=$playerId&playerId2=&player2Search=&matchFormat=$mf&disc=$dc&inningsDate=Inning\"><small>Compare</small></a></b></h2>";
    $playerFound = 1;
}

   $disc = "Batting";
   echo "<form class=\"form-inline\" role=\"form\" name=\"selectForm\" method=\"get\" action=\"player.php\">";
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
      foreach ($matchFormats as $mf) {
	  if ($mf == $matchFormat) {
	      echo "<option selected=\"selected\" value=\"$mf\">$mf</option>";
	  } else {
	      echo "<option value=\"$mf\">$mf</option>";
	  }
      }
   }
   echo "</select>";
   echo "</div>";

   echo "<div class=\"form-group\">";
   echo "<select class=\"form-control\" name=\"disc\" onChange=\"submitForms()\">";
   $discs = array("Batting", "Bowling", "All-Round", "Fielding", "Win Shares");
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
   echo "<input type=\"hidden\" name=\"playerId\" value=\"$playerId\">";
    echo "</form>";

    if ($disc == "Fielding" && ($matchFormat != "Test" && $matchFormat != "ODI" && $matchFormat != "FT20")) {
	$matchFormat = "ODI";
    }

    if ($disc == "Win Shares" && ($matchFormat != "ODI" && $matchFormat != "FT20")) {
	$matchFormat = "ODI";
    }

   $matchFormatLower = strtolower($matchFormat);
   $disciplineLower = strtolower($disc);
   if ($disciplineLower == "all-round") {
      $disciplineLower = "allRound";
   } else if ($disciplineLower == "win shares") {
      $disciplineLower = "winShares";
   }

$dbName = "ccr.db";
if ($matchFormat == "ODI") {
    $dbName = "ccrODI.db";
} elseif ($matchFormat == "T20I") {
    $dbName = "ccrT20I.db";
} elseif ($matchFormat == "FT20") {
    $dbName = "ccrFT20.db";
}

$db = new SQLite3($dbName);

if ($matchFormat == "FT20") {
    $sql = "select teams from playerInfo where playerId=".$playerId;
} else {
    $sql = "select country from playerInfo where playerId=".$playerId;
}
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");
$res = $result->fetchArray(SQLITE3_NUM);
$country = $res[0];

if ($matchFormat == "FT20") {
    echo "&nbsp;&nbsp;$country";
} else {
    echo "&nbsp;&nbsp;<a href=\"team.php?team=".$country."&matchFormat=$matchFormat\"><img src=\"images/".$country.".png\" alt=\"$country\" style='border:1px solid #A9A9A9'/></a>";
}

echo "<ul class=\"list-group\">";
if ($disc == "Batting") {
    # batting career
    if ($matchFormat == "Test") {
	$sql = "select startDate, endDate, ".$matchFormatLower."s, innings, notOuts, runs, average, strikeRate, fifties, hundreds, dblHundreds, tripleHundreds, rating from batting".$matchFormat."Career where playerId=".$playerId;
    } else {
	$sql = "select startDate, endDate, innings, notOuts, runs, average, strikeRate, fifties, hundreds, rating from batting".$matchFormat."Career where playerId=".$playerId;
    }
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    $res = $result->fetchArray(SQLITE3_NUM);

    $tableHtml = "";
    if (!empty($res) && $res[0] != "") {
	echo "<li class=\"list-group-item\">";
	echo "<h4>Career Summary</h4>";
	echo "<table class=\"table table-hover table-condensed\" id=\"playerTable\">";
	echo "<thead><tr>";

	if ($matchFormat == "Test") {
	    echo "<th>Span</th>";
	    echo "<th>Mat</th>";
	    echo "<th>Inns</th>";
	    echo "<th>NO</th>";
	    echo "<th>Runs</th>";
	    echo "<th>Ave</th>";
	    echo "<th>SR</th>";
	    echo "<th>50</th>";
	    echo "<th>100</th>";
	    echo "<th>200</th>";
	    echo "<th>300</th>";
	    echo "<th>Career Rating</th>";
	    echo "</tr></thead>";
	    echo "<tr>";
	    $numInns = $res[3];
	    echo "<td>".substr($res[0], 0, 4)."-".substr($res[1], 0, 4)."</td>"; # span
	    echo "<td>$res[2]</td><td>$res[3]</td><td>$res[4]</td><td>$res[5]</td>";
	    echo "<td>".number_format(round($res[6], 2), 2)."</td>";
	    if ($res[7] != "") {
		echo "<td>".number_format(round($res[7], 2), 2)."</td>";
	    } else {
		echo "<td></td>";
	    }
	    echo "<td>$res[8]</td><td>$res[9]</td><td>$res[10]</td><td>$res[11]</td>";
	    echo "<td><b>".round($res[12], 0)."</b></td>";
	} else {
	    echo "<th>Span</th>";
	    echo "<th>Inns</th>";
	    echo "<th>NO</th>";
	    echo "<th>Runs</th>";
	    echo "<th>Ave</th>";
	    echo "<th>SR</th>";
	    echo "<th>50</th>";
	    echo "<th>100</th>";
	    echo "<th>Career Rating</th>";
	    echo "</tr></thead>";
	    echo "<tr>";
	    $numInns = $res[2];
	    echo "<td>".substr($res[0], 0, 4)."-".substr($res[1], 0, 4)."</td>"; # span
	    echo "<td>$res[2]</td><td>$res[3]</td><td>$res[4]</td>";
	    echo "<td>".number_format(round($res[5], 2), 2)."</td><td>".number_format(round($res[6], 2), 2)."</td>";
	    echo "<td>$res[7]</td><td>$res[8]</td>";
	    echo "<td><b>".round($res[9], 0)."</b></td>";
	}
	echo "</tr>";
	echo "</table><br/>";
	echo "</li>";

	# batting innings
	$sql = "select t.startDate, t.".$matchFormatLower."Id, b.inningsId, b.notOut, b.runs, b.balls, b.rating, l.rating, t.team1, t.team2, t.ground from batting".$matchFormat."Innings b, batting".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId;
	$result = $db->query($sql);
	if (!$result) die("Cannot execute query.");
	$tableHtml .= "<div class=\"col-lg-7\">";
	$tableHtml .= "<li class=\"list-group-item\">";
	$tableHtml .= "<h4>Innings List</h4>";
	$tableHtml .= "<table class=\"table table-hover table-condensed\" id=\"inningsTable\">";
	$tableHtml .= "<thead><tr>";
	$tableHtml .= "<th>Inn #</th>";
	$tableHtml .= "<th>Date</th>";
	$tableHtml .= "<th>".$matchFormat." #</th>";
	$tableHtml .= "<th>Inn</th>";
	$tableHtml .= "<th>Runs</th>";
	$tableHtml .= "<th>Balls</th>";
	$tableHtml .= "<th>SR</th>";
	$tableHtml .= "<th>InnRtg</th>";
	$tableHtml .= "<th>LiveRtg</th>";
	$tableHtml .= "<th>Vs</th>";
	$tableHtml .= "<th>Ground</th>";
	$tableHtml .= "</tr></thead>";
	$k = 1;
	while($res = $result->fetchArray(SQLITE3_NUM)) {
	    $tableHtml .= "<td>$k</td>";
	    for ($j = 0; $j < $result->numColumns(); $j++) {
		if ($j == 0) { # match date
		    $dateMod = substr($res[$j], 0, 4)."-".substr($res[$j], 4, 2)."-".substr($res[$j], 6, 2);
		    $tableHtml .= "<td>".$dateMod."</td>";
		} elseif ($j == 1) {
		    $tableHtml .= "<td><a href=\"scorecard.php?matchFormat=".$matchFormat."&matchId=".$res[$j]."\">".$res[$j]."</a></td>";
		    $inningsId = $res[$j+1];
		    $inn = substr($inningsId, strlen($res[$j]), 1);
		    $tableHtml .= "<td>".$inn."</td>";
		    $j++;
		} elseif ($j == 3) { # not out
		    $no = $res[$j];
		    $runs = $res[$j+1];
		    $balls = $res[$j+2];
		    if ($no == 1) {
			$tableHtml .= "<td>".$runs."*</td>";
		    } else {
			$tableHtml .= "<td>".$runs."&nbsp;</td>";
		    }
		    $tableHtml .= "<td>".$balls."</td>";
		    if ($balls > 0) {
			$sr = 100 * $runs / $balls;
			$tableHtml .= "<td>".number_format(round($sr, 2), 2)."</td>";
		    } else {
			$tableHtml .= "<td></td>";
		    }
		    $j = $j + 2;
		} elseif ($j == 6) { # innings rating or live rating
		    $tableHtml .= "<td><b>".round($res[$j], 0)."</b></td>";
		    $tableHtml .= "<td><b>".round($res[$j+1], 0)."</b></td>";
		    $j++;
		} elseif ($j == 8) { # opposition
		    if ($matchFormat == "FT20") {
			if (strrpos($country, $res[$j]) === false) {
			    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\">".$res[$j]."</a></td>";
			} else {
			    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";
			}
		    } else {
			if ($country == $res[$j]) {
			    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" style='border:1px solid #A9A9A9'/></a></td>";
			} else {
			    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" style='border:1px solid #A9A9A9'/></a></td>";
			}
		    }
		    $j++;
		} elseif ($j == 10) { # ground
		    $tableHtml .= "<td>$res[$j]</td>";
		} else {
		    $tableHtml .= "<td>$res[$j]</td>";
		}
	    }
	    $tableHtml .= "</tr>";
	    $k++;
	}
	$tableHtml .= "</table><br/>";
	$tableHtml .= "</li>";
	$tableHtml .= "</div>";

	echo "<li class=\"list-group-item\">";
	if ($numInns > 20) {
	    echo "<h4>Current & Innings Rating Timeline</h4>";
	    echo "<div class=\"chart\">";
	    echo "<div id=\"chart\"></div></div>";
	    echo "<div class=\"text-center\">Innings Rating <img src=\"images/player1.png\"/>&nbsp;&nbsp;Current Rating <img src=\"images/player2.png\"/></div>";
	} else {
	    $chartWidth = 0.55*$_SESSION['screen_width'];
	    echo "<div class=\"chart\" style=\"width:".$chartWidth."px;\">";
	    echo "</div>";
	}
	echo "</li>";
	echo "</div>";
	echo $tableHtml;
    }
} else if ($disc == "Bowling") {
    # bowling career
    if ($matchFormat == "Test") {
	$sql = "select startDate, endDate, ".$matchFormatLower."s, innings, balls, runs, wickets, average, econRate, strikeRate, fiveWkts, tenWkts, rating from bowling".$matchFormat."Career where playerId=".$playerId;
    } else {
	$sql = "select startDate, endDate, innings, balls, runs, wickets, average, econRate, strikeRate, threeWkts, fiveWkts, rating from bowling".$matchFormat."Career where playerId=".$playerId;
    }
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    $res = $result->fetchArray(SQLITE3_NUM);

    $tableHtml = "";
    if (!empty($res) && $res[0] != "") {
	echo "<li class=\"list-group-item\">";
	echo "<h4>Career Summary</h4>";
	echo "<table class=\"table table-hover table-condensed\" id=\"playerTable\">";
	echo "<thead><tr>";
	if ($matchFormat == "Test") {
	    echo "<th>Span</th>";
	    echo "<th>Mat</th>";
	    echo "<th>Inns</th>";
	    echo "<th>Balls</th>";
	    echo "<th>Runs</th>";
	    echo "<th>Wkts</th>";
	    echo "<th>Ave</th>";
	    echo "<th>Econ</th>";
	    echo "<th>SR</th>";
	    echo "<th>5</th>";
	    echo "<th>10</th>";
	    echo "<th>Career Rating</th>";
	    echo "</tr></thead>";
	    echo "<tr>";
	    $numInns = $res[3];
	    echo "<td>".substr($res[0], 0, 4)."-".substr($res[1], 0, 4)."</td>"; # span
	    echo "<td>$res[2]</td><td>$res[3]</td><td>$res[4]</td><td>$res[5]</td><td>$res[6]</td>";
	    echo "<td>".number_format(round($res[7], 2), 2)."</td><td>".number_format(round($res[8], 2), 2)."</td>";
	    echo "<td>".number_format(round($res[9], 2), 1)."</td>";
	    echo "<td>$res[10]</td><td>$res[11]</td>";
	    echo "<td><b>".round($res[12], 0)."</b></td>";
	} else {
	    echo "<th>Span</th>";
	    echo "<th>Inns</th>";
	    echo "<th>Balls</th>";
	    echo "<th>Runs</th>";
	    echo "<th>Wkts</th>";
	    echo "<th>Ave</th>";
	    echo "<th>Econ</th>";
	    echo "<th>SR</th>";
	    echo "<th>3</th>";
	    echo "<th>5</th>";
	    echo "<th>Career Rating</th>";
	    echo "</tr></thead>";
	    echo "<tr>";
	    $numInns = $res[2];
	    echo "<td>".substr($res[0], 0, 4)."-".substr($res[1], 0, 4)."</td>"; # span
	    echo "<td>$res[2]</td><td>$res[3]</td><td>$res[4]</td><td>$res[5]</td>";
	    echo "<td>".number_format(round($res[6], 2), 2)."</td><td>".number_format(round($res[7], 2), 2)."</td><td>".number_format(round($res[8], 2), 1)."</td>";
	    echo "<td>$res[9]</td><td>$res[10]</td>";
	    echo "<td><b>".round($res[11], 0)."</b></td>";
	}
	echo "</tr>";
	echo "</table><br/>";
	echo "</li>";

	# bowling innings
	if ($matchFormat == "T20I" || $matchFormat == "FT20") {
	    $sql = "select t.startDate, t.".$matchFormatLower."Id, b.inningsId, b.balls, b.runs, b.wkts, b.rating, l.rating, t.team1, t.team2, t.ground from bowling".$matchFormat."Innings b, bowling".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId;
	} else {
	    $sql = "select t.startDate, t.".$matchFormatLower."Id, b.inningsId, b.balls, b.runs, b.wkts, b.rating, l.rating, t.team1, t.team2, t.ground, t.ballsPerOver from bowling".$matchFormat."Innings b, bowling".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.inningsId=l.inningsId and p.playerId=".$playerId;
	}
	$result = $db->query($sql);
	if (!$result) die("Cannot execute query.");
	$tableHtml .= "<div class=\"col-lg-6\">";
	$tableHtml .= "<li class=\"list-group-item\">";
	$tableHtml .= "<h4>Innings List</h4>";
	$tableHtml .= "<table class=\"table table-hover table-condensed\" id=\"inningsTable\">";
	$tableHtml .= "<thead><tr>";
	$tableHtml .= "<th>Inn #</th>";
	$tableHtml .= "<th>Date</th>";
	$tableHtml .= "<th>".$matchFormat." #</th>";
	$tableHtml .= "<th>Inn</th>";
	$tableHtml .= "<th>Overs</th>";
	$tableHtml .= "<th>Runs</th>";
	$tableHtml .= "<th>Wkts</th>";
	$tableHtml .= "<th>InnRtg</th>";
	$tableHtml .= "<th>LiveRtg</th>";
	$tableHtml .= "<th>Vs</th>";
	$tableHtml .= "<th>Ground</th>";
	$tableHtml .= "</tr></thead>";
	$k = 1;
	while($res = $result->fetchArray(SQLITE3_NUM)) {
	    $tableHtml .= "<td>$k</td>";
	    for ($j = 0; $j < $result->numColumns(); $j++) {
		if ($j == 0) { # match date
		    $dateMod = substr($res[$j], 0, 4)."-".substr($res[$j], 4, 2)."-".substr($res[$j], 6, 2);
		    $tableHtml .= "<td>".$dateMod."</td>";
		} elseif ($j == 1) {
		    $tableHtml .= "<td><a href=\"scorecard.php?matchFormat=".$matchFormat."&matchId=".$res[$j]."\">".$res[$j]."</a></td>";
		    $inningsId = $res[$j+1];
		    $inn = substr($inningsId, strlen($res[$j]), 1);
		    $tableHtml .= "<td>".$inn."</td>";
		    $j++;
		} elseif ($j == 3) { # overs
		    if ($matchFormat == "T20I" || $matchFormat == "FT20") {
			$bpo = 6;
		    } else {
			$bpo = $res[11];
		    }

		    if ($bpo == '') {
			$bpo = 6;
		    }
		    $balls = $res[$j] % $bpo;
		    $overs = ($res[$j]-$balls) / $bpo;
		    if ($bpo == 6) {
			$tableHtml .= "<td>".$overs.".".$balls."</td>";
		    } else {
			$tableHtml .= "<td>".$overs.".".$balls."x".$bpo."</td>";
		    }
		} elseif ($j == 6) { # innings rating or live rating
		    $tableHtml .= "<td><b>".round($res[$j], 0)."</b></td>";
		    $tableHtml .= "<td><b>".round($res[$j+1], 0)."</b></td>";
		    $j++;
		} elseif ($j == 8) { # team and opposition
		    if ($matchFormat == "FT20") {
			if (strrpos($country, $res[$j]) === false) {
			    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\">".$res[$j]."</a></td>";
			} else {
			    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";
			}
		    } else {
			if ($country == $res[$j]) {
			    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" style='border:1px solid #A9A9A9'/></a></td>";
			} else {
			    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" style='border:1px solid #A9A9A9'/></a></td>";
			}
		    }
		    $j++;
		} elseif ($j == 10) { # ground
		    $tableHtml .= "<td>$res[$j]</td>";
		} elseif ($j == 11) { # ignore balls per over
		} else {
		    $tableHtml .= "<td>$res[$j]</td>";
		}
	    }
	    $tableHtml .= "</tr>";
	    $k++;
	}
	$tableHtml .= "</table><br/>";
	$tableHtml .= "</li>";
	$tableHtml .= "</div>";

	echo "<li class=\"list-group-item\">";
	if ($numInns > 20) {
	    echo "<h4>Current & Innings Rating Timeline</h4>";
	    echo "<div class=\"chart\">";
	    echo "<div id=\"chart\"></div></div>";
	    echo "<div class=\"text-center\">Match Rating <img src=\"images/player1.png\"/>&nbsp;&nbsp;Current Rating <img src=\"images/player2.png\"/></div>";
	} else {
	    $chartWidth = 0.55*$_SESSION['screen_width'];
	    echo "<div class=\"chart\" style=\"width:".$chartWidth."px;\">";
	    echo "</div>";
	}
	echo "</li>";
	echo "</div>";
	echo $tableHtml;
    }
} else if ($disc == "All-Round") {
    # all-round career
    if ($matchFormat == "Test") {
	$sql = "select startDate, endDate, ".$matchFormatLower."s, runs, battingAverage, hundreds, wickets, bowlingAverage, fiveWkts, hundredFiveWkts, rating from allRound".$matchFormat."Career where playerId=".$playerId;
    } else {
	if ($matchFormat == "FT20" || $matchFormat == "T20I") {
	    $sql = "select startDate, endDate, ".$matchFormatLower."s, runs, battingAverage, fifties, wickets, bowlingAverage, threeWkts, thirtyTwoWkts, rating from allRound".$matchFormat."Career where playerId=".$playerId;
	} else {
	    $sql = "select startDate, endDate, ".$matchFormatLower."s, runs, battingAverage, fifties, wickets, bowlingAverage, threeWkts, fiftyThreeWkts, rating from allRound".$matchFormat."Career where playerId=".$playerId;
	}
    }
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    $res = $result->fetchArray(SQLITE3_NUM);

    $tableHtml = "";
    if (!empty($res) && $res[0] != "") {
	echo "<li class=\"list-group-item\">";
	echo "<h4>Career Summary</h4>";
	echo "<table class=\"table table-hover table-condensed\" id=\"playerTable\">";
	echo "<thead><tr>";
	if ($matchFormat == "Test") {
	    echo "<th>Span</th>";
	    echo "<th>Mat</th>";
	    echo "<th>Runs</th>";
	    echo "<th>Bat Ave</th>";
	    echo "<th>100</th>";
	    echo "<th>Wkts</th>";
	    echo "<th>Bowl Ave</th>";
	    echo "<th>5</th>";
	    echo "<th>100r+5w</th>";
	    echo "<th>Career Rating</th>";
	    echo "</tr></thead>";
	    echo "<tr>";
	    $numMat = $res[2];
	    echo "<td>".substr($res[0], 0, 4)."-".substr($res[1], 0, 4)."</td>"; # span
	    echo "<td>$res[2]</td><td>$res[3]</td>";
	    echo "<td>".number_format(round($res[4], 2), 2)."</td>";
	    echo "<td>$res[5]</td><td>$res[6]</td>";
	    echo "<td>".number_format(round($res[7], 2), 2)."</td>";
	    echo "<td>$res[8]</td><td>$res[9]</td>";
	    echo "<td><b>".round($res[10], 0)."</b></td>";
	} else {
	    echo "<th>Span</th>";
	    echo "<th>Mat</th>";
	    echo "<th>Runs</th>";
	    echo "<th>Bat Ave</th>";
	    echo "<th>50</th>";
	    echo "<th>Wkts</th>";
	    echo "<th>Bowl Ave</th>";
	    echo "<th>3</th>";
	    if ($matchFormat == "ODI") {
		echo "<th>50r+3w</th>";
	    } else {
		echo "<th>30r+2w</th>";
	    }
	    echo "<th>Career Rating</th>";
	    echo "</tr></thead>";
	    echo "<tr>";
	    $numMat = $res[2];
	    echo "<td>".substr($res[0], 0, 4)."-".substr($res[1], 0, 4)."</td>"; # span
	    echo "<td>$res[2]</td><td>$res[3]</td>";
	    echo "<td>".number_format(round($res[4], 2), 2)."</td>";
	    echo "<td>$res[5]</td><td>$res[6]</td>";
	    echo "<td>".number_format(round($res[7], 2), 2)."</td>";
	    echo "<td>$res[8]</td><td>$res[9]</td>";
	    echo "<td><b>".round($res[10], 0)."</b></td>";
	}
	echo "</tr>";
	echo "</table><br/>";
	echo "</li>";

	# all-round matches
	if ($matchFormat == "Test") {
	    $sql = "select t.startDate, b.".$matchFormatLower."Id, b.notOut1, b.runs1, b.notOut2, b.runs2, b.wkts1, b.bowlRuns1, b.wkts2, b.bowlRuns2, b.rating, l.rating, t.team1, t.team2, t.ground from allRound".$matchFormat."Match b, allRound".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId;
	} else {
	    $sql = "select t.startDate, b.".$matchFormatLower."Id, b.notOut, b.runs, b.wkts, b.bowlRuns, b.rating, l.rating, t.team1, t.team2, t.ground from allRound".$matchFormat."Match b, allRound".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId;
	}

	$result = $db->query($sql);
	if (!$result) die("Cannot execute query.");
	$tableHtml .= "<div class=\"col-lg-6\">";
	$tableHtml .= "<li class=\"list-group-item\">";
	$tableHtml .= "<h4>Match List</h4>";
	$tableHtml .= "<table class=\"table table-hover table-condensed\" id=\"inningsTable\">";
	$tableHtml .= "<thead><tr>";
	$tableHtml .= "<th>Mat #</th>";
	$tableHtml .= "<th>Date</th>";
	$tableHtml .= "<th>".$matchFormat." #</th>";
	if ($matchFormat == "Test") {
	    $tableHtml .= "<th>Runs1</th>";
	    $tableHtml .= "<th>Runs2</th>";
	    $tableHtml .= "<th>Wkts1</th>";
	    $tableHtml .= "<th>Wkts2</th>";
	} else {
	    $tableHtml .= "<th>Runs</th>";
	    $tableHtml .= "<th>Wkts</th>";
	}
	$tableHtml .= "<th>MatRtg</th>";
	$tableHtml .= "<th>LiveRtg</th>";
	$tableHtml .= "<th>Vs</th>";
	$tableHtml .= "<th>Ground</th>";
	$tableHtml .= "</tr></thead>";
	$k = 1;
	while($res = $result->fetchArray(SQLITE3_NUM)) {
	    $tableHtml .= "<td>$k</td>";
	    for ($j = 0; $j < $result->numColumns(); $j++) {
		if ($j == 0) { # match date
		    $dateMod = substr($res[$j], 0, 4)."-".substr($res[$j], 4, 2)."-".substr($res[$j], 6, 2);
		    $tableHtml .= "<td>".$dateMod."</td>";
		} elseif ($j == 1) {
		    $tableHtml .= "<td><a href=\"scorecard.php?matchFormat=".$matchFormat."&matchId=".$res[$j]."\">".$res[$j]."</a></td>";
		} else {
		    if ($matchFormat == "Test") {
			if ($j == 2) { # not out
			    $no1 = $res[$j];
			    $runs1 = $res[$j+1];
			    $no2 = $res[$j+2];
			    $runs2 = $res[$j+3];
			    if ($no1 == 1) {
				$tableHtml .= "<td>".$runs1."*</td>";
			    } else {
				$tableHtml .= "<td>".$runs1."&nbsp;</td>";
			    }
			    if ($no2 == 1) {
				$tableHtml .= "<td>".$runs2."*</td>";
			    } else {
				$tableHtml .= "<td>".$runs2."&nbsp;</td>";
			    }
			    $j = $j + 3;
			} elseif ($j == 6) { # bowling figures
			    $wkts1 = $res[$j];
			    $bowlRuns1 = $res[$j+1];
			    $wkts2 = $res[$j+2];
			    $bowlRuns2 = $res[$j+3];
			    if ($wkts1 == "" and $bowlRuns1 == "") {
				$tableHtml .= "<td></td>";
			    } else {
				$tableHtml .= "<td>".$wkts1."/".$bowlRuns1."</td>";
			    }
			    if ($wkts2 == "" and $bowlRuns2 == "") {
				$tableHtml .= "<td></td>";
			    } else {
				$tableHtml .= "<td>".$wkts2."/".$bowlRuns2."</td>";
			    }
			    $j = $j + 3;
			} elseif ($j == 10) { # innings rating or live rating
			    $tableHtml .= "<td><b>".round($res[$j], 0)."</b></td>";
			    $tableHtml .= "<td><b>".round($res[$j+1], 0)."</b></td>";
			    $j++;
			} elseif ($j == 12) { # team and opposition
			    if ($matchFormat == "FT20") {
				if (strrpos($country, $res[$j]) === false) {
				    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\">".$res[$j]."</a></td>";
				} else {
				    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";
				}
			    } else {
				if ($country == $res[$j]) {
				    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" style='border:1px solid #A9A9A9'/></a></td>";
				} else {
				    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" style='border:1px solid #A9A9A9'/></a></td>";
				}
			    }
			    $j++;
			} else {
			    $tableHtml .= "<td>$res[$j]</td>";
			}
		    } else {
			if ($j == 2) { # not out
			    $no = $res[$j];
			    $runs = $res[$j+1];
			    if ($no == 1) {
				$tableHtml .= "<td>".$runs."*</td>";
			    } else {
				$tableHtml .= "<td>".$runs."&nbsp;</td>";
			    }
			    $j++;
			} elseif ($j == 4) { # bowling figures
			    $wkts = $res[$j];
			    $bowlRuns = $res[$j+1];
			    $tableHtml .= "<td>".$wkts."/".$bowlRuns."</td>";
			    $j++;
			} elseif ($j == 6) { # innings rating or live rating
			    $tableHtml .= "<td><b>".round($res[$j], 0)."</b></td>";
			    $tableHtml .= "<td><b>".round($res[$j+1], 0)."</b></td>";
			    $j++;
			} elseif ($j == 8) { # team and opposition
			    if ($matchFormat == "FT20") {
				if (strrpos($country, $res[$j]) === false) {
				    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\">".$res[$j]."</a></td>";
				} else {
				    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";
				}
			    } else {
				if ($country == $res[$j]) {
				    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" style='border:1px solid #A9A9A9'/></a></td>";
				} else {
				    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" style='border:1px solid #A9A9A9'/></a></td>";
				}
			    }
			    $j++;
			} else {
			    $tableHtml .= "<td>$res[$j]</td>";
			}
		    }
		}
	    }
	    $tableHtml .= "</tr>";
	    $k++;
	}
	$tableHtml .= "</table><br/>";
	$tableHtml .= "</li>";
	$tableHtml .= "</div>";

	echo "<li class=\"list-group-item\">";
	if ($numMat > 20) {
	    echo "<h4>Current & Match Rating Timeline</h4>";
	    echo "<div class=\"chart\">";
	    echo "<div id=\"chart\"></div></div>";
	    echo "<div class=\"text-center\">Innings Rating <img src=\"images/player1.png\"/>&nbsp;&nbsp;Current Rating <img src=\"images/player2.png\"/></div>";
	} else {
	    $chartWidth = 0.55*$_SESSION['screen_width'];
	    echo "<div class=\"chart\" style=\"width:".$chartWidth."px;\">";
	    echo "</div>";
	}
	echo "</li>";
	echo "</div>";
	echo $tableHtml;
    }
} else if ($disc == "Fielding") {
    #fielding career
    $sql = "select startDate, endDate, ".$matchFormatLower."s, keeper, catches, droppedCatches, dropRate, matPerDrop, greatCatches, directHits, runsSaved, stumpings, missedStumpings, stumpRate, rating from fielding".$matchFormat."Career where playerId=".$playerId;

    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    $res = $result->fetchArray(SQLITE3_NUM);

    $tableHtml = "";
    if (!empty($res) && $res[0] != "") {
	$keeper = $res[3];
	echo "<li class=\"list-group-item\">";
	echo "<h4>Career Summary</h4>";
	echo "<table class=\"table table-hover table-condensed\" id=\"playerTable\">";
	echo "<thead><tr>";
	echo "<th>Span</th>";
	echo "<th>Mat</th>";
	echo "<th>Keeper</th>";
	echo "<th>Catches</th>";
	echo "<th>Drops</th>";
	echo "<th>Drop%</th>";
	echo "<th>Mat/Drop</th>";
	echo "<th>GreatCatches</th>";
	if ($keeper == 1) {
	    echo "<th>Stump</th>";
	    echo "<th>MissStump</th>";
	    echo "<th>Drop%</th>";
	} else {
	    echo "<th>DirectHit</th>";
	    echo "<th>RunsSaved</th>";
	}
	echo "<th>Career Rating</th>";
	echo "</tr></thead>";
	echo "<tr>";
	$numMat = $res[2];
	echo "<td>".substr($res[0], 0, 4)."-".substr($res[1], 0, 4)."</td>"; # span
	echo "<td>$res[2]</td><td>$res[3]</td><td>$res[4]</td><td>$res[5]</td>";
	echo "<td>".number_format(round($res[6] * 100, 2), 2)."</td>";
	echo "<td>".number_format(round($res[7], 1), 1)."</td>";
	echo "<td>$res[8]</td>";
	if ($keeper == 1) {
	    echo "<td>$res[11]</td><td>$res[12]</td>";
	    echo "<td>".number_format(round($res[13], 2), 2)."</td>";
	} else {
	    echo "<td>$res[9]</td><td>$res[10]</td>";
	}
	echo "<td><b>".round($res[14], 0)."</b></td>";
	echo "</tr>";
	echo "</table><br/>";
	echo "</li>";

	# fielding matches
	if ($keeper == 1) {
	    $sql = "select t.startDate, b.".$matchFormatLower."Id, b.catches, b.droppedCatches, b.greatCatches, b.stumpings, b.missedStumpings, b.rating, l.rating, t.team1, t.team2, t.ground from fielding".$matchFormat."Match b, fielding".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId;
	} else {
	    $sql = "select t.startDate, b.".$matchFormatLower."Id, b.catches, b.droppedCatches, b.greatCatches, b.directHits, b.runsSaved, b.rating, l.rating, t.team1, t.team2, t.ground from fielding".$matchFormat."Match b, fielding".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId;
	}

	$result = $db->query($sql);
	if (!$result) die("Cannot execute query.");
	$tableHtml .= "<div class=\"col-lg-6\">";
	$tableHtml .= "<li class=\"list-group-item\">";
	$tableHtml .= "<h4>Match List</h4>";
	$tableHtml .= "<table class=\"table table-hover table-condensed\" id=\"inningsTable\">";
	$tableHtml .= "<thead><tr>";
	$tableHtml .= "<th>Mat #</th>";
	$tableHtml .= "<th>Date</th>";
	$tableHtml .= "<th>".$matchFormat." #</th>";
	$tableHtml .= "<th>Cat</th>";
	$tableHtml .= "<th>Drops</th>";
	$tableHtml .= "<th>GrtCat</th>";
	if ($keeper == 1) {
	    $tableHtml .= "<th>Stmp</th>";
	    $tableHtml .= "<th>MisStp</th>";
	} else {
	    $tableHtml .= "<th>DirHit</th>";
	    $tableHtml .= "<th>Run</th>";
	}
	$tableHtml .= "<th>MatRtg</th>";
	$tableHtml .= "<th>LiveRtg</th>";
	$tableHtml .= "<th>Vs</th>";
	$tableHtml .= "<th>Ground</th>";
	$tableHtml .= "</tr></thead>";
	$k = 1;
	while($res = $result->fetchArray(SQLITE3_NUM)) {
	    $tableHtml .= "<td>$k</td>";
	    for ($j = 0; $j < $result->numColumns(); $j++) {
		if ($j == 0) { # match date
		    $dateMod = substr($res[$j], 0, 4)."-".substr($res[$j], 4, 2)."-".substr($res[$j], 6, 2);
		    $tableHtml .= "<td>".$dateMod."</td>";
		} elseif ($j == 1) {
		    $tableHtml .= "<td><a href=\"scorecard.php?matchFormat=".$matchFormat."&matchId=".$res[$j]."\">".$res[$j]."</a></td>";
		} elseif ($j == 7) { # match rating or live rating
		    $tableHtml .= "<td><b>".round($res[$j], 0)."</b></td>";
		    $tableHtml .= "<td><b>".round($res[$j+1], 0)."</b></td>";
		    $j++;
		} elseif ($j == 9) { # team and opposition
		    if ($matchFormat == "FT20") {
			if (strrpos($country, $res[$j]) === false) {
			    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\">".$res[$j]."</a></td>";
			} else {
			    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";
			}
		    } else {
			if ($country == $res[$j]) {
			    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" style='border:1px solid #A9A9A9'/></a></td>";
			} else {
			    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" style='border:1px solid #A9A9A9'/></a></td>";
			}
		    }
		    $j++;
		} else {
		    $tableHtml .= "<td>$res[$j]</td>";
		}
	    }
	    $tableHtml .= "</tr>";
	    $k++;
	}
	$tableHtml .= "</table><br/>";
	$tableHtml .= "</li>";
	$tableHtml .= "</div>";

	echo "<li class=\"list-group-item\">";
	if ($numMat > 20) {
	    echo "<h4>Current & Match Rating Timeline</h4>";
	    echo "<div class=\"chart\">";
	    echo "<div id=\"chart\"></div></div>";
	    echo "<div class=\"text-center\">Match Rating <img src=\"images/player1.png\"/>&nbsp;&nbsp;Current Rating <img src=\"images/player2.png\"/></div>";
	} else {
	    $chartWidth = 0.55*$_SESSION['screen_width'];
	    echo "<div class=\"chart\" style=\"width:".$chartWidth."px;\">";
	    echo "</div>";
	}
	echo "</li>";
	echo "</div>";
	echo $tableHtml;
    }
} else if ($disc == "Win Shares") {
    #win shares career
    $sql = "select startDate, endDate, ".$matchFormatLower."s, battingAdjWSAvg, bowlingAdjWSAvg, fieldingAdjWSAvg, totalAdjWSAvg, totalRating from winShares".$matchFormat."Career where playerId=".$playerId;

    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    $res = $result->fetchArray(SQLITE3_NUM);

    $tableHtml = "";
    if (!empty($res) && $res[0] != "") {
	$keeper = $res[3];
	echo "<li class=\"list-group-item\">";
	echo "<h4>Career Summary</h4>";
	echo "<table class=\"table table-hover table-condensed\" id=\"playerTable\">";
	echo "<thead><tr>";
	echo "<th>Span</th>";
	echo "<th>Mat</th>";
	echo "<th>BatAvg</th>";
	echo "<th>BowlAvg</th>";
	echo "<th>FieldAvg</th>";
	echo "<th>TotalAvg</th>";
	echo "<th>Career Rating</th>";
	echo "</tr></thead>";
	echo "<tr>";
	$numMat = $res[2];
	echo "<td>".substr($res[0], 0, 4)."-".substr($res[1], 0, 4)."</td>"; # span
	echo "<td>$res[2]</td>";
	echo "<td>".number_format(round($res[3], 3), 3)."</td>";
	echo "<td>".number_format(round($res[4], 3), 3)."</td>";
	echo "<td>".number_format(round($res[5], 3), 3)."</td>";
	echo "<td>".number_format(round($res[6], 3), 3)."</td>";
	echo "<td><b>".round($res[7], 3)."</b></td>";
	echo "</tr>";
	echo "</table><br/>";
	echo "</li>";

	# win shares matches
	$sql = "select t.startDate, b.".$matchFormatLower."Id, b.battingAdjWS, b.bowlingAdjWS, b.fieldingAdjWS, b.totalAdjWS, l.totalRating, t.team1, t.team2, t.ground from winShares".$matchFormat."Match b, winShares".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId;
	$result = $db->query($sql);
	if (!$result) die("Cannot execute query.");
	$tableHtml .= "<div class=\"col-lg-6\">";
	$tableHtml .= "<li class=\"list-group-item\">";
	$tableHtml .= "<h4>Match List</h4>";
	$tableHtml .= "<table class=\"table table-hover table-condensed\" id=\"inningsTable\">";
	$tableHtml .= "<thead><tr>";
	$tableHtml .= "<th>Mat #</th>";
	$tableHtml .= "<th>Date</th>";
	$tableHtml .= "<th>".$matchFormat." #</th>";
	$tableHtml .= "<th>Bat</th>";
	$tableHtml .= "<th>Bowl</th>";
	$tableHtml .= "<th>Field</th>";
	$tableHtml .= "<th>Total</th>";
	$tableHtml .= "<th>LiveRtg</th>";
	$tableHtml .= "<th>Vs</th>";
	$tableHtml .= "<th>Ground</th>";
	$tableHtml .= "</tr></thead>";
	$k = 1;
	while($res = $result->fetchArray(SQLITE3_NUM)) {
	    $tableHtml .= "<td>$k</td>";
	    for ($j = 0; $j < $result->numColumns(); $j++) {
		if ($j == 0) { # match date
		    $dateMod = substr($res[$j], 0, 4)."-".substr($res[$j], 4, 2)."-".substr($res[$j], 6, 2);
		    $tableHtml .= "<td>".$dateMod."</td>";
		} elseif ($j == 1) {
		    $tableHtml .= "<td><a href=\"scorecard.php?matchFormat=".$matchFormat."&matchId=".$res[$j]."\">".$res[$j]."</a></td>";
		} elseif ($j == 2) { # match rating or live rating
		    $tableHtml .= "<td>".number_format(round($res[$j], 3), 3)."</td>";
		    $tableHtml .= "<td>".number_format(round($res[$j+1], 3), 3)."</td>";
		    $tableHtml .= "<td>".number_format(round($res[$j+2], 3), 3)."</td>";
		    $tableHtml .= "<td><b>".number_format(round($res[$j+3], 3), 3)."</b></td>";
		    $tableHtml .= "<td><b>".number_format(round($res[$j+4], 3), 3)."</b></td>";
		    $j = $j + 4;
		} elseif ($j == 7) { # team and opposition
		    if ($matchFormat == "FT20") {
			if (strrpos($country, $res[$j]) === false) {
			    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\">".$res[$j]."</a></td>";
			} else {
			    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";
			}
		    } else {
			if ($country == $res[$j]) {
			    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" style='border:1px solid #A9A9A9'/></a></td>";
			} else {
			    $tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" style='border:1px solid #A9A9A9'/></a></td>";
			}
		    }
		    $j++;
		} else {
		    $tableHtml .= "<td>$res[$j]</td>";
		}
	    }
	    $tableHtml .= "</tr>";
	    $k++;
	}
	$tableHtml .= "</table><br/>";
	$tableHtml .= "</li>";
	$tableHtml .= "</div>";

	echo "<li class=\"list-group-item\">";
	if ($numMat > 20) {
	    echo "<h4>Current & Match Rating Timeline</h4>";
	    echo "<div class=\"chart\">";
	    echo "<div id=\"chart\"></div></div>";
	    echo "<div class=\"text-center\">Match Rating <img src=\"images/player1.png\"/>&nbsp;&nbsp;Current Rating <img src=\"images/player2.png\"/></div>";
	} else {
	    $chartWidth = 0.55*$_SESSION['screen_width'];
	    echo "<div class=\"chart\" style=\"width:".$chartWidth."px;\">";
	    echo "</div>";
	}
	echo "</li>";
	echo "</div>";
	echo $tableHtml;
    }
}
echo "</ul>";
echo "</div>";
echo "</div>";
echo "</div>";
$db->close();

if ($playerFound == 0) {
    echo "<h2>Player not found.</h2>";
}
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
