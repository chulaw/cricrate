<!DOCTYPE html>
<?php
session_start();
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
if(isset($_GET['span'])) {
   $span = $_GET['span'];
} else {
   $span = "1877-2099";
}
if(isset($_GET['team'])) {
   $team = $_GET['team'];
} else {
   $team = "All teams";
}

if ($matchFormat == "Test") {
    $spans = array("1877-2099", "1877-1914", "1915-1929", "1930-1939", "1940-1949", "1950-1959", "1960-1969", "1970-1979", "1980-1989", "1990-1999", "2000-2009", "2010-2019");
} else if ($matchFormat == "ODI") {
    $spans = array("1971-2099", "1971-1984", "1985-1989", "1990-1994", "1995-1999", "2000-2004", "2005-2009", "2010-2014", "2015-2019");
} else if ($matchFormat == "T20I") {
    $spans = array("2005-2099", "2005-2009", "2010-2014", "2015-2019");
} else if ($matchFormat == "FT20") {
    $spans = array("2008-2099", "2008-2010", "2011-2014", "2015-2018");
}

if (!in_array($span, $spans)) {
    $span = $spans[0];
    $_GET['span'] = $spans[0];
}

if ($matchFormat == "Test") {
    if ($disc == "Batting") {
	$xValMod = array("average"=>"Average", "runs"=>"Runs", "strikeRate"=>"Strike Rate", "fifties"=>"Fifties", "hundreds"=>"Hundreds", "rating"=>"Rating", "innings"=>"Innings", "tests"=>"Tests");
	$yValMod = array("strikeRate"=>"Strike Rate", "average"=>"Average", "runs"=>"Runs", "fifties"=>"Fifties", "hundreds"=>"Hundreds", "rating"=>"Rating", "innings"=>"Innings", "tests"=>"Tests");
    } else if ($disc == "Bowling") {
	$xValMod = array("average"=>"Average", "runs"=>"Runs", "strikeRate"=>"Strike Rate", "balls"=>"Balls", "wickets"=>"Wickets", "econRate"=>"Econ Rate", "fiveWkts"=>"Five Wkts", "tenWkts"=>"Ten Wkts", "rating"=>"Rating", "innings"=>"Innings", "tests"=>"Tests");
	$yValMod = array("strikeRate"=>"Strike Rate", "average"=>"Average", "runs"=>"Runs", "balls"=>"Balls", "wickets"=>"Wickets", "econRate"=>"Econ Rate", "fiveWkts"=>"Five Wkts", "tenWkts"=>"Ten Wkts", "rating"=>"Rating", "innings"=>"Innings", "tests"=>"Tests");
    } else if ($disc == "All-Round") {
	$xValMod = array("battingAverage"=>"Batting Average", "bowlingAverage"=>"Bowling Average", "runs"=>"Runs", "wickets"=>"Wickets", "hundreds"=>"Hundreds", "fiveWkts"=>"Five Wkts", "hundredFiveWkts"=>"Hundred Runs + Five Wkts", "rating"=>"Rating", "tests"=>"Tests");
	$yValMod = array("bowlingAverage"=>"Bowling Average", "battingAverage"=>"Batting Average", "runs"=>"Runs", "wickets"=>"Wickets", "hundreds"=>"Hundreds", "fiveWkts"=>"Five Wkts", "hundredFiveWkts"=>"Hundred Runs  + Five Wkts", "rating"=>"Rating", "tests"=>"Tests");
    } else if ($disc == "Team") {
	$xValMod = array("wins"=>"Wins", "losses"=>"Losses", "draws"=>"Draws", "winPct"=>"Win %", "rating"=>"Rating", "tests"=>"Tests");
	$yValMod = array("losses"=>"Losses", "wins"=>"Wins", "draws"=>"Draws", "winPct"=>"Win %", "rating"=>"Rating", "tests"=>"Tests");
    }
} else if ($matchFormat == "ODI" || $matchFormat == "T20I" || $matchFormat == "FT20") {
    if ($disc == "Batting") {
	$xValMod = array("average"=>"Average", "runs"=>"Runs", "strikeRate"=>"Strike Rate", "fifties"=>"Fifties", "hundreds"=>"Hundreds", "rating"=>"Rating", "innings"=>"Innings");
	$yValMod = array("strikeRate"=>"Strike Rate", "average"=>"Average", "runs"=>"Runs", "fifties"=>"Fifties", "hundreds"=>"Hundreds", "rating"=>"Rating", "innings"=>"Innings");
    } else if ($disc == "Bowling") {
	$xValMod = array("average"=>"Average", "runs"=>"Runs", "strikeRate"=>"Strike Rate", "balls"=>"Balls", "wickets"=>"Wickets", "econRate"=>"Econ Rate", "fiveWkts"=>"Five Wkts", "threeWkts"=>"Three Wkts", "rating"=>"Rating", "innings"=>"Innings");
	$yValMod = array("strikeRate"=>"Strike Rate", "average"=>"Average", "runs"=>"Runs", "balls"=>"Balls", "wickets"=>"Wickets", "econRate"=>"Econ Rate", "fiveWkts"=>"Five Wkts", "threeWkts"=>"Three Wkts", "rating"=>"Rating", "innings"=>"Innings");
    } else if ($disc == "All-Round") {
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
    }  else if ($disc == "Team") {
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

if ($disc == "Fielding" || $disc == "Win Shares") {
    $xValMod = array("average"=>"Average", "runs"=>"Runs", "strikeRate"=>"Strike Rate", "fifties"=>"Fifties", "hundreds"=>"Hundreds", "rating"=>"Rating", "innings"=>"Innings", "tests"=>"Tests");
    $yValMod = array("strikeRate"=>"Strike Rate", "average"=>"Average", "runs"=>"Runs", "fifties"=>"Fifties", "hundreds"=>"Hundreds", "rating"=>"Rating", "innings"=>"Innings", "tests"=>"Tests");
}

$xKeys = array_keys($xValMod);
$yKeys = array_keys($yValMod);
if(isset($_GET['xVal'])) {
    if (in_array($_GET['xVal'], $xKeys)) {
	$xVal = $_GET['xVal'];
    } else {
	$xVal = $xKeys[0];
    }
} else {
    $xVal = $xKeys[0];
}

if(isset($_GET['yVal'])) {
    if (in_array($_GET['yVal'], $yKeys)) {
	$yVal = $_GET['yVal'];
    } else {
	$yVal = $yKeys[0];
    }
} else {
    $yVal = $yKeys[0];
}

$xAxis = $xValMod[$xVal];
$yAxis = $yValMod[$yVal];

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

if(isset($_SESSION['screen_width']) AND isset($_SESSION['screen_height'])){
} else if(isset($_REQUEST['width']) AND isset($_REQUEST['height'])) {
    $_SESSION['screen_width'] = $_REQUEST['width'];
    $_SESSION['screen_height'] = $_REQUEST['height'];

    header("Location: career.php?matchFormat=".$matchFormat."&disc=".$disc."&span=".$span."&team=".$team."&xVal=".$xVal."&yVal=".$yVal);
} else {
    echo '<script type="text/javascript">window.location = "' . $_SERVER['PHP_SELF'] . '?matchFormat='.$matchFormat.'&disc='.$disc.'&span='.$span.'&team='.$team.'&xVal='.$xVal.'&yVal='.$yVal.'&width="+screen.width+"&height="+screen.height;</script>';
}

?>
<html>
<head>
    <title>cricrate | Career Ratings - <?php echo($matchFormat." ".$disc); ?></title>
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

    var chartWidth = screen.width * 0.3;
    var chartHeight = screen.height * 0.45;
    if (isMobile == true) {
	chartWidth = chartWidth * 2;
    }

    var matchFormat = <?php echo json_encode($_GET['matchFormat']); ?>;
    var disc = <?php echo json_encode($_GET['disc']); ?>;
    var batBowl = disc.toLowerCase();
    if (batBowl == "all-round") {
       batBowl = "allRound";
    } else if (batBowl == "win shares") {
       batBowl = "winShares";
    }
    var xVal = <?php echo json_encode($xVal); ?>;
    var yVal = <?php echo json_encode($yVal); ?>;
    var xAxis = <?php echo json_encode($xAxis); ?>;
    var yAxis = <?php echo json_encode($yAxis); ?>;
    var span = <?php echo json_encode($span); ?>;
    var team = <?php echo json_encode($team); ?>;

    if (batBowl != "fielding" && batBowl != "winShares") {
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);
   }

    function drawChart() {
       var jsonData = $.ajax({
	   url: "charts/career.php?matchFormat="+matchFormat+"&batBowl="+batBowl+"&xVal="+xVal+"&yVal="+yVal+"&span="+span+"&team="+team,
	   dataType:"json",
	   async: false
	   }).responseText;

       // Create our data table out of JSON data loaded from server.
       var data = new google.visualization.DataTable(jsonData);

       var xMax = data.getColumnRange(1).max;
       var xMin = data.getColumnRange(1).min;
       var yMax = data.getColumnRange(2).max;
       var yMin = data.getColumnRange(2).min;


	var options = {
	    fontName: "Lucida Sans Unicode",
	    backgroundColor: {
			   backgroundColor: '#FFFFFF',
			   fill:'#FFFFFF'
			   },
	    chartArea: {
	       width: "85%",
	       height: "80%",
	       left: "10%",
	       top: "5%"
	       },
	    width: chartWidth,
	    height: chartHeight,
	   hAxis: {
		   title: xAxis,
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
		    viewWindow: {
				max: xMax * 1.05,
				min: xMin * 0.95,
			    },
		   },
	   vAxis: {
		   title: yAxis,
		   format: "####",
		   viewWindowMode: "maximized",
		   gridlines: {count: 12},
		   textStyle: {
			       color: '#000000',
			       fontSize: 11
			       },
		   titleTextStyle: {
				   color: '#000000',
				   italic: "false",
				   },
		    viewWindow: {
				    max: yMax * 1.05,
				    min: yMin * 0.95,
				},
	       },
	    legend: 'bottom',
	    crosshair: { trigger: 'both' },
	    sizeAxis: {minValue: 1,  maxSize: 5},
	    animation: {
			"startup": true,
			duration: 1000,
			easing: 'inAndOut',
			},
	    bubble: {
		    textStyle: {
		      color: 'transparent'
		    }
		  }
        };

       var chart = new google.visualization.BubbleChart(document.getElementById('chart'));
       chart.draw(data, options);
    }

    $(document).ready(function() {
       $('#ratingsTable').DataTable( {
      "pageLength": 16,
      "lengthMenu": [[16, 25, 50, 100, -1], [16, 25, 50, 100, "All"]],
       "order": [[ 0, "asc" ]],
   } );

      $('#ratingsTable2').DataTable( {
       "pageLength": 16,
       "lengthMenu": [[16, 25, 50, 100, -1], [16, 25, 50, 100, "All"]],
       "order": [[ 0, "asc" ]],
   } );
   } );

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

    chartForms = function(){
	    window.document.chartForm.submit();
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
                            <li><a href="methodology.php?matchFormat=Test&disc=Team"><b>Test</b></a></li>
                            <li><a href="current.php?matchFormat=Test&disc=Team">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "Team" && $matchFormat == "Test") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=Test&disc=Team\">&nbsp;&nbsp;Overall<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=Test&disc=Team\">&nbsp;&nbsp;Overall</a></li>"; } ?>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=ODI&disc=Team"><b>ODI</b></a></li>
                            <li><a href="current.php?matchFormat=ODI&disc=Team">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "Team" && $matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=ODI&disc=Team\">&nbsp;&nbsp;Overall<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=ODI&disc=Team\">&nbsp;&nbsp;Overall</a></li>"; } ?>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=T20I&disc=Team"><b>T20I</b></a></li>
                            <li><a href="current.php?matchFormat=T20I&disc=Team">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "Team" && $matchFormat == "T20I") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=T20I&disc=Team\">&nbsp;&nbsp;Overall<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=T20I&disc=Team\">&nbsp;&nbsp;Overall</a></li>"; } ?>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=Team"><b>FT20</b></a></li>
                            <li><a href="current.php?matchFormat=FT20&disc=Team">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "Team" && $matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=FT20&disc=Team\">&nbsp;&nbsp;Overall<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=FT20&disc=Team\">&nbsp;&nbsp;Overall</a></li>"; } ?>
                        </ul>
                    </li>
                    <?php if ($disc == "Batting") { echo "<li class=\"active\">"; } else { echo "<li class=\"dropdown\">"; } ?>
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Batting <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="methodology.php?matchFormat=Test&disc=Batting"><b>Test</b></a></li>
                            <li><a href="current.php?matchFormat=Test&disc=Batting">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "Batting" && $matchFormat == "Test") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=Test&disc=Batting\">&nbsp;&nbsp;Career<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=Test&disc=Batting\">&nbsp;&nbsp;Career</a></li>"; } ?>
                            <li><a href="performances.php?matchFormat=Test&disc=Batting">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=ODI&disc=Batting"><b>ODI</b></a></li>
                            <li><a href="current.php?matchFormat=ODI&disc=Batting">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "Batting" && $matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=ODI&disc=Batting\">&nbsp;&nbsp;Career<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=ODI&disc=Batting\">&nbsp;&nbsp;Career</a></li>"; } ?>
                            <li><a href="performances.php?matchFormat=ODI&disc=Batting">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=T20I&disc=Batting"><b>T20I</b></a></li>
                            <li><a href="current.php?matchFormat=T20I&disc=Batting">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "Batting" && $matchFormat == "T20I") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=T20I&disc=Batting\">&nbsp;&nbsp;Career<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=T20I&disc=Batting\">&nbsp;&nbsp;Career</a></li>"; } ?>
                            <li><a href="performances.php?matchFormat=T20I&disc=Batting">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=Batting"><b>FT20</b></a></li>
                            <li><a href="current.php?matchFormat=FT20&disc=Batting">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "Batting" && $matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=FT20&disc=Batting\">&nbsp;&nbsp;Career<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=FT20&disc=Batting\">&nbsp;&nbsp;Career</a></li>"; } ?>
                            <li><a href="performances.php?matchFormat=FT20&disc=Batting">&nbsp;&nbsp;Performances</a></li>
                        </ul>
                    </li>
                    <?php if ($disc == "Bowling") { echo "<li class=\"active\">"; } else { echo "<li class=\"dropdown\">"; } ?>
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Bowling <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="methodology.php?matchFormat=Test&disc=Bowling"><b>Test</b></a></li>
                            <li><a href="current.php?matchFormat=Test&disc=Bowling">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "Bowling" && $matchFormat == "Test") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=Test&disc=Bowling\">&nbsp;&nbsp;Career<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=Test&disc=Bowling\">&nbsp;&nbsp;Career</a></li>"; } ?>
                            <li><a href="performances.php?matchFormat=Test&disc=Bowling">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=ODI&disc=Bowling"><b>ODI</b></a></li>
                            <li><a href="current.php?matchFormat=ODI&disc=Bowling">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "Bowling" && $matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=ODI&disc=Bowling\">&nbsp;&nbsp;Career<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=ODI&disc=Bowling\">&nbsp;&nbsp;Career</a></li>"; } ?>
                            <li><a href="performances.php?matchFormat=ODI&disc=Bowling">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=T20I&disc=Bowling"><b>T20I</b></a></li>
                            <li><a href="current.php?matchFormat=T20I&disc=Bowling">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "Bowling" && $matchFormat == "T20I") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=T20I&disc=Bowling\">&nbsp;&nbsp;Career<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=T20I&disc=Bowling\">&nbsp;&nbsp;Career</a></li>"; } ?>
                            <li><a href="performances.php?matchFormat=T20I&disc=Bowling">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=Bowling"><b>FT20</b></a></li>
                            <li><a href="current.php?matchFormat=FT20&disc=Bowling">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "Bowling" && $matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=FT20&disc=Bowling\">&nbsp;&nbsp;Career<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=FT20&disc=Bowling\">&nbsp;&nbsp;Career</a></li>"; } ?>
                            <li><a href="performances.php?matchFormat=FT20&disc=Bowling">&nbsp;&nbsp;Performances</a></li>
                        </ul>
                    </li>
                    <?php if ($disc == "All-Round") { echo "<li class=\"active\">"; } else { echo "<li class=\"dropdown\">"; } ?>
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">All-Round <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="methodology.php?matchFormat=Test&disc=All-Round"><b>Test</b></a></li>
                            <li><a href="current.php?matchFormat=Test&disc=All-Round">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "All-Round" && $matchFormat == "Test") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=Test&disc=All-Round\">&nbsp;&nbsp;Career<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=Test&disc=All-Round\">&nbsp;&nbsp;Career</a></li>"; } ?>
                            <li><a href="performances.php?matchFormat=Test&disc=All-Round">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=ODI&disc=All-Round"><b>ODI</b></a></li>
                            <li><a href="current.php?matchFormat=ODI&disc=All-Round">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "All-Round" && $matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=ODI&disc=All-Round\">&nbsp;&nbsp;Career<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=ODI&disc=All-Round\">&nbsp;&nbsp;Career</a></li>"; } ?>
                            <li><a href="performances.php?matchFormat=ODI&disc=All-Round">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=T20I&disc=All-Round"><b>T20I</b></a></li>
                            <li><a href="current.php?matchFormat=T20I&disc=All-Round">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "All-Round" && $matchFormat == "T20I") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=T20I&disc=All-Round\">&nbsp;&nbsp;Career<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=T20I&disc=All-Round\">&nbsp;&nbsp;Career</a></li>"; } ?>
                            <li><a href="performances.php?matchFormat=T20I&disc=All-Round">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=All-Round"><b>FT20</b></a></li>
                            <li><a href="current.php?matchFormat=FT20&disc=All-Round">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "All-Round" && $matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=FT20&disc=All-Round\">&nbsp;&nbsp;Career<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=FT20&disc=All-Round\">&nbsp;&nbsp;Career</a></li>"; } ?>
                            <li><a href="performances.php?matchFormat=FT20&disc=All-Round">&nbsp;&nbsp;Performances</a></li>
                        </ul>
                    </li>
                    <?php if ($disc == "Fielding") { echo "<li class=\"active\">"; } else { echo "<li class=\"dropdown\">"; } ?>
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Fielding <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="methodology.php?matchFormat=Test&disc=Fielding"><b>Test</b></a></li>
                            <li><a href="current.php?matchFormat=Test&disc=Fielding">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "Fielding" && $matchFormat == "Test") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=Test&disc=Fielding\">&nbsp;&nbsp;Career<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=Test&disc=Fielding\">&nbsp;&nbsp;Career</a></li>"; } ?>
                            <li><a href="performances.php?matchFormat=Test&disc=Fielding">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=ODI&disc=Fielding"><b>ODI</b></a></li>
                            <li><a href="current.php?matchFormat=ODI&disc=Fielding">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "Fielding" && $matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=ODI&disc=Fielding\">&nbsp;&nbsp;Career<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=ODI&disc=Fielding\">&nbsp;&nbsp;Career</a></li>"; } ?>
                            <li><a href="performances.php?matchFormat=ODI&disc=Fielding">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=Fielding"><b>FT20</b></a></li>
                            <li><a href="current.php?matchFormat=FT20&disc=Fielding">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "Fielding" && $matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=FT20&disc=Fielding\">&nbsp;&nbsp;Career<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=FT20&disc=Fielding\">&nbsp;&nbsp;Career</a></li>"; } ?>
                            <li><a href="performances.php?matchFormat=FT20&disc=Fielding">&nbsp;&nbsp;Performances</a></li>
                        </ul>
                    </li>
                    <?php if ($disc == "Win Shares") { echo "<li class=\"active\">"; } else { echo "<li class=\"dropdown\">"; } ?>
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Win Shares <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="methodology.php?matchFormat=ODI&disc=Win Shares"><b>ODI</b></a></li>
                            <li><a href="current.php?matchFormat=ODI&disc=Win Shares">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "Win Shares" && $matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=ODI&disc=Win Shares\">&nbsp;&nbsp;Career<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=ODI&disc=Win Shares\">&nbsp;&nbsp;Career</a></li>"; } ?>
                            <li><a href="performances.php?matchFormat=ODI&disc=Win Shares">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=Win Shares"><b>FT20</b></a></li>
                            <li><a href="current.php?matchFormat=FT20&disc=Win Shares">&nbsp;&nbsp;Current</a></li>
			    <?php if ($disc == "Win Shares" && $matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"career.php?matchFormat=FT20&disc=Win Shares\">&nbsp;&nbsp;Career<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"career.php?matchFormat=FT20&disc=Win Shares\">&nbsp;&nbsp;Career</a></li>"; } ?>
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
   echo "<div class=\"row\">";
   if ($disc == "Fielding" || $disc == "Win Shares") {
	echo "<div class=\"col-lg-6\">";
   } else {
	echo "<div class=\"col-lg-8\">";
   }
   echo "<h2><b>Career Ratings&nbsp;&nbsp;<small>&nbsp;&nbsp;<a href=\"methodology.php?matchFormat=$matchFormat&disc=$disc\">Methodology</a></small></b></h2>";
   $matchFormat = "Test";
   $disc = "Batting";
   $span = "1877-2099";
   $team = "All teams";
   echo "<form class=\"form-inline\" role=\"form\" name=\"selectForm\" method=\"get\" action=\"career.php\">";
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

    if ($matchFormat == "Test") {
	$spans = array("1877-2099", "1877-1914", "1915-1929", "1930-1939", "1940-1949", "1950-1959", "1960-1969", "1970-1979", "1980-1989", "1990-1999", "2000-2009", "2010-2019");
    } else if ($matchFormat == "ODI") {
	$spans = array("1971-2099", "1971-1984", "1985-1989", "1990-1994", "1995-1999", "2000-2004", "2005-2009", "2010-2014", "2015-2019");
    } else if ($matchFormat == "T20I") {
	$spans = array("2005-2099", "2005-2009", "2010-2014", "2015-2019");
    } else if ($matchFormat == "FT20") {
	$spans = array("2008-2099", "2008-2010", "2011-2014", "2015-2018");
    }

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

    echo "<div class=\"form-group\">";
    echo "<select class=\"form-control\" name=\"span\"  onChange=\"submitForms()\">";
    if (isset($_GET['span'])) {
	$span = $_GET['span'];
	if (!in_array($span, $spans)) {
	    $span = $spans[0];
	    $_GET['span'] = $spans[0];
	}
	foreach ($spans as $sn) {
	    if ($span == $sn) {
		if (($sn == "1877-2099" && $matchFormat == "Test") || ($sn == "1971-2099" && $matchFormat == "ODI") || ($sn == "2005-2099" && $matchFormat == "T20I") || ($sn == "2008-2099" && $matchFormat == "FT20")) {
		    echo "<option selected=\"selected\" value=\"$sn\">All-time</option>";
		} else {
		    echo "<option selected=\"selected\" value=\"$sn\">$sn</option>";
		}
	    } else {
		if (($sn == "1877-2099" && $matchFormat == "Test") || ($sn == "1971-2099" && $matchFormat == "ODI") || ($sn == "2005-2099" && $matchFormat == "T20I") || ($sn == "2008-2099" && $matchFormat == "FT20")) {
		    echo "<option value=\"$sn\">All-time</option>";
		} else {
		    echo "<option value=\"$sn\">$sn</option>";
		}
	    }
	}
    } else {
	$count = 0;
	foreach ($spans as $sn) {
	    if ($count == 0) {
		if (($sn == "1877-2099" && $matchFormat == "Test") || ($sn == "1971-2099" && $matchFormat == "ODI") || ($sn == "2005-2099" && $matchFormat == "T20I") || ($sn == "2008-2099" && $matchFormat == "FT20")) {
		    echo "<option selected=\"selected\" value=\"$sn\">All-time</option>";
		} else {
		    echo "<option selected=\"selected\" value=\"$sn\">$sn</option>";
		}
		$span = $sn;
	    } else {
		if (($sn == "1877-2099" && $matchFormat == "Test") || ($sn == "1971-2099" && $matchFormat == "ODI") || ($sn == "2005-2099" && $matchFormat == "T20I") || ($sn == "2008-2099" && $matchFormat == "FT20")) {
		    echo "<option value=\"$sn\">All-time</option>";
		} else {
		    echo "<option value=\"$sn\">$sn</option>";
		}
	    }
	    $count = $count + 1;
	}
    }
    echo "</select>";
    echo "</div>";

    echo "<div class=\"form-group\">";
    echo "<select class=\"form-control\" name=\"team\" onChange=\"submitForms()\">";
    if ($matchFormat == "FT20" || $disc == "Team") {
	$teams = array("All teams");
    } else {
	$teams = array("All teams", "Australia", "Bangladesh", "England", "India", "New Zealand", "Pakistan", "South Africa", "Sri Lanka", "West Indies", "Zimbabwe");
    }
    if (isset($_GET['team'])) {
	$team = $_GET['team'];
	foreach ($teams as $tm) {
	    if ($team == $tm) {
		echo "<option selected=\"selected\" value=\"$tm\">$tm</option>";
	    } else {
		echo "<option value=\"$tm\">$tm</option>";
	    }
	}
    } else {
	$count = 0;
	foreach ($teams as $tm) {
	    if ($count == 0) {
		echo "<option selected=\"selected\" value=\"$tm\">$tm</option>";
		$team = $tm;
	    } else {
		echo "<option value=\"$tm\">$tm</option>";
	    }
	    $count = $count + 1;
	}
    }
    if (!in_array($span, $spans)) {
	$span = $spans[0];
	$_GET['span'] = $spans[0];
    }
    echo "</select>";
    echo "</div>";

    echo "<input type=\"hidden\" name=\"xVal\" value=\"$xVal\">";
    echo "<input type=\"hidden\" name=\"yVal\" value=\"$yVal\">";
    echo "</form>";

   $matchFormatLower = strtolower($matchFormat);
   $disciplineLower = strtolower($disc);
   if ($disciplineLower == "all-round") {
      $disciplineLower = "allRound";
   } else if ($disciplineLower == "win shares") {
      $disciplineLower = "winShares";
   }

    if ($disc == "Fielding" && ($matchFormat != "Test" && $matchFormat != "ODI" && $matchFormat != "FT20")) {
	$matchFormat = "ODI";
    }

    if ($disc == "Win Shares" && ($matchFormat != "ODI" && $matchFormat != "FT20")) {
	$matchFormat = "ODI";
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
    $spanDates = explode("-", $span);
    $startSpan = $spanDates[0]."0000";
    $endSpan = $spanDates[1]."9999";
    if ($matchFormat == "Test") {
	if ($disc == "Batting") {
	    if ($team == "All teams") {
		$sql = "select b.playerId, b.player, p.country, b.startDate, b.endDate, b.tests, b.innings, b.notOuts, b.runs, b.average, b.strikeRate, b.fifties, b.hundreds, b.dblHundreds, b.tripleHundreds, b.rating, b.confInt95 from battingTestCareer b, playerInfo p where p.playerId=b.playerId and ((b.startDate+b.endDate)/2)>".$startSpan." and ((b.startDate+b.endDate)/2)<=".$endSpan." order by b.rating desc limit 500";
	    } else {
		$sql = "select b.playerId, b.player, p.country, b.startDate, b.endDate, b.tests, b.innings, b.notOuts, b.runs, b.average, b.strikeRate, b.fifties, b.hundreds, b.dblHundreds, b.tripleHundreds, b.rating, b.confInt95 from battingTestCareer b, playerInfo p where p.playerId=b.playerId and ((b.startDate+b.endDate)/2)>".$startSpan." and ((b.startDate+b.endDate)/2)<=".$endSpan." and p.country='".$team."' order by b.rating desc limit 100";
	    }
	} else if ($disc == "Bowling") {
	    if ($team == "All teams") {
		$sql = "select b.playerId, b.player, p.country, b.startDate, b.endDate, b.tests, b.innings, b.balls, b.runs, b.wickets, b.average, b.econRate, b.strikeRate, b.fiveWkts, b.tenWkts, b.rating, b.confInt95 from bowlingTestCareer b, playerInfo p where p.playerId=b.playerId and ((b.startDate+b.endDate)/2)>".$startSpan." and ((b.startDate+b.endDate)/2)<=".$endSpan." order by b.rating desc limit 500";
	    } else {
		$sql = "select b.playerId, b.player, p.country, b.startDate, b.endDate, b.tests, b.innings, b.balls, b.runs, b.wickets, b.average, b.econRate, b.strikeRate, b.fiveWkts, b.tenWkts, b.rating, b.confInt95 from bowlingTestCareer b, playerInfo p where p.playerId=b.playerId and ((b.startDate+b.endDate)/2)>".$startSpan." and ((b.startDate+b.endDate)/2)<=".$endSpan." and p.country='".$team."' order by b.rating desc limit 100";
	    }
	} else if ($disc == "All-Round") {
	    if ($team == "All teams") {
		$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.tests, a.runs, a.battingAverage, a.hundreds, a.wickets, a.bowlingAverage, a.fiveWkts, a.hundredFiveWkts, a.rating, a.confInt95 from allRoundTestCareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." order by a.rating desc limit 500";
	    } else {
		$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.tests, a.runs, a.battingAverage, a.hundreds, a.wickets, a.bowlingAverage, a.fiveWkts, a.hundredFiveWkts, a.rating, a.confInt95 from allRoundTestCareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." and p.country='".$team."' order by a.rating desc limit 100";
	    }
	} else if ($disc == "Fielding") {
	    if ($team == "All teams") {
		$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.tests, a.catches, a.droppedCatches, a.dropRate, a.greatCatches, a.directHits, a.runsSaved, a.rating from fieldingTestCareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." order by a.rating desc limit 500";
	    } else {
		$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.tests, a.catches, a.droppedCatches, a.dropRate, a.greatCatches, a.directHits, a.runsSaved, a.rating from fieldingTestCareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." and p.country='".$team."' order by a.rating desc limit 100";
	    }
	} else if ($disc == "Team") {
	    $sql = "select team, startDate, endDate, tests, wins, draws, losses, winPct, rating from teamTestOverall where span='".$span."' order by rating desc";
	}
    } else if ($matchFormat == "ODI" || $matchFormat == "T20I") {
	if ($disc == "Batting") {
	    if ($team == "All teams") {
		$sql = "select b.playerId, b.player, p.country, b.startDate, b.endDate, b.innings, b.notOuts, b.runs, b.average, b.strikeRate, b.fifties, b.hundreds, b.rating, b.confInt95 from batting".$matchFormat."Career b, playerInfo p where p.playerId=b.playerId and ((b.startDate+b.endDate)/2)>".$startSpan." and ((b.startDate+b.endDate)/2)<=".$endSpan." order by b.rating desc limit 500";
	    } else {
		$sql = "select b.playerId, b.player, p.country, b.startDate, b.endDate, b.innings, b.notOuts, b.runs, b.average, b.strikeRate, b.fifties, b.hundreds, b.rating, b.confInt95 from batting".$matchFormat."Career b, playerInfo p where p.playerId=b.playerId and ((b.startDate+b.endDate)/2)>".$startSpan." and ((b.startDate+b.endDate)/2)<=".$endSpan." and p.country='".$team."' order by b.rating desc limit 100";
	    }
	} else if ($disc == "Bowling") {
	    if ($team == "All teams") {
		$sql = "select b.playerId, b.player, p.country, b.startDate, b.endDate, b.innings, b.balls, b.runs, b.wickets, b.average, b.econRate, b.strikeRate, b.threeWkts, b.fiveWkts, b.rating, b.confInt95 from bowling".$matchFormat."Career b, playerInfo p where p.playerId=b.playerId and ((b.startDate+b.endDate)/2)>".$startSpan." and ((b.startDate+b.endDate)/2)<=".$endSpan." order by b.rating desc limit 500";
	    } else {
		$sql = "select b.playerId, b.player, p.country, b.startDate, b.endDate, b.innings, b.balls, b.runs, b.wickets, b.average, b.econRate, b.strikeRate, b.threeWkts, b.fiveWkts, b.rating, b.confInt95 from bowling".$matchFormat."Career b, playerInfo p where p.playerId=b.playerId and ((b.startDate+b.endDate)/2)>".$startSpan." and ((b.startDate+b.endDate)/2)<=".$endSpan." and p.country='".$team."' order by b.rating desc limit 100";
	    }
	} else if ($disc == "All-Round") {
	    if ($team == "All teams") {
		if ($matchFormat == "ODI") {
		    $sql = "select b.playerId, b.player, p.country, b.startDate, b.endDate, b.".$matchFormatLower."s, b.runs, b.battingAverage, b.fifties, b.wickets, b.bowlingAverage, b.threeWkts, b.fiftyThreeWkts, b.rating, b.confInt95 from allRound".$matchFormat."Career b, playerInfo p where p.playerId=b.playerId and ((b.startDate+b.endDate)/2)>".$startSpan." and ((b.startDate+b.endDate)/2)<=".$endSpan." order by b.rating desc limit 500";
		} else {
		    $sql = "select b.playerId, b.player, p.country, b.startDate, b.endDate, b.".$matchFormatLower."s, b.runs, b.battingAverage, b.fifties, b.wickets, b.bowlingAverage, b.threeWkts, b.thirtyTwoWkts, b.rating, b.confInt95 from allRound".$matchFormat."Career b, playerInfo p where p.playerId=b.playerId and ((b.startDate+b.endDate)/2)>".$startSpan." and ((b.startDate+b.endDate)/2)<=".$endSpan." order by b.rating desc limit 500";
		}
	    } else {
		if ($matchFormat == "ODI") {
		    $sql = "select b.playerId, b.player, p.country, b.startDate, b.endDate, b.".$matchFormatLower."s, b.runs, b.battingAverage, b.fifties, b.wickets, b.bowlingAverage, b.threeWkts, b.fiftyThreeWkts, b.rating, b.confInt95 from allRound".$matchFormat."Career b, playerInfo p where p.playerId=b.playerId and ((b.startDate+b.endDate)/2)>".$startSpan." and ((b.startDate+b.endDate)/2)<=".$endSpan." and p.country='".$team."' order by b.rating desc limit 100";
		} else {
		    $sql = "select b.playerId, b.player, p.country, b.startDate, b.endDate, b.".$matchFormatLower."s, b.runs, b.battingAverage, b.fifties, b.wickets, b.bowlingAverage, b.threeWkts, b.thirtyTwoWkts, b.rating, b.confInt95 from allRound".$matchFormat."Career b, playerInfo p where p.playerId=b.playerId and ((b.startDate+b.endDate)/2)>".$startSpan." and ((b.startDate+b.endDate)/2)<=".$endSpan." and p.country='".$team."' order by b.rating desc limit 100";
		}
	    }
	} else if ($disc == "Fielding") {
	    if ($team == "All teams") {
		$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.catches, a.droppedCatches, a.dropRate, a.greatCatches, a.directHits, a.runsSaved, a.rating from fielding".$matchFormat."Career a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." order by a.rating desc limit 500";
	    } else {
		$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.catches, a.droppedCatches, a.dropRate, a.greatCatches, a.directHits, a.runsSaved, a.rating from fielding".$matchFormat."Career a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." and p.country='".$team."' order by a.rating desc limit 100";
	    }
	} else if ($disc == "Win Shares") {
	    if ($team == "All teams") {
		$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.battingAdjWSAvg, a.bowlingAdjWSAvg, a.fieldingAdjWSAvg, a.totalAdjWSAvg, a.totalRating from winSharesODICareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." order by a.totalRating desc limit 500";
	    } else {
		$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.battingAdjWSAvg, a.bowlingAdjWSAvg, a.fieldingAdjWSAvg, a.totalAdjWSAvg, a.totalRating from winSharesODICareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." and p.country='".$team."' order by a.totalRating desc limit 100";
	    }
	} else if ($disc == "Team") {
	    $sql = "select team, startDate, endDate, ".$matchFormatLower."s, wins, ties, losses, winPct, rating from team".$matchFormat."Overall where span='".$span."' order by rating desc";
	}
    }  else if ($matchFormat == "FT20") {
	if ($disc == "Batting") {
	    $sql = "select b.playerId, b.player, b.startDate, b.endDate, b.innings, b.notOuts, b.runs, b.average, b.strikeRate, b.fifties, b.hundreds, b.rating from battingFT20Career b, playerInfo p where p.playerId=b.playerId and ((b.startDate+b.endDate)/2)>".$startSpan." and ((b.startDate+b.endDate)/2)<=".$endSpan." order by b.rating desc limit 500";
	} else if ($disc == "Bowling") {
	    $sql = "select b.playerId, b.player, b.startDate, b.endDate, b.innings, b.balls, b.runs, b.wickets, b.average, b.econRate, b.strikeRate, b.threeWkts, b.fiveWkts, b.rating from bowlingFT20Career b, playerInfo p where p.playerId=b.playerId and ((b.startDate+b.endDate)/2)>".$startSpan." and ((b.startDate+b.endDate)/2)<=".$endSpan." order by b.rating desc limit 500";
	} else if ($disc == "All-Round") {
	    $sql = "select b.playerId, b.player, b.startDate, b.endDate, b.".$matchFormatLower."s, b.runs, b.battingAverage, b.fifties, b.wickets, b.bowlingAverage, b.threeWkts, b.thirtyTwoWkts, b.rating from allRoundFT20Career b, playerInfo p where p.playerId=b.playerId and ((b.startDate+b.endDate)/2)>".$startSpan." and ((b.startDate+b.endDate)/2)<=".$endSpan." order by b.rating desc limit 500";
	} else if ($disc == "Fielding") {
	    $sql = "select a.playerId, a.player, a.startDate, a.endDate, a.".$matchFormatLower."s, a.catches, a.droppedCatches, a.dropRate, a.greatCatches, a.directHits, a.runsSaved, a.rating from fieldingFT20Career a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." order by a.rating desc limit 500";
	} else if ($disc == "Win Shares") {
	    $sql = "select a.playerId, a.player, a.startDate, a.endDate, a.".$matchFormatLower."s, a.battingAdjWSAvg, a.bowlingAdjWSAvg, a.fieldingAdjWSAvg, a.totalAdjWSAvg, a.totalRating from winSharesFT20Career a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." order by a.totalRating desc limit 500";
	} else if ($disc == "Team") {
	    $sql = "select team, startDate, endDate, ".$matchFormatLower."s, wins, ties, losses, winPct, rating from team".$matchFormat."Overall where span='".$span."' order by rating desc";
	}
    }

    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    echo "<ul class=\"list-group\">";
    echo "<li class=\"list-group-item\">";
    if ($disc == "Fielding" || $disc == "Win Shares") {
	echo "<h3>Best</h3>";
    }
    echo "<table class=\"table table-hover table-condensed\" id=\"ratingsTable\">";
    echo "<thead><tr>";
    echo "<th>Rank</th>";
    if ($disc == "Team" and $matchFormat != "FT20") {
	echo "<th>Flag</th>";
    } else if ($disc != "Team") {
	echo "<th>Player</th>";
    }
    if ($disc == "Fielding") {
	if ($matchFormat != "FT20") {
	    echo "<th>Team</th>";
	}
	echo "<th>Span</th>";
	echo "<th>Mat</th>";
	echo "<th>Cat</th>";
	echo "<th>Drops</th>";
	echo "<th>Drop%</th>";
	echo "<th>GrtCat</th>";
	echo "<th>DirHits</th>";
	echo "<th>Runs</th>";
    } else if ($disc == "Win Shares") {
	if ($matchFormat != "FT20") {
	    echo "<th>Team</th>";
	}
	echo "<th>Span</th>";
	echo "<th>Mat</th>";
	echo "<th>BatAvg</th>";
	echo "<th>BowlAvg</th>";
	echo "<th>FieldAvg</th>";
	echo "<th>TotalAvg</th>";
    } else if ($disc == "Team") {
	echo "<th>Team</th>";
	echo "<th>Span</th>";
	echo "<th>Mat</th>";
	echo "<th>Wins</th>";
	if ($matchFormat == "Test") {
	    echo "<th>Draws</th>";
	} else {
	    echo "<th>Ties/NR</th>";
	}
	echo "<th>Losses</th>";
	echo "<th>Win %</th>";
    } else {
	if ($matchFormat == "Test") {
	    echo "<th>Team</th>";
	    echo "<th>Span</th>";
	    echo "<th>Mat</th>";
	    if ($disc == "Batting") {
		echo "<th>Inns</th>";
		echo "<th>NO</th>";
		echo "<th>Runs</th>";
		echo "<th>Ave</th>";
		echo "<th>SR</th>";
		echo "<th>50</th>";
		echo "<th>100</th>";
		echo "<th>200</th>";
		echo "<th>300</th>";
	    } else if ($disc == "Bowling") {
		echo "<th>Inns</th>";
		echo "<th>Balls</th>";
		echo "<th>Runs</th>";
		echo "<th>Wkts</th>";
		echo "<th>Ave</th>";
		echo "<th>Econ</th>";
		echo "<th>SR</th>";
		echo "<th>5</th>";
		echo "<th>10</th>";
	    } else if ($disc == "All-Round") {
		echo "<th>Runs</th>";
		echo "<th>Bat Ave</th>";
		echo "<th>100</th>";
		echo "<th>Wkts</th>";
		echo "<th>Bowl Ave</th>";
		echo "<th>5</th>";
		echo "<th>100r+5w</th>";
	    }
	} else if ($matchFormat == "ODI" || $matchFormat == "T20I") {
	    echo "<th>Team</th>";
	    echo "<th>Span</th>";
	    echo "<th>Inns</th>";
	    if ($disc == "Batting") {
		echo "<th>NO</th>";
		echo "<th>Runs</th>";
		echo "<th>Ave</th>";
		echo "<th>SR</th>";
		echo "<th>50</th>";
		echo "<th>100</th>";
	    } else if ($disc == "Bowling") {
		echo "<th>Balls</th>";
		echo "<th>Runs</th>";
		echo "<th>Wkts</th>";
		echo "<th>Ave</th>";
		echo "<th>Econ</th>";
		echo "<th>SR</th>";
		echo "<th>3</th>";
		echo "<th>5</th>";
	    } else if ($disc == "All-Round") {
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
	    }
	} else {
	    echo "<th>Span</th>";
	    echo "<th>Inns</th>";
	    if ($disc == "Batting") {
		echo "<th>NO</th>";
		echo "<th>Runs</th>";
		echo "<th>Ave</th>";
		echo "<th>SR</th>";
		echo "<th>50</th>";
		echo "<th>100</th>";
	    } else if ($disc == "Bowling") {
		echo "<th>Balls</th>";
		echo "<th>Runs</th>";
		echo "<th>Wkts</th>";
		echo "<th>Ave</th>";
		echo "<th>Econ</th>";
		echo "<th>SR</th>";
		echo "<th>3</th>";
		echo "<th>5</th>";
	    } else if ($disc == "All-Round") {
		echo "<th>Runs</th>";
		echo "<th>Bat Ave</th>";
		echo "<th>50</th>";
		echo "<th>Wkts</th>";
		echo "<th>Bowl Ave</th>";
		echo "<th>3</th>";
		echo "<th>30r+2w</th>";
	    }
	}
    }
    echo "<th>Rating</th>";
    echo "</tr></thead>";

    $k = 1;
    while($res = $result->fetchArray(SQLITE3_NUM)) {
	echo "<tr>";
	echo "<td>$k</td>";
	if ($disc == "Team") {
	    if ($matchFormat != "FT20") {
		echo "<td><a href=\"team.php?team=".$res[0]."&matchFormat=$matchFormat\"><img src=\"images/".$res[0].".png\" style='border:1px solid #A9A9A9'/></a></td>";
	    }
	    echo "<td><a href=\"team.php?team=".$res[0]."&matchFormat=$matchFormat\">".$res[0]."</a></td>";
	}
	for ($j = 1; $j < $result->numColumns(); $j++) {
	    if ($j == 1) {
		if ($disc != "Team") {
		    echo "<td><a href=\"player.php?playerId=".$res[0]."&matchFormat=$matchFormat&disc=$disc\">".str_replace("Sir ","",$res[$j])."</a></td>";
		} else {
		    echo "<td>".substr($res[$j], 0, 4)."-".substr($res[$j+1], 0, 4)."</td>";
		    $j++;
		}
	    } else {
		if ($matchFormat == "Test") {
		    if ($j == 2) { # country
			if ($disc != "Team") {
			    echo "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" alt=\"$res[$j]\" style='border:1px solid #A9A9A9'/></a></td>";
			}
		    } elseif ($j == 3) { # span
			if ($disc != "Team") {
			    echo "<td>".substr($res[$j], 0, 4)."-".substr($res[$j+1], 0, 4)."</td>";
			    $j++;
			} else {
			    echo "<td>$res[$j]</td>";
			}
		    } else {
			if ($disc == "Batting") {
			    if ($j == 9) { # average
				echo "<td>".number_format(round($res[$j], 2), 2)."</td>";
			    } elseif ($j == 10) { # strike rate
				if ($res[$j] != "") {
				    echo "<td>".number_format(round($res[$j], 2), 2)."</td>";
				} else {
				    echo "<td></td>";
				}
			    } elseif ($j == 15) { # rating
				echo "<td><b>".round($res[$j], 0)."</b> &plusmn; ".round($res[$j+1], 0)."</td>";
			    } else {
            if ($j != 16) {
                echo "<td>$res[$j]</td>";
            }
			    }
			} else if ($disc == "Bowling") {
			    if ($j == 10 || $j == 11) { # average and economy rate
				echo "<td>".number_format(round($res[$j], 2), 2)."</td>";
			    } elseif ($j == 12) { # strike rate
				echo "<td>".number_format(round($res[$j], 1), 1)."</td>";
			    } elseif ($j == 15) { # rating
				echo "<td><b>".round($res[$j], 0)."</b> &plusmn; ".round($res[$j+1], 0)."</td>";
			    } else {
            if ($j != 16) {
                echo "<td>$res[$j]</td>";
            }
			    }
			} else if ($disc == "All-Round") {
			    if ($j == 7 || $j == 10) { # average
				echo "<td>".number_format(round($res[$j], 2), 2)."</td>";
			    } elseif ($j == 13) { # rating
				echo "<td><b>".round($res[$j], 0)."</b> &plusmn; ".round($res[$j+1], 0)."</td>";
			    } else {
            if ($j != 14) {
				       echo "<td>$res[$j]</td>";
            }
			    }
			} else if ($disc == "Fielding") {
			    if ($j == 8) { # drop rate %
				echo "<td>".number_format(round($res[$j] * 100, 2), 2)."</td>";
			    } elseif ($j == 12) { # rating
				echo "<td><b>".round($res[$j], 0)."</b></td>";
			    } else {
				echo "<td>$res[$j]</td>";
			    }
			} else if ($disc == "Team") {
			    if ($j == 7) { # winPct
				echo "<td>".number_format(round($res[$j], 1), 1)."</td>";
			    } elseif ($j == 8) { # rating
				echo "<td><b>".round($res[$j], 0)."</b></td>";
			    } else {
              echo "<td>$res[$j]</td>";
			    }
			}
		    }
		} else if ($matchFormat == "ODI" || $matchFormat == "T20I") {
		    if ($j == 2) { # country
			echo "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" alt=\"$res[$j]\" style='border:1px solid #A9A9A9'/></a></td>";
		    } elseif ($j == 3) { # span
			if ($disc != "Team") {
			    echo "<td>".substr($res[$j], 0, 4)."-".substr($res[$j+1], 0, 4)."</td>";
			    $j++;
			} else {
			    echo "<td>$res[$j]</td>";
			}
		    } else {
			if ($disc == "Batting") {
			    if ($j == 8) { # average
				echo "<td>".number_format(round($res[$j], 2), 2)."</td>";
			    } elseif ($j == 9) { # strike rate
				if ($res[$j] != "") {
				    echo "<td>".number_format(round($res[$j], 2), 2)."</td>";
				} else {
				    echo "<td></td>";
				}
			    } elseif ($j == 12) { # rating
				echo "<td><b>".round($res[$j], 0)."</b> &plusmn; ".round($res[$j+1], 0)."</td>";
			    } else {
            if ($j != 13) {
				          echo "<td>$res[$j]</td>";
            }
			    }
			} else if ($disc == "Bowling") {
			    if ($j == 9 || $j == 10) { # average and economy rate
				echo "<td>".number_format(round($res[$j], 2), 2)."</td>";
			    } elseif ($j == 11) { # strike rate
				echo "<td>".number_format(round($res[$j], 1), 1)."</td>";
			    } elseif ($j == 14) { # rating
				echo "<td><b>".round($res[$j], 0)."</b> &plusmn; ".round($res[$j+1], 0)."</td>";
			    } else {
             if ($j != 15) {
				       echo "<td>$res[$j]</td>";
             }
			    }
			} else if ($disc == "All-Round") {
			    if ($j == 7 || $j == 10) { # average
				echo "<td>".number_format(round($res[$j], 2), 2)."</td>";
			    } elseif ($j == 13) { # rating
				echo "<td><b>".round($res[$j], 0)."</b> &plusmn; ".round($res[$j+1], 0)."</td>";
			    } else {
            if ($j != 14) {
				      echo "<td>$res[$j]</td>";
            }
			    }
			} else if ($disc == "Fielding") {
			    if ($j == 8) { # drop rate %
				echo "<td>".number_format(round($res[$j] * 100, 2), 2)."</td>";
			    } elseif ($j == 12) { # rating
				echo "<td><b>".round($res[$j], 0)."</b></td>";
			    } else {
				echo "<td>$res[$j]</td>";
			    }
			} else if ($disc == "Win Shares") {
			    if ($j == 6 || $j == 7 || $j == 8 || $j == 9) { # win shares
				echo "<td>".number_format(round($res[$j], 3), 3)."</td>";
			    } elseif ($j == 10) { # rating
				echo "<td><b>".number_format(round($res[$j], 3), 3)."</b></td>";
			    } else {
				echo "<td>$res[$j]</td>";
			    }
			} else if ($disc == "Team") {
			    if ($j == 7) { # winPct
				echo "<td>".number_format(round($res[$j], 1), 1)."</td>";
			    } elseif ($j == 8) { # rating
				echo "<td><b>".round($res[$j], 0)."</b></td>";
			    } else {
				echo "<td>$res[$j]</td>";
			    }
			}
		    }
		} else {
		    if ($j == 2) { # span
			if ($disc != "Team") {
			    echo "<td>".substr($res[$j], 0, 4)."-".substr($res[$j+1], 0, 4)."</td>";
			    $j++;
			} else {
			    echo "<td>$res[$j]</td>";
			}
		    } else {
			if ($disc == "Batting") {
			    if ($j == 7) { # average
				echo "<td>".number_format(round($res[$j], 2), 2)."</td>";
			    } elseif ($j == 8) { # strike rate
				if ($res[$j] != "") {
				    echo "<td>".number_format(round($res[$j], 2), 2)."</td>";
				} else {
				    echo "<td></td>";
				}
			    } elseif ($j == 11) { # rating
				echo "<td><b>".round($res[$j], 0)."</b></td>";
			    } else {
				echo "<td>$res[$j]</td>";
			    }
			} else if ($disc == "Bowling") {
			    if ($j == 8 || $j == 9) { # average and economy rate
				echo "<td>".number_format(round($res[$j], 2), 2)."</td>";
			    } elseif ($j == 10) { # strike rate
				echo "<td>".number_format(round($res[$j], 1), 1)."</td>";
			    } elseif ($j == 13) { # rating
				echo "<td><b>".round($res[$j], 0)."</b></td>";
			    } else {
				echo "<td>$res[$j]</td>";
			    }
			} else if ($disc == "All-Round") {
			    if ($j == 6 || $j == 9) { # average
				echo "<td>".number_format(round($res[$j], 2), 2)."</td>";
			    } elseif ($j == 12) { # rating
				echo "<td><b>".round($res[$j], 0)."</b></td>";
			    } else {
				echo "<td>$res[$j]</td>";
			    }
			} else if ($disc == "Fielding") {
			    if ($j == 7) { # drop rate %
				echo "<td>".number_format(round($res[$j] * 100, 2), 2)."</td>";
			    } elseif ($j == 11) { # rating
				echo "<td><b>".round($res[$j], 0)."</b></td>";
			    } else {
				echo "<td>$res[$j]</td>";
			    }
			} else if ($disc == "Win Shares") {
			    if ($j == 5 || $j == 6 || $j == 7 || $j == 8) { # win shares
				echo "<td>".number_format(round($res[$j], 3), 3)."</td>";
			    } elseif ($j == 9) { # rating
				echo "<td><b>".number_format(round($res[$j], 3), 3)."</b></td>";
			    } else {
				echo "<td>$res[$j]</td>";
			    }
			} else if ($disc == "Team") {
			    if ($j == 7) { # winPct
				echo "<td>".number_format(round($res[$j], 1), 1)."</td>";
			    } elseif ($j == 8) { # rating
				echo "<td><b>".round($res[$j], 0)."</b></td>";
			    } else {
				echo "<td>$res[$j]</td>";
			    }
			}
		    }
		}
	    }
	}
	echo "</tr>";
	$k++;
    }
    echo "</table>";
    echo "</li>";
    echo "</ul>";
    echo "</div>";

    if ($disc == "Fielding" || $disc == "Win Shares") {
	echo "<div class=\"col-lg-6\">";
    } else {
	echo "<div class=\"col-lg-4\">";
    }
    echo "<br/><br/><br/><br/><br/>";
    echo "<ul class=\"list-group\">";
    echo "<li class=\"list-group-item\">";
    if ($disc == "Fielding" || $disc == "Win Shares") {
       echo "<h3>Worst</h3>";

	if ($matchFormat == "Test") {
	    if ($disc == "Fielding") {
		if ($team == "All teams") {
		    $sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.tests, a.catches, a.droppedCatches, a.dropRate, a.greatCatches, a.directHits, a.runsSaved, a.rating from fieldingTestCareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." order by a.rating asc limit 500";
		} else {
		    $sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.tests, a.catches, a.droppedCatches, a.dropRate, a.greatCatches, a.directHits, a.runsSaved, a.rating from fieldingTestCareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." and p.country='".$team."' order by a.rating asc limit 100";
		}
	    }
	} else if ($matchFormat == "ODI" || $matchFormat == "T20I") {
	    if ($disc == "Fielding") {
		if ($team == "All teams") {
		    $sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.catches, a.droppedCatches, a.dropRate, a.greatCatches, a.directHits, a.runsSaved, a.rating from fielding".$matchFormat."Career a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." order by a.rating asc limit 500";
		} else {
		    $sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.catches, a.droppedCatches, a.dropRate, a.greatCatches, a.directHits, a.runsSaved, a.rating from fielding".$matchFormat."Career a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." and p.country='".$team."' order by a.rating asc limit 100";
		}
	    } else {
		if ($team == "All teams") {
		    $sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.battingAdjWSAvg, a.bowlingAdjWSAvg, a.fieldingAdjWSAvg, a.totalAdjWSAvg, a.totalRating from winSharesODICareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." order by a.totalRating asc limit 500";
		} else {
		    $sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.battingAdjWSAvg, a.bowlingAdjWSAvg, a.fieldingAdjWSAvg, a.totalAdjWSAvg, a.totalRating from winSharesODICareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." and p.country='".$team."' order by a.totalRating asc limit 100";
		}
	    }
	} else if ($matchFormat == "FT20") {
	    if ($disc == "Fielding") {
		$sql = "select a.playerId, a.player, a.startDate, a.endDate, a.".$matchFormatLower."s, a.catches, a.droppedCatches, a.dropRate, a.greatCatches, a.directHits, a.runsSaved, a.rating from fieldingFT20Career a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." order by a.rating asc limit 500";
	    } else {
	        $sql = "select a.playerId, a.player, a.startDate, a.endDate, a.".$matchFormatLower."s, a.battingAdjWSAvg, a.bowlingAdjWSAvg, a.fieldingAdjWSAvg, a.totalAdjWSAvg, a.totalRating from winSharesFT20Career a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." order by a.totalRating asc limit 500";
	    }
	}

	$result = $db->query($sql);
	if (!$result) die("Cannot execute query.");

	echo "<table class=\"table table-hover table-condensed\" id=\"ratingsTable2\">";
	echo "<thead><tr>";
	echo "<th>Rank</th>";
	echo "<th>Player</th>";

	if ($disc == "Fielding") {
	    if ($matchFormat != "FT20") {
		echo "<th>Team</th>";
	    }
	    echo "<th>Span</th>";
	    echo "<th>Mat</th>";
	    echo "<th>Cat</th>";
	    echo "<th>Drops</th>";
	    echo "<th>Drop%</th>";
	    echo "<th>GrtCat</th>";
	    echo "<th>DirHits</th>";
	    echo "<th>Runs</th>";
	} else if ($disc == "Win Shares") {
	    if ($matchFormat != "FT20") {
		echo "<th>Team</th>";
	    }
	    echo "<th>Span</th>";
	    echo "<th>Mat</th>";
	    echo "<th>BatAvg</th>";
	    echo "<th>BowlAvg</th>";
	    echo "<th>FieldAvg</th>";
	    echo "<th>TotalAvg</th>";
	}
	echo "<th>Rating</th>";
	echo "</tr></thead>";

	$k = 1;
	while($res = $result->fetchArray(SQLITE3_NUM)) {
	    echo "<tr>";
	    echo "<td>$k</td>";
	    for ($j = 1; $j < $result->numColumns(); $j++) {
		if ($j == 1) {
		    echo "<td><a href=\"player.php?playerId=".$res[0]."&matchFormat=$matchFormat&disc=$disc\">".str_replace("Sir ","",$res[$j])."</a></td>";
		} else {
		    if ($matchFormat == "Test") {
			if ($j == 2) { # country
			    echo "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" alt=\"$res[$j]\" style='border:1px solid #A9A9A9'/></a></td>";
			} elseif ($j == 3) { # span
			    echo "<td>".substr($res[$j], 0, 4)."-".substr($res[$j+1], 0, 4)."</td>";
			    $j++;
			} else {
			    if ($disc == "Fielding") {
				if ($j == 8) { # drop rate %
				    echo "<td>".number_format(round($res[$j] * 100, 2), 2)."</td>";
				} elseif ($j == 12) { # rating
				    echo "<td><b>".round($res[$j], 0)."</b></td>";
				} else {
				    echo "<td>$res[$j]</td>";
				}
			    }
			}
		    } else if ($matchFormat == "ODI" || $matchFormat == "T20I") {
			if ($j == 2) { # country
			    echo "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" alt=\"$res[$j]\" style='border:1px solid #A9A9A9'/></a></td>";
			} elseif ($j == 3) { # span
			    echo "<td>".substr($res[$j], 0, 4)."-".substr($res[$j+1], 0, 4)."</td>";
			    $j++;
			} else {
			    if ($disc == "Fielding") {
				if ($j == 8) { # drop rate %
				    echo "<td>".number_format(round($res[$j] * 100, 2), 2)."</td>";
				} elseif ($j == 12) { # rating
				    echo "<td><b>".round($res[$j], 0)."</b></td>";
				} else {
				    echo "<td>$res[$j]</td>";
				}
			    } else if ($disc == "Win Shares") {
				if ($j == 6 || $j == 7 || $j == 8 || $j == 9) { # win shares
				    echo "<td>".number_format(round($res[$j], 3), 3)."</td>";
				} elseif ($j == 10) { # rating
				    echo "<td><b>".number_format(round($res[$j], 3), 3)."</b></td>";
				} else {
				    echo "<td>$res[$j]</td>";
				}
			    }
			}
		    } else {
			if ($j == 2) { # span
			    echo "<td>".substr($res[$j], 0, 4)."-".substr($res[$j+1], 0, 4)."</td>";
			    $j++;
			} else {
			    if ($disc == "Fielding") {
				if ($j == 7) { # drop rate %
				    echo "<td>".number_format(round($res[$j] * 100, 2), 2)."</td>";
				} elseif ($j == 11) { # rating
				    echo "<td><b>".round($res[$j], 0)."</b></td>";
				} else {
				    echo "<td>$res[$j]</td>";
				}
			    } else if ($disc == "Win Shares") {
				if ($j == 5 || $j == 6 || $j == 7 || $j == 8) { # win shares
				    echo "<td>".number_format(round($res[$j], 3), 3)."</td>";
				} elseif ($j == 9) { # rating
				    echo "<td><b>".number_format(round($res[$j], 3), 3)."</b></td>";
				} else {
				    echo "<td>$res[$j]</td>";
				}
			    }
			}
		    }
		}
	    }
	    echo "</tr>";
	    $k++;
	}
	echo "</table>";
    } else {
	echo "<h3>Correlations</h3>";
	if ($matchFormat == "Test") {
	    if ($disc == "Batting") {
		$xVals = array("Average"=>"average", "Runs"=>"runs", "Strike Rate"=>"strikeRate", "Fifties"=>"fifties", "Hundreds"=>"hundreds", "Rating"=>"rating", "Innings"=>"innings", "Tests"=>"tests");
		$yVals = array("Strike Rate"=>"strikeRate", "Average"=>"average", "Runs"=>"runs", "Fifties"=>"fifties", "Hundreds"=>"hundreds", "Rating"=>"rating", "Innings"=>"innings", "Tests"=>"tests");
	    } else if ($disc == "Bowling") {
		$xVals = array("Average"=>"average", "Runs"=>"runs", "Strike Rate"=>"strikeRate", "Balls"=>"balls", "Wickets"=>"wickets", "Econ Rate"=>"econRate", "Five Wkts"=>"fiveWkts", "Ten Wkts"=>"tenWkts", "Rating"=>"rating", "Innings"=>"innings", "Tests"=>"tests");
		$yVals = array("Strike Rate"=>"strikeRate", "Average"=>"average", "Runs"=>"runs", "Balls"=>"balls", "Wickets"=>"wickets", "Econ Rate"=>"econRate", "Five Wkts"=>"fiveWkts", "Ten Wkts"=>"tenWkts", "Rating"=>"rating", "Innings"=>"innings", "Tests"=>"tests");
	    } else if ($disc == "All-Round") {
		$xVals = array("Batting Average"=>"battingAverage", "Bowling Average"=>"bowlingAverage", "Runs"=>"runs", "Wickets"=>"wickets", "Hundreds"=>"hundreds", "Five Wkts"=>"fiveWkts", "Hundred Runs + Five Wkts"=>"hundredFiveWkts", "Rating"=>"rating", "Tests"=>"tests");
		$yVals = array("Bowling Average"=>"bowlingAverage", "Batting Average"=>"battingAverage", "Runs"=>"runs", "Wickets"=>"wickets", "Hundreds"=>"hundreds", "Five Wkts"=>"fiveWkts", "Hundred Runs + Five Wkts"=>"hundredFiveWkts", "Rating"=>"rating", "Tests"=>"tests");
	    } else if ($disc == "Team") {
		$xVals = array("Wins"=>"wins", "Losses"=>"losses", "Draws"=>"draws", "Win %"=>"winPct", "Rating"=>"rating", "Tests"=>"tests");
		$yVals = array("Losses"=>"losses", "Wins"=>"wins", "Draws"=>"draws", "Win %"=>"winPct", "Rating"=>"rating", "Tests"=>"tests");
	    }
	} else if ($matchFormat == "ODI" || $matchFormat == "T20I" || $matchFormat == "FT20") {
	    if ($disc == "Batting") {
		$xVals = array("Average"=>"average", "Runs"=>"runs", "Strike Rate"=>"strikeRate", "Fifties"=>"fifties", "Hundreds"=>"hundreds", "Rating"=>"rating", "Innings"=>"innings");
		$yVals = array("Strike Rate"=>"strikeRate", "Average"=>"average", "Runs"=>"runs", "Fifties"=>"fifties", "Hundreds"=>"hundreds", "Rating"=>"rating", "Innings"=>"innings");
	    } else if ($disc == "Bowling") {
		$xVals = array("Average"=>"average", "Runs"=>"runs", "Strike Rate"=>"strikeRate", "Balls"=>"balls", "Wickets"=>"wickets", "Econ Rate"=>"econRate", "Five Wkts"=>"fiveWkts", "Three Wkts"=>"threeWkts", "Rating"=>"rating", "Innings"=>"innings");
		$yVals = array("Strike Rate"=>"strikeRate", "Average"=>"average", "Runs"=>"runs", "Balls"=>"balls", "Wickets"=>"wickets", "Econ Rate"=>"econRate", "Five Wkts"=>"fiveWkts", "Three Wkts"=>"threeWkts", "Rating"=>"rating", "Innings"=>"innings");
	    } else if ($disc == "All-Round") {
		if ($matchFormat == "ODI") {
		    $xVals = array("Batting Average"=>"battingAverage", "Bowling Average"=>"bowlingAverage", "Runs"=>"runs", "Wickets"=>"wickets", "Fifties"=>"fifties", "Three Wkts"=>"threeWkts", "Fifty Runs + Three Wkts"=>"fiftyThreeWkts", "Rating"=>"rating", "ODIs"=>"odis");
		    $yVals = array("Bowling Average"=>"bowlingAverage", "Batting Average"=>"battingAverage", "Runs"=>"runs", "Wickets"=>"wickets", "Fifties"=>"fifties", "Three Wkts"=>"threeWkts", "Fifty Runs + Three Wkts"=>"fiftyThreeWkts", "Rating"=>"rating", "ODIs"=>"odis");
		} else if ($matchFormat == "T20I") {
		    $xVals = array("Batting Average"=>"battingAverage", "Bowling Average"=>"bowlingAverage", "Runs"=>"runs", "Wickets"=>"wickets", "Fifties"=>"fifties", "Three Wkts"=>"threeWkts", "Thirty Runs + Two Wkts"=>"fiftyThreeWkts", "Rating"=>"rating", "T20Is"=>"t20is");
		    $yVals = array("Bowling Average"=>"bowlingAverage", "Batting Average"=>"battingAverage", "Runs"=>"runs", "Wickets"=>"wickets", "Fifties"=>"fifties", "Three Wkts"=>"threeWkts", "Thirty Runs + Two Wkts"=>"fiftyThreeWkts", "Rating"=>"rating", "T20Is"=>"t20is");
		} else if ($matchFormat == "FT20") {
		    $xVals = array("Batting Average"=>"battingAverage", "Bowling Average"=>"bowlingAverage", "Runs"=>"runs", "Wickets"=>"wickets", "Fifties"=>"fifties", "Three Wkts"=>"threeWkts", "Thirty Runs + Two Wkts"=>"fiftyThreeWkts", "Rating"=>"rating", "FT20s"=>"ft20s");
		    $yVals = array("Bowling Average"=>"bowlingAverage", "Batting Average"=>"battingAverage", "Runs"=>"runs", "Wickets"=>"wickets", "Fifties"=>"fifties", "Three Wkts"=>"threeWkts", "Thirty Runs + Two Wkts"=>"fiftyThreeWkts", "Rating"=>"rating", "FT20s"=>"ft20s");
		}
	    } else if ($disc == "Team") {
		if ($matchFormat == "ODI") {
		    $xVals = array("Wins"=>"wins", "Losses"=>"losses", "Ties/NR"=>"ties", "Win %"=>"winPct", "Rating"=>"rating", "ODIs"=>"odis");
		    $yVals = array("Losses"=>"losses", "Wins"=>"wins", "Ties/NR"=>"ties", "Win %"=>"winPct", "Rating"=>"rating", "ODIs"=>"odis");
		} else if ($matchFormat == "T20I") {
		    $xVals = array("Wins"=>"wins", "Losses"=>"losses", "Ties/NR"=>"ties", "Win %"=>"winPct", "Rating"=>"rating", "T20Is"=>"t20is");
		    $yVals = array("Losses"=>"losses", "Wins"=>"wins", "Ties/NR"=>"ties", "Win %"=>"winPct", "Rating"=>"rating", "T20Is"=>"t20is");
		} else {
		    $xVals = array("Wins"=>"wins", "Losses"=>"losses", "Ties/NR"=>"ties", "Win %"=>"winPct", "Rating"=>"rating", "FT20s"=>"ft20s");
		    $yVals = array("Losses"=>"losses", "Wins"=>"wins", "Ties/NR"=>"ties", "Win %"=>"winPct", "Rating"=>"rating", "FT20s"=>"ft20s");
		}
	    }
	}

	echo "<form class=\"form-inline\" role=\"form\" name=\"chartForm\" method=\"get\" action=\"career.php\">";
	echo "<div class=\"form-group\">";
	echo "<select class=\"form-control\" name=\"yVal\" onChange=\"chartForms()\">";
	if (isset($_GET['yVal'])) {
	    $yVal = $_GET['yVal'];
	    foreach (array_keys($yVals) as $y) {
		if ($yVal == $yVals[$y]) {
		    echo "<option selected=\"selected\" value=\"$yVals[$y]\">$y</option>";
		} else {
		    echo "<option value=\"$yVals[$y]\">$y</option>";
		}
	    }
	} else {
	    $count = 0;
	    foreach (array_keys($yVals) as $y) {
		if ($count == 0) {
		    echo "<option selected=\"selected\" value=\"$yVals[$y]\">$y</option>";
		    $yVal = $yVals[$y];
		} else {
		    echo "<option value=\"$yVals[$y]\">$y</option>";
		}
		$count = $count + 1;
	    }
	}
	echo "</select>";
	echo "</div>";

	echo "<div class=\"chart\">";
	echo "<div id=\"chart\"></div>";
	echo "</div>";

	echo "<div class=\"form-group  pull-center\">";
	echo "<select class=\"form-control\" name=\"xVal\" onChange=\"chartForms()\">";
	if (isset($_GET['xVal'])) {
	    $xVal = $_GET['xVal'];
	    foreach (array_keys($xVals) as $x) {
		if ($xVal == $xVals[$x]) {
		    echo "<option selected=\"selected\" value=\"$xVals[$x]\">$x</option>";
		} else {
		    echo "<option value=\"$xVals[$x]\">$x</option>";
		}
	    }
	} else {
	    $count = 0;
	    foreach (array_keys($xVals) as $x) {
		if ($count == 0) {
		    echo "<option selected=\"selected\" value=\"$xVals[$x]\">$x</option>";
		    $xVal = $xVals[$x];
		} else {
		    echo "<option value=\"$xVals[$x]\">$x</option>";
		}
		$count = $count + 1;
	    }
	}
	echo "</select>";
	echo "</div>";
	echo "<input type=\"hidden\" name=\"matchFormat\" value=\"$matchFormat\">";
	echo "<input type=\"hidden\" name=\"disc\" value=\"$disc\">";
	echo "<input type=\"hidden\" name=\"span\" value=\"$span\">";
	echo "<input type=\"hidden\" name=\"team\" value=\"$team\">";
	echo "</form>";
    }
    echo "</li>";
    echo "</ul>";
    echo "</div>";
    echo "</div>";
    echo "</div>";
    $db->close();
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
