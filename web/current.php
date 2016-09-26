<!DOCTYPE html>
<?php
session_start();
$playerId1 = 0;
$playerId2 = 0;
$playerId3 = 0;
$playerId4 = 0;
$playerId5 = 0;
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
if(isset($_GET['currentSelect'])) {
   $currSelect = $_GET['currentSelect'];
} else {
   $currSelect = 0;
}

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

if ($disc == "Team") {
   $sql = "select team from ".$disciplineLower.$matchFormat."Current order by rating desc limit 5";
} else {
   $retiredPlayers = "";
   if ($matchFormat == "Test" || $matchFormat == "ODI") {
      $sql = "select playerId from retiredPlayers";
      $result = $db->query($sql);
      if (!$result) die("Cannot execute query.");
      while($res = $result->fetchArray(SQLITE3_NUM)) {
	 $retiredPlayers = $retiredPlayers . $res[0] . ",";
      }
      $retiredPlayers = rtrim($retiredPlayers, ",");
   }
   $sql = "select playerId from ".$disciplineLower.$matchFormat."Current where playerId not in ($retiredPlayers) order by rating desc limit 5";
}

$result = $db->query($sql);
if (!$result) die("Cannot execute query.");
$k = 0;
while($res = $result->fetchArray(SQLITE3_NUM)) {
   if ($k == 0) {
       $playerId1 = $res[0];
   } else if ($k == 1) {
       $playerId2 = $res[0];
   } else if ($k == 2) {
       $playerId3 = $res[0];
   } else if ($k == 3) {
       $playerId4 = $res[0];
   } else if ($k == 4) {
       $playerId5 = $res[0];
   }
   $k = $k + 1;
}

if(isset($_SESSION['screen_width']) AND isset($_SESSION['screen_height'])){
} else if(isset($_REQUEST['width']) AND isset($_REQUEST['height'])) {
    $_SESSION['screen_width'] = $_REQUEST['width'];
    $_SESSION['screen_height'] = $_REQUEST['height'];

    header("Location: current.php?playerId1=".$playerId1."&playerId2=".$playerId2."&playerId3=".$playerId3."&playerId4=".$playerId4."&playerId5=".$playerId5."&matchFormat=".$matchFormat."&disc=".$disc."&currentSelect=".$currSelect);
} else {
    echo '<script type="text/javascript">window.location = "' . $_SERVER['PHP_SELF'] . '?playerId1='.$playerId1.'&playerId2='.$playerId2.'&playerId3='.$playerId3.'&playerId4='.$playerId4.'&playerId5='.$playerId5.'&matchFormat='.$matchFormat.'&disc='.$disc."&currentSelect=".$currSelect.'&width="+screen.width+"&height="+screen.height;</script>';
}

$player1 = "";
$player2 = "";
$player3 = "";
$player4 = "";
$player5 = "";
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

if ($playerId1 != "" && $playerId2 != "" && $playerId3 != "" && $playerId4 != "" && $playerId5 != "") {
   if ($disc == "Team") {
      $player1 = $playerId1;
      $player2 = $playerId2;
      $player3 = $playerId3;
      $player4 = $playerId4;
      $player5 = $playerId5;
   } else {
      $player1 = getPlayerName($db, $playerId1, $player1);
      $player2 = getPlayerName($db, $playerId2, $player2);
      $player3 = getPlayerName($db, $playerId3, $player3);
      $player4 = getPlayerName($db, $playerId4, $player4);
      $player5 = getPlayerName($db, $playerId5, $player5);
   }
}
$db->close();

