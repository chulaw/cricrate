<!DOCTYPE html>
<?php
session_start();
$playerId1 = $_GET["playerId1"];
$playerId2 = $_GET["playerId2"];
$player2Search = $_GET["player2Search"];
$matchFormat = $_GET["matchFormat"];
$disc = $_GET["disc"];
$inningsDate = $_GET["inningsDate"];

if(isset($_SESSION['screen_width']) AND isset($_SESSION['screen_height'])){
} else if(isset($_REQUEST['width']) AND isset($_REQUEST['height'])) {
    $_SESSION['screen_width'] = $_REQUEST['width'];
    $_SESSION['screen_height'] = $_REQUEST['height'];
    header("Location: compare.php?playerId1=".$playerId1."&playerId2=".$playerId2."&player2Search=".$player2Search."&matchFormat=".$matchFormat."&disc=".$disc."&inningsDate=".$inningsDate);
} else {
    echo '<script type="text/javascript">window.location = "' . $_SERVER['PHP_SELF'] . '?playerId1='.$playerId1.'&playerId2='.$playerId2.'&player2Search='.$player2Search.'&matchFormat='.$matchFormat.'&disc='.$disc.'&inningsDate='.$inningsDate.'&width="+screen.width+"&height="+screen.height;</script>';
}

$player1 = "";
$player2 = "";
$country1 = "";
$country2 = "";
function getPlayerName($db, $playerId, $player) {
    if ($player == "") {        
        $sql = "select player from playerInfo where playerId=".$playerId;
        $result = $db->query($sql);
        if (!$result) die("Cannot execute query.");
        $res = $result->fetchArray(SQLITE3_NUM);
        
        if (!empty($res)) {   
            $player = $res[0];
        }        
    }
    return $player;
}

if ($playerId1 != "" && $playerId2 != "") {
    $db = new SQLite3('ccr.db');
    $player1 = getPlayerName($db, $playerId1, $player1);
    $player2 = getPlayerName($db, $playerId2, $player2);
    $db->close();
    $db = new SQLite3('ccrODI.db');
    $player1 = getPlayerName($db, $playerId1, $player1);
    $player2 = getPlayerName($db, $playerId2, $player2);
    $db->close();
    $db = new SQLite3('ccrT20I.db');
    $player1 = getPlayerName($db, $playerId1, $player1);
    $player2 = getPlayerName($db, $playerId2, $player2);
    $db->close();
    $db = new SQLite3('ccrFT20.db');
    $player1 = getPlayerName($db, $playerId1, $player1);
    $player2 = getPlayerName($db, $playerId2, $player2);
    $db->close();
}