?>
<html>
<head>
   <title>cricrate | Current Ratings - <?php echo($matchFormat." ".$disc); ?></title>
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
    var chartHeight = screen.height * 0.4;
    if (isMobile == true) {
	chartWidth = chartWidth * 2;
    }

   var player1 = <?php echo json_encode($playerId1) ?>;
   var player2 = <?php echo json_encode($playerId2) ?>;
   var player3 = <?php echo json_encode($playerId3) ?>;
   var player4 = <?php echo json_encode($playerId4) ?>;
   var player5 = <?php echo json_encode($playerId5) ?>;

   var matchFormat = <?php echo json_encode($matchFormat); ?>;
   var disc = <?php echo json_encode($disc); ?>;
   var batBowl = disc.toLowerCase();
   if (batBowl == "all-round") {
      batBowl = "allRound";
   } else if (batBowl == "win shares") {
      batBowl = "winShares";
   }

   if (batBowl != "fielding" && batBowl != "winShares") {
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);
   }

   function drawChart() {
      var jsonData = $.ajax({
	  url: "charts/current.php?playerId1="+player1+"&playerId2="+player2+"&playerId3="+player3+"&playerId4="+player4+"&playerId5="+player5+"&matchFormat="+matchFormat+"&batBowl="+batBowl,
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
	  colors:['#2c518d','#ff3232','#87ce00','#ffd700','#f07b2b'],
	  width: chartWidth,
	    height: chartHeight,
	  vAxis: {
		  title: "Current Rating",
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

      var chart = new google.visualization.LineChart(document.getElementById('chart'));
      chart.draw(data, options);
   }

   $(document).ready(function() {
       $('#ratingsTable').DataTable( {
       "lengthChange":   false,
       "pageLength": 15,
       "order": [[ 1, "asc" ]],
   } );

      $('#ratingsTable2').DataTable( {
       "lengthChange":   false,
       "pageLength": 15,
       "order": [[ 1, "asc" ]],
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
                            <?php if ($disc == "Team" && $matchFormat == "Test") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=Test&disc=Team\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=Test&disc=Team\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=Test&disc=Team">&nbsp;&nbsp;Overall</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=ODI&disc=Team"><b>ODI</b></a></li>
                            <?php if ($disc == "Team" && $matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=ODI&disc=Team\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=ODI&disc=Team\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=ODI&disc=Team">&nbsp;&nbsp;Overall</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=T20I&disc=Team"><b>T20I</b></a></li>
                            <?php if ($disc == "Team" && $matchFormat == "T20I") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=T20I&disc=Team\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=T20I&disc=Team\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=T20I&disc=Team">&nbsp;&nbsp;Overall</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=Team"><b>FT20</b></a></li>
                            <?php if ($disc == "Team" && $matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=FT20&disc=Team\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=FT20&disc=Team\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=FT20&disc=Team">&nbsp;&nbsp;Overall</a></li>
                        </ul>
                    </li>
                    <?php if ($disc == "Batting") { echo "<li class=\"active\">"; } else { echo "<li class=\"dropdown\">"; } ?>
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Batting <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="methodology.php?matchFormat=Test&disc=Batting"><b>Test</b></a></li>
			    <?php if ($disc == "Batting" && $matchFormat == "Test") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=Test&disc=Batting\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=Test&disc=Batting\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=Test&disc=Batting">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=Test&disc=Batting">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=ODI&disc=Batting"><b>ODI</b></a></li>
			    <?php if ($disc == "Batting" && $matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=ODI&disc=Batting\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=ODI&disc=Batting\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=ODI&disc=Batting">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=ODI&disc=Batting">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=T20I&disc=Batting"><b>T20I</b></a></li>
                            <?php if ($disc == "Batting" && $matchFormat == "T20I") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=T20I&disc=Batting\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=T20I&disc=Batting\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=T20I&disc=Batting">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=T20I&disc=Batting">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=Batting"><b>FT20</b></a></li>
                            <?php if ($disc == "Batting" && $matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=FT20&disc=Batting\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=FT20&disc=Batting\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=FT20&disc=Batting">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=FT20&disc=Batting">&nbsp;&nbsp;Performances</a></li>
                        </ul>
                    </li>
                    <?php if ($disc == "Bowling") { echo "<li class=\"active\">"; } else { echo "<li class=\"dropdown\">"; } ?>
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Bowling <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="methodology.php?matchFormat=Test&disc=Bowling"><b>Test</b></a></li>
                            <?php if ($disc == "Bowling" && $matchFormat == "Test") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=Test&disc=Bowling\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=Test&disc=Bowling\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=Test&disc=Bowling">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=Test&disc=Bowling">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=ODI&disc=Bowling"><b>ODI</b></a></li>
                            <?php if ($disc == "Bowling" && $matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=ODI&disc=Bowling\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=ODI&disc=Bowling\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=ODI&disc=Bowling">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=ODI&disc=Bowling">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=T20I&disc=Bowling"><b>T20I</b></a></li>
                            <?php if ($disc == "Bowling" && $matchFormat == "T20I") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=T20I&disc=Bowling\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=T20I&disc=Bowling\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=T20I&disc=Bowling">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=T20I&disc=Bowling">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=Bowling"><b>FT20</b></a></li>
                            <?php if ($disc == "Bowling" && $matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=FT20&disc=Bowling\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=FT20&disc=Bowling\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=FT20&disc=Bowling">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=FT20&disc=Bowling">&nbsp;&nbsp;Performances</a></li>
                        </ul>
                    </li>
                    <?php if ($disc == "All-Round") { echo "<li class=\"active\">"; } else { echo "<li class=\"dropdown\">"; } ?>
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">All-Round <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="methodology.php?matchFormat=Test&disc=All-Round"><b>Test</b></a></li>
                            <?php if ($disc == "All-Round" && $matchFormat == "Test") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=Test&disc=All-Round\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=Test&disc=All-Round\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=Test&disc=All-Round">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=Test&disc=All-Round">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=ODI&disc=All-Round"><b>ODI</b></a></li>
                            <?php if ($disc == "All-Round" && $matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=ODI&disc=All-Round\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=ODI&disc=All-Round\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=ODI&disc=All-Round">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=ODI&disc=All-Round">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=T20I&disc=All-Round"><b>T20I</b></a></li>
                            <?php if ($disc == "All-Round" && $matchFormat == "T20I") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=T20I&disc=All-Round\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=T20I&disc=All-Round\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=T20I&disc=All-Round">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=T20I&disc=All-Round">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=All-Round"><b>FT20</b></a></li>
                            <?php if ($disc == "All-Round" && $matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=FT20&disc=All-Round\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=FT20&disc=All-Round\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=FT20&disc=All-Round">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=FT20&disc=All-Round">&nbsp;&nbsp;Performances</a></li>
                        </ul>
                    </li>
                    <?php if ($disc == "Fielding") { echo "<li class=\"active\">"; } else { echo "<li class=\"dropdown\">"; } ?>
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Fielding <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="methodology.php?matchFormat=Test&disc=Fielding"><b>Test</b></a></li>
                            <?php if ($disc == "Fielding" && $matchFormat == "Test") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=Test&disc=Fielding\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=Test&disc=Fielding\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=Test&disc=Fielding">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=Test&disc=Fielding">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=ODI&disc=Fielding"><b>ODI</b></a></li>
                            <?php if ($disc == "Fielding" && $matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=ODI&disc=Fielding\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=ODI&disc=Fielding\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=ODI&disc=Fielding">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=ODI&disc=Fielding">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=Fielding"><b>FT20</b></a></li>
                            <?php if ($disc == "Fielding" && $matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=FT20&disc=Fielding\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=FT20&disc=Fielding\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=FT20&disc=Fielding">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=FT20&disc=Fielding">&nbsp;&nbsp;Performances</a></li>
                        </ul>
                    </li>
                    <?php if ($disc == "Win Shares") { echo "<li class=\"active\">"; } else { echo "<li class=\"dropdown\">"; } ?>
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Win Shares <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="methodology.php?matchFormat=ODI&disc=Win Shares"><b>ODI</b></a></li>
                            <?php if ($disc == "Win Shares" && $matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=ODI&disc=Win Shares\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=ODI&disc=Win Shares\">&nbsp;&nbsp;Current</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=ODI&disc=Win Shares">&nbsp;&nbsp;Career</a></li>
                            <li><a href="performances.php?matchFormat=ODI&disc=Win Shares">&nbsp;&nbsp;Performances</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=Win Shares"><b>FT20</b></a></li>
                            <?php if ($disc == "Win Shares" && $matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"current.php?matchFormat=FT20&disc=Win Shares\">&nbsp;&nbsp;Current<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"current.php?matchFormat=FT20&disc=Win Shares\">&nbsp;&nbsp;Current</a></li>"; } ?>
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
   echo "<div class=\"row\">";
   echo "<div class=\"col-lg-6\">";
   echo "<h2><b>Current Ratings&nbsp;&nbsp;<small>&nbsp;&nbsp;<a href=\"methodology.php?matchFormat=$matchFormat&disc=$disc\">Methodology</a></small></b></h2>";
   $matchFormat = "Test";
   $disc = "Batting";
   $currSelect = 0;
   echo "<form class=\"form-inline\" role=\"form\" name=\"selectForm\" method=\"get\" action=\"current.php\">";
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

   echo "<div class=\"form-group\">";
   echo "<select class=\"form-control\" name=\"currentSelect\" onChange=\"submitForms()\">";
   if(isset($_GET['currentSelect'])) {
       $currSelect = $_GET['currentSelect'];
       if ($currSelect == 1) {
	   echo "<option value=\"0\">Current</option>";
	   echo "<option selected=\"selected\" value=\"1\">All-time</option>";
       } else {
	   echo "<option selected=\"selected\" value=\"0\">Current</option>";
	   echo "<option value=\"1\">All-time</option>";
       }
   } else {
      $currSelect = 0;
       echo "<option selected=\"selected\" value=\"0\">Current</option>";
       echo "<option value=\"1\">All-time</option>";
   }
   echo "</select>";
   echo "</div>";
   echo "</form>";

   $dbName = "ccr.db";
   if ($matchFormat == "ODI") {
     $dbName = "ccrODI.db";
   } elseif ($matchFormat == "T20I") {
     $dbName = "ccrT20I.db";
   } elseif ($matchFormat == "FT20") {
     $dbName = "ccrFT20.db";
   }

   $db = new SQLite3($dbName);

   $sql = "select max(startDate) as maxDate from ".$disciplineLower.$matchFormat."Current";
   $result = $db->query($sql);
   if (!$result) die("Cannot execute query.");
   $maxDate = $result->fetchArray(SQLITE3_NUM);
   $maxDateMod = substr($maxDate[0], 0, 4)."-".substr($maxDate[0], 4, 2)."-".substr($maxDate[0], 6, 2);
   echo "&nbsp;&nbsp;Last update: $maxDateMod";

   $retiredPlayers = "";
   if (($matchFormat == "Test" || $matchFormat == "ODI" || $matchFormat == "T20I") && $disc != "Team") {
      $sql = "select playerId from retiredPlayers";
      $result = $db->query($sql);
      if (!$result) die("Cannot execute query.");
      while($res = $result->fetchArray(SQLITE3_NUM)) {
	 $retiredPlayers = $retiredPlayers . $res[0] . ",";
      }
      $retiredPlayers = rtrim($retiredPlayers, ",");
   }

   if ($disc == "Team") {
      if ($currSelect == 0) {
	 $sql = "select team, rankDiff, rank, rating, team, bestCurrentRating from ".$disciplineLower.$matchFormat."Current order by rating desc";
      } else {
	 $sql = "select team, max(rating) as maxRating from ".$disciplineLower.$matchFormat."Live group by team order by maxRating desc";
      }
   } else {
      if ($currSelect == 0) {
	 if ($matchFormat == "FT20") {
	    $sql = "select playerId, rankDiff, rank, rating, player, bestCurrentRating from ".$disciplineLower.$matchFormat."Current where playerId not in ($retiredPlayers) order by rating desc";
	 } else {
	    $sql = "select playerId, rankDiff, rank, rating, player, country, bestCurrentRating from ".$disciplineLower.$matchFormat."Current where playerId not in ($retiredPlayers) order by rating desc";
	 }
      } else {
	 if ($matchFormat == "FT20") {
	    $sql = "select playerId, rank, rating, player, bestCurrentRating from ".$disciplineLower.$matchFormat."CurrentAllTime order by rating desc limit 500";
	 } else {
	    $sql = "select playerId, rank, rating, player, country, bestCurrentRating from ".$disciplineLower.$matchFormat."CurrentAllTime order by rating desc limit 500";
	 }
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
   echo "<th>+/-</th>";
   echo "<th>Rank</th>";
   echo "<th>Rating</th>";
   if ($disc == "Team") {
      echo "<th>Team</th>";
      if ($matchFormat != "FT20") {
	 echo "<th>Flag</th>";
      }
   } else {
      echo "<th>Player</th>";
      if ($matchFormat != "FT20") {
	 echo "<th>Country</th>";
      }
   }
   echo "<th>Best Current Rating</th>";
   echo "</tr></thead>";

   $k = 1;
   while($res = $result->fetchArray(SQLITE3_NUM)) {
      if ($disc == "Team" && $currSelect == 1) {
	 echo "<tr><td><b>-</b></td>";
	 echo "<td>$k</td>";
	 echo "<td><b>".round($res[1], 0)."</b></td>";
	 echo "<td><a href=\"team.php?team=".$res[0]."&matchFormat=$matchFormat\">".$res[0]."</a></td>";
	 if ($matchFormat != "FT20") {
	    echo "<td><a href=\"team.php?team=".$res[0]."&matchFormat=$matchFormat\"><img src=\"images/".$res[0].".png\" alt=\"$res[0]\" style='border:1px solid #A9A9A9'/></a></td>";
	 }
	 echo "<td><b>".round($res[1], 0)."</b></td>";
      } else {
	 $startIndex = 3;
	 if ($currSelect == 0) {
	     $rankDiff = $res[1];
	     if ($rankDiff > 0) {
		 echo "<tr><td><font color=\"green\"><b>+".$rankDiff."</b></font></td>";
	     } elseif ($rankDiff == 0) {
		 echo "<tr><td><b>-</b></td>";
	     } else {
		 echo "<tr><td><font color=\"red\"><b>$rankDiff</b></font></td>";
	     }
	 } else {
	     echo "<tr><td><b>-</b></td>";
	     $startIndex = 2;
	 }

	 echo "<td>$k</td>";
	 for ($j = $startIndex; $j < $result->numColumns(); $j++) {
	   if ($j == $startIndex) { # rating
	       if ($disc == "Win Shares") {
		  echo "<td><b>".round($res[$j], 3)."</b></td>";
	       } else {
		  echo "<td><b>".round($res[$j], 0)."</b></td>";
	       }
	   } elseif ($j == $startIndex+1) {
	      if ($disc == "Team") {
		 echo "<td><a href=\"team.php?team=".$res[0]."&matchFormat=$matchFormat\">".$res[$j]."</a></td>";
		 if ($matchFormat != "FT20") {
		     echo "<td><a href=\"team.php?team=".$res[0]."&matchFormat=$matchFormat\"><img src=\"images/".$res[0].".png\" alt=\"$res[0]\" style='border:1px solid #A9A9A9'/></a></td>";
		 }
	      } else {
		 echo "<td><a href=\"player.php?playerId=".$res[0]."&matchFormat=$matchFormat&disc=$disc\">".str_replace("Sir ","",$res[$j])."</a></td>";
	      }
	   } elseif ($j == $startIndex+2 && $matchFormat != "FT20") { # country
	      if ($disc == "Team") {
		 echo "<td>$res[$j]</td>";
	      } else {
		 echo "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" alt=\"$res[$j]\" style='border:1px solid #A9A9A9'/></a></td>";
	      }
	   } else {
	      echo "<td>$res[$j]</td>";
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
   echo "<div class=\"col-lg-6\">";
   if ($disc == "Fielding" || $disc == "Win Shares" || ($disc == "Team" && $matchFormat == "Test")) {
      echo "<br/><br/><br/><br/><br/>";
   } else {
      echo "<br/><br/><br/><br/><br/><br/>";
   }
   echo "<ul class=\"list-group\">";
   echo "<li class=\"list-group-item\">";
   if ($disc == "Fielding" || $disc == "Win Shares") {
      echo "<h3>Worst</h3>";
      if ($currSelect == 0) {
	 if ($matchFormat == "FT20") {
	    $sql = "select playerId, rankDiff, rank, rating, player, bestCurrentRating from ".$disciplineLower.$matchFormat."Current where playerId not in ($retiredPlayers) order by rating asc";
	 } else {
	    $sql = "select playerId, rankDiff, rank, rating, player, country, bestCurrentRating from ".$disciplineLower.$matchFormat."Current where playerId not in ($retiredPlayers) order by rating asc";
	 }
      } else {
	 if ($matchFormat == "FT20") {
	    $sql = "select playerId, rank, rating, player, bestCurrentRating from ".$disciplineLower.$matchFormat."CurrentAllTime order by rating asc limit 500";
	 } else {
	    $sql = "select playerId, rank, rating, player, country, bestCurrentRating from ".$disciplineLower.$matchFormat."CurrentAllTime order by rating asc limit 500";
	 }
      }

      $result = $db->query($sql);
      if (!$result) die("Cannot execute query.");

      echo "<table class=\"table table-hover table-condensed\" id=\"ratingsTable2\">";
      echo "<thead><tr>";
      echo "<th>+/-</th>";
      echo "<th>Rank</th>";
      echo "<th>Rating</th>";
      echo "<th>Player</th>";
      if ($matchFormat != "FT20") {
	 echo "<th>Country</th>";
      }
      echo "<th>Best Current Rating</th>";
      echo "</tr></thead>";

      $k = 1;
      while($res = $result->fetchArray(SQLITE3_NUM)) {
	 $startIndex = 3;
	 if ($currSelect == 0) {
	     $rankDiff = $res[1];
	     if ($rankDiff > 0) {
		 echo "<tr><td><font color=\"green\"><b>+".$rankDiff."</b></font></td>";
	     } elseif ($rankDiff == 0) {
		 echo "<tr><td><b>-</b></td>";
	     } else {
		 echo "<tr><td><font color=\"red\"><b>$rankDiff</b></font></td>";
	     }
	 } else {
	     echo "<tr><td><b>-</b></td>";
	     $startIndex = 2;
	 }

	 echo "<td>$k</td>";
	 for ($j = $startIndex; $j < $result->numColumns(); $j++) {
	   if ($j == $startIndex) { # rating
	       if ($disc == "Win Shares") {
		  echo "<td><b>".round($res[$j], 3)."</b></td>";
	       } else {
		  echo "<td><b>".round($res[$j], 0)."</b></td>";
	       }
	   } elseif ($j == $startIndex+1) {
	      if ($disc == "Team") {
		 echo "<td><a href=\"team.php?team=".$res[0]."&matchFormat=$matchFormat\">".$res[$j]."</a></td>";
		 echo "<td><a href=\"team.php?team=".$res[0]."&matchFormat=$matchFormat\"><img src=\"images/".$res[0].".png\" alt=\"$res[0]\" style='border:1px solid #A9A9A9'/></a></td>";
	      } else {
		 echo "<td><a href=\"player.php?playerId=".$res[0]."&matchFormat=$matchFormat&disc=$disc\">".str_replace("Sir ","",$res[$j])."</a></td>";
	      }
	   } elseif ($j == $startIndex+2 && $matchFormat != "FT20") { # country
	      if ($disc == "Team") {
		 echo "<td>$res[$j]</td>";
	      } else {
		 echo "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" alt=\"$res[$j]\" style='border:1px solid #A9A9A9'/></a></td>";
	      }
	   } else {
	      echo "<td>$res[$j]</td>";
	   }
	 }
	  echo "</tr>";
	  $k++;
      }
      echo "</table>";
   } else {
      echo "<h3>Timeline</h3>";
      echo "<div class=\"chart\">";
      echo "<div id=\"chart\"></div>";
      echo "</div>";
      echo "<div class=\"text-center\">$player1 <img src=\"images/player1.png\"/>&nbsp;&nbsp;$player2 <img src=\"images/player2.png\"/>&nbsp;&nbsp;$player3 <img src=\"images/player3.png\"/>&nbsp;&nbsp;$player4 <img src=\"images/player4.png\"/>&nbsp;&nbsp;$player5 <img src=\"images/player5.png\"/></div>";
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