?>
<html>
<head>
    <?php
    
    if ($player1 != "" &&  $player2 != "") {
	echo "<title>cricrate | ".$player1." vs ".$player2." - ".$matchFormat." ".$disc."</title>";
    } else {
	echo "<title>cricrate | Compare Players</title>";
    }     
    ?>
    <link rel="icon" href="images/cricrate.png" />
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
    
    var chartWidth = screen.width * 0.475;
    var chartHeight = screen.height * 0.35;
    if (isMobile == true) {
	chartWidth = chartWidth * 2;
    }
    
    var player1 = <?php echo $_GET['playerId1'] ?>;
    var player2 = <?php echo $_GET['playerId2'] ?>;
    var matchFormat = <?php echo json_encode($_GET['matchFormat']); ?>;
    var disc = <?php echo json_encode($_GET['disc']); ?>;
    var inningsDate = <?php echo json_encode($_GET['inningsDate']); ?>;
    var batBowl = disc.toLowerCase();
    if (batBowl == "all-round") {
       batBowl = "allRound";
    } else if (batBowl == "win shares") {
       batBowl = "winShares";
    }
    
    var xAxis = "Inning";
    if (batBowl == "allRound" || batBowl == "fielding" || batBowl == "winShares") {
	var xAxis = "Match";
    }    
    
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);
      
    function drawChart() {
	var jsonData = $.ajax({
	    url: "charts/compare.php?playerId1="+player1+"&playerId2="+player2+"&matchFormat="+matchFormat+"&batBowl="+batBowl+"&inningsDate="+inningsDate,
	    dataType:"json",
	    async: false
	    }).responseText;

	// Create our data table out of JSON data loaded from server.	
	var data = new google.visualization.DataTable(jsonData);
        var showEvery = parseInt(data.getNumberOfRows() / 8);

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
		    title: "Current Rating",
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
		    },
	    tooltip: {
		    textStyle: {
				fontSize: 11,
				color: '#000000',
				bold: 'true'
				},
		    isHtml: true
		    },
	    animation: {
			"startup": true,
			duration: 1000,
			easing: 'inAndOut',
			},
	    curveType: 'function'
	};
    
	var chart = new google.visualization.LineChart(document.getElementById('chart'));
	chart.draw(data, options);
    }
    
    var sortCol = 5;
    if (batBowl == "allRound") {
	if (matchFormat == "Test") {
	    sortCol = 6;
	} else {
	    sortCol = 4;    
	}
    } else if (batBowl == "fielding") {
	sortCol = 7;
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
    
    $(document).ready(function() {
	$('#inningsTable1').DataTable( {
        "lengthChange":   false,
	"searching":   false,
	"pageLength": 7,
	"order": [[ sortCol, "desc" ]],
    } );
	
	$('#inningsTable2').DataTable( {
        "lengthChange":   false,
	"searching":   false,
	"pageLength": 7,
	"order": [[ sortCol, "desc" ]],
    } );
    } );

    submitForms = function(){
	    window.document.selectForm.submit();
	}
	
    chartForms = function(){
	    window.document.chartForm.submit();
	}	
    </script>
    <link rel="stylesheet" type="text/css" href="style.css" />
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

function getPlayerCountry($db, $playerId, $country) {
    if ($country == "") {        
        $sql = "select country from playerInfo where playerId=".$playerId;
        $result = $db->query($sql);
        if (!$result) die("Cannot execute query.");
        $res = $result->fetchArray(SQLITE3_NUM);
        
        if (!empty($res)) {   
            $country = $res[0];
        }        
    }
    return $country;
}

if ($playerId2 == "" && $player2Search == "") {
    $db = new SQLite3('ccr.db');
    $player1 = getPlayerName($db, $playerId1, $player1);
    $country1 = getPlayerCountry($db, $playerId1, $country1);
    $db->close();
    $db = new SQLite3('ccrODI.db');
    $player1 = getPlayerName($db, $playerId1, $player1);
    $country1 = getPlayerCountry($db, $playerId1, $country1);
    $db->close();
    $db = new SQLite3('ccrT20I.db');
    $player1 = getPlayerName($db, $playerId1, $player1);
    $country1 = getPlayerCountry($db, $playerId1, $country1);
    $db->close();
    $db = new SQLite3('ccrFT20.db');
    $player1 = getPlayerName($db, $playerId1, $player1);
    $country1 = getPlayerCountry($db, $playerId1, $country1);
    $db->close();
    
    echo "<div class=\"container\">";
    echo "<div class=\"panel panel-default\">";
    echo "<div class=\"panel-body\">";
    echo "<h2><b>Compare Players</b></h2><br/>";    
    echo "<form class=\"form-inline\" name=\"selectForm\" action=\"compare.php\" method=\"get\">";
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
    echo "<br/><br/>";
    echo "<img src=\"images/".$country1.".png\" border=1px/>&nbsp;&nbsp;&nbsp;<a href=\"player.php?playerId=$playerId1\">".$player1."</a><br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; vs <br/><br/>";
    echo "<div class=\"form-group\">";
    echo "<input id=\"compare\" type=\"text\" class=\"form-control\" id=\"compare\" name=\"player2Search\">";
    echo "</div>";
    echo "<input type=\"hidden\" name=\"playerId1\" value=\"".$playerId1."\">";
    echo "<input type=\"hidden\" name=\"playerId2\" value=\"\">";
    echo "<input type=\"hidden\" name=\"inningsDate\" value=\"Inning\">";
    echo "<input type=\"submit\" class=\"btn btn-default\" value=\"Search\">";
    echo "</form>";
    echo "</div>";
    echo "</div>";
    echo "</div>";
} else if ($playerId2 == "" && $player2Search != "") {
    $db = new SQLite3('ccr.db');
    $player1 = getPlayerName($db, $playerId1, $player1);
    $country1 = getPlayerCountry($db, $playerId1, $country1);
    $db->close();
    $db = new SQLite3('ccrODI.db');
    $player1 = getPlayerName($db, $playerId1, $player1);
    $country1 = getPlayerCountry($db, $playerId1, $country1);
    $db->close();
    $db = new SQLite3('ccrT20I.db');
    $player1 = getPlayerName($db, $playerId1, $player1);
    $country1 = getPlayerCountry($db, $playerId1, $country1);
    $db->close();
    $db = new SQLite3('ccrFT20.db');
    $player1 = getPlayerName($db, $playerId1, $player1);
    $country1 = getPlayerCountry($db, $playerId1, $country1);
    $db->close();
    
    echo "<div class=\"container\">";
    echo "<div class=\"panel panel-default\">";
    echo "<div class=\"panel-body\">";
    echo "<h2><b>Compare Players</b></h2><br/>";
    echo "<form class=\"form-inline\" name=\"selectForm\" action=\"compare.php\" method=\"get\">";
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
   echo "<br/><br/>";
    echo "<img src=\"images/".$country1.".png\" border=1px/>&nbsp;&nbsp;&nbsp;<a href=\"player.php?playerId=$playerId1\">".$player1."</a><br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; vs <br/><br/>";
    echo "<div class=\"form-group\">";
    echo "<input type=\"text\" class=\"form-control\" name=\"player2Search\">";
    echo "</div>";
    echo "<input type=\"hidden\" name=\"playerId1\" value=\"".$playerId1."\">";
    echo "<input type=\"hidden\" name=\"playerId2\" value=\"\">";
    echo "<input type=\"hidden\" name=\"inningsDate\" value=\"Inning\">";
    echo "<input type=\"submit\" class=\"btn btn-default\" value=\"Search\">";    
    echo "</form><br/><br/>";

    $db = new SQLite3('ccr.db');
    $sql = "select playerId, player, country from playerInfo where player like \"%".$player2Search."%\"";
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    
    $playerCount = 0;
    $playersFound = array();
    echo "<ul>";
    while($res = $result->fetchArray(SQLITE3_NUM)) {
	echo "<li><img src=\"images/".$res[2].".png\" border=1px/>&nbsp;&nbsp;&nbsp;<a href=\"compare.php?playerId1=$playerId1&playerId2=".$res[0]."&player2Search=$player2Search&matchFormat=$matchFormat&disc=$disc&inningsDate=$inningsDate\">".str_replace("Sir ","",$res[1])."</a></li>";
	$playersFound[$res[0]] = 1;
	$playerCount++;
    }
    
    $db = new SQLite3('ccrODI.db');
    $sql = "select playerId, player, country from playerInfo where player like \"%".$player2Search."%\"";
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    
    while($res = $result->fetchArray(SQLITE3_NUM)) {
	if (array_key_exists($res[0], $playersFound)) {
	    continue;
	}
	echo "<li><img src=\"images/".$res[2].".png\" border=1px/>&nbsp;&nbsp;&nbsp;<a href=\"compare.php?playerId1=$playerId1&playerId2=".$res[0]."&player2Search=$player2Search&matchFormat=$matchFormat&disc=$disc&inningsDate=$inningsDate\">".str_replace("Sir ","",$res[1])."</a></li>";
	$playersFound[$res[0]] = 1;
	$playerCount++;
    }
    $db->close();
    
    $db = new SQLite3('ccrT20I.db');
    $sql = "select playerId, player, country from playerInfo where player like \"%".$player2Search."%\"";
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    
    while($res = $result->fetchArray(SQLITE3_NUM)) {
	if (array_key_exists($res[0], $playersFound)) {
	    continue;
	}
	echo "<li><img src=\"images/".$res[2].".png\" border=1px/>&nbsp;&nbsp;&nbsp;<a href=\"compare.php?playerId1=$playerId1&playerId2=".$res[0]."&player2Search=$player2Search&matchFormat=$matchFormat&disc=$disc&inningsDate=$inningsDate\">".str_replace("Sir ","",$res[1])."</a></li>";
	$playersFound[$res[0]] = 1;
	$playerCount++;
    }
    $db->close();
    
    $db = new SQLite3('ccrFT20.db');
    $sql = "select playerId, player, teams from playerInfo where player like \"%".$player2Search."%\"";
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
    
    while($res = $result->fetchArray(SQLITE3_NUM)) {
	if (array_key_exists($res[0], $playersFound)) {
	    continue;
	}
	echo "<li><a href=\"compare.php?playerId1=$playerId1&playerId2=".$res[0]."&player2Search=$player2Search&matchFormat=$matchFormat&disc=$disc&inningsDate=$inningsDate\">".str_replace("Sir ","",$res[1])."</a></li>";
	$playersFound[$res[0]] = 1;
	$playerCount++;
    }
    $db->close();
    echo "</ul>";
    echo "</div>";
    echo "</div>";
    echo "</div>";
} else {
    $playerFound = 0;   
    
    $db = new SQLite3('ccr.db');
    $country1 = getPlayerCountry($db, $playerId1, $country1);
    $country2 = getPlayerCountry($db, $playerId2, $country2);
    $db->close();
    $db = new SQLite3('ccrODI.db');
    $country1 = getPlayerCountry($db, $playerId1, $country1);
    $country2 = getPlayerCountry($db, $playerId2, $country2);
    $db->close();
    $db = new SQLite3('ccrT20I.db');
    $country1 = getPlayerCountry($db, $playerId1, $country1);
    $country2 = getPlayerCountry($db, $playerId2, $country2);
    $db->close();
    $db = new SQLite3('ccrFT20.db');
    $country1 = getPlayerCountry($db, $playerId1, $country1);
    $country2 = getPlayerCountry($db, $playerId2, $country2);
    $db->close();
    
    echo "<div class=\"panel panel-inverse\">";
    echo "<div class=\"panel-body\">";
    echo "<div class=\"row\">";    
    echo "<div class=\"col-lg-6\">";
    if ($country1 == "" && $country2 == "") {
	echo "<h2><b>".$player1."</b>&nbsp;<b>vs ".$player2."</b></h2>";
    } else {
	echo "<h2><b>".$player1."</b>&nbsp;&nbsp;<a href=\"team.php?team=".$country1."&matchFormat=$matchFormat\"><img src=\"images/".$country1.".png\" border=1px/></a>&nbsp; <b>vs ".$player2."</b>&nbsp;&nbsp;<a href=\"team.php?team=".$country2."&matchFormat=$matchFormat\"><img src=\"images/".$country2.".png\" border=1px/></a></h2>";
	$playerFound = 1;   
    }                
	
    echo "<form class=\"form-inline\" name=\"selectForm\" action=\"compare.php\" method=\"get\">";
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
    echo "<input type=\"hidden\" name=\"playerId1\" value=\"$playerId1\">";
    echo "<input type=\"hidden\" name=\"playerId2\" value=\"$playerId2\">";
    echo "<input type=\"hidden\" name=\"player2Search\" value=\"$player2Search\">";
    echo "<input type=\"hidden\" name=\"inningsDate\" value=\"$inningsDate\">";    
    echo "</form>";
    
    if ($disc == "Fielding" && ($matchFormat != "Test" && $matchFormat != "ODI" && $matchFormat != "FT20")) {
	$matchFormat = "ODI";
    }
    
    if ($disc == "Win Shares" && ($matchFormat != "ODI" && $matchFormat != "FT20")) {
	$matchFormat = "ODI";
    }
    
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
    
    echo "<ul class=\"list-group\">";
    if ($disc == "Batting") {
	# batting career    
	if ($matchFormat == "Test") {
	    $sql1 = "select startDate, endDate, ".$matchFormatLower."s, innings, notOuts, runs, average, strikeRate, fifties, hundreds, dblHundreds, tripleHundreds, rating from batting".$matchFormat."Career where playerId=".$playerId1;
	    $sql2 = "select startDate, endDate, ".$matchFormatLower."s, innings, notOuts, runs, average, strikeRate, fifties, hundreds, dblHundreds, tripleHundreds, rating from batting".$matchFormat."Career where playerId=".$playerId2;
	} else {
	    $sql1 = "select startDate, endDate, innings, notOuts, runs, average, strikeRate, fifties, hundreds, rating from batting".$matchFormat."Career where playerId=".$playerId1;
	    $sql2 = "select startDate, endDate, innings, notOuts, runs, average, strikeRate, fifties, hundreds, rating from batting".$matchFormat."Career where playerId=".$playerId2;
	}
	$result = $db->query($sql1);
	if (!$result) die("Cannot execute query.");
	$res1 = $result->fetchArray(SQLITE3_NUM);
	$result = $db->query($sql2);
	if (!$result) die("Cannot execute query.");
	$res2 = $result->fetchArray(SQLITE3_NUM);
	
	$tableHtml = "";
	if (!empty($res1) && $res1[0] != "" && !empty($res2) && $res2[0] != "") {
	    echo "<li class=\"list-group-item\">";
	    echo "<h4>Career Summary</h4>";
	    echo "<table class=\"table table-hover table-condensed\" id=\"playerTable\">";
	    echo "<thead><tr>";
	    
	    if ($matchFormat == "Test") {
		echo "<th>Player</th>";
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
		$numInns1 = $res1[3];
		echo "<tr>";
		echo "<td><a href=\"player.php?playerId=$playerId1&matchFormat=$matchFormat&disc=$disc\">$player1</a></th>";
		echo "<td>".substr($res1[0], 0, 4)."-".substr($res1[1], 0, 4)."</td>"; # span
		echo "<td>$res1[2]</td><td>$res1[3]</td><td>$res1[4]</td><td>$res1[5]</td>";   
		echo "<td>".number_format(round($res1[6], 2), 2)."</td><td>".number_format(round($res1[7], 2), 2)."</td>";
		echo "<td>$res1[8]</td><td>$res1[9]</td><td>$res1[10]</td><td>$res1[11]</td>";   
		echo "<td><b>".round($res1[12], 0)."</b></td>";
		echo "</tr>";
		$numInns2 = $res2[3];
		echo "<tr>";
		echo "<td><a href=\"player.php?playerId=$playerId2&matchFormat=$matchFormat&disc=$disc\">$player2</a></th>";
		echo "<td>".substr($res2[0], 0, 4)."-".substr($res2[1], 0, 4)."</td>"; 
		echo "<td>$res2[2]</td><td>$res2[3]</td><td>$res2[4]</td><td>$res2[5]</td>";   
		echo "<td>".number_format(round($res2[6], 2), 2)."</td><td>".number_format(round($res2[7], 2), 2)."</td>";
		echo "<td>$res2[8]</td><td>$res2[9]</td><td>$res2[10]</td><td>$res2[11]</td>";   
		echo "<td><b>".round($res2[12], 0)."</b></td>";
		echo "</tr>";
	    } else {
		echo "<th>Player</th>";
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
		$numInns1 = $res1[2];
		echo "<tr>";
		echo "<td><a href=\"player.php?playerId=$playerId1&matchFormat=$matchFormat&disc=$disc\">$player1</a></th>";
		echo "<td>".substr($res1[0], 0, 4)."-".substr($res1[1], 0, 4)."</td>"; # span
		echo "<td>$res1[2]</td><td>$res1[3]</td><td>$res1[4]</td>";   
		echo "<td>".number_format(round($res1[5], 2), 2)."</td><td>".number_format(round($res1[6], 2), 2)."</td>";
		echo "<td>$res1[7]</td><td>$res1[8]</td>";   
		echo "<td><b>".round($res1[9], 0)."</b></td>";
		echo "</tr>";
		$numInns2 = $res2[2];
		echo "<tr>";
		echo "<td><a href=\"player.php?playerId=$playerId2&matchFormat=$matchFormat&disc=$disc\">$player2</a></th>";
		echo "<td>".substr($res2[0], 0, 4)."-".substr($res2[1], 0, 4)."</td>"; # span
		echo "<td>$res2[2]</td><td>$res2[3]</td><td>$res2[4]</td>";   
		echo "<td>".number_format(round($res2[5], 2), 2)."</td><td>".number_format(round($res2[6], 2), 2)."</td>";
		echo "<td>$res2[7]</td><td>$res2[8]</td>";   
		echo "<td><b>".round($res2[9], 0)."</b></td>";
		echo "</tr>";
	    }                
	    echo "</table>";
		    
	    echo "</li>";    
	    echo "<li class=\"list-group-item\">";		    
	    if ($numInns1 > 20 && $numInns2 > 20) {
		echo "<h4>Current Rating Timeline</h4>";
		$inningsDates = array("Inning", "Date");
		echo "By ";
		echo "<form class=\"form-inline\" role=\"form\" name=\"chartForm\" method=\"get\" action=\"compare.php\">";
		echo "<div class=\"form-group\">";
		echo "<select class=\"form-control\" name=\"inningsDate\" onChange=\"chartForms()\">";
		$innDt = "";
		if(isset($_GET['inningsDate'])) {    
		    $innDt = $_GET['inningsDate'];
		    foreach ($inningsDates as $id) {
			if ($innDt == $id) {
			    echo "<option selected=\"selected\" value=\"$id\">$id</option>";
			} else {
			    echo "<option value=\"$id\">$id</option>";
			}
		    }    
		} else {
		    $count = 0;
		    foreach ($inningsDates as $id) {
			if ($count == 0) {
			    echo "<option selected=\"selected\" value=\"$id\">$id</option>";
			    $innDt = $id;
			} else {
			    echo "<option value=\"$id\">$id</option>";
			}
			$count = $count + 1;
		    }    
		}
		echo "</select>";
		echo "</div>";
		echo "<input type=\"hidden\" name=\"playerId1\" value=\"$playerId1\">";
		echo "<input type=\"hidden\" name=\"playerId2\" value=\"$playerId2\">";
		echo "<input type=\"hidden\" name=\"player2Search\" value=\"$player2Search\">";
		echo "<input type=\"hidden\" name=\"matchFormat\" value=\"$matchFormat\">";
		echo "<input type=\"hidden\" name=\"disc\" value=\"$disc\">";    
		echo "</form>";
		echo "<div class=\"chart\">";
		echo "<div id=\"chart\"></div>";
		echo "</div>";
		echo "<div class=\"text-center\">$player1 <img src=\"images/player1.png\"/>&nbsp;&nbsp;$player2 <img src=\"images/player2.png\"/></div>";	    
	    } else {
		$chartWidth = 0.55*$_SESSION['screen_width'];
		echo "<div class=\"chart\" style=\"width:".$chartWidth."px;\">";
		echo "</div>";   
	    }
	    
	    echo "</div>";
	    echo "</li>";
	    echo "<div class=\"col-lg-6\">";
	    
	    # top batting innings
	    $tableHtml .= "<li class=\"list-group-item\">";
	    $tableHtml .= "<h4>Top Performances: $player1</h4>";
	    $sql1 = "select t.startDate,t.".$matchFormatLower."Id, b.notOut, b.runs, b.balls, b.rating, t.team1, t.team2, t.ground from batting".$matchFormat."Innings b, ".$matchFormatLower."Info t where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=".$playerId1." order by b.rating desc";   
	    $result = $db->query($sql1);
	    if (!$result) die("Cannot execute query.");	    
	    $tableHtml .= "<div><table class=\"table table-hover table-condensed\" id=\"inningsTable1\">";	    
	    $tableHtml .= "<thead><tr>";
	    $tableHtml .= "<th>Match Date</th>";
	    $tableHtml .= "<th>".$matchFormat." #</th>";
	    $tableHtml .= "<th>Runs</th>";
	    $tableHtml .= "<th>Balls</th>";
	    $tableHtml .= "<th>SR</th>";
	    $tableHtml .= "<th>Rating</th>";
	    $tableHtml .= "<th>Opposition</th>";
	    $tableHtml .= "<th>Ground</th>";
	    $tableHtml .= "</tr></thead>";
	    while($res1 = $result->fetchArray(SQLITE3_NUM)) {
		$tableHtml .= "<tr>";
		for ($j = 0; $j < $result->numColumns(); $j++) {
		    if ($j == 0) { # match date
			$dateMod = substr($res1[$j], 0, 4)."-".substr($res1[$j], 4, 2)."-".substr($res1[$j], 6, 2);
			$tableHtml .= "<td>".$dateMod."</td>";
		    } elseif ($j == 1) {
			$tableHtml .= "<td><a href=\"scorecard.php?matchFormat=".$matchFormat."&matchId=".$res1[$j]."\">".$res1[$j]."</a></td>";
		    } elseif ($j == 2) {
			$no = $res1[$j];
			$runs = $res1[$j+1];
			$balls = $res1[$j+2];
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
		    } elseif ($j == 5) { # innings rating
			$tableHtml .= "<td><b>".round($res1[$j], 0)."</b></td>";
		    } elseif ($j == 6) { # team and opposition
			if ($matchFormat == "FT20") {
			    if (strrpos($country1, $res1[$j]) === false) {
				$tableHtml .= "<td><a href=\"team.php?team=".$res1[$j]."&matchFormat=$matchFormat\">".$res1[$j]."</a></td>";
			    } else {
				$tableHtml .= "<td><a href=\"team.php?team=".$res1[$j+1]."&matchFormat=$matchFormat\">".$res1[$j+1]."</a></td>";
			    }	       
			} else {
			    if ($country1 == $res1[$j]) {
				$tableHtml .= "<td><a href=\"team.php?team=".$res1[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res1[$j+1].".png\" border=1px/></a></td>";
			    } else {
				$tableHtml .= "<td><a href=\"team.php?team=".$res1[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res1[$j].".png\" border=1px/></a></td>";
			    }	       
			}		    		    		    
			$j++;
		    } elseif ($j == 8) { # ground
			$tableHtml .= "<td>$res1[$j]</td>";
		    }        
		}       
		$tableHtml .= "</tr>";
	    } 
	    $tableHtml .= "</table><br/>";
	    $tableHtml .= "</li>";
	    $tableHtml .= "<li class=\"list-group-item\">";
	    
	    $tableHtml .= "<h4>Top Performances: $player2</h4>";
	    $sql2 = "select t.startDate,t.".$matchFormatLower."Id, b.notOut, b.runs, b.balls, b.rating, t.team1, t.team2, t.ground from batting".$matchFormat."Innings b, ".$matchFormatLower."Info t where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=".$playerId2." order by b.rating desc";   
	    $result = $db->query($sql2);
	    if (!$result) die("Cannot execute query.");
	    $tableHtml .= "<table class=\"table table-hover table-condensed\" id=\"inningsTable2\">";
	    $tableHtml .= "<thead><tr>";
	    $tableHtml .= "<th>Match Date</th>";
	    $tableHtml .= "<th>".$matchFormat." #</th>";
	    $tableHtml .= "<th>Runs</th>";
	    $tableHtml .= "<th>Balls</th>";
	    $tableHtml .= "<th>SR</th>";
	    $tableHtml .= "<th>Rating</th>";
	    $tableHtml .= "<th>Opposition</th>";
	    $tableHtml .= "<th>Ground</th>";
	    $tableHtml .= "</tr></thead>";
	    while($res2 = $result->fetchArray(SQLITE3_NUM)) {
		$tableHtml .= "<tr>";
		for ($j = 0; $j < $result->numColumns(); $j++) {
		    if ($j == 0) { # match date
			$dateMod = substr($res2[$j], 0, 4)."-".substr($res2[$j], 4, 2)."-".substr($res2[$j], 6, 2);
			$tableHtml .= "<td>".$dateMod."</td>";
		    } elseif ($j == 1) {
			$tableHtml .= "<td><a href=\"scorecard.php?matchFormat=".$matchFormat."&matchId=".$res2[$j]."\">".$res2[$j]."</a></td>";
		    } elseif ($j == 2) {
			$no = $res2[$j];
			$runs = $res2[$j+1];
			$balls = $res2[$j+2];
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
		    } elseif ($j == 5) { # innings rating
			$tableHtml .= "<td><b>".round($res2[$j], 0)."</b></td>";
		    } elseif ($j == 6) { # team and opposition
			if ($matchFormat == "FT20") {
			    if (strrpos($country2, $res2[$j]) === false) {
				$tableHtml .= "<td><a href=\"team.php?team=".$res2[$j]."&matchFormat=$matchFormat\">".$res2[$j]."</a></td>";
			    } else {
				$tableHtml .= "<td><a href=\"team.php?team=".$res2[$j+1]."&matchFormat=$matchFormat\">".$res2[$j+1]."</a></td>";
			    }	       
			} else {
			    if ($country2 == $res2[$j]) {
				$tableHtml .= "<td><a href=\"team.php?team=".$res2[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res2[$j+1].".png\" border=1px/></a></td>";
			    } else {
				$tableHtml .= "<td><a href=\"team.php?team=".$res2[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res2[$j].".png\" border=1px/></a></td>";
			    }	       
			}   
			$j++;
		    } elseif ($j == 8) { # ground
			$tableHtml .= "<td>$res2[$j]</td>";
		    }        
		}       
		$tableHtml .= "</tr>";
	    } 
	    $tableHtml .= "</table></div>";
	    $tableHtml .= "</li>";
	    echo $tableHtml;
	    echo "</div>";	    
	    echo "</div>";
	    echo "</div>";
	}    	    	
    } else if ($disc == "Bowling") {
	# bowling career    
	if ($matchFormat == "Test") {
	    $sql1 = "select startDate, endDate, ".$matchFormatLower."s, innings, balls, runs, wickets, average, econRate, strikeRate, fiveWkts, tenWkts, rating from bowling".$matchFormat."Career where playerId=".$playerId1;
	    $sql2 = "select startDate, endDate, ".$matchFormatLower."s, innings, balls, runs, wickets, average, econRate, strikeRate, fiveWkts, tenWkts, rating from bowling".$matchFormat."Career where playerId=".$playerId2;   
	} else {        
	    $sql1 = "select startDate, endDate, innings, balls, runs, wickets, average, econRate, strikeRate, threeWkts, fiveWkts, rating from bowling".$matchFormat."Career where playerId=".$playerId1;
	    $sql2 = "select startDate, endDate, innings, balls, runs, wickets, average, econRate, strikeRate, threeWkts, fiveWkts, rating from bowling".$matchFormat."Career where playerId=".$playerId2;
	}
	$result = $db->query($sql1);
	if (!$result) die("Cannot execute query.");
	$res1 = $result->fetchArray(SQLITE3_NUM);
	$result = $db->query($sql2);
	if (!$result) die("Cannot execute query.");
	$res2 = $result->fetchArray(SQLITE3_NUM);
	
	$tableHtml = "";    
	if (!empty($res1) && $res1[0] != "" && !empty($res2) && $res2[0] != "") {
	    echo "<li class=\"list-group-item\">";
	    echo "<h4>Career Summary</h4>";
	    echo "<table class=\"table table-hover table-condensed\" id=\"playerTable\">";
	    echo "<thead><tr>";
	    if ($matchFormat == "Test") {
		echo "<th>Player</th>";
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
		$numInns1 = $res1[3];
		echo "<tr>";            
		echo "<td><a href=\"player.php?playerId=$playerId1&matchFormat=$matchFormat&disc=$disc\">$player1</a></th>";
		echo "<td>".substr($res1[0], 0, 4)."-".substr($res1[1], 0, 4)."</td>"; # span
		echo "<td>$res1[2]</td><td>$res1[3]</td><td>$res1[4]</td><td>$res1[5]</td><td>$res1[6]</td>";   
		echo "<td>".number_format(round($res1[7], 2), 2)."</td><td>".number_format(round($res1[8], 2), 2)."</td>";
		echo "<td>".number_format(round($res1[9], 2), 1)."</td>";
		echo "<td>$res1[10]</td><td>$res1[11]</td>";   
		echo "<td><b>".round($res1[12], 0)."</b></td>";
		echo "</tr>";
		$numInns2 = $res2[3];
		echo "<tr>";
		echo "<td><a href=\"player.php?playerId=$playerId2&matchFormat=$matchFormat&disc=$disc\">$player2</a></th>";
		echo "<td>".substr($res2[0], 0, 4)."-".substr($res2[1], 0, 4)."</td>"; # span
		echo "<td>$res2[2]</td><td>$res2[3]</td><td>$res2[4]</td><td>$res2[5]</td><td>$res2[6]</td>";   
		echo "<td>".number_format(round($res2[7], 2), 2)."</td><td>".number_format(round($res2[8], 2), 2)."</td>";
		echo "<td>".number_format(round($res2[9], 2), 1)."</td>";
		echo "<td>$res2[10]</td><td>$res2[11]</td>";   
		echo "<td><b>".round($res2[12], 0)."</b></td>";
		echo "</tr>";
	    } else {
		echo "<th>Player</th>";
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
		$numInns1 = $res1[2];
		echo "<tr>";
		echo "<td><a href=\"player.php?playerId=$playerId1&matchFormat=$matchFormat&disc=$disc\">$player1</a></th>";
		echo "<td>".substr($res1[0], 0, 4)."-".substr($res1[1], 0, 4)."</td>"; # span
		echo "<td>$res1[2]</td><td>$res1[3]</td><td>$res1[4]</td><td>$res1[5]</td>";   
		echo "<td>".number_format(round($res1[6], 2), 2)."</td><td>".number_format(round($res1[7], 2), 2)."</td><td>".number_format(round($res1[8], 2), 1)."</td>";
		echo "<td>$res1[9]</td><td>$res1[10]</td>";   
		echo "<td><b>".round($res1[11], 0)."</b></td>";
		echo "</tr>";
		$numInns2 = $res2[2];
		echo "<tr>";
		echo "<td><a href=\"player.php?playerId=$playerId2&matchFormat=$matchFormat&disc=$disc\">$player2</a></th>";
		echo "<td>".substr($res2[0], 0, 4)."-".substr($res2[1], 0, 4)."</td>"; # span
		echo "<td>$res2[2]</td><td>$res2[3]</td><td>$res2[4]</td><td>$res2[5]</td>";   
		echo "<td>".number_format(round($res2[6], 2), 2)."</td><td>".number_format(round($res2[7], 2), 2)."</td><td>".number_format(round($res2[8], 2), 1)."</td>";
		echo "<td>$res2[9]</td><td>$res2[10]</td>";   
		echo "<td><b>".round($res2[11], 0)."</b></td>";
		echo "</tr>";
	    }        
	    echo "</table>";
	    
	    # current bowling ratings
	    $sql1 = "select rating from bowling".$matchFormat."Live where playerId=".$playerId1;   
	    $result1 = $db->query($sql1);
	    if (!$result1) die("Cannot execute query.");
	    $sql2 = "select rating from bowling".$matchFormat."Live where playerId=".$playerId2;   
	    $result2 = $db->query($sql2);	
	    if (!$result2) die("Cannot execute query.");
	    echo "</li>";
	    echo "<li class=\"list-group-item\">";
	    if ($numInns1 > 20 & $numInns2 > 20) {
		echo "<h4>Current Rating Timeline</h4>";
		echo "By ";
		$inningsDates = array("Inning", "Date");
		echo "<form class=\"form-inline\" role=\"form\" name=\"chartForm\" method=\"get\" action=\"compare.php\">";
		echo "<div class=\"form-group\">";
		echo "<select class=\"form-control\" name=\"inningsDate\" onChange=\"chartForms()\">";
		$innDt = "";
		if(isset($_GET['inningsDate'])) {    
		    $innDt = $_GET['inningsDate'];
		    foreach ($inningsDates as $id) {
			if ($innDt == $id) {
			    echo "<option selected=\"selected\" value=\"$id\">$id</option>";
			} else {
			    echo "<option value=\"$id\">$id</option>";
			}
		    }    
		} else {
		    $count = 0;
		    foreach ($inningsDates as $id) {
			if ($count == 0) {
			    echo "<option selected=\"selected\" value=\"$id\">$id</option>";
			    $innDt = $id;
			} else {
			    echo "<option value=\"$id\">$id</option>";
			}
			$count = $count + 1;
		    }    
		}
		echo "</select>";
		echo "</div>";
		echo "<input type=\"hidden\" name=\"playerId1\" value=\"$playerId1\">";
		echo "<input type=\"hidden\" name=\"playerId2\" value=\"$playerId2\">";
		echo "<input type=\"hidden\" name=\"player2Search\" value=\"$player2Search\">";
		echo "<input type=\"hidden\" name=\"matchFormat\" value=\"$matchFormat\">";
		echo "<input type=\"hidden\" name=\"disc\" value=\"$disc\">";    
		echo "</form>";
		echo "<div class=\"chart\">";
		echo "<div id=\"chart\"></div>";
		echo "</div>";
		echo "<div class=\"text-center\">$player1 <img src=\"images/player1.png\"/>&nbsp;&nbsp;$player2 <img src=\"images/player2.png\"/></div>";
	    } else {
		$chartWidth = 0.55*$_SESSION['screen_width'];
		echo "<div class=\"chart\" style=\"width:".$chartWidth."px;\">";
		echo "</div>";   
	    }
	    
	    echo "</div>";
	    echo "</li>";
	    echo "<div class=\"col-lg-6\">";
	    
	    # top 10 bowling innings	    
	    $tableHtml .= "<li class=\"list-group-item\">";
	    $tableHtml .= "<h4>Top Performances: $player1</h4>";
	    if ($matchFormat == "T20I" || $matchFormat == "FT20") {
		$sql1 = "select t.startDate, t.".$matchFormatLower."Id, b.balls, b.runs, b.wkts, b.rating, t.team1, t.team2, t.ground from bowling".$matchFormat."Innings b, ".$matchFormatLower."Info t where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=".$playerId1." order by b.rating desc";      
	    } else {
		$sql1 = "select t.startDate, t.".$matchFormatLower."Id, b.balls, b.runs, b.wkts, b.rating, t.team1, t.team2, t.ground, t.ballsPerOver from bowling".$matchFormat."Innings b, ".$matchFormatLower."Info t where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=".$playerId1." order by b.rating desc";      
	    }
	    $result = $db->query($sql1);
	    if (!$result) die("Cannot execute query.");
	    $tableHtml .= "<div><table class=\"table table-hover table-condensed\" id=\"inningsTable1\">";
	    $tableHtml .= "<thead><tr>";
	    $tableHtml .= "<th>Match Date</th>";
	    $tableHtml .= "<th>".$matchFormat." #</th>";
	    $tableHtml .= "<th>Overs</th>";
	    $tableHtml .= "<th>Runs</th>";
	    $tableHtml .= "<th>Wkts</th>";       
	    $tableHtml .= "<th>Rating</th>";
	    $tableHtml .= "<th>Opposition</th>";
	    $tableHtml .= "<th>Ground</th>";
	    $tableHtml .= "</tr></thead>";
	    while($res1 = $result->fetchArray(SQLITE3_NUM)) {
		$tableHtml .= "<tr>";
		for ($j = 0; $j < $result->numColumns(); $j++) {
		    if ($j == 0) { # match date
			$dateMod = substr($res1[$j], 0, 4)."-".substr($res1[$j], 4, 2)."-".substr($res1[$j], 6, 2);
			$tableHtml .= "<td>".$dateMod."</td>";
		    } elseif ($j == 1) {
			$tableHtml .= "<td><a href=\"scorecard.php?matchFormat=".$matchFormat."&matchId=".$res1[$j]."\">".$res1[$j]."</a></td>";
		    } elseif ($j == 2) {
			if ($matchFormat == "T20I" || $matchFormat == "FT20") {
			    $bpo = 6;
			} else {
			    $bpo = $res1[9];
			}
			
			if ($bpo == '') {
			    $bpo = 6;
			}
			$balls = $res1[$j] % $bpo;
			$overs = ($res1[$j]-$balls) / $bpo;
			if ($bpo == 6) {
			    $tableHtml .= "<td>".$overs.".".$balls."</td>";
			} else {
			    $tableHtml .= "<td>".$overs.".".$balls."x".$bpo."</td>";
			}
		    } elseif ($j == 5) { # innings rating
			$tableHtml .= "<td><b>".round($res1[$j], 0)."</b></td>";
		    } elseif ($j == 6) { # team and opposition		    
			if ($matchFormat == "FT20") {
			    if (strrpos($country1, $res1[$j]) === false) {
				$tableHtml .= "<td><a href=\"team.php?team=".$res1[$j]."&matchFormat=$matchFormat\">".$res1[$j]."</a></td>";
			    } else {
				$tableHtml .= "<td><a href=\"team.php?team=".$res1[$j+1]."&matchFormat=$matchFormat\">".$res1[$j+1]."</a></td>";
			    }	       
			} else {
			    if ($country1 == $res1[$j]) {
				$tableHtml .= "<td><a href=\"team.php?team=".$res1[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res1[$j+1].".png\" border=1px/></a></td>";
			    } else {
				$tableHtml .= "<td><a href=\"team.php?team=".$res1[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res1[$j].".png\" border=1px/></a></td>";
			    }	       
			}	    
			$j++;
		    } elseif ($j == 8) { # ground
			$tableHtml .= "<td>$res1[$j]</td>";
		    } elseif ($j == 9) { # ignore balls per over
		    } else {
			$tableHtml .= "<td>$res1[$j]</td>";
		    }        
		}       
		$tableHtml .= "</tr>";
	    } 
	    $tableHtml .= "</table><br/>";
	    
	    if ($matchFormat == "T20I" || $matchFormat == "FT20") {
		$sql2 = "select t.startDate, t.".$matchFormatLower."Id, b.balls, b.runs, b.wkts, b.rating, t.team1, t.team2, t.ground from bowling".$matchFormat."Innings b, ".$matchFormatLower."Info t where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=".$playerId2." order by b.rating desc";      
	    } else {
		$sql2 = "select t.startDate, t.".$matchFormatLower."Id, b.balls, b.runs, b.wkts, b.rating, t.team1, t.team2, t.ground, t.ballsPerOver from bowling".$matchFormat."Innings b, ".$matchFormatLower."Info t where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=".$playerId2." order by b.rating desc";      
	    }
	    $tableHtml .= "</li>";
	    $tableHtml .= "<li class=\"list-group-item\">";
	    $tableHtml .= "<h4>Top Performances: $player2</h4>";
	    $result = $db->query($sql2);
	    if (!$result) die("Cannot execute query.");
	    $tableHtml .= "<table class=\"table table-hover table-condensed\" id=\"inningsTable2\">";
	    $tableHtml .= "<thead><tr>";
	    $tableHtml .= "<th>Match Date</th>";
	    $tableHtml .= "<th>".$matchFormat." #</th>";
	    $tableHtml .= "<th>Overs</th>";
	    $tableHtml .= "<th>Runs</th>";
	    $tableHtml .= "<th>Wkts</th>";       
	    $tableHtml .= "<th>Rating</th>";
	    $tableHtml .= "<th>Opposition</th>";
	    $tableHtml .= "<th>Ground</th>";
	    $tableHtml .= "</tr></thead>";
	    while($res2 = $result->fetchArray(SQLITE3_NUM)) {
		$tableHtml .= "<tr>";
		for ($j = 0; $j < $result->numColumns(); $j++) {
		    if ($j == 0) { # match date
			$dateMod = substr($res2[$j], 0, 4)."-".substr($res2[$j], 4, 2)."-".substr($res2[$j], 6, 2);
			$tableHtml .= "<td>".$dateMod."</td>";
		    } elseif ($j == 1) {
			$tableHtml .= "<td><a href=\"scorecard.php?matchFormat=".$matchFormat."&matchId=".$res2[$j]."\">".$res2[$j]."</a></td>";
		    } elseif ($j == 2) {
			if ($matchFormat == "T20I" || $matchFormat == "FT20") {
			    $bpo = 6;
			} else {
			    $bpo = $res2[9];
			}
			
			if ($bpo == '') {
			    $bpo = 6;
			}
			$balls = $res2[$j] % $bpo;
			$overs = ($res2[$j]-$balls) / $bpo;
			if ($bpo == 6) {
			    $tableHtml .= "<td>".$overs.".".$balls."</td>";
			} else {
			    $tableHtml .= "<td>".$overs.".".$balls."x".$bpo."</td>";
			}
		    } elseif ($j == 5) { # innings rating
			$tableHtml .= "<td><b>".round($res2[$j], 0)."</b></td>";
		    } elseif ($j == 6) { # team and opposition
			if ($matchFormat == "FT20") {
			    if (strrpos($country2, $res2[$j]) === false) {
				$tableHtml .= "<td><a href=\"team.php?team=".$res2[$j]."&matchFormat=$matchFormat\">".$res2[$j]."</a></td>";
			    } else {
				$tableHtml .= "<td><a href=\"team.php?team=".$res2[$j+1]."&matchFormat=$matchFormat\">".$res2[$j+1]."</a></td>";
			    }	       
			} else {
			    if ($country2 == $res2[$j]) {
				$tableHtml .= "<td><a href=\"team.php?team=".$res2[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res2[$j+1].".png\" border=1px/></a></td>";
			    } else {
				$tableHtml .= "<td><a href=\"team.php?team=".$res2[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res2[$j].".png\" border=1px/></a></td>";
			    }	       
			}    
			$j++;
		    } elseif ($j == 8) { # ground
			$tableHtml .= "<td>$res2[$j]</td>";
		    } elseif ($j == 9) { # ignore balls per over
		    } else {
			$tableHtml .= "<td>$res2[$j]</td>";
		    }     
		}       
		$tableHtml .= "</tr>";
	    } 
	    $tableHtml .= "</table></div>";
	    $tableHtml .= "</li>";
	    echo $tableHtml;
	    echo "</div>";	    
	    echo "</div>";
	    echo "</div>";
	}	
    } else if ($disc == "All-Round") {
	# all-round career
	if ($matchFormat == "Test") {
	    $sql1 = "select startDate, endDate, ".$matchFormatLower."s, runs, battingAverage, hundreds, wickets, bowlingAverage, fiveWkts, hundredFiveWkts, rating from allRound".$matchFormat."Career where playerId=".$playerId1;
	    $sql2 = "select startDate, endDate, ".$matchFormatLower."s, runs, battingAverage, hundreds, wickets, bowlingAverage, fiveWkts, hundredFiveWkts, rating from allRound".$matchFormat."Career where playerId=".$playerId2; 
	} else {
	    if ($matchFormat == "FT20" || $matchFormat == "T20I") {
		$sql1 = "select startDate, endDate, ".$matchFormatLower."s, runs, battingAverage, fifties, wickets, bowlingAverage, threeWkts, thirtyTwoWkts, rating from allRound".$matchFormat."Career where playerId=".$playerId1;
		$sql2 = "select startDate, endDate, ".$matchFormatLower."s, runs, battingAverage, fifties, wickets, bowlingAverage, threeWkts, thirtyTwoWkts, rating from allRound".$matchFormat."Career where playerId=".$playerId2;
	    } else {
		$sql1 = "select startDate, endDate, ".$matchFormatLower."s, runs, battingAverage, fifties, wickets, bowlingAverage, threeWkts, fiftyThreeWkts, rating from allRound".$matchFormat."Career where playerId=".$playerId1;
		$sql2 = "select startDate, endDate, ".$matchFormatLower."s, runs, battingAverage, fifties, wickets, bowlingAverage, threeWkts, fiftyThreeWkts, rating from allRound".$matchFormat."Career where playerId=".$playerId2;
	    }	    
	}
	$result = $db->query($sql1);
	if (!$result) die("Cannot execute query.");
	$res1 = $result->fetchArray(SQLITE3_NUM);
	$result = $db->query($sql2);
	if (!$result) die("Cannot execute query.");
	$res2 = $result->fetchArray(SQLITE3_NUM);
	
	$tableHtml = "";    
	if (!empty($res1) && $res1[0] != "" && !empty($res2) && $res2[0] != "") {
	    echo "<li class=\"list-group-item\">";
	    echo "<h4>Career Summary</h4>";
	    echo "<table class=\"table table-hover table-condensed\" id=\"playerTable\">";
	    echo "<thead><tr>";
	    
	    if ($matchFormat == "Test") {
		echo "<th>Player</th>";
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
		$numInns1 = $res1[2];
		echo "<tr>";					    
		echo "<td><a href=\"player.php?playerId=$playerId1&matchFormat=$matchFormat&disc=$disc\">$player1</a></th>";
		echo "<td>".substr($res1[0], 0, 4)."-".substr($res1[1], 0, 4)."</td>"; # span
		echo "<td>$res1[2]</td><td>$res1[3]</td>";
		echo "<td>".number_format(round($res1[4], 2), 2)."</td>";
		echo "<td>$res1[5]</td><td>$res1[6]</td>";
		echo "<td>".number_format(round($res1[7], 2), 2)."</td>";
		echo "<td>$res1[8]</td><td>$res1[9]</td>";
		echo "<td><b>".round($res1[10], 0)."</b></td>";   
		echo "</tr>";
		$numInns2 = $res2[2];
		echo "<tr>";
		echo "<td><a href=\"player.php?playerId=$playerId2&matchFormat=$matchFormat&disc=$disc\">$player2</a></th>";
		echo "<td>".substr($res2[0], 0, 4)."-".substr($res2[1], 0, 4)."</td>"; # span
		echo "<td>$res2[2]</td><td>$res2[3]</td>";
		echo "<td>".number_format(round($res2[4], 2), 2)."</td>";
		echo "<td>$res2[5]</td><td>$res2[6]</td>";
		echo "<td>".number_format(round($res2[7], 2), 2)."</td>";
		echo "<td>$res2[8]</td><td>$res2[9]</td>";
		echo "<td><b>".round($res2[10], 0)."</b></td>";   
		echo "</tr>";
	    } else {
		echo "<th>Player</th>";
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
		$numInns1 = $res1[2];
		echo "<tr>";
		echo "<td><a href=\"player.php?playerId=$playerId1&matchFormat=$matchFormat&disc=$disc\">$player1</a></th>";
		echo "<td>".substr($res1[0], 0, 4)."-".substr($res1[1], 0, 4)."</td>"; # span
		echo "<td>$res1[2]</td><td>$res1[3]</td>";
		echo "<td>".number_format(round($res1[4], 2), 2)."</td>";
		echo "<td>$res1[5]</td><td>$res1[6]</td>";
		echo "<td>".number_format(round($res1[7], 2), 2)."</td>";
		echo "<td>$res1[8]</td><td>$res1[9]</td>";
		echo "<td><b>".round($res1[10], 0)."</b></td>";   
		echo "</tr>";
		$numInns2 = $res2[2];
		echo "<tr>";
		echo "<td><a href=\"player.php?playerId=$playerId2&matchFormat=$matchFormat&disc=$disc\">$player2</a></th>";
		echo "<td>".substr($res2[0], 0, 4)."-".substr($res2[1], 0, 4)."</td>"; # span
		echo "<td>$res2[2]</td><td>$res2[3]</td>";
		echo "<td>".number_format(round($res2[4], 2), 2)."</td>";
		echo "<td>$res2[5]</td><td>$res2[6]</td>";
		echo "<td>".number_format(round($res2[7], 2), 2)."</td>";
		echo "<td>$res2[8]</td><td>$res2[9]</td>";
		echo "<td><b>".round($res2[10], 0)."</b></td>";   
		echo "</tr>";
	    }        
	    echo "</table>";
	    		
	    # current all-round ratings
	    $sql1 = "select rating from allRound".$matchFormat."Live where playerId=".$playerId1;   
	    $result1 = $db->query($sql1);
	    if (!$result1) die("Cannot execute query.");
	    $sql2 = "select rating from allRound".$matchFormat."Live where playerId=".$playerId2;   
	    $result2 = $db->query($sql2);	
	    if (!$result2) die("Cannot execute query.");
	    echo "</li>";
	    echo "<li class=\"list-group-item\">";
	    if ($numInns1 > 20 & $numInns2 > 20) {
		echo "<h4>Current Rating Timeline</h4>";
		echo "By ";
		$inningsDates = array("Inning", "Date");
		echo "<form class=\"form-inline\" role=\"form\" name=\"chartForm\" method=\"get\" action=\"compare.php\">";
		echo "<div class=\"form-group\">";
		echo "<select class=\"form-control\" name=\"inningsDate\" onChange=\"chartForms()\">";
		$innDt = "";
		if(isset($_GET['inningsDate'])) {    
		    $innDt = $_GET['inningsDate'];		    
		    foreach ($inningsDates as $id) {
			if ($id == "Inning") {
			    $idMod ="Match";
			} else {
			    $idMod = "Date";
			}
			if ($innDt == $id) {
			    echo "<option selected=\"selected\" value=\"$id\">$idMod</option>";
			} else {
			    echo "<option value=\"$id\">$idMod</option>";
			}
		    }    
		} else {
		    $count = 0;
		    foreach ($inningsDates as $id) {
			if ($id == "Inning") {
			    $idMod ="Match";
			} else {
			    $idMod = "Date";
			}
			if ($count == 0) {
			    echo "<option selected=\"selected\" value=\"$id\">$idMod</option>";
			    $innDt = $id;
			} else {
			    echo "<option value=\"$id\">$idMod</option>";
			}
			$count = $count + 1;
		    }    
		}
		echo "</select>";
		echo "</div>";
		echo "<input type=\"hidden\" name=\"playerId1\" value=\"$playerId1\">";
		echo "<input type=\"hidden\" name=\"playerId2\" value=\"$playerId2\">";
		echo "<input type=\"hidden\" name=\"player2Search\" value=\"$player2Search\">";
		echo "<input type=\"hidden\" name=\"matchFormat\" value=\"$matchFormat\">";
		echo "<input type=\"hidden\" name=\"disc\" value=\"$disc\">";    
		echo "</form>";
		echo "<div class=\"chart\">";
		echo "<div id=\"chart\"></div>";
		echo "</div>";
		echo "<div class=\"text-center\">$player1 <img src=\"images/player1.png\"/>&nbsp;&nbsp;$player2 <img src=\"images/player2.png\"/></div>";
	    } else {
		$chartWidth = 0.55*$_SESSION['screen_width'];
		echo "<div class=\"chart\" style=\"width:".$chartWidth."px;\">";
		echo "</div>";   
	    }
	    
	    echo "</div>";
	    echo "</li>";
	    echo "<div class=\"col-lg-6\">";
	    
	    # top allRound matches
	    $tableHtml .= "<li class=\"list-group-item\">";
	    $tableHtml .= "<h4>Top Performances: $player1</h4>";	
	    if ($matchFormat == "Test") {
		$sql1 = "select t.startDate, t.".$matchFormatLower."Id, b.notOut1, b.runs1, b.notOut2, b.runs2, b.wkts1, b.bowlRuns1, b.wkts2, b.bowlRuns2, b.rating, t.team1, t.team2, t.ground from allRound".$matchFormat."Match b, ".$matchFormatLower."Info t where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=".$playerId1." order by b.rating desc";      
	    } else {
		$sql1 = "select t.startDate, t.".$matchFormatLower."Id, b.notOut, b.runs, b.wkts, b.bowlRuns, b.rating, t.team1, t.team2, t.ground from allRound".$matchFormat."Match b, ".$matchFormatLower."Info t where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=".$playerId1." order by b.rating desc";      
	    }
	    $result = $db->query($sql1);
	    if (!$result) die("Cannot execute query.");
	    $tableHtml .= "<table class=\"table table-hover table-condensed\" id=\"inningsTable1\">";
	    $tableHtml .= "<thead><tr>";
	    $tableHtml .= "<th>Match Date</th>";
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
	    $tableHtml .= "<th>Rating</th>";
	    $tableHtml .= "<th>Opposition</th>";
	    $tableHtml .= "<th>Ground</th>";
	    $tableHtml .= "</tr></thead>";
	    while($res = $result->fetchArray(SQLITE3_NUM)) {
		$tableHtml .= "<tr>";
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
			    } elseif ($j == 10) { # match rating
				$tableHtml .= "<td><b>".round($res[$j], 0)."</b></td>";
			    } elseif ($j == 11) { # team and opposition
				if ($matchFormat == "FT20") {
				    if (strrpos($country1, $res[$j]) === false) {
					$tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\">".$res[$j]."</a></td>";                            
				    } else {
					$tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";
				    }	       
				} else {
				    if ($country1 == $res[$j]) {
					$tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td>";
				    } else {
					$tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" border=1px/></a></td>";
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
			    } elseif ($j == 6) { # match rating
				$tableHtml .= "<td><b>".round($res[$j], 0)."</b></td>";
			    } elseif ($j == 7) { # team and opposition
				if ($matchFormat == "FT20") {
				    if (strrpos($country1, $res[$j]) === false) {
					$tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\">".$res[$j]."</a></td>";                            
				    } else {
					$tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";
				    }	       
				} else {
				    if ($country1 == $res[$j]) {
					$tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td>";
				    } else {
					$tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" border=1px/></a></td>";
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
	    } 
	    $tableHtml .= "</table><br/>";	    	
	    $tableHtml .= "</li>";
	    
	    $tableHtml .= "<li class=\"list-group-item\">";
	    $tableHtml .= "<h4>Top Performances: $player2</h4>";
	    if ($matchFormat == "Test") {
		$sql2 = "select t.startDate, t.".$matchFormatLower."Id, b.notOut1, b.runs1, b.notOut2, b.runs2, b.wkts1, b.bowlRuns1, b.wkts2, b.bowlRuns2, b.rating, t.team1, t.team2, t.ground from allRound".$matchFormat."Match b, ".$matchFormatLower."Info t where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=".$playerId2." order by b.rating desc";      
	    } else {
		$sql2 = "select t.startDate, t.".$matchFormatLower."Id, b.notOut, b.runs, b.wkts, b.bowlRuns, b.rating, t.team1, t.team2, t.ground from allRound".$matchFormat."Match b, ".$matchFormatLower."Info t where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=".$playerId2." order by b.rating desc";      
	    }
	    $result = $db->query($sql2);
	    if (!$result) die("Cannot execute query.");
	    $tableHtml .= "<table class=\"table table-hover table-condensed\" id=\"inningsTable2\">";
	    $tableHtml .= "<thead><tr>";
	    $tableHtml .= "<th>Match Date</th>";
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
	    $tableHtml .= "<th>Rating</th>";
	    $tableHtml .= "<th>Opposition</th>";
	    $tableHtml .= "<th>Ground</th>";
	    $tableHtml .= "</tr></thead>";
	    while($res = $result->fetchArray(SQLITE3_NUM)) {
		$tableHtml .= "<tr>";
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
			    } elseif ($j == 10) { # match rating
				$tableHtml .= "<td><b>".round($res[$j], 0)."</b></td>";
			    } elseif ($j == 11) { # team and opposition
				if ($matchFormat == "FT20") {
				    if (strrpos($country2, $res[$j]) === false) {
					$tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\">".$res[$j]."</a></td>";                            
				    } else {
					$tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";
				    }	       
				} else {
				    if ($country2 == $res[$j]) {
					$tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td>";
				    } else {
					$tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" border=1px/></a></td>";
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
			    } elseif ($j == 6) { # match rating
				$tableHtml .= "<td><b>".round($res[$j], 0)."</b></td>";
			    } elseif ($j == 7) { # team and opposition
				if ($matchFormat == "FT20") {
				    if (strrpos($country2, $res[$j]) === false) {
					$tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\">".$res[$j]."</a></td>";                            
				    } else {
					$tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";
				    }	       
				} else {
				    if ($country2 == $res[$j]) {
					$tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td>";
				    } else {
					$tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" border=1px/></a></td>";
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
	    } 	    
	    $tableHtml .= "</table>";
	    $tableHtml .= "</li>";
	    echo $tableHtml;
	    echo "</div>";	    
	    echo "</div>";
	    echo "</div>";
	}	
    } else if ($disc == "Fielding") {
 	# fielding career
 	$sql1 = "select startDate, endDate, ".$matchFormatLower."s, keeper, catches, droppedCatches, dropRate, matPerDrop, greatCatches, directHits, runsSaved, stumpings, missedStumpings, stumpRate, rating from fielding".$matchFormat."Career where playerId=".$playerId1;
	$sql2 = "select startDate, endDate, ".$matchFormatLower."s, keeper, catches, droppedCatches, dropRate, matPerDrop, greatCatches, directHits, runsSaved, stumpings, missedStumpings, stumpRate, rating from fielding".$matchFormat."Career where playerId=".$playerId2;	
	$result = $db->query($sql1);
	if (!$result) die("Cannot execute query.");
	$res1 = $result->fetchArray(SQLITE3_NUM);
	$result = $db->query($sql2);
	if (!$result) die("Cannot execute query.");
	$res2 = $result->fetchArray(SQLITE3_NUM);
	$keeper1 = $res1[3];
	$keeper2 = $res2[3];
	$tableHtml = "";    
	if (!empty($res1) && $res1[0] != "" && !empty($res2) && $res2[0] != "") {
	    echo "<li class=\"list-group-item\">";
	    echo "<h4>Career Summary</h4>";
	    echo "<table class=\"table table-hover table-condensed\" id=\"playerTable\">";
	    echo "<thead><tr>";	    
	    echo "<th>Player</th>";
	    echo "<th>Span</th>";
	    echo "<th>Mat</th>";
	    echo "<th>Keeper</th>";
	    echo "<th>Cat</th>";
	    echo "<th>Drop</th>";
	    echo "<th>Drop%</th>";
	    echo "<th>Mat/Drop</th>";
	    echo "<th>GrtCat</th>";
	    if ($keeper1 == 1 and $keeper2 == 1) {
		echo "<th>Stump</th>";
		echo "<th>MissStump</th>";
		echo "<th>Drop%</th>";
	    } else {
		echo "<th>DirectHit</th>";
		echo "<th>RunsSaved</th>";   
	    }			    
	    echo "<th>Career Rating</th>";     
	    echo "</tr></thead>";
	    $numInns1 = $res1[2];
	    echo "<tr>";
	    echo "<td><a href=\"player.php?playerId=$playerId1&matchFormat=$matchFormat&disc=$disc\">$player1</a></th>";	    
	    echo "<td>".substr($res1[0], 0, 4)."-".substr($res1[1], 0, 4)."</td>"; # span
	    echo "<td>$res1[2]</td><td>$res1[3]</td><td>$res1[4]</td><td>$res1[5]</td>";
	    echo "<td>".number_format(round($res1[6] * 100, 2), 2)."</td>";
	    echo "<td>".number_format(round($res1[7], 1), 1)."</td>";
	    echo "<td>$res1[8]</td>";
	    if ($keeper1 == 1) {
		echo "<td>$res1[11]</td><td>$res1[12]</td>";
		echo "<td>".number_format(round($res1[13], 2), 2)."</td>";
	    } else {
		echo "<td>$res1[9]</td><td>$res1[10]</td>";	    
	    }	
	    echo "<td><b>".round($res1[14], 0)."</b></td>";   	    
	    echo "</tr>";
	    $numInns2 = $res2[2];
	    echo "<tr>";
	    echo "<td><a href=\"player.php?playerId=$playerId1&matchFormat=$matchFormat&disc=$disc\">$player2</a></th>";	    
	    echo "<td>".substr($res2[0], 0, 4)."-".substr($res2[1], 0, 4)."</td>"; # span
	    echo "<td>$res2[2]</td><td>$res2[3]</td><td>$res2[4]</td><td>$res2[5]</td>";
	    echo "<td>".number_format(round($res2[6] * 100, 2), 2)."</td>";
	    echo "<td>".number_format(round($res2[7], 1), 1)."</td>";
	    echo "<td>$res2[8]</td>";
	    if ($keeper2 == 1) {
		echo "<td>$res2[11]</td><td>$res2[12]</td>";
		echo "<td>".number_format(round($res2[13], 2), 2)."</td>";
	    } else {
		echo "<td>$res2[9]</td><td>$res2[10]</td>";	    
	    }	
	    echo "<td><b>".round($res2[14], 0)."</b></td>";
	    echo "</tr>";
	    echo "</table>";
	    		
	    # current fielding ratings
	    $sql1 = "select rating from fielding".$matchFormat."Live where playerId=".$playerId1;   
	    $result1 = $db->query($sql1);
	    if (!$result1) die("Cannot execute query.");
	    $sql2 = "select rating from fielding".$matchFormat."Live where playerId=".$playerId2;   
	    $result2 = $db->query($sql2);	
	    if (!$result2) die("Cannot execute query.");
	    echo "</li>";
	    echo "<li class=\"list-group-item\">";
	    if ($numInns1 > 20 & $numInns2 > 20) {
		echo "<h4>Current Rating Timeline</h4>";
		echo "By ";
		$inningsDates = array("Inning", "Date");
		echo "<form class=\"form-inline\" role=\"form\" name=\"chartForm\" method=\"get\" action=\"compare.php\">";
		echo "<div class=\"form-group\">";
		echo "<select class=\"form-control\" name=\"inningsDate\" onChange=\"chartForms()\">";
		$innDt = "";
		if(isset($_GET['inningsDate'])) {    
		    $innDt = $_GET['inningsDate'];		    
		    foreach ($inningsDates as $id) {
			if ($id == "Inning") {
			    $idMod ="Match";
			} else {
			    $idMod = "Date";
			}
			if ($innDt == $id) {
			    echo "<option selected=\"selected\" value=\"$id\">$idMod</option>";
			} else {
			    echo "<option value=\"$id\">$idMod</option>";
			}
		    }    
		} else {
		    $count = 0;
		    foreach ($inningsDates as $id) {
			if ($id == "Inning") {
			    $idMod ="Match";
			} else {
			    $idMod = "Date";
			}
			if ($count == 0) {
			    echo "<option selected=\"selected\" value=\"$id\">$idMod</option>";
			    $innDt = $id;
			} else {
			    echo "<option value=\"$id\">$idMod</option>";
			}
			$count = $count + 1;
		    }    
		}
		echo "</select>";
		echo "</div>";
		echo "<input type=\"hidden\" name=\"playerId1\" value=\"$playerId1\">";
		echo "<input type=\"hidden\" name=\"playerId2\" value=\"$playerId2\">";
		echo "<input type=\"hidden\" name=\"player2Search\" value=\"$player2Search\">";
		echo "<input type=\"hidden\" name=\"matchFormat\" value=\"$matchFormat\">";
		echo "<input type=\"hidden\" name=\"disc\" value=\"$disc\">";    
		echo "</form>";
		echo "<div class=\"chart\">";
		echo "<div id=\"chart\"></div>";
		echo "</div>";
		echo "<div class=\"text-center\">$player1 <img src=\"images/player1.png\"/>&nbsp;&nbsp;$player2 <img src=\"images/player2.png\"/></div>";
	    } else {
		$chartWidth = 0.55*$_SESSION['screen_width'];
		echo "<div class=\"chart\" style=\"width:".$chartWidth."px;\">";
		echo "</div>";   
	    }
	    
	    echo "</div>";
	    echo "</li>";
	    echo "<div class=\"col-lg-6\">";
	    
	    # top fielding matches
	    $tableHtml .= "<li class=\"list-group-item\">";
	    $tableHtml .= "<h4>Top Performances: $player1</h4>";
	    if ($keeper1 == 1) {
		$sql1 = "select t.startDate, b.".$matchFormatLower."Id, b.catches, b.droppedCatches, b.greatCatches, b.stumpings, b.missedStumpings, b.rating, t.team1, t.team2, t.ground from fielding".$matchFormat."Match b, fielding".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId1." order by b.rating desc";           
	    } else {
		$sql1 = "select t.startDate, b.".$matchFormatLower."Id, b.catches, b.droppedCatches, b.greatCatches, b.directHits, b.runsSaved, b.rating, t.team1, t.team2, t.ground from fielding".$matchFormat."Match b, fielding".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId1." order by b.rating desc";              
	    }
	    $result = $db->query($sql1);
	    if (!$result) die("Cannot execute query.");
	    $tableHtml .= "<table class=\"table table-hover table-condensed\" id=\"inningsTable1\">";
	    $tableHtml .= "<thead><tr>";
	    $tableHtml .= "<th>Match Date</th>";
	    $tableHtml .= "<th>".$matchFormat." #</th>";
	    $tableHtml .= "<th>Cat</th>";
	    $tableHtml .= "<th>Drops</th>";
	    $tableHtml .= "<th>GrtCat</th>";
	    if ($keeper1 == 1) {
		$tableHtml .= "<th>Stmp</th>";
		$tableHtml .= "<th>MisStp</th>";   
	    } else {
		$tableHtml .= "<th>DirHit</th>";
		$tableHtml .= "<th>Run</th>";   
	    }		   
	    $tableHtml .= "<th>Rating</th>";
	    $tableHtml .= "<th>Opposition</th>";
	    $tableHtml .= "<th>Ground</th>";
	    $tableHtml .= "</tr></thead>";
	    while($res = $result->fetchArray(SQLITE3_NUM)) {
		$tableHtml .= "<tr>";
		for ($j = 0; $j < $result->numColumns(); $j++) {
		    if ($j == 0) { # match date
			$dateMod = substr($res[$j], 0, 4)."-".substr($res[$j], 4, 2)."-".substr($res[$j], 6, 2);
			$tableHtml .= "<td>".$dateMod."</td>";
		    } elseif ($j == 1) {
			$tableHtml .= "<td><a href=\"scorecard.php?matchFormat=".$matchFormat."&matchId=".$res[$j]."\">".$res[$j]."</a></td>";		    
		    } elseif ($j == 7) { # match rating or live rating
			$tableHtml .= "<td><b>".round($res[$j], 0)."</b></td>";
		    } elseif ($j == 8) { # team and opposition
			if ($matchFormat == "FT20") {
			    if (strrpos($country1, $res[$j]) === false) {
				$tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\">".$res[$j]."</a></td>";                            
			    } else {
				$tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";
			    }	       
			} else {
			    if ($country1 == $res[$j]) {
				$tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td>";
			    } else {
				$tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" border=1px/></a></td>";
			    }	       
			}                    
			$j++;
		    } else {
			$tableHtml .= "<td>$res[$j]</td>";
		    }
		}
		$tableHtml .= "</tr>";
	    } 
	    $tableHtml .= "</table><br/>";	    	
	    $tableHtml .= "</li>";
	    
	    $tableHtml .= "<li class=\"list-group-item\">";
	    $tableHtml .= "<h4>Top Performances: $player2</h4>";
	    if ($keeper2 == 1) {
		$sql2 = "select t.startDate, b.".$matchFormatLower."Id, b.catches, b.droppedCatches, b.greatCatches, b.stumpings, b.missedStumpings, b.rating, t.team1, t.team2, t.ground from fielding".$matchFormat."Match b, fielding".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId2." order by b.rating desc";           
	    } else {
		$sql2 = "select t.startDate, b.".$matchFormatLower."Id, b.catches, b.droppedCatches, b.greatCatches, b.directHits, b.runsSaved, b.rating, t.team1, t.team2, t.ground from fielding".$matchFormat."Match b, fielding".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId2." order by b.rating desc";              
	    }
	    $result = $db->query($sql2);
	    if (!$result) die("Cannot execute query.");
	    $tableHtml .= "<table class=\"table table-hover table-condensed\" id=\"inningsTable2\">";
	    $tableHtml .= "<thead><tr>";
	    $tableHtml .= "<th>Match Date</th>";
	    $tableHtml .= "<th>".$matchFormat." #</th>";
	    $tableHtml .= "<th>Cat</th>";
	    $tableHtml .= "<th>Drops</th>";
	    $tableHtml .= "<th>GrtCat</th>";
	    if ($keeper2 == 1) {
		$tableHtml .= "<th>Stmp</th>";
		$tableHtml .= "<th>MisStp</th>";   
	    } else {
		$tableHtml .= "<th>DirHit</th>";
		$tableHtml .= "<th>Run</th>";   
	    }		   
	    $tableHtml .= "<th>Rating</th>";
	    $tableHtml .= "<th>Opposition</th>";
	    $tableHtml .= "<th>Ground</th>";
	    $tableHtml .= "</tr></thead>";
	    while($res = $result->fetchArray(SQLITE3_NUM)) {
		$tableHtml .= "<tr>";
		for ($j = 0; $j < $result->numColumns(); $j++) {
		    if ($j == 0) { # match date
			$dateMod = substr($res[$j], 0, 4)."-".substr($res[$j], 4, 2)."-".substr($res[$j], 6, 2);
			$tableHtml .= "<td>".$dateMod."</td>";
		    } elseif ($j == 1) {
			$tableHtml .= "<td><a href=\"scorecard.php?matchFormat=".$matchFormat."&matchId=".$res[$j]."\">".$res[$j]."</a></td>";		    
		    } elseif ($j == 7) { # match rating or live rating
			$tableHtml .= "<td><b>".round($res[$j], 0)."</b></td>";
		    } elseif ($j == 8) { # team and opposition
			if ($matchFormat == "FT20") {
			    if (strrpos($country2, $res[$j]) === false) {
				$tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\">".$res[$j]."</a></td>";                            
			    } else {
				$tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";
			    }	       
			} else {
			    if ($country2 == $res[$j]) {
				$tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td>";
			    } else {
				$tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" border=1px/></a></td>";
			    }	       
			}                    
			$j++;
		    } else {
			$tableHtml .= "<td>$res[$j]</td>";
		    }
		}
		$tableHtml .= "</tr>";
	    } 	    
	    $tableHtml .= "</table>";
	    $tableHtml .= "</li>";
	    echo $tableHtml;
	    echo "</div>";	    
	    echo "</div>";
	    echo "</div>";
	}	
    } else if ($disc == "Win Shares") {
 	# winShares career
 	$sql1 = "select startDate, endDate, ".$matchFormatLower."s, battingAdjWSAvg, bowlingAdjWSAvg, fieldingAdjWSAvg, totalAdjWSAvg, totalRating from winShares".$matchFormat."Career where playerId=".$playerId1;
	$sql2 = "select startDate, endDate, ".$matchFormatLower."s, battingAdjWSAvg, bowlingAdjWSAvg, fieldingAdjWSAvg, totalAdjWSAvg, totalRating from winShares".$matchFormat."Career where playerId=".$playerId2;
	$result = $db->query($sql1);
	if (!$result) die("Cannot execute query.");
	$res1 = $result->fetchArray(SQLITE3_NUM);
	$result = $db->query($sql2);
	if (!$result) die("Cannot execute query.");
	$res2 = $result->fetchArray(SQLITE3_NUM);
	$keeper1 = $res1[3];
	$keeper2 = $res2[3];
	$tableHtml = "";    
	if (!empty($res1) && $res1[0] != "" && !empty($res2) && $res2[0] != "") {
	    echo "<li class=\"list-group-item\">";
	    echo "<h4>Career Summary</h4>";
	    echo "<table class=\"table table-hover table-condensed\" id=\"playerTable\">";
	    echo "<thead><tr>";	    
	    echo "<th>Player</th>";
	    echo "<th>Span</th>";
	    echo "<th>Mat</th>";
	    echo "<th>BatAvg</th>";
	    echo "<th>BowlAvg</th>";
	    echo "<th>FieldAvg</th>";	
	    echo "<th>TotalAvg</th>";		    
	    echo "<th>Career Rating</th>";     
	    echo "</tr></thead>";
	    $numInns1 = $res1[2];
	    echo "<tr>";
	    echo "<td><a href=\"player.php?playerId=$playerId1&matchFormat=$matchFormat&disc=$disc\">$player1</a></th>";
	    echo "<td>".substr($res1[0], 0, 4)."-".substr($res1[1], 0, 4)."</td>"; # span
	    echo "<td>$res1[2]</td>";	
	    echo "<td>".number_format(round($res1[3], 3), 3)."</td>";
	    echo "<td>".number_format(round($res1[4], 3), 3)."</td>";
	    echo "<td>".number_format(round($res1[5], 3), 3)."</td>";
	    echo "<td>".number_format(round($res1[6], 3), 3)."</td>";	
	    echo "<td><b>".round($res1[7], 3)."</b></td>";
	    echo "</tr>";
	    $numInns2 = $res2[2];
	    echo "<tr>";
	    echo "<td><a href=\"player.php?playerId=$playerId1&matchFormat=$matchFormat&disc=$disc\">$player2</a></th>";	    
	    echo "<td>".substr($res2[0], 0, 4)."-".substr($res2[1], 0, 4)."</td>"; # span
	    echo "<td>$res2[2]</td>";	
	    echo "<td>".number_format(round($res2[3], 3), 3)."</td>";
	    echo "<td>".number_format(round($res2[4], 3), 3)."</td>";
	    echo "<td>".number_format(round($res2[5], 3), 3)."</td>";
	    echo "<td>".number_format(round($res2[6], 3), 3)."</td>";	
	    echo "<td><b>".round($res2[7], 3)."</b></td>";
	    echo "</tr>";
	    echo "</table>";
	    		
	    # current winShares ratings
	    $sql1 = "select totalRating from winShares".$matchFormat."Live where playerId=".$playerId1;   
	    $result1 = $db->query($sql1);
	    if (!$result1) die("Cannot execute query.");
	    $sql2 = "select totalRating from winShares".$matchFormat."Live where playerId=".$playerId2;   
	    $result2 = $db->query($sql2);	
	    if (!$result2) die("Cannot execute query.");
	    echo "</li>";
	    echo "<li class=\"list-group-item\">";
	    if ($numInns1 > 20 & $numInns2 > 20) {
		echo "<h4>Current Rating Timeline</h4>";
		echo "By ";
		$inningsDates = array("Inning", "Date");
		echo "<form class=\"form-inline\" role=\"form\" name=\"chartForm\" method=\"get\" action=\"compare.php\">";
		echo "<div class=\"form-group\">";
		echo "<select class=\"form-control\" name=\"inningsDate\" onChange=\"chartForms()\">";
		$innDt = "";
		if(isset($_GET['inningsDate'])) {    
		    $innDt = $_GET['inningsDate'];		    
		    foreach ($inningsDates as $id) {
			if ($id == "Inning") {
			    $idMod ="Match";
			} else {
			    $idMod = "Date";
			}
			if ($innDt == $id) {
			    echo "<option selected=\"selected\" value=\"$id\">$idMod</option>";
			} else {
			    echo "<option value=\"$id\">$idMod</option>";
			}
		    }    
		} else {
		    $count = 0;
		    foreach ($inningsDates as $id) {
			if ($id == "Inning") {
			    $idMod ="Match";
			} else {
			    $idMod = "Date";
			}
			if ($count == 0) {
			    echo "<option selected=\"selected\" value=\"$id\">$idMod</option>";
			    $innDt = $id;
			} else {
			    echo "<option value=\"$id\">$idMod</option>";
			}
			$count = $count + 1;
		    }    
		}
		echo "</select>";
		echo "</div>";
		echo "<input type=\"hidden\" name=\"playerId1\" value=\"$playerId1\">";
		echo "<input type=\"hidden\" name=\"playerId2\" value=\"$playerId2\">";
		echo "<input type=\"hidden\" name=\"player2Search\" value=\"$player2Search\">";
		echo "<input type=\"hidden\" name=\"matchFormat\" value=\"$matchFormat\">";
		echo "<input type=\"hidden\" name=\"disc\" value=\"$disc\">";    
		echo "</form>";
		echo "<div class=\"chart\">";
		echo "<div id=\"chart\"></div>";
		echo "</div>";
		echo "<div class=\"text-center\">$player1 <img src=\"images/player1.png\"/>&nbsp;&nbsp;$player2 <img src=\"images/player2.png\"/></div>";
	    } else {
		$chartWidth = 0.55*$_SESSION['screen_width'];
		echo "<div class=\"chart\" style=\"width:".$chartWidth."px;\">";
		echo "</div>";   
	    }
	    
	    echo "</div>";
	    echo "</li>";
	    echo "<div class=\"col-lg-6\">";
	    
	    # top fielding matches
	    $tableHtml .= "<li class=\"list-group-item\">";
	    $tableHtml .= "<h4>Top Performances: $player1</h4>";	    
	    $sql1 = "select t.startDate, b.".$matchFormatLower."Id, b.battingAdjWS, b.bowlingAdjWS, b.fieldingAdjWS, b.totalAdjWS, t.team1, t.team2, t.ground from winShares".$matchFormat."Match b, winShares".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId1." order by b.totalAdjWS desc";            
	    $result = $db->query($sql1);
	    if (!$result) die("Cannot execute query.");
	    $tableHtml .= "<table class=\"table table-hover table-condensed\" id=\"inningsTable1\">";
	    $tableHtml .= "<thead><tr>";
	    $tableHtml .= "<th>Match Date</th>";
	    $tableHtml .= "<th>".$matchFormat." #</th>";
	    $tableHtml .= "<th>Bat</th>";
	    $tableHtml .= "<th>Bowl</th>";
	    $tableHtml .= "<th>Field</th>";	    
	    $tableHtml .= "<th>Rating</th>";
	    $tableHtml .= "<th>Opposition</th>";
	    $tableHtml .= "<th>Ground</th>";
	    $tableHtml .= "</tr></thead>";
	    while($res = $result->fetchArray(SQLITE3_NUM)) {
		$tableHtml .= "<tr>";
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
			$j = $j + 3;
		    } elseif ($j == 6) { # team and opposition
			if ($matchFormat == "FT20") {
			    if (strrpos($country1, $res[$j]) === false) {
				$tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\">".$res[$j]."</a></td>";                            
			    } else {
				$tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";
			    }	       
			} else {
			    if ($country1 == $res[$j]) {
				$tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td>";
			    } else {
				$tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" border=1px/></a></td>";
			    }	       
			}                    
			$j++;
		    } else {
			$tableHtml .= "<td>$res[$j]</td>";
		    }   			
		} 
		$tableHtml .= "</tr>";
	    } 
	    $tableHtml .= "</table><br/>";	    	
	    $tableHtml .= "</li>";
	    
	    $tableHtml .= "<li class=\"list-group-item\">";
	    $tableHtml .= "<h4>Top Performances: $player2</h4>";
	    $sql2 = "select t.startDate, b.".$matchFormatLower."Id, b.battingAdjWS, b.bowlingAdjWS, b.fieldingAdjWS, b.totalAdjWS, t.team1, t.team2, t.ground from winShares".$matchFormat."Match b, winShares".$matchFormat."Live l, ".$matchFormatLower."Info t, playerInfo p where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.playerId=p.playerId and b.matchId=l.matchId and p.playerId=".$playerId2." order by b.totalAdjWS desc";            
	    $result = $db->query($sql2);
	    if (!$result) die("Cannot execute query.");
	    $tableHtml .= "<table class=\"table table-hover table-condensed\" id=\"inningsTable2\">";
	    $tableHtml .= "<thead><tr>";
	    $tableHtml .= "<th>Match Date</th>";
	    $tableHtml .= "<th>".$matchFormat." #</th>";
	    $tableHtml .= "<th>Bat</th>";
	    $tableHtml .= "<th>Bowl</th>";
	    $tableHtml .= "<th>Field</th>";
	    $tableHtml .= "<th>Rating</th>";
	    $tableHtml .= "<th>Opposition</th>";
	    $tableHtml .= "<th>Ground</th>";
	    $tableHtml .= "</tr></thead>";
	    while($res = $result->fetchArray(SQLITE3_NUM)) {
		$tableHtml .= "<tr>";
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
			$j = $j + 3;
		    } elseif ($j == 6) { # team and opposition
			if ($matchFormat == "FT20") {
			    if (strrpos($country2, $res[$j]) === false) {
				$tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\">".$res[$j]."</a></td>";                            
			    } else {
				$tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";
			    }	       
			} else {
			    if ($country2 == $res[$j]) {
				$tableHtml .= "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td>";
			    } else {
				$tableHtml .= "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" border=1px/></a></td>";
			    }	       
			}                    
			$j++;
		    } else {
			$tableHtml .= "<td>$res[$j]</td>";
		    }   			
		} 
		$tableHtml .= "</tr>";
	    } 	    
	    $tableHtml .= "</table>";
	    $tableHtml .= "</li>";
	    echo $tableHtml;
	    echo "</div>";	    
	    echo "</div>";
	    echo "</div>";
	}	
    }
    $db->close();
    echo "</ul>";
    if ($playerFound == 0) {
	echo "<h2>Players not found.</h2>";
    }
}
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