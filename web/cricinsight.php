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
if(isset($_GET['player'])) {    
   $player = $_GET['player'];
} else {
   $player = "";
}
if(isset($_GET['league'])) {    
   $league = $_GET['league'];
} else {
   $league = "";
}
$teamsLink = "";
if(isset($_GET['teams'])) {
    foreach($_GET['teams'] as $team) {
	$teamsLink .= "&teams%5B%5D=".$team;
    }
} else {
   $teams = "";
}
$oppositionsLink = "";
if(isset($_GET['oppositions'])) {
    foreach($_GET['oppositions'] as $opp) {
	$oppositionsLink .= "&oppositions%5B%5D=".$opp;
    }
} else {
   $oppositions = "";
}
if(isset($_GET['matchType'])) {    
   $matchType = $_GET['matchType'];
} else {
   $matchType = "";
}
if(isset($_GET['homeAway'])) {    
   $homeAway = $_GET['homeAway'];
} else {
   $homeAway = 2;
}
$hostsLink = "";
if(isset($_GET['hosts'])) {
    foreach($_GET['hosts'] as $host) {
	$hostsLink .= "&hosts%5B%5D=".$host;
    }
} else {
   $host = "";
}
$winLossLink = "";
if(isset($_GET['winLoss'])) {
    foreach($_GET['winLoss'] as $winLoss) {
	$winLossLink .= "&winLoss%5B%5D=".$winLoss;
    }
} else {
   $winLoss = "";
}
if(isset($_GET['batFieldFirst'])) {    
   $batFieldFirst = $_GET['batFieldFirst'];
} else {    
    $batFieldFirst = "Either";
}
if(isset($_GET['ground'])) {    
   $ground = $_GET['ground'];
} else {
   $ground = "";
}
$inningsLink = "";
if(isset($_GET['innings'])) {
    foreach($_GET['innings'] as $inn) {
	$inningsLink .= "&innings%5B%5D=".$inn;
    }
} else {
   $innings = "";
}
if(isset($_GET['groupBy'])) {    
   $groupBy = $_GET['groupBy'];
} else {
   $groupBy = "Player";
}
if(isset($_GET['startDate'])) {    
   $startDate = $_GET['startDate'];
} else {
   $startDate = "";
}
if(isset($_GET['endDate'])) {    
   $endDate = $_GET['endDate'];
} else {
   $endDate = "";
}
if(isset($_GET['resultQual'])) {    
   $resultQual = $_GET['resultQual'];
} else {
   $resultQual = "";
}
if(isset($_GET['resultQualFrom'])) {    
   $resultQualFrom = $_GET['resultQualFrom'];
} else {
   $resultQualFrom = "";
}
if(isset($_GET['resultQualTo'])) {    
   $resultQualTo = $_GET['resultQualTo'];
} else {
   $resultQualTo = "";
}
if(isset($_GET['sortBy'])) {    
   $sortBy = $_GET['sortBy'];
} else {
   $sortBy = "";
}
$submitLink = "";
if (isset($_GET["Submit"])) {
   $submitLink = "&Submit=submit";
} 

if ($disc == "Batting") {
    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	$xValMod = array("average"=>"Average", "runs"=>"Runs", "strikeRate"=>"Strike Rate", "rating"=>"Rating", "innings"=>"Innings");
	$yValMod = array("strikeRate"=>"Strike Rate", "average"=>"Average", "runs"=>"Runs", "rating"=>"Rating", "innings"=>"Innings");
	$histValMod = array("average"=>"Average", "runs"=>"Runs", "strikeRate"=>"Strike Rate", "rating"=>"Rating", "innings"=>"Innings");
    } else {
	$xValMod = array("runs"=>"Runs", "strikeRate"=>"Strike Rate", "balls"=>"Balls", "rating"=>"Rating");
	$yValMod = array("strikeRate"=>"Strike Rate", "runs"=>"Runs", "balls"=>"Balls", "rating"=>"Rating");
	$histValMod = array("runs"=>"Runs", "strikeRate"=>"Strike Rate", "balls"=>"Balls", "rating"=>"Rating");
    }    
} else if ($disc == "Bowling") {
    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	$xValMod = array("average"=>"Average", "runs"=>"Runs", "strikeRate"=>"Strike Rate", "balls"=>"Balls", "wickets"=>"Wickets", "econRate"=>"Econ Rate", "rating"=>"Rating", "innings"=>"Innings");
	$yValMod = array("strikeRate"=>"Strike Rate", "average"=>"Average", "runs"=>"Runs", "balls"=>"Balls", "wickets"=>"Wickets", "econRate"=>"Econ Rate", "rating"=>"Rating", "innings"=>"Innings");
	$histValMod = array("average"=>"Average", "runs"=>"Runs", "strikeRate"=>"Strike Rate", "balls"=>"Balls", "wickets"=>"Wickets", "econRate"=>"Econ Rate", "rating"=>"Rating", "innings"=>"Innings");
    } else {
	$xValMod = array("wickets"=>"Wickets", "runs"=>"Runs", "balls"=>"Balls", "rating"=>"Rating");
	$yValMod = array("runs"=>"Runs", "wickets"=>"Wickets", "balls"=>"Balls", "rating"=>"Rating");
	$histValMod = array("wickets"=>"Wickets", "runs"=>"Runs", "balls"=>"Balls", "rating"=>"Rating");
    }      
} else if ($disc == "All-Round") {
    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {	    
	$xValMod = array("battingAverage"=>"Batting Average", "bowlingAverage"=>"Bowling Average", "runs"=>"Runs", "wickets"=>"Wickets", "rating"=>"Rating", "matches"=>"Matches");
	$yValMod = array("bowlingAverage"=>"Bowling Average", "battingAverage"=>"Batting Average", "runs"=>"Runs", "wickets"=>"Wickets", "rating"=>"Rating", "matches"=>"Matches");
	$histValMod = array("battingAverage"=>"Batting Average", "bowlingAverage"=>"Bowling Average", "runs"=>"Runs", "wickets"=>"Wickets", "rating"=>"Rating", "matches"=>"Matches");
    } else {
	$xValMod = array("runs"=>"Runs", "wickets"=>"Wickets", "rating"=>"Rating");
	$yValMod = array("wickets"=>"Wickets", "runs"=>"Runs", "rating"=>"Rating");
	$histValMod = array("rating"=>"Rating", "runs"=>"Runs", "wickets"=>"Wickets");
    }        
} else if ($disc == "Fielding") {
    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {	    
	$xValMod = array("catches"=>"Catches", "droppedCatches"=>"Dropped Catches", "dropRate"=>"Drop Rate", "greatCatches"=>"Great Catches", "directHits"=>"Direct Hits", "runsSaved"=>"Runs Saved", "rating"=>"Rating", "innings"=>"Innings");
	$yValMod = array("droppedCatches"=>"Dropped Catches", "catches"=>"catches", "dropRate"=>"Drop Rate", "greatCatches"=>"Great Catches", "directHits"=>"Direct Hits", "runsSaved"=>"Runs Saved", "rating"=>"Rating", "innings"=>"Innings");
	$histValMod = array("dropRate"=>"Drop Rate", "catches"=>"catches", "droppedCatches"=>"Dropped Catches", "greatCatches"=>"Great Catches", "directHits"=>"Direct Hits", "runsSaved"=>"Runs Saved", "rating"=>"Rating", "innings"=>"Innings");
    } else {
	$xValMod = array("catches"=>"Catches", "droppedCatches"=>"Dropped Catches", "greatCatches"=>"Great Catches", "directHits"=>"Direct Hits", "runsSaved"=>"Runs Saved", "rating"=>"Rating");
	$yValMod = array("droppedCatches"=>"Dropped Catches", "catches"=>"catches", "greatCatches"=>"Great Catches", "directHits"=>"Direct Hits", "runsSaved"=>"Runs Saved", "rating"=>"Rating");
	$histValMod = array("catches"=>"Catches", "droppedCatches"=>"Dropped Catches", "greatCatches"=>"Great Catches", "directHits"=>"Direct Hits", "runsSaved"=>"Runs Saved", "rating"=>"Rating");
    }	
} else if ($disc == "Win Shares") {
    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	$xValMod = array("battingWSAvg"=>"Batting WSAvg", "bowlingWSAvg"=>"Bowling WSAvg", "totalWSAvg"=>"Total WSAvg", "fieldingWSAvg"=>"Fielding WSAvg", "innings"=>"Innings");
	$yValMod = array("bowlingWSAvg"=>"Bowling WSAvg", "battingWSAvg"=>"Batting WSAvg", "totalWSAvg"=>"Total WSAvg", "fieldingWSAvg"=>"Fielding WSAvg", "innings"=>"Innings");
	$histValMod = array("totalWSAvg"=>"Total WSAvg", "battingWSAvg"=>"Batting WSAvg", "bowlingWSAvg"=>"Bowling WSAvg", "fieldingWSAvg"=>"Fielding WSAvg", "innings"=>"Innings");
    } else {
	$xValMod = array("battingWS"=>"Batting WS", "bowlingWS"=>"Bowling WS", "totalWS"=>"Total WS", "fieldingWS"=>"Fielding WS");
	$yValMod = array("bowlingWS"=>"Bowling WS", "battingWS"=>"Batting WS", "totalWS"=>"Total WS", "fieldingWS"=>"Fielding WS");
	$histValMod = array("totalWS"=>"Total WS", "battingWS"=>"Batting WS", "bowlingWS"=>"Bowling WS", "fieldingWS"=>"Fielding WS");
    }	
}

$xKeys = array_keys($xValMod);
$yKeys = array_keys($yValMod);
$histKeys = array_keys($histValMod);
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

if(isset($_GET['histVal'])) {
    if (in_array($_GET['histVal'], $histKeys)) {
	$histVal = $_GET['histVal'];
    } else {
	$histVal = $histKeys[0];
    }
} else {
    $histVal = $histKeys[0];
}

$xAxis = $xValMod[$xVal];
$yAxis = $yValMod[$yVal];
$histAxis = $histValMod[$histVal];

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
    
    header("Location: cricinsight.php?matchFormat=".$matchFormat."&disc=".$disc."&xVal=".$xVal."&yVal=".$yVal."&histVal=".$histVal.$submitLink.$teamsLink.$oppositionsLink.$hostsLink."&homeAway=".$homeAway."&batFieldFirst=".$batFieldFirst."&matchType=".$matchType.$winLossLink."&player=".$player."&league=".$league."&ground=".$ground.$inningsLink."&groupBy=".$groupBy."&startDate=".$startDate."&endDate=".$endDate."&resultQual=".$resultQual."&resultQualFrom=".$resultQualFrom."&resultQualTo=".$resultQualTo."&sortBy=".$sortBy);
} else {
    echo '<script type="text/javascript">window.location = "' . $_SERVER['PHP_SELF'] . '?matchFormat='.$matchFormat.'&disc='.$disc.'&xVal='.$xVal.'&yVal='.$yVal.'&histVal='.$histVal.$submitLink.$teamsLink.$oppositionsLink.$hostsLink.'&homeAway='.$homeAway."&batFieldFirst=".$batFieldFirst."&matchType=".$matchType.$winLossLink.'&player='.$player."&league=".$league.'&ground='.$ground.$inningsLink.'&groupBy='.$groupBy.'&startDate='.$startDate.'&endDate='.$endDate.'&resultQual='.$resultQual.'&resultQualFrom='.$resultQualFrom.'&resultQualTo='.$resultQualTo.'&sortBy='.$sortBy.'&width="+screen.width+"&height="+screen.height;</script>';
}

?>
<html>
<head>
    <title>cricrate | cricinsight</title>		
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
    <link href="css/bootstrap-chosen.css" rel="stylesheet">
    <script src="js/chosen.jquery.js"></script>    
    <!--<script src="http://harvesthq.github.io/chosen/chosen.jquery.js"></script>-->
    <script type="text/javascript">
	
    var isMobile = false; //initiate as false
    // device detection
    if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent) 
    || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))) isMobile = true;
    
    var chartWidth = screen.width * 0.375;
    var chartHeight = screen.height * 0.2;
    var chartHeightB = screen.height * 0.375;    
    if (isMobile == true) {
	chartWidth = chartWidth * 2;
    }	  
    
    var matchFormat = <?php echo json_encode($matchFormat); ?>;
    var disc = <?php echo json_encode($disc); ?>;
    var batBowl = disc.toLowerCase();
    if (batBowl == "all-round") {
       batBowl = "allRound";
    } else if (batBowl == "win shares") {
       batBowl = "winShares";
    }
    var player = <?php echo json_encode($player); ?>;
    var league = <?php echo json_encode($league); ?>;
    var teams = <?php echo json_encode($teamsLink); ?>;
    var oppositions = <?php echo json_encode($oppositionsLink); ?>;
    var homeAway = <?php echo json_encode($homeAway); ?>;
    var hosts = <?php echo json_encode($hostsLink); ?>;
    var winLoss = <?php echo json_encode($winLossLink); ?>;
    var batFieldFirst = <?php echo json_encode($batFieldFirst); ?>;
    var ground = <?php echo json_encode($ground); ?>;
    var matchType = <?php echo json_encode($matchType); ?>;
    var innings = <?php echo json_encode($inningsLink); ?>;
    var groupBy = <?php echo json_encode($groupBy); ?>;
    var startDate = <?php echo json_encode($startDate); ?>;
    var endDate = <?php echo json_encode($endDate); ?>;
    var resultQual = <?php echo json_encode($resultQual); ?>;
    var resultQualFrom = <?php echo json_encode($resultQualFrom); ?>;
    var resultQualTo = <?php echo json_encode($resultQualTo); ?>;
    
    var xVal = <?php echo json_encode($xVal); ?>;
    var yVal = <?php echo json_encode($yVal); ?>;    
    var xAxis = <?php echo json_encode($xAxis); ?>;
    var yAxis = <?php echo json_encode($yAxis); ?>;
    var histVal = <?php echo json_encode($histVal); ?>;    
    var histAxis = <?php echo json_encode($histAxis); ?>;
    
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChartHist);
    google.charts.setOnLoadCallback(drawChartBubble);            
            
    function drawChartHist() {
       var jsonData = $.ajax({
	   url: "charts/cricinsightHist.php?matchFormat="+matchFormat+"&batBowl="+batBowl+"&histVal="+histVal+teams+oppositions+hosts+winLoss+"&homeAway="+homeAway+"&batFieldFirst="+batFieldFirst+"&ground="+ground+"&matchType="+matchType+"&player="+player+"&league="+league+innings+"&startDate="+startDate+"&endDate="+endDate+"&groupBy="+groupBy+"&resultQual="+resultQual+"&resultQualFrom="+resultQualFrom+"&resultQualTo="+resultQualTo,
	   dataType:"json",
	   async: false
	   }).responseText;
	          
       // Create our data table out of JSON data loaded from server.	
       var data = new google.visualization.DataTable(jsonData);              
 
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
	    colors: ['#2c518d'],
	    width: chartWidth,
	    height: chartHeight,
	    legend: 'none',
	    hAxis: {
		    title: histAxis,
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
	    vAxis: {
		    title: "Count",
		   format: "####",
		   viewWindowMode: "maximized",		   
		   textStyle: {
			       color: '#000000',
			       fontSize: 11
			       },
		   titleTextStyle: {
				   color: '#000000',
				   italic: "false",
				   },
	       },
	    bar: { gap: 0 },
	    histogram: {
		maxNumBuckets: 60,
	      },
	    animation: {
			"startup": true,
			duration: 1000,
			easing: 'inAndOut',
			},	    
        };
	
       var chart = new google.visualization.Histogram(document.getElementById('chart'));
       chart.draw(data, options);       
    }
    
    function drawChartBubble() {
       var jsonData = $.ajax({
	   url: "charts/cricinsightBubble.php?matchFormat="+matchFormat+"&batBowl="+batBowl+"&xVal="+xVal+"&yVal="+yVal+teams+oppositions+hosts+winLoss+"&homeAway="+homeAway+"&batFieldFirst="+batFieldFirst+"&ground="+ground+"&matchType="+matchType+"&player="+player+"&league="+league+innings+"&startDate="+startDate+"&endDate="+endDate+"&groupBy="+groupBy+"&resultQual="+resultQual+"&resultQualFrom="+resultQualFrom+"&resultQualTo="+resultQualTo,
	   dataType:"json",
	   async: false
	   }).responseText;
	    
	//document.write("charts/customB.php?matchFormat="+matchFormat+"&batBowl="+batBowl+"&xVal="+xVal+"&yVal="+yVal+teams+oppositions+homeAway+winLoss+"&ground="+ground+innings+"&startDate="+startDate+"&endDate="+endDate+"&groupBy="+groupBy+"&resultQual="+resultQual+"&resultQualFrom="+resultQualFrom+"&resultQualTo="+resultQualTo);
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
	    height: chartHeightB,
	   hAxis: {
		   title: xAxis,
		   slantedText: "false",		   
		   maxAlternation: 1,
		   gridlines: {count: 15},
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
	
       var chart = new google.visualization.BubbleChart(document.getElementById('chartB'));
       chart.draw(data, options);       
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
       $('#ratingsTable').DataTable( {
       "lengthChange":   false,
       "pageLength": 11,
       "order": [[ 0, "asc" ]],
    } );
    } );
       
    submitForms = function(){
	    window.document.selectForm.submit();
	}
	
    chartForms = function(){
	    window.document.chartForm.submit();
	}
	
    chartFormsH = function(){
	    window.document.chartFormH.submit();
	}
	
    $(function() {
        $('.chosen-select').chosen();
        $('.chosen-select-deselect').chosen({ allow_single_deselect: true });
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
		    <li class="active"><a href="cricinsight.php" ><b>cricinsight <span class="label label-warning">new</span><span class="sr-only">(current)</span></b></a></li>
                    <li><a href="about.php">About</a></li>
                </ul>
                <div class="twitter navbar-text pull-right"><a href="https://twitter.com/cricrate" class="twitter-follow-button" data-show-count="false" data-show-screen-name="false">Follow @cricrate</a></div>
                <div class="fb-like navbar-text pull-right" data-href="https://www.facebook.com/cricrate" data-layout="button" data-action="like" data-show-faces="true" data-share="false"></div>
            </div>
        </div>
    </nav>
    
<?php

if (!isset($_GET["Submit"])) {
    echo "<div class=\"container\">";
    echo "<div class=\"panel panel-default\">";
    echo "<div class=\"panel-body\">";
    echo "<h2><b style=\"color:#2c518d;\">cric</b><b style=\"color:#FFBC00;\">insight</b></h2><br/>";
    echo "<div class=\"row\">";        
   $matchFormat = "Test";
   $disc = "Batting";
   $groupBy = "Player";
   echo "<form class=\"form-inline\" role=\"form\" name=\"selectForm\" method=\"get\" action=\"cricinsight.php\">";
   echo "<div class=\"col-lg-6\">";
   echo "<div class=\"form-group\">";
   echo "<b>Match format:</b>";
   echo "<br/>";
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
   echo "<br/><br/>";
            
   echo "<div class=\"form-group\">";
   echo "<b>Discipline:</b>";
   echo "<br/>";
   echo "<select class=\"form-control\" name=\"disc\" onChange=\"submitForms()\">";
   if ($matchFormat == "ODI" || $matchFormat == "FT20") {
	$discs = array("Batting", "Bowling", "All-Round", "Fielding", "Win Shares");
   } else if ($matchFormat == "Test") {
	$discs = array("Batting", "Bowling", "All-Round", "Fielding");
   } else if ($matchFormat == "T20I") {
	$discs = array("Batting", "Bowling", "All-Round");
   }   
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
   
   $dbName = "ccr.db";
   if ($matchFormat == "ODI") {
     $dbName = "ccrODI.db";
   } elseif ($matchFormat == "T20I") {
     $dbName = "ccrT20I.db";
   } elseif ($matchFormat == "FT20") {
     $dbName = "ccrFT20.db";
   }
   
   $db = new SQLite3($dbName);
   
    $sql = "select distinct player from playerInfo order by player asc"; 
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
   
    echo "<br/><br/>";
    echo "<div class=\"form-group\">";
    echo "<b>Player:</b>";
    echo "<br/>";    
    echo "<select class=\"chosen-select\" data-placeholder=\"All\" tabindex=\"2\" name=\"player\">";
    $playerSet = "All";
    if (isset($_GET['player'])) {
	$playerSet = $_GET['player'];
    }
    if ($playerSet == "All") {
	echo "<option selected=\"selected\" value=\"All\">All</option>";
    } else {
	echo "<option value=\"All\">All</option>";
    }
    $count = 0;
    while($res = $result->fetchArray(SQLITE3_NUM)) {
	 $player = $res[0];
	 if ($player == $playerSet) {
	    echo "<option selected=\"selected\" value=\"$player\">$player</option>";
	 } else {
	    echo "<option value=\"$player\">$player</option>";  
	 }	 
     }    
    echo "</select>";
    echo "</div>";  
   
    if ($matchFormat == "FT20") {
	echo "<br/><br/>";
	echo "<b>League:</b>";
	echo "<br/>";
	
	echo "<select class=\"form-control\" name=\"league\">";
	echo "<option selected=\"selected\" value=\"All\">All</option>";
	echo "<option value=\"IPL\">IPL</option>";
	echo "<option value=\"BBL\">BBL</option>";
	echo "<option value=\"CPL\">CPL</option>";
	echo "</select>";
    } else {
	$sql = "select distinct country from playerInfo order by country asc";
	$result = $db->query($sql);
	if (!$result) die("Cannot execute query.");
	
	echo "<br/><br/>";
	echo "<b>Team:</b>";
	echo "<br/>";
	while($res = $result->fetchArray(SQLITE3_NUM)) {
	    if ($res[0] != "United States of America" and $res[0] != "East Africa" and $res[0] != "Papua New Guinea") {
		echo "<input type=\"checkbox\" name=\"teams[]\" value=\"$res[0]\"> $res[0]&nbsp;&nbsp;&nbsp;";
	    }	    
	}
	echo "<br/><br/>";
	echo "<b>Opposition:</b>";
	echo "<br/>";
	while($res = $result->fetchArray(SQLITE3_NUM)) {
	    if ($res[0] != "United States of America" and $res[0] != "East Africa" and $res[0] != "Papua New Guinea") {
		echo "<input type=\"checkbox\" name=\"oppositions[]\" value=\"$res[0]\"> $res[0]&nbsp;&nbsp;&nbsp;";
	    }
	}
    }   
   
    echo "<br/><br/>";
    echo "<b>Home or away:</b>";    
    echo "<br/>";
    echo "<input type=\"radio\" name=\"homeAway\" value=\"0\"> Home&nbsp;&nbsp;&nbsp;";
    echo "<input type=\"radio\" name=\"homeAway\" value=\"1\"> Away&nbsp;&nbsp;&nbsp;";
    echo "<input type=\"radio\" name=\"homeAway\" value=\"2\" checked=\"checked\"> Either&nbsp;&nbsp;&nbsp;";
    
    if ($matchFormat != "FT20") {
	$sql = "select distinct location from ".$matchFormatLower."Info order by location asc";
	$result = $db->query($sql);
	if (!$result) die("Cannot execute query.");
	
	echo "<br/><br/>";
	echo "<b>Host country:</b>";
	echo "<br/>";
	while($res = $result->fetchArray(SQLITE3_NUM)) {
	    echo "<input type=\"checkbox\" name=\"hosts[]\" value=\"$res[0]\"> $res[0]&nbsp;&nbsp;&nbsp;";
	}
	echo "<br/><br/>";
    }     
    
    $sql = "select distinct ground from ".$matchFormatLower."Info order by ground asc";
   $result = $db->query($sql);
   if (!$result) die("Cannot execute query.");
    
   if ($matchFormat != "FT20") {
	echo "</div>";
	echo "<div class=\"col-lg-6\">";	
    } else {
	echo "<br/><br/>";
    }
        
    echo "<div class=\"form-group\">";
   echo "<b>Ground:</b>";
   echo "<br/>";
   echo "<select class=\"chosen-select\" data-placeholder=\"All\" tabindex=\"2\" name=\"ground\">";
   $groundSet = "All";
    if (isset($_GET['ground'])) {
	$groundSet = $_GET['ground'];
    }
    if ($groundSet == "All") {
	echo "<option selected=\"selected\" value=\"All\">All</option>";
    } else {
	echo "<option value=\"All\">All</option>";
    }
   $count = 0;
   while($res = $result->fetchArray(SQLITE3_NUM)) {
	$ground = $res[0];
	if ($ground == $groundSet) {
	    echo "<option selected=\"selected\" value=\"$ground\">$ground</option>";
	} else {
	    echo "<option value=\"$ground\">$ground</option>";   
	}	
    }    
    echo "</select>";
    echo "</div>";                    
    echo "<br/><br/>";    
    
    echo "<b>Date range:</b>";    
    echo "<br/>";
    echo "<input type=\"date\" class=\"form-control\" name=\"startDate\">&nbsp;to&nbsp;";
    echo "<input type=\"date\" class=\"form-control\" name=\"endDate\">";
    
    if ($matchFormat == "FT20") {
	echo "</div>";
	echo "<div class=\"col-lg-6\">";              
    }
    
    if ($matchFormat != "FT20" and $matchFormat != "Test") {
	echo "<br/><br/>";
	echo "<b>Match type:</b>";
	echo "<br/>";
	
	echo "<select class=\"form-control\" name=\"matchType\">";
	echo "<option selected=\"selected\" value=\"Any\">Any</option>";
	echo "<option value=\"Knockout\">Knockout</option>";
	echo "<option value=\"World Cup\">World Cup</option>";
	echo "</select>";
    } else if ($matchFormat == "FT20") {
	echo "<br/><br/>";
	echo "<b>Match type:</b>";
	echo "<br/>";
	
	echo "<select class=\"form-control\" name=\"matchType\">";
	echo "<option selected=\"selected\" value=\"Any\">Any</option>";
	echo "<option value=\"Knockout\">Knockout</option>";
	echo "</select>";
    } 
    
    echo "<br/><br/>";
    echo "<b>Match result:</b>";
    echo "<br/>";    
    echo "<input type=\"checkbox\" name=\"winLoss[]\" value=\"2\"> Win&nbsp;&nbsp;&nbsp;";
    echo "<input type=\"checkbox\" name=\"winLoss[]\" value=\"0\"> Loss&nbsp;&nbsp;&nbsp;";
    if ($matchFormat == "Test") {
	echo "<input type=\"checkbox\" name=\"winLoss[]\" value=\"1\"> Draw/Tie/NR&nbsp;&nbsp;&nbsp;";
    } else {
	echo "<input type=\"checkbox\" name=\"winLoss[]\" value=\"1\"> Tie/NR&nbsp;&nbsp;&nbsp;";
    }
    
    if ($matchFormat != "FT20") {
	echo "<br/><br/>";
	echo "<b>Batting or fielding first:</b>";    
	echo "<br/>";
	echo "<input type=\"radio\" name=\"batFieldFirst\" value=\"Batting\"> Batting first&nbsp;&nbsp;&nbsp;";
	echo "<input type=\"radio\" name=\"batFieldFirst\" value=\"Fielding\"> Fielding first&nbsp;&nbsp;&nbsp;";
	echo "<input type=\"radio\" name=\"batFieldFirst\" value=\"Either\" checked=\"checked\"> Either&nbsp;&nbsp;&nbsp;";
    }
    
    echo "<br/><br/>";
    echo "<b>Innings:</b>";    
    echo "<br/>";
    echo "<input type=\"checkbox\" name=\"innings[]\" value=\"1\"> 1st&nbsp;&nbsp;&nbsp;";
    echo "<input type=\"checkbox\" name=\"innings[]\" value=\"2\"> 2nd&nbsp;&nbsp;&nbsp;";
    if ($matchFormat == "Test") {
	echo "<input type=\"checkbox\" name=\"innings[]\" value=\"3\"> 3rd&nbsp;&nbsp;&nbsp;";
	echo "<input type=\"checkbox\" name=\"innings[]\" value=\"4\"> 4th&nbsp;&nbsp;&nbsp;";
    }    
    echo "<br/><br/>";
    echo "<b>Result qualification:</b>";
    echo "<br/>";
    if (isset($_GET['groupBy'])) {
	$groupBy = $_GET['groupBy'];
    }
    echo "<div class=\"form-group\">";
    echo "<select class=\"form-control\" name=\"resultQual\">";
    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	if ($disc == "Batting") {
	    $resultQuals = array("None", "Innings played", "Runs scored", "Rated");
	} else if ($disc == "Bowling") {
	    $resultQuals = array("None", "Innings played", "Wickets taken", "Rated");
	} else if ($disc == "All-Round") {
	    $resultQuals = array("None", "Matches played", "Runs scored", "Wickets taken", "Rated");
	} else if ($disc == "Fielding") {
	    $resultQuals = array("None", "Innings played", "Catches taken", "Rated");
	} else if ($disc == "Win Shares") {
	    $resultQuals = array("None", "Innings played", "Total WSAvg");
	} else {
	    $resultQuals = array("None", "Innings played", "Rated");
	}
    } else {
	if ($disc == "Batting") {
	    $resultQuals = array("None", "Runs scored", "Rated");
	} else if ($disc == "Bowling") {
	    $resultQuals = array("None", "Wickets taken", "Rated");
	} else if ($disc == "All-Round") {
	    $resultQuals = array("None", "Runs scored", "Wickets taken", "Rated");
	} else if ($disc == "Fielding") {
	    $resultQuals = array("None", "Catches taken", "Rated");
	} else if ($disc == "Win Shares") {
	    $resultQuals = array("None", "Total WS");
	} else {
	    $resultQuals = array("None", "Rated");
	}
    }
    $count = 0;
    foreach ($resultQuals as $rq) {
	if ($count == 0) {
	    echo "<option selected=\"selected\" value=\"$rq\">$rq</option>";
	} else {
	    echo "<option value=\"$rq\">$rq</option>";
	}
	$count = $count + 1;
    }
    echo "</select>";
    echo "&nbsp;from <input type=\"text\"  class=\"form-control\" size=\"5\" onkeypress='return event.charCode >= 48 && event.charCode <= 57' name=\"resultQualFrom\">";
    echo "&nbsp;to <input type=\"text\" class=\"form-control\" size=\"5\" onkeypress='return event.charCode >= 48 && event.charCode <= 57' name=\"resultQualTo\">";
    echo "<br/><br/>";
    echo "<b>Group by:</b>";
    echo "<br/>";
    echo "<select class=\"form-control\" name=\"groupBy\" onChange=\"submitForms()\">";
    if ($matchFormat == "FT20") {
	$groupBys = array("Player", "Ground", "Inning");
    } else {
	$groupBys = array("Player", "Ground", "Opposition", "Inning");
    }    
    if(isset($_GET['groupBy'])) {    
	$groupBy = $_GET['groupBy'];
	foreach ($groupBys as $gb) {
	    if ($groupBy == $gb) {
		echo "<option selected=\"selected\" value=\"$gb\">$gb</option>";
	    } else {
		echo "<option value=\"$gb\">$gb</option>";
	    }
	}    
    } else {
	$count = 0;
	foreach ($groupBys as $gb) {
	    if ($count == 0) {
		echo "<option selected=\"selected\" value=\"$gb\">$gb</option>";
		$groupBy = $gb;
	    } else {
		echo "<option value=\"$gb\">$gb</option>";
	    }
	    $count = $count + 1;
	}
    }
    echo "</select>";
    echo "<br/><br/>";
    echo "<b>Sort results by:</b>";
    echo "<br/>";
    echo "<select class=\"form-control\" name=\"sortBy\">";
    if ($groupBy == "Player") {
	if ($disc == "Batting") {
	    $sortBys = array("Runs scored", "Average", "Strike Rate", "Innings played", "Rating", "Player name");
	} else if ($disc == "Bowling") {
	    $sortBys = array("Wickets taken", "Average", "Strike Rate", "Innings played", "Econ Rate", "Rating", "Player name");
	} else if ($disc == "All-Round") {
	    $sortBys = array("Rating", "Runs scored", "Wickets taken", "Batting Average", "Bowling Average", "Matches played", "Player name");
	} else if ($disc == "Fielding") {
	    $sortBys = array("Rating", "Drop rate", "Catches taken", "Innings played", "Player name");
	} else if ($disc == "Win Shares") {
	    $sortBys = array("Total WSAvg", "Batting WSAvg", "Bowling WSAvg", "Innings played", "Player name");
	} else {
	    $sortBys = array("Innings played", "Rating", "Player name");
	}
    } else if ($groupBy == "Ground") {
	if ($disc == "Batting") {
	    $sortBys = array("Runs scored", "Average", "Strike Rate", "Innings played", "Rating", "Ground");
	} else if ($disc == "Bowling") {
	    $sortBys = array("Wickets taken", "Average", "Strike Rate", "Innings played", "Econ Rate", "Rating", "Ground");
	} else if ($disc == "All-Round") {
	    $sortBys = array("Rating", "Runs scored", "Wickets taken", "Batting Average", "Bowling Average", "Matches played", "Ground");
	} else if ($disc == "Fielding") {
	    $sortBys = array("Rating", "Drop rate", "Catches taken", "Innings played", "Ground");
	} else if ($disc == "Win Shares") {
	    $sortBys = array("Total WSAvg", "Batting WSAvg", "Bowling WSAvg", "Innings played", "Ground");
	} else {
	    $sortBys = array("Innings played", "Rating", "Ground");
	}
    } else if ($groupBy == "Opposition") {
	if ($disc == "Batting") {
	    $sortBys = array("Runs scored", "Average", "Strike Rate", "Innings played", "Rating", "Opposition");
	} else if ($disc == "Bowling") {
	    $sortBys = array("Wickets taken", "Average", "Strike Rate", "Innings played", "Econ Rate", "Rating", "Opposition");
	} else if ($disc == "All-Round") {
	    $sortBys = array("Rating", "Runs scored", "Wickets taken", "Batting Average", "Bowling Average", "Matches played", "Opposition");
	} else if ($disc == "Fielding") {
	    $sortBys = array("Rating", "Drop rate", "Catches taken", "Innings played", "Opposition");
	} else if ($disc == "Win Shares") {
	    $sortBys = array("Total WSAvg", "Batting WSAvg", "Bowling WSAvg", "Innings played", "Opposition");
	} else {
	    $sortBys = array("Innings played", "Rating", "Opposition");
	}
    } else {
	if ($disc == "Batting") {
	    $sortBys = array("Runs scored", "Balls faced", "Strike Rate", "Rating", "Player name");
	} else if ($disc == "Bowling") {
	    $sortBys = array("Wickets taken", "Balls bowled", "Rating", "Player name");
	} else if ($disc == "All-Round") {
	    $sortBys = array("Rating", "Runs scored", "Wickets taken", "Player name");
	} else if ($disc == "Fielding") {
	    $sortBys = array("Rating", "Catches taken", "Player name");
	} else if ($disc == "Win Shares") {
	    $sortBys = array("Total WS", "Batting WS", "Bowling WS", "Player name");
	} else {
	    $sortBys = array("Rating", "Player name");
	}
    }
    if(isset($_GET['sortBy'])) {    
	$sortBy = $_GET['sortBy'];
	foreach ($sortBys as $sb) {
	    if ($sortBy == $sb) {
		echo "<option selected=\"selected\" value=\"$sb\">$sb</option>";
	    } else {
		echo "<option value=\"$sb\">$sb</option>";
	    }
	}    
    } else {
	$count = 0;
	foreach ($sortBys as $sb) {
	    if ($count == 0) {
		echo "<option selected=\"selected\" value=\"$sb\">$sb</option>";
		$sortBy = $sb;
	    } else {
		echo "<option value=\"$sb\">$sb</option>";
	    }
	    $count = $count + 1;
	}
    }
    echo "</select>";
    echo "</div>";
    echo "<br/><br/>";
    
    echo "<input type=\"submit\" name=\"Submit\" class=\"btn btn-primary\" value=\"Submit\">";
    echo "</div>";
    echo "</form>";    
    echo "</div>";
    echo "</div>";
    echo "</div>";
    echo "</div>";
} else {    
    echo "<div class=\"panel panel-inverse\">";    
    echo "<div class=\"panel-body\">";    
    echo "<div class=\"row\">";        
    echo "<div class=\"col-lg-3\">";
    echo "<h2><b style=\"color:#2c518d;\">&nbsp;&nbsp;cric</b><b style=\"color:#FFBC00;\">insight&nbsp;&nbsp;</b><b><small><a href=\"#\" onclick=\"history.go(-1)\">edit</a>&nbsp;&nbsp;<a href=\"cricinsight.php\">clear</a></small></b></h2>";
    echo "<ul class=\"list-group\">";
    echo "<li class=\"list-group-item\">";
    
    $dbName = "ccr.db";
    if ($matchFormat == "ODI") {
      $dbName = "ccrODI.db";
    } elseif ($matchFormat == "T20I") {
      $dbName = "ccrT20I.db";
    } elseif ($matchFormat == "FT20") {
      $dbName = "ccrFT20.db";
    }    
    $db = new SQLite3($dbName);
    
    $filterText = "<b>Match format:</b> $matchFormat<br/>";
    $filterText .= "<b>Discipline:</b> $disc<br/>";
    
    $playerFilter = "";
    if(isset($_GET['player']) ) {
	$player = $_GET['player'];	
	if ($player != "All") {	
	    if ($disc != "All-Round" and $disc != "Fielding") {
		$playerFilter = "and b.player='".$player."'";
	    } else {
		$playerFilter = "and a.player='".$player."'";
	    }
	    $filterText .= "<b>Player:</b> $player<br/>";	
	} else {
	    $filterText .= "<b>Player:</b> All<br/>";
	}
    } else {
	$filterText .= "<b>Player:</b> All<br/>";
    }
    
    $countryTeams = "p.country";
    if ($matchFormat == "FT20") {
       $countryTeams = "p.teams";
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
	    $filterText .= "<b>League:</b> $league<br/>";   
	}	
    } else {
	$filterText .= "<b>League:</b> All<br/>";
    }
    
    $teamFilter = "";    
    if( isset($_GET['teams']) ) {
	$teamFilter = "and ".$countryTeams." in (";
	$filterText .= "<b>Team:</b> ";
	foreach($_GET['teams'] as $team) {    
	    $teamFilter .= "'".$team."',";
	    $filterText .= "$team, ";
	}
	$teamFilter .= "'') ";
	$filterText = substr($filterText, 0, -2);
	$filterText .= "<br/>";
    } else {
	$filterText .= "<b>Team:</b> All<br/>";
    }
    
    $oppFilter = "";    
    if( isset($_GET['oppositions']) ) {
	$oppFilter1 = "and ((t.team1 in (";
	$oppFilter2 = "or (t.team2 in (";
	$filterText .= "<b>Opposition:</b> ";
	foreach($_GET['oppositions'] as $opp) {    
	    $oppFilter1 .= "'".$opp."',";
	    $oppFilter2 .= "'".$opp."',";
	    $filterText .= "$opp, ";
	}
	$oppFilter1 .= "'') and t.team2=".$countryTeams.")";
	$oppFilter2 .= "'') and t.team1=".$countryTeams."))";    
	$oppFilter = $oppFilter1.$oppFilter2;
	$filterText = substr($filterText, 0, -2);
	$filterText .= "<br/>";
    } else {
	$filterText .= "<b>Opposition:</b> All<br/>";
    }
    
    $homeAwayFilter = "";    
    if (isset($_GET['homeAway']) ) {
	$homeAway = $_GET['homeAway'];
	if ($homeAway != 2) {
	    $homeAwayFilter = "and b.homeAway=".$homeAway." ";
	}
	$filterText .= "<b>Home or away:</b> ";
	if ($homeAway == 0) {
	    $filterText .= "Home<br/>";
	} elseif ($homeAway == 1) {
	    $filterText .= "Away<br/>";
	} else {
	    $filterText .= "Either<br/>";
	}	   	 
    } else {
	$filterText .= "<b>Home or away:</b> Either<br/>";
    }
    
    $hostFilter = "";    
    if( isset($_GET['hosts']) ) {
	$hostFilter = "and t.location in (";
	$filterText .= "<b>Host country:</b> ";
	foreach($_GET['hosts'] as $host) {    
	    $hostFilter .= "'".$host."',";
	    $filterText .= "$host, ";
	}
	$hostFilter .= "'') ";
	$filterText = substr($filterText, 0, -2);
	$filterText .= "<br/>";
    } else {
	$filterText .= "<b>Host country:</b> All<br/>";
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
	    
	    $filterText .= "<b>Match type:</b> $matchType<br/>";   
	}	
    } else {
	$filterText .= "<b>Match type:</b> Any<br/>";
    }
    
    echo $filterText;
    $filterText = "";
    echo "</li>";
    echo "</ul>";
    echo "</div>";    
    echo "<div class=\"col-lg-3\">";
    echo "<br/><br/><br/>";
    echo "<ul class=\"list-group\">";
    echo "<li class=\"list-group-item\">";
    
    $winLossFilter = "";    
    if( isset($_GET['winLoss']) ) {
	$winLossFilter = "and b.result in (";
	$filterText .= "<b>Match result:</b> ";
	foreach($_GET['winLoss'] as $matchResult) {
	    $winLossFilter .= $matchResult.",";
	    if ($matchResult == 2) {
		$filterText .= "Win, ";
	    } else if ($matchResult == 1) {
		if ($matchFormat == "Test") {
		    $filterText .= "Draw/Tie/NR, ";
		} else {
		    $filterText .= "Tie/NR, ";   
		}		
	    } else {
		$filterText .= "Loss, ";
	    }
	}
	$winLossFilter .= "'') ";
	$filterText = substr($filterText, 0, -2);
	$filterText .= "<br/>";
    } else {
	$filterText .= "<b>Match result:</b> Any<br/>";
    }         
    
   $batFieldFirstFilter = "";
   if ($matchFormat != "FT20") {	    
       if (isset($_GET['batFieldFirst']) ) {
	   $batFieldFirst = $_GET['batFieldFirst'];
	   if ($batFieldFirst == "Batting") {
	       $batFieldFirstFilter = "and d.innings=1 and d.batTeam=p.country";
	   } elseif ($batFieldFirst == "Fielding") {
	       $batFieldFirstFilter = "and d.innings=1 and d.bowlTeam=p.country";
	   } else {
	       $batFieldFirstFilter = "and d.innings=1";
	   }
	   $filterText .= "<b>Batting or fielding first:</b> ";
	   if ($batFieldFirst == "Batting" || $batFieldFirst == "Fielding") {
	       $filterText .= "$batFieldFirst first<br/>";
	   } else {
	       $filterText .= "Either<br/>";
	   }	   	 
       } else {
	   $filterText .= "<b>Batting or fielding first:</b> Either<br/>";
       }        
   } else {
     $batFieldFirstFilter = "and d.innings=1";
   }
  
    $groundFilter = "";    
    if ($_GET['ground'] != "All") {
	$ground = $_GET['ground'];
	$groundFilter = "and t.ground='".$ground."'";
	$filterText .= "<b>Ground:</b> $ground<br/>";	
    } else {
	$filterText .= "<b>Ground:</b> All<br/>";
    }        
    
    $inningsFilter = "";    
    if( isset($_GET['innings']) ) {
	$inningsFilter = "and b.innings in (";
	$filterText .= "<b>Innings:</b> ";
	foreach($_GET['innings'] as $inn) {
	    $inningsFilter .= $inn.",";
	    $filterText .= "$inn, ";
	}
	$inningsFilter .= "'') ";
	$filterText = substr($filterText, 0, -2);
	$filterText .= "<br/>";
    } else {
	$filterText .= "<b>Innings:</b> All<br/>";
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
	    $filterText .= "<b>From:</b> ".substr($startDate, 0, 4)."-".substr($startDate, 4, 2)."-".substr($startDate, 6, 2)."<br/>"; 
	} else {
	    $startDates = explode("-", $_GET['startDate']);
	    $startDate = $startDates[0].$startDates[1].$startDates[2];
	    $filterText .= "<b>From:</b> ".$_GET['startDate']."<br/>";   
	}	
    } else {
	$filterText .= "<b>From:</b> Any date<br/>";
    }
    
    if ($_GET['endDate'] != "") {
	if (strpos($_GET['endDate'], "-") == false) {
	    $endDate = $_GET['endDate'];
	    $filterText .= "<b>To:</b> ".substr($endDate, 0, 4)."-".substr($endDate, 4, 2)."-".substr($endDate, 6, 2)."<br/>"; 
	} else {
	    $endDates = explode("-", $_GET['endDate']);
	    $endDate = $endDates[0].$endDates[1].$endDates[2];
	    $filterText .= "<b>To:</b> ".$_GET['endDate']."<br/>";
	}
    } else {
	$filterText .= "<b>To:</b> Any date<br/>";
    }    
   
    $groupBy = "Player";
    if( isset($_GET['groupBy']) ) {
	$groupBy = $_GET['groupBy'];
    }
    $filterText .= "<b>Grouped by:</b> $groupBy<br/>";    
    
    $resultQualFilter = "";    
    if( isset($_GET['resultQual']) ) {
	$filterText .= "<b>Result qualification:</b> ";
	$resultQual = $_GET['resultQual'];
	$resultQualFrom = $_GET['resultQualFrom'];
	$resultQualTo = $_GET['resultQualTo'];
	
	if ($resultQual == "None") {
	    $filterText .= "None"; 
	} else if ($resultQual == "Innings played") {
	    $filterText .= "Innings played ";	    
	    if ($resultQualFrom != "") {
		$resultQualFilter = "having numInn>=".$resultQualFrom." ";
		$filterText .= ">= ".$resultQualFrom." "; 
	    }
	    
	    if ($resultQualTo != "") {
		if ($resultQualFrom != "") {
		    $resultQualFilter .= "and";
		    $filterText .= "and ";
		} else {
		    $resultQualFilter .= "having";
		}
		$resultQualFilter .= " numInn<=".$resultQualTo." ";
		$filterText .= "<= ".$resultQualTo." "; 
	    }
	} else if ($resultQual == "Matches played") {
	    $filterText .= "Matches played ";	    
	    if ($resultQualFrom != "") {
		$resultQualFilter = "having numMat>=".$resultQualFrom." ";
		$filterText .= ">= ".$resultQualFrom." "; 
	    }
	    
	    if ($resultQualTo != "") {
		if ($resultQualFrom != "") {
		    $resultQualFilter .= "and";
		    $filterText .= "and ";
		} else {
		    $resultQualFilter .= "having";
		}
		$resultQualFilter .= " numMat<=".$resultQualTo." ";
		$filterText .= "<= ".$resultQualTo." "; 
	    }
	} else if ($resultQual == "Runs scored") {
	    $filterText .= "Runs scored ";
	    if ($resultQualFrom != "") {
		if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
		    $resultQualFilter = "having sumRuns>=".$resultQualFrom." ";   
		} else {
		    $resultQualFilter = "and sumRuns>=".$resultQualFrom." ";
		}		
		$filterText .= ">= ".$resultQualFrom." "; 
	    }
	    
	    if ($resultQualTo != "") {
		if ($resultQualFrom != "") {
		    $resultQualFilter .= "and";
		    $filterText .= "and ";
		} else {
		    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
			$resultQualFilter .= "having";
		    } else {
			$resultQualFilter .= "and";
		    }		    
		}
		$resultQualFilter .= " sumRuns<=".$resultQualTo." ";
		$filterText .= "<= ".$resultQualTo." "; 
	    }
	} else if ($resultQual == "Wickets taken") {
	    $filterText .= "Wickets taken ";
	    if ($resultQualFrom != "") {
		if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
		    $resultQualFilter = "having sumWkts>=".$resultQualFrom." ";   
		} else {
		    $resultQualFilter = "and sumWkts>=".$resultQualFrom." ";
		}
		$filterText .= ">= ".$resultQualFrom." "; 
	    }
	    
	    if ($resultQualTo != "") {
		if ($resultQualFrom != "") {
		    $resultQualFilter .= "and";
		    $filterText .= "and ";
		} else {
		    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
			$resultQualFilter .= "having";
		    } else {
			$resultQualFilter .= "and";
		    }
		}
		$resultQualFilter .= " sumWkts<=".$resultQualTo." ";
		$filterText .= "<= ".$resultQualTo." "; 
	    }
	} else if ($resultQual == "Catches taken") {
	    $filterText .= "Catches taken ";
	    if ($resultQualFrom != "") {
		if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
		    $resultQualFilter = "having sumCatches>=".$resultQualFrom." ";   
		} else {
		    $resultQualFilter = "and sumCatches>=".$resultQualFrom." ";
		}
		$filterText .= ">= ".$resultQualFrom." "; 
	    }
	    
	    if ($resultQualTo != "") {
		if ($resultQualFrom != "") {
		    $resultQualFilter .= "and";
		    $filterText .= "and ";
		} else {
		    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
			$resultQualFilter .= "having";
		    } else {
			$resultQualFilter .= "and";
		    }
		}
		$resultQualFilter .= " sumCatches<=".$resultQualTo." ";
		$filterText .= "<= ".$resultQualTo." "; 
	    }
	} else if ($resultQual == "Rated" || $result == "Total WSAvg" || $result == "Total WS") {
	    $filterText .= "Rated ";
	    if ($resultQualFrom != "") {
		if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
		    $resultQualFilter = "having avgRtg>=".$resultQualFrom." ";   
		} else {
		    $resultQualFilter = "and avgRtg>=".$resultQualFrom." ";
		}
		$filterText .= ">= ".$resultQualFrom." "; 
	    }
	    
	    if ($resultQualTo != "") {
		if ($resultQualFrom != "") {
		    $resultQualFilter .= "and";
		    $filterText .= "and ";
		} else {
		    if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
			$resultQualFilter .= "having";
		    } else {
			$resultQualFilter .= "and";
		    }
		}
		$resultQualFilter .= " avgRtg<=".$resultQualTo." ";
		$filterText .= "<= ".$resultQualTo." "; 
	    }
	}
	$filterText .= "<br/>";
    } else {
	$filterText .= "<b>Result qualification:</b> None<br/>";
    }    
    
    $sortByFilter = "";    
    if( isset($_GET['sortBy']) ) {
	$sortBy = $_GET['sortBy'];
	$filterText .= "<b>Sort results by:</b> $sortBy";
	
	if ($sortBy == "Innings played") {
	    $sortByFilter .= " numInn desc";
	} else if ($sortBy == "Matches played") {
	    $sortByFilter .= " numMat desc";
	} else if ($sortBy == "Runs scored") {
	    $sortByFilter .= " sumRuns desc";
	} else if ($sortBy == "Wickets taken") {
	    $sortByFilter .= " sumWkts desc";
	} else if ($sortBy == "Catches taken") {
	    $sortByFilter .= " sumCatches desc";
	} else if ($sortBy == "Rating" || $sortBy == "Total WSAvg" || $sortBy == "Total WS") {
	    $sortByFilter .= " avgRtg desc";
	} else if ($sortBy == "Player name") {
	    $sortByFilter .= " b.player asc";
	} else if ($sortBy == "Ground") {
	    $sortByFilter .= " t.ground asc";
	} else if ($sortBy == "Opposition") {
	    $sortByFilter .= " opposition asc";
	} else if ($sortBy == "Average") {
	    if ($disc == "Batting") {
		$sortByFilter .= " average desc";
	    } else if ($disc == "Bowling") {
		$sortByFilter .= " average asc";
	    }	    
	} else if ($sortBy == "Strike rate") {
	    if ($disc == "Batting") {
		$sortByFilter .= " strikeRate desc";
	    } else if ($disc == "Bowling") {
		$sortByFilter .= " strikeRate asc";
	    }
	} else if ($sortBy == "Balls faced" || $sortBy == "Balls bowled") {
	    $sortByFilter .= " sumBalls desc";	    
	} else if ($sortBy == "Econ rate") {
	    $sortByFilter .= " econRate asc";	    
	} else if ($sortBy == "Drop rate") {
	    $sortByFilter .= " dropRate asc";	    
	} else if ($sortBy == "Batting WSAvg" || $sortBy == "Batting WS") {
	    $sortByFilter .= " avgBattingWS desc";	    
	} else if ($sortBy == "Bowling WSAvg" || $sortBy == "Bowling WS") {
	    $sortByFilter .= " avgBowlingWS desc";	    
	}	
	$filterText .= "<br/>";
    }      
    
    $ballsPerOverText = "";
    if ($matchFormat == "Test") {
	$ballsPerOverText = ", t.ballsPerOver";
    }
    
    $location = "t.location";
    if ($matchFormat == "FT20") {
       $location = "t.ground";
    }
    
    if ($disc == "Batting") {
	if ($groupBy == "Player") {
	    $sql = "select b.playerId, b.player, ".$countryTeams.", count(b.innings) as numInn, sum(b.notOut), sum(b.runs) as sumRuns, sum(b.balls) as sumBalls, (sum(b.runs)*1.0/(count(b.innings)-sum(b.notOut))) as average, (sum(b.runs) * 100.0 / sum(b.balls)) as strikeRate, avg(b.rating) as avgRtg from batting".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter $batFieldFirstFilter $groundFilter $inningsFilter group by b.playerId $resultQualFilter order by $sortByFilter";
	} else if ($groupBy == "Ground") {
	    $sql = "select t.ground, $location, count(b.innings) as numInn, sum(b.notOut), sum(b.runs) as sumRuns, sum(b.balls) as sumBalls, (sum(b.runs)*1.0/(count(b.innings)-sum(b.notOut))) as average, (sum(b.runs) * 100.0 / sum(b.balls)) as strikeRate, avg(b.rating) as avgRtg from batting".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter group by t.ground $resultQualFilter order by $sortByFilter";
	} else if ($groupBy == "Opposition") {
	    $sql = "select (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, count(b.innings) as numInn, sum(b.notOut), sum(b.runs) as sumRuns, sum(b.balls) as sumBalls, (sum(b.runs)*1.0/(count(b.innings)-sum(b.notOut))) as average, (sum(b.runs) * 100.0 / sum(b.balls)) as strikeRate, avg(b.rating) as avgRtg from batting".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter group by opposition $resultQualFilter order by $sortByFilter";
	} else {
	    $sql = "select b.playerId, b.player, b.notOut, b.runs as sumRuns, b.balls as sumBalls, (b.runs * 100.0 / b.balls) as strikeRate, b.rating as avgRtg, ".$countryTeams.", t.team1, t.team2, t.ground, t.startDate, t.".$matchFormatLower."Id from batting".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter $resultQualFilter order by $sortByFilter limit 5000";     
	}
    } else if ($disc == "Bowling") {
	if ($groupBy == "Player") {
	    $sql = "select b.playerId, b.player, ".$countryTeams.", count(b.innings) as numInn, sum(b.balls) as sumBalls, sum(b.runs) as sumRuns, sum(b.wkts) as sumWkts, (sum(b.runs) * 1.0 / sum(b.wkts)) as average, (sum(b.runs) * 6.0 / sum(b.balls)) as econRate, (sum(b.balls) * 1.0 / sum(b.wkts)) as strikeRate, avg(b.rating) as avgRtg from bowling".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter group by b.playerId $resultQualFilter order by $sortByFilter";
	} else if ($groupBy == "Ground") {
	    $sql = "select t.ground, $location, count(b.innings) as numInn, sum(b.balls) as sumBalls, sum(b.runs) as sumRuns, sum(b.wkts) as sumWkts, (sum(b.runs) * 1.0 / sum(b.wkts)) as average, (sum(b.runs) * 6.0 / sum(b.balls)) as econRate, (sum(b.balls) * 1.0 / sum(b.wkts)) as strikeRate, avg(b.rating) as avgRtg from bowling".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter group by t.ground $resultQualFilter order by $sortByFilter";
	} else if ($groupBy == "Opposition") {
	    $sql = "select (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, count(b.innings) as numInn, sum(b.balls) as sumBalls, sum(b.runs) as sumRuns, sum(b.wkts) as sumWkts, (sum(b.runs) * 1.0 / sum(b.wkts)) as average, (sum(b.runs) * 6.0 / sum(b.balls)) as econRate, (sum(b.balls) * 1.0 / sum(b.wkts)) as strikeRate, avg(b.rating) as avgRtg from bowling".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter group by opposition $resultQualFilter order by $sortByFilter";
	} else {
	    $sql = "select b.playerId, b.player, b.balls as sumBalls, b.runs as sumRuns, b.wkts as sumWkts, b.rating as avgRtg, ".$countryTeams.", t.team1, t.team2, t.ground, t.startDate, t.".$matchFormatLower."Id $ballsPerOverText from bowling".$matchFormat."Innings b, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where b.".$matchFormatLower."Id=t.".$matchFormatLower."Id and b.".$matchFormatLower."Id=d.".$matchFormatLower."Id and b.playerId=p.playerId and t.startDate>=$startDate and t.startDate<=$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter $resultQualFilter order by $sortByFilter limit 5000";
	}
    } else if ($disc == "All-Round") {
	if ($matchFormat == "Test") {
	    if ($groupBy == "Player") {
		$sql = "select a.playerId, a.player, ".$countryTeams.", count(a.".$matchFormatLower."Id) as numMat, (sum(a.runs1) + sum(a.runs2)) as sumRuns, (sum(a.runs1) + sum(a.runs2)) * 1.0/(count(a.runs1) + count(a.runs2) - sum(a.notOut1) - sum(a.notOut2)) as battingAverage, (sum(a.wkts1) + sum(a.wkts2)) as sumWkts, (sum(a.bowlRuns1)+sum(a.bowlRuns2)) * 1.0 / (sum(a.wkts1)+sum(a.wkts2)) as bowlingAverage, avg(a.rating) as avgRtg from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter group by a.playerId $resultQualFilter order by $sortByFilter";
	    } else if ($groupBy == "Ground") {
		$sql = "select t.ground, $location, count(a.".$matchFormatLower."Id) as numMat, (sum(a.runs1) + sum(a.runs2)) as sumRuns, (sum(a.runs1) + sum(a.runs2)) * 1.0/(count(a.runs1) + count(a.runs2) - sum(a.notOut1) - sum(a.notOut2)) as battingAverage, (sum(a.wkts1) + sum(a.wkts2)) as sumWkts, (sum(a.bowlRuns1)+sum(a.bowlRuns2)) * 1.0 / (sum(a.wkts1)+sum(a.wkts2)) as bowlingAverage, avg(a.rating) as avgRtg from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter group by t.ground $resultQualFilter order by $sortByFilter";
	    } else if ($groupBy == "Opposition") {
		$sql = "select (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, count(a.".$matchFormatLower."Id) as numMat, (sum(a.runs1) + sum(a.runs2)) as sumRuns, (sum(a.runs1) + sum(a.runs2)) * 1.0/(count(a.runs1) + count(a.runs2) - sum(a.notOut1) - sum(a.notOut2)) as battingAverage, (sum(a.wkts1) + sum(a.wkts2)) as sumWkts, (sum(a.bowlRuns1)+sum(a.bowlRuns2)) * 1.0 / (sum(a.wkts1)+sum(a.wkts2)) as bowlingAverage, avg(a.rating) as avgRtg from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter group by opposition $resultQualFilter order by $sortByFilter";
	    } else {
		$sql = "select a.playerId, a.player, a.runs1, a.notOut1, a.runs2, a.notOut2, a.wkts1, a.bowlRuns1, a.wkts2, a.bowlRuns2, a.rating as avgRtg, ".$countryTeams.", t.team1, t.team2, t.ground, t.startDate, t.".$matchFormatLower."Id, (a.runs1+a.runs2) as sumRuns, (a.wkts1+a.wkts2) as sumWkts from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter $resultQualFilter order by $sortByFilter limit 5000";
	    }
	} else {
	    if ($groupBy == "Player") {
		$sql = "select a.playerId, a.player, ".$countryTeams.", count(a.".$matchFormatLower."Id) as numMat, sum(a.runs) as sumRuns, sum(a.runs) * 1.0/(count(a.runs) - sum(a.notOut)) as battingAverage, sum(a.wkts) as sumWkts, (sum(a.bowlRuns) * 1.0 / sum(a.wkts)) as bowlingAverage, avg(a.rating) as avgRtg from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter group by a.playerId $resultQualFilter order by $sortByFilter";
	    } else if ($groupBy == "Ground") {
		$sql = "select t.ground, $location, count(a.".$matchFormatLower."Id) as numMat, sum(a.runs) as sumRuns, sum(a.runs) * 1.0/(count(a.runs) - sum(a.notOut)) as battingAverage, sum(a.wkts) as sumWkts, (sum(a.bowlRuns) * 1.0 / sum(a.wkts)) as bowlingAverage, avg(a.rating) as avgRtg from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter group by t.ground $resultQualFilter order by $sortByFilter";
	    } else if ($groupBy == "Opposition") {
		$sql = "select (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, count(a.".$matchFormatLower."Id) as numMat, sum(a.runs) as sumRuns, sum(a.runs) * 1.0/(count(a.runs) - sum(a.notOut)) as battingAverage, sum(a.wkts) as sumWkts, (sum(a.bowlRuns) * 1.0 / sum(a.wkts)) as bowlingAverage, avg(a.rating) as avgRtg from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter group by opposition $resultQualFilter order by $sortByFilter";
	    } else {		
		$sql = "select a.playerId, a.player, a.runs as sumRuns, a.notOut, a.wkts as sumWkts, a.bowlRuns, a.rating as avgRtg, ".$countryTeams.", t.team1, t.team2, t.ground, t.startDate, t.".$matchFormatLower."Id from allRound".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and a.playerId=p.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter $resultQualFilter order by $sortByFilter limit 5000";
	    }
	}
    } else if ($disc == "Fielding") {
	if ($groupBy == "Player") {
	    $sql = "select a.playerId, a.player, ".$countryTeams.", count(t.".$matchFormatLower."Id) as numInn, sum(a.catches) as sumCatches, sum(a.droppedCatches) as droppedCatches, (sum(a.droppedCatches) * 1.0 / (sum(a.droppedCatches) + sum(a.catches))) as dropRate, sum(a.greatCatches) as sumGreatCatches, sum(a.directHits) as sumDirectHits, sum(a.runsSaved) as sumRunsSaved, avg(a.rating) avgRtg from fielding".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate  $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter group by a.playerId $resultQualFilter order by $sortByFilter";
	} else if ($groupBy == "Ground") {
	    $sql = "select t.ground, $location, count(t.".$matchFormatLower."Id) as numInn, sum(a.catches) as sumCatches, sum(a.droppedCatches) as droppedCatches, (sum(a.droppedCatches) * 1.0 / (sum(a.droppedCatches) + sum(a.catches))) as dropRate, sum(a.greatCatches) as sumGreatCatches, sum(a.directHits) as sumDirectHits, sum(a.runsSaved) as sumRunsSaved, avg(a.rating) avgRtg from fielding".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate  $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter group by t.ground $resultQualFilter order by $sortByFilter";
	} else if ($groupBy == "Opposition") {
	    $sql = "select (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, count(t.".$matchFormatLower."Id) as numInn, sum(a.catches) as sumCatches, sum(a.droppedCatches) as droppedCatches, (sum(a.droppedCatches) * 1.0 / (sum(a.droppedCatches) + sum(a.catches))) as dropRate, sum(a.greatCatches) as sumGreatCatches, sum(a.directHits) as sumDirectHits, sum(a.runsSaved) as sumRunsSaved, avg(a.rating) avgRtg from fielding".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate  $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter group by opposition $resultQualFilter order by $sortByFilter";
	} else {
	    $sql = "select a.playerId, a.player, a.catches as sumCatches, a.droppedCatches as droppedCatches, a.greatCatches as sumGreatCatches, a.directHits as sumDirectHits, a.runsSaved as sumRunsSaved, a.rating as avgRtg, ".$countryTeams.", t.team1, t.team2, t.ground, t.startDate, t.".$matchFormatLower."Id from fielding".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter $resultQualFilter order by $sortByFilter limit 5000";
	}
    } else if ($disc == "Win Shares") {	
	if ($groupBy == "Player") {
	    $sql = "select a.playerId, a.player, ".$countryTeams.", count(t.".$matchFormatLower."Id) as numInn, avg(a.battingAdjWS) as avgBattingWS, avg(a.bowlingAdjWS) as avgBowlingWS, avg(a.fieldingAdjWS) as avgFieldingWS, avg(a.totalAdjWS) as avgRtg from winShares".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter group by a.playerId $resultQualFilter order by $sortByFilter";
	} else if ($groupBy == "Ground") {
	    $sql = "select t.ground, $location, count(t.".$matchFormatLower."Id) as numInn, avg(a.battingAdjWS) as avgBattingWS, avg(a.bowlingAdjWS) as avgBowlingWS, avg(a.fieldingAdjWS) as avgFieldingWS, avg(a.totalAdjWS) as avgRtg from winShares".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter group by t.ground $resultQualFilter order by $sortByFilter";
	} else if ($groupBy == "Opposition") {
	    $sql = "select (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, (case when p.country==t.team1 then t.team2 else t.team1 end) as opposition, count(t.".$matchFormatLower."Id) as numInn, avg(a.battingAdjWS) as avgBattingWS, avg(a.bowlingAdjWS) as avgBowlingWS, avg(a.fieldingAdjWS) as avgFieldingWS, avg(a.totalAdjWS) as avgRtg from winShares".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter group by opposition $resultQualFilter order by $sortByFilter";
	} else {
	    $sql = "select a.playerId, a.player, a.battingAdjWS as avgBattingWS, a.bowlingAdjWS as avgBowlingWS, a.fieldingAdjWS as avgFieldingWS, a.totalAdjWS as avgRtg, ".$countryTeams.", t.team1, t.team2, t.ground, t.startDate, t.".$matchFormatLower."Id from winShares".$matchFormat."Match a, ".$matchFormatLower."Info t, playerInfo p, details".$matchFormat."Innings d where a.".$matchFormatLower."Id=t.".$matchFormatLower."Id and t.".$matchFormatLower."Id=d.".$matchFormatLower."Id and p.playerId=a.playerId and t.startDate>$startDate and t.startDate<$endDate $playerFilter $leagueFilter $teamFilter $oppFilter $matchTypeFilter $winLossFilter $homeAwayFilter $hostFilter  $batFieldFirstFilter $groundFilter $inningsFilter $resultQualFilter order by $sortByFilter limit 5000";
	}
    }
    
    //echo $sql;
    echo $filterText;
    echo "</li>";
    echo "</ul>";
    echo "</div>";
    echo "<div class=\"col-lg-1\">";
    echo "</div>";
    echo "<div class=\"col-lg-5\">";
    echo "<ul class=\"list-group\">";
    echo "<li class=\"list-group-item\">";
    if ($disc == "Batting") {	    
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	    $histVals = array("Average"=>"average", "Runs"=>"runs", "Strike Rate"=>"strikeRate", "Rating"=>"rating", "Innings"=>"innings");	    
	} else {
	    $histVals = array("Runs"=>"runs", "Balls"=>"balls", "Strike Rate"=>"strikeRate", "Rating"=>"rating");	    
	}			    
    } else if ($disc == "Bowling") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	    $histVals = array("Average"=>"average", "Runs"=>"runs", "Strike Rate"=>"strikeRate", "Balls"=>"balls", "Wickets"=>"wickets", "Econ Rate"=>"econRate", "Rating"=>"rating", "Innings"=>"innings");
	} else {
	    $histVals = array("Wickets"=>"wickets", "Runs"=>"runs", "Balls"=>"balls", "Rating"=>"rating");
	}
    } else if ($disc == "All-Round") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {	    
	    $histVals = array("Batting Average"=>"battingAverage", "Bowling Average"=>"bowlingAverage", "Runs"=>"runs", "Wickets"=>"wickets", "Rating"=>"rating", "Matches"=>"matches");
	} else {
	    $histVals = array("Rating"=>"rating", "Runs"=>"runs", "Wickets"=>"wickets");
	}	
    } else if ($disc == "Fielding") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {	    
	    $histVals = array("Drop Rate"=>"dropRate", "Catches"=>"catches", "Dropped Catches"=>"droppedCatches", "Great Catches"=>"greatCatches", "Direct Hits"=>"directHits", "Runs Saved"=>"runsSaved", "Rating"=>"rating", "Innings"=>"innings");
	} else {
	    $histVals = array("Catches"=>"catches", "Dropped Catches"=>"droppedCatches", "Great Catches"=>"greatCatches", "Direct Hits"=>"directHits", "Runs Saved"=>"runsSaved", "Rating"=>"rating");
	}	
    } else if ($disc == "Win Shares") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {	    
	    $histVals = array("Total WSAvg"=>"totalWSAvg", "Batting WSAvg"=>"battingWSAvg", "Bowling WSAvg"=>"bowlingWSAvg", "Fielding WSAvg"=>"fieldingWSAvg", "Innings"=>"innings");
	} else {
	    $histVals = array("Total WS"=>"totalWS", "Batting WS"=>"battingWS", "Bowling WS"=>"bowlingWS", "Fielding WS"=>"fieldingWS");
	}	
    }

    echo "<div class=\"chart\">";
    echo "<div id=\"chart\"></div>";
    echo "</div>";
    
    echo "<form class=\"form-inline\" role=\"form\" name=\"chartFormH\" method=\"get\" action=\"cricinsight.php\">";	
    echo "<div class=\"form-group\">";
    echo "<select class=\"form-control\" name=\"histVal\" onChange=\"chartFormsH()\">";
    if (isset($_GET['histVal'])) {
	$histVal = $_GET['histVal'];
	foreach (array_keys($histVals) as $h) {
	    if ($histVal == $histVals[$h]) {
		echo "<option selected=\"selected\" value=\"$histVals[$h]\">$h</option>";   		
	    } else {
		echo "<option value=\"$histVals[$h]\">$h</option>";
	    }
	}  	
    } else {
	$count = 0;
	foreach (array_keys($histVals) as $h) {
	    if ($count == 0) {
		echo "<option selected=\"selected\" value=\"$histVals[$h]\">$h</option>";
		$histVal = $histVals[$h];
	    } else {
		echo "<option value=\"$histVals[$h]\">$h</option>";
	    }
	    $count = $count + 1;
	} 	
    }
    echo "</select>";
    echo "</div>";
    echo "<input type=\"hidden\" name=\"matchFormat\" value=\"$matchFormat\">";
    echo "<input type=\"hidden\" name=\"disc\" value=\"$disc\">";
    echo "<input type=\"hidden\" name=\"league\" value=\"$league\">";
    echo "<input type=\"hidden\" name=\"player\" value=\"$player\">";
    echo "<input type=\"hidden\" name=\"homeAway\" value=\"$homeAway\">";
    echo "<input type=\"hidden\" name=\"batFieldFirst\" value=\"$batFieldFirst\">";    
    echo "<input type=\"hidden\" name=\"ground\" value=\"$ground\">";
    echo "<input type=\"hidden\" name=\"groupBy\" value=\"$groupBy\">";
    echo "<input type=\"hidden\" name=\"matchType\" value=\"$matchType\">";
    echo "<input type=\"hidden\" name=\"startDate\" value=\"$startDate\">";
    echo "<input type=\"hidden\" name=\"endDate\" value=\"$endDate\">";
    echo "<input type=\"hidden\" name=\"resultQual\" value=\"$resultQual\">";
    echo "<input type=\"hidden\" name=\"resultQualFrom\" value=\"$resultQualFrom\">";
    echo "<input type=\"hidden\" name=\"resultQualTo\" value=\"$resultQualTo\">";
    if(isset($_GET['teams'])) {
	foreach($_GET['teams'] as $team) {
	    echo "<input type=\"hidden\" name=\"teams[]\" value=\"$team\">";
	}
    }
    if(isset($_GET['oppositions'])) {
	foreach($_GET['oppositions'] as $opp) {
	    echo "<input type=\"hidden\" name=\"oppositions[]\" value=\"$opp\">";
	}
    }
    if(isset($_GET['winLoss'])) {
	foreach($_GET['winLoss'] as $winLoss) {
	    echo "<input type=\"hidden\" name=\"winLoss[]\" value=\"$winLoss\">";
	}
    }
    if(isset($_GET['innings'])) {
	foreach($_GET['innings'] as $inn) {
	    echo "<input type=\"hidden\" name=\"innings[]\" value=\"$inn\">";
	}
    }
    if(isset($_GET['hosts'])) {
	foreach($_GET['hosts'] as $host) {
	    echo "<input type=\"hidden\" name=\"hosts[]\" value=\"$host\">";
	}
    }
    echo "<input type=\"hidden\" name=\"sortBy\" value=\"$sortBy\">";
    echo "<input type=\"hidden\" name=\"xVal\" value=\"$xVal\">";
    echo "<input type=\"hidden\" name=\"yVal\" value=\"$yVal\">";
    echo "<input type=\"hidden\" name=\"Submit\" value=\"submit\">";
    echo "</form>";
    echo "</li>";
    echo "</ul>";
    echo "</div>";
    echo "</div>";
    
    $result = $db->query($sql);
    if (!$result) die("Cannot execute query.");
           
    echo "<div class=\"row\">";
    echo "<div class=\"col-lg-7\">";
    echo "<ul class=\"list-group\">";
    echo "<li class=\"list-group-item\">";
    echo "<table class=\"table table-hover table-condensed\" id=\"ratingsTable\">";
    echo "<thead><tr>";
    echo "<th>Rank</th>";        
    
    if ($disc == "Fielding") {
	if ($groupBy == "Player") {
	    echo "<th>Player</th>";
	    if ($matchFormat != "FT20") {
		echo "<th>Team</th>";   
	    }	
	    echo "<th>Inns</th>";
	    echo "<th>Cat</th>";
	    echo "<th>Drops</th>";
	    echo "<th>Drop%</th>";
	    echo "<th>GrtCat</th>";
	    echo "<th>DirHits</th>";
	    echo "<th>Runs</th>";
	    echo "<th>AvgInnRtg</th>"; 
	} else if ($groupBy == "Ground") {
	    echo "<th>Ground</th>";
	    if ($matchFormat != "FT20") {
		echo "<th>Location</th>";   
	    }	
	    echo "<th>Inns</th>";
	    echo "<th>Cat</th>";
	    echo "<th>Drops</th>";
	    echo "<th>Drop%</th>";
	    echo "<th>GrtCat</th>";
	    echo "<th>DirHits</th>";
	    echo "<th>Runs</th>";
	    echo "<th>AvgInnRtg</th>"; 
	} else if ($groupBy == "Opposition") {
	    echo "<th>Opposition</th>";
	    echo "<th>Flag</th>";
	    echo "<th>Inns</th>";
	    echo "<th>Cat</th>";
	    echo "<th>Drops</th>";
	    echo "<th>Drop%</th>";
	    echo "<th>GrtCat</th>";
	    echo "<th>DirHits</th>";
	    echo "<th>Runs</th>";
	    echo "<th>AvgInnRtg</th>"; 
	} else {
	    echo "<th>Player</th>";
	    echo "<th>Cat</th>";
	    echo "<th>Drops</th>";
	    echo "<th>GrtCat</th>";
	    echo "<th>DirHits</th>";
	    echo "<th>Runs</th>";
	    echo "<th>InnRtg</th>";   
	    echo "<th>Team</th>";
	    echo "<th>Vs</th>";
	    echo "<th>Ground</th>";
	    echo "<th>Date</th>";	    
	    echo "<th>Scorecard</th>";	    
	}
    } else if ($disc == "Win Shares") {
	if ($groupBy == "Player") {
	    echo "<th>Player</th>";
	    if ($matchFormat != "FT20") {
		echo "<th>Team</th>";   
	    }	
	    echo "<th>Inns</th>";
	    echo "<th>BatAvg</th>";
	    echo "<th>BowlAvg</th>";
	    echo "<th>FieldAvg</th>";	
	    echo "<th>TotalAvg</th>";
	} else if ($groupBy == "Ground") {
	    echo "<th>Ground</th>";
	    if ($matchFormat != "FT20") {
		echo "<th>Location</th>";   
	    }	
	    echo "<th>Inns</th>";
	    echo "<th>BatAvg</th>";
	    echo "<th>BowlAvg</th>";
	    echo "<th>FieldAvg</th>";	
	    echo "<th>TotalAvg</th>";
	} else if ($groupBy == "Opposition") {
	    echo "<th>Opposition</th>";
	    echo "<th>Flag</th>";
	    echo "<th>Inns</th>";
	    echo "<th>BatAvg</th>";
	    echo "<th>BowlAvg</th>";
	    echo "<th>FieldAvg</th>";	
	    echo "<th>TotalAvg</th>";
	} else {
	    echo "<th>Player</th>";
	    echo "<th>Bat</th>";
	    echo "<th>Bowl</th>";
	    echo "<th>Field</th>";	
	    echo "<th>Total</th>";
	    echo "<th>Team</th>";
	    echo "<th>Vs</th>";
	    echo "<th>Ground</th>";
	    echo "<th>Date</th>";	    
	    echo "<th>Scorecard</th>";	    
	}
    } else if ($disc == "Batting") {
	if ($groupBy == "Player") {
	    echo "<th>Player</th>";
	    if ($matchFormat != "FT20") {
		echo "<th>Team</th>";   
	    }	
	    echo "<th>Inns</th>";
	    echo "<th>NO</th>";
	    echo "<th>Runs</th>";
	    echo "<th>Ave</th>";
	    echo "<th>SR</th>";
	    echo "<th>AvgInnRtg</th>"; 
	} else if ($groupBy == "Ground") {
	    echo "<th>Ground</th>";
	    if ($matchFormat != "FT20") {
		echo "<th>Location</th>";   
	    }
	    echo "<th>Inns</th>";
	    echo "<th>NO</th>";
	    echo "<th>Runs</th>";
	    echo "<th>Ave</th>";
	    echo "<th>SR</th>";
	    echo "<th>AvgInnRtg</th>"; 
	} else if ($groupBy == "Opposition") {
	    echo "<th>Opposition</th>";
	    echo "<th>Flag</th>";   
	    echo "<th>Inns</th>";
	    echo "<th>NO</th>";
	    echo "<th>Runs</th>";
	    echo "<th>Ave</th>";
	    echo "<th>SR</th>";
	    echo "<th>AvgInnRtg</th>"; 
	} else {
	    echo "<th>Player</th>";
	    echo "<th>Runs</th>";
	    echo "<th>Balls</th>";
	    echo "<th>SR</th>";
	    echo "<th>InnRtg</th>";   
	    echo "<th>Team</th>";
	    echo "<th>Vs</th>";
	    echo "<th>Ground</th>";
	    echo "<th>Date</th>";	    
	    echo "<th>Scorecard</th>";	    
	}
    } else if ($disc == "Bowling") {
	if ($groupBy == "Player") {
	    echo "<th>Player</th>";
	    if ($matchFormat != "FT20") {
		echo "<th>Team</th>";   
	    }
	    echo "<th>Inns</th>";
	    echo "<th>Balls</th>";
	    echo "<th>Runs</th>";
	    echo "<th>Wkts</th>";
	    echo "<th>Ave</th>";
	    echo "<th>Econ</th>";
	    echo "<th>SR</th>";
	    echo "<th>AvgInnRtg</th>"; 
	} else if ($groupBy == "Ground") {
	    echo "<th>Ground</th>";
	    if ($matchFormat != "FT20") {
		echo "<th>Location</th>";   
	    }
	    echo "<th>Inns</th>";
	    echo "<th>Balls</th>";
	    echo "<th>Runs</th>";
	    echo "<th>Wkts</th>";
	    echo "<th>Ave</th>";
	    echo "<th>Econ</th>";
	    echo "<th>SR</th>";
	    echo "<th>AvgInnRtg</th>"; 
	} else if ($groupBy == "Opposition") {
	    echo "<th>Opposition</th>";
	    echo "<th>Flag</th>";   
	    echo "<th>Inns</th>";
	    echo "<th>Balls</th>";
	    echo "<th>Runs</th>";
	    echo "<th>Wkts</th>";
	    echo "<th>Ave</th>";
	    echo "<th>Econ</th>";
	    echo "<th>SR</th>";
	    echo "<th>AvgInnRtg</th>"; 
	} else {
	    echo "<th>Player</th>";
	    echo "<th>Overs</th>";
	    echo "<th>Runs</th>";
	    echo "<th>Wkts</th>";
	    echo "<th>Econ</th>";
	    echo "<th>InnRtg</th>";   
	    echo "<th>Team</th>";
	    echo "<th>Vs</th>";
	    echo "<th>Ground</th>";
	    echo "<th>Date</th>";	    
	    echo "<th>Scorecard</th>";	    
	}
    } else if ($disc == "All-Round") {
	if ($groupBy == "Player") {
	    echo "<th>Player</th>";
	    if ($matchFormat != "FT20") {
		echo "<th>Team</th>";   
	    }
	    echo "<th>Mats</th>";
	    echo "<th>Runs</th>";
	    echo "<th>BatAve</th>";
	    echo "<th>Wkts</th>";
	    echo "<th>BowlAve</th>";
	    echo "<th>AvgMatRtg</th>"; 
	} else if ($groupBy == "Ground") {
	    echo "<th>Ground</th>";
	    if ($matchFormat != "FT20") {
		echo "<th>Location</th>";   
	    }
	    echo "<th>Mats</th>";
	    echo "<th>Runs</th>";
	    echo "<th>BatAve</th>";
	    echo "<th>Wkts</th>";
	    echo "<th>BowlAve</th>";
	    echo "<th>AvgMatRtg</th>"; 
	} else if ($groupBy == "Opposition") {
	    echo "<th>Opposition</th>";
	    echo "<th>Flag</th>";   
	    echo "<th>Mats</th>";
	    echo "<th>Runs</th>";
	    echo "<th>BatAve</th>";
	    echo "<th>Wkts</th>";
	    echo "<th>BowlAve</th>";
	    echo "<th>AvgMatRtg</th>"; 
	} else {
	    echo "<th>Player</th>";
	    if ($matchFormat == "Test") {
		echo "<th>Runs1</th>";
		echo "<th>Runs2</th>";
		echo "<th>Wkts1</th>";
		echo "<th>Wkts2</th>";
	    } else {
		echo "<th>Runs</th>";
		echo "<th>Wkts</th>";
	    }
	    
	    echo "<th>MatRtg</th>";   
	    echo "<th>Team</th>";
	    echo "<th>Vs</th>";
	    echo "<th>Ground</th>";
	    echo "<th>Date</th>";	    
	    echo "<th>Scorecard</th>";	    
	}
    } 
    echo "</tr></thead>";
    
    $k = 1;
    while($res = $result->fetchArray(SQLITE3_NUM)) {	
	echo "<tr>";   
	echo "<td>$k</td>";
	if ($groupBy == "Ground" || $groupBy == "Opposition") {
	    echo "<td>".$res[0]."</td>";
	}
	for ($j = 1; $j < $result->numColumns(); $j++) {	    	    	    
	    if ($groupBy == "Player") {
		if ($j == 1) {
		    echo "<td><a href=\"player.php?playerId=".$res[0]."&matchFormat=$matchFormat&disc=$disc\">".str_replace("Sir ","",$res[$j])."</a></td>";  	    	   
		} else if ($j == 2) { # country
		    if ($matchFormat != "FT20") {
			echo "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" alt=\"$res[$j]\" border=1px/></a></td>";
		    }
		} else {
		    if ($disc == "Batting") {
			if ($j == 7) { # average
			    $numInn = $res[3];
			    $notOuts = $res[4];
			    if (($numInn - $notOuts) == 0) {
				echo "<td>-</td>";
			    } else {
				echo "<td>".number_format(round($res[$j], 2), 2)."</td>";   
			    }				
			} elseif ($j == 8) { # sr
			    if ($res[6] == 0) {
				echo "<td>-</td>";
			    } else {
				echo "<td>".number_format(round($res[$j], 2), 2)."</td>";   
			    }				
			} elseif ($j == 6) { # balls not shown
			} elseif ($j == 9) { # rating
			    echo "<td>".round($res[$j], 0)."</td>";
			} else {
			    echo "<td>$res[$j]</td>";   
			}
		    } else if ($disc == "Bowling") {
			if ($j == 4) { # wkts + ave + econ + sr
			    $balls = $res[4];
			    $runs = $res[5];
			    $wkts = $res[6];
			    echo "<td>$balls</td>";
			    echo "<td>$runs</td>";
			    echo "<td>$wkts</td>";     
			    if ($wkts == 0) {
				echo "<td>-</td>";
			    } else {
				echo "<td>".number_format(round($res[7], 2), 2)."</td>";   
			    }
			    if ($balls == 0) {
				echo "<td>-</td>";
			    } else {
				echo "<td>".number_format(round($res[8], 2), 2)."</td>";   
			    }
			    if ($wkts == 0) {
				echo "<td>-</td>";
			    } else {
				echo "<td>".number_format(round($res[9], 1), 1)."</td>";   
			    }			
			    $j = $j + 5;
			} elseif ($j == 10) { # rating
			    echo "<td>".round($res[$j], 0)."</td>";
			} else {
			    echo "<td>$res[$j]</td>";   
			}
		    } else if ($disc == "All-Round") {
			if ($j == 5 || $j == 7) { # bat/bowl average
			    echo "<td>".number_format(round($res[$j], 2), 2)."</td>";
			} elseif ($j == 8) { # rating
			    echo "<td>".round($res[$j], 0)."</td>";
			} else {
			    echo "<td>$res[$j]</td>";   
			}
		    } else if ($disc == "Fielding") {
			if ($j == 6) { # drop rate %
			    echo "<td>".number_format(round($res[$j] * 100, 2), 2)."</td>";
			} elseif ($j == 10) { # rating
			    echo "<td>".round($res[$j], 0)."</td>";
			} else {
			    echo "<td>$res[$j]</td>";   
			}
		    } else if ($disc == "Win Shares") {
			if ($j == 4 || $j == 5 || $j == 6 || $j == 7) { # win shares
			    echo "<td>".round($res[$j], 3)."</td>";
			} else {
			    echo "<td>$res[$j]</td>";   
			}
		    }
		}
	    } else if ($groupBy == "Ground" || $groupBy == "Opposition") {
		if ($j == 1) { # country
		    if ($matchFormat != "FT20") {
			echo "<td><a href=\"team.php?team=".$res[$j]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j].".png\" alt=\"$res[$j]\" border=1px/></a></td>";
		    }
		} else {
		    if ($disc == "Batting") {
			if ($j == 6) { # average
			    $numInn = $res[2];
			    $notOuts = $res[3];
			    if (($numInn - $notOuts) == 0) {
				echo "<td>-</td>";
			    } else {
				echo "<td>".number_format(round($res[$j], 2), 2)."</td>";   
			    }				
			} elseif ($j == 7) { # sr
			    if ($res[5] == 0) {
				echo "<td>-</td>";
			    } else {
				echo "<td>".number_format(round($res[$j], 2), 2)."</td>";   
			    }				
			} elseif ($j == 5) { # balls not shown
			} elseif ($j == 8) { # rating
			    echo "<td>".round($res[$j], 0)."</td>";
			} else {
			    echo "<td>$res[$j]</td>";   
			}
		    } else if ($disc == "Bowling") {
			if ($j == 3) { # wkts + ave + econ + sr
			    $balls = $res[3];
			    $runs = $res[4];
			    $wkts = $res[5];
			    echo "<td>$balls</td>";
			    echo "<td>$runs</td>";
			    echo "<td>$wkts</td>";     
			    if ($wkts == 0) {
				echo "<td>-</td>";
			    } else {
				echo "<td>".number_format(round($res[6], 2), 2)."</td>";   
			    }
			    if ($balls == 0) {
				echo "<td>-</td>";
			    } else {
				echo "<td>".number_format(round($res[7], 2), 2)."</td>";   
			    }
			    if ($wkts == 0) {
				echo "<td>-</td>";
			    } else {
				echo "<td>".number_format(round($res[8], 1), 1)."</td>";   
			    }			
			    $j = $j + 5;
			} elseif ($j == 9) { # rating
			    echo "<td>".round($res[$j], 0)."</td>";
			} else {
			    echo "<td>$res[$j]</td>";   
			}
		    } else if ($disc == "All-Round") {
			if ($j == 4 || $j == 6) { # bat/bowl average
			    echo "<td>".number_format(round($res[$j], 2), 2)."</td>";
			} elseif ($j == 7) { # rating
			    echo "<td>".round($res[$j], 0)."</td>";
			} else {
			    echo "<td>$res[$j]</td>";   
			}
		    } else if ($disc == "Fielding") {
			if ($j == 5) { # drop rate %
			    echo "<td>".number_format(round($res[$j] * 100, 2), 2)."</td>";
			} elseif ($j == 9) { # rating
			    echo "<td>".round($res[$j], 0)."</td>";
			} else {
			    echo "<td>$res[$j]</td>";   
			}
		    } else if ($disc == "Win Shares") {
			if ($j == 3 || $j == 4 || $j == 5 || $j == 6) { # win shares
			    echo "<td>".round($res[$j], 3)."</td>";
			} else {
			    echo "<td>$res[$j]</td>";   
			}
		    }
		}
	    } else {
		if ($j == 1) {
		    echo "<td><a href=\"player.php?playerId=".$res[0]."&matchFormat=$matchFormat&disc=$disc\">".str_replace("Sir ","",$res[$j])."</a></td>";  	    	   
		} else {
		    if ($disc == "Batting") {
			if ($j == 2) { # runs + sr
			    $no = $res[$j];
			    $runs = $res[$j+1];
			    $balls = $res[$j+2];
			    if ($no == 1) {
				echo "<td>".$runs."*</td>";                        
			    } else {
				echo  "<td>".$runs."&nbsp;</td>";
			    }
			    echo  "<td>".$balls."</td>";
			    $j = $j + 2; 
			 } elseif ($j == 5) { # sr
			    echo "<td>".number_format(round($res[$j], 2), 2)."</td>";
			 } elseif ($j == 6) { # rating
			    echo "<td>".round($res[$j], 0)."</td>";
			 }  elseif ($j == 7) { # team and opposition
			    if ($matchFormat == "FT20") {
			       if (strrpos($res[$j], $res[$j+1]) === false) {
				  echo "<td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\">".$res[$j+2]."</a></td><td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";		
			       } else {
				  echo "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td><td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\">".$res[$j+2]."</a></td>";
			       }  
			    } else {
			       if ($res[$j] == $res[$j+1]) {
				  echo "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td><td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+2].".png\" border=1px/></a></td>";
			       } else {
				  echo "<td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+2].".png\" border=1px/></a></td><td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td>";
			       }
			    }		     		  		    
			    $j = $j + 2;
			 } elseif ($j == 11) { # match date
			    echo "<td>".substr($res[$j], 0, 4)."-".substr($res[$j], 4, 2)."-".substr($res[$j], 6, 2)."</td>";
			 } elseif ($j == 12) { # scorecard link
			    echo "<td><a href=\"scorecard.php?matchFormat=$matchFormat&matchId=".$res[$j]."\">$matchFormat #".$res[$j]."</a></td>";
			 } else {
			    echo "<td>$res[$j]</td>";
			 }    
		    } else if ($disc == "Bowling") {
			if ($j == 2) { # overs
			    if ($matchFormat == "Test") {
			       $bpo = $res[12];
			    } else {
			       $bpo = 6;
			    }		     
			    $balls = $res[$j] % $bpo;
			    $overs = ($res[$j]-$balls) / $bpo;
			    if ($bpo == 6) {
				echo "<td>".$overs.".".$balls."</td>";
			    } else {
				echo "<td>".$overs.".".$balls."x".$bpo."</td>";
			    }
			    
			    $runs = $res[$j+1];
			    $wkts = $res[$j+2];
			    echo "<td>$runs</td>";
			    echo "<td>$wkts</td>";
			    if ($res[$j] > 0) {
				$econ = 6 * $runs / $res[$j];
				echo "<td>".number_format(round($econ, 2), 2)."</td>";
			    } else {
				echo "<td></td>";
			    }	    
			    $j = $j + 2;
			 } elseif ($j == 5) { # rating
			    echo "<td>".round($res[$j], 0)."</td>";
			 }  elseif ($j == 6) { # team and opposition
			    if ($matchFormat == "FT20") {
			       if (strrpos($res[$j], $res[$j+1]) === false) {
				  echo "<td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\">".$res[$j+2]."</a></td><td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";		
			       } else {
				  echo "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td><td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\">".$res[$j+2]."</a></td>";
			       }  
			    } else {
			       if ($res[$j] == $res[$j+1]) {
				  echo "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td><td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+2].".png\" border=1px/></a></td>";
			       } else {
				  echo "<td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+2].".png\" border=1px/></a></td><td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td>";
			       }
			    }
			    $j = $j + 2;
			 } elseif ($j == 10) { # match date
			    echo "<td>".substr($res[$j], 0, 4)."-".substr($res[$j], 4, 2)."-".substr($res[$j], 6, 2)."</td>";
			 } elseif ($j == 11) { # scorecard link
			    echo "<td><a href=\"scorecard.php?matchFormat=$matchFormat&matchId=".$res[$j]."\">$matchFormat #".$res[$j]."</a></td>";
			 }  elseif ($j == 12) { #bpo
			 } else {
			    echo "<td>$res[$j]</td>";
			 }
		    } else if ($disc == "All-Round") {
			if ($matchFormat == "Test") {
			    if ($j == 2) { # runs1 + runs2
				$runs1 = $res[$j];
				$no1 = $res[$j+1];
				$runs2 = $res[$j+2];
				$no2 = $res[$j+3];
				
				if ($no1 == 1) {
				    echo "<td>".$runs1."*</td>";                        
				} else {
				    echo  "<td>".$runs1."&nbsp;</td>";
				}
				
				if ($no2 == 1) {
				    echo "<td>".$runs2."*</td>";                        
				} else {
				    echo  "<td>".$runs2."&nbsp;</td>";
				}
				$j = $j + 3; 
			    } else if ($j == 6) { # wkts1 + wkts2
				$wkts1 = $res[$j];
				$bowlRuns1 = $res[$j+1];
				$wkts2 = $res[$j+2];
				$bowlRuns2 = $res[$j+3];
				if ($wkts1 != "" and $bowlRuns1 != "") {
				    echo "<td>".$wkts1."/".$bowlRuns1."</td>";
				} else {
				    echo "<td>-</td>";
				}
				
				if ($wkts2 != "" and $bowlRuns2 != "") {
				    echo "<td>".$wkts2."/".$bowlRuns2."</td>";
				} else {
				    echo "<td>-</td>";
				}
				$j = $j + 3;
			    } elseif ($j == 10) { # rating
				echo "<td>".round($res[$j], 0)."</td>";
			    } elseif ($j == 11) { # team and opposition
				if ($matchFormat == "FT20") {
				   if (strrpos($res[$j], $res[$j+1]) === false) {
				      echo "<td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\">".$res[$j+2]."</a></td><td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";		
				   } else {
				      echo "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td><td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\">".$res[$j+2]."</a></td>";
				   }  
				} else {
				    if ($res[$j] == $res[$j+1]) {
				       echo "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td><td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+2].".png\" border=1px/></a></td>";
				    } else {
				       echo "<td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+2].".png\" border=1px/></a></td><td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td>";
				    }
				}
				$j = $j + 2;
			    } elseif ($j == 15) { # match date
				echo "<td>".substr($res[$j], 0, 4)."-".substr($res[$j], 4, 2)."-".substr($res[$j], 6, 2)."</td>";
			    } elseif ($j == 16) { # scorecard link
				echo "<td><a href=\"scorecard.php?matchFormat=$matchFormat&matchId=".$res[$j]."\">$matchFormat #".$res[$j]."</a></td>";
			    }  elseif ($j > 16) { 
			    } else {
				echo "<td>$res[$j]</td>";
			    }
			} else {
			    if ($j == 2) { # runs
				$runs = $res[$j];
				$no = $res[$j+1];
				
				if ($no == 1) {
				    echo "<td>".$runs."*</td>";                        
				} else {
				    echo  "<td>".$runs."&nbsp;</td>";
				}
								
				$j = $j + 1; 
			    } else if ($j == 4) { # wkts
				$wkts = $res[$j];
				$bowlRuns = $res[$j+1];
				if ($wkts != "" and $bowlRuns != "") {
				    echo "<td>".$wkts."/".$bowlRuns."</td>";
				} else {
				    echo "<td>-</td>";
				}
				
				$j = $j + 1;
			    } elseif ($j == 6) { # rating
				echo "<td>".round($res[$j], 0)."</td>";
			    } elseif ($j == 7) { # team and opposition
				if ($matchFormat == "FT20") {
				   if (strrpos($res[$j], $res[$j+1]) === false) {
				      echo "<td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\">".$res[$j+2]."</a></td><td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";		
				   } else {
				      echo "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td><td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\">".$res[$j+2]."</a></td>";
				   }  
				} else {
				    if ($res[$j] == $res[$j+1]) {
				       echo "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td><td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+2].".png\" border=1px/></a></td>";
				    } else {
				       echo "<td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+2].".png\" border=1px/></a></td><td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td>";
				    }
				}
				$j = $j + 2;
			    } elseif ($j == 11) { # match date
				echo "<td>".substr($res[$j], 0, 4)."-".substr($res[$j], 4, 2)."-".substr($res[$j], 6, 2)."</td>";
			    } elseif ($j == 12) { # scorecard link
				echo "<td><a href=\"scorecard.php?matchFormat=$matchFormat&matchId=".$res[$j]."\">$matchFormat #".$res[$j]."</a></td>";
			    } else {
				echo "<td>$res[$j]</td>";
			    }
			}
		    } else if ($disc == "Fielding") {
			if ($j == 7) { # rating
			    echo "<td>".round($res[$j], 0)."</td>";
			}  elseif ($j == 8) { # team and opposition
			   if ($matchFormat == "FT20") {
			      if (strrpos($res[$j], $res[$j+1]) === false) {
				 echo "<td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\">".$res[$j+2]."</a></td><td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";		
			      } else {
				 echo "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td><td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\">".$res[$j+2]."</a></td>";
			      }  
			   } else {
			      if ($res[$j] == $res[$j+1]) {
				 echo "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td><td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+2].".png\" border=1px/></a></td>";
			      } else {
				 echo "<td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+2].".png\" border=1px/></a></td><td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td>";
			      }
			   }		     		  		    
			   $j = $j + 2;
			} elseif ($j == 12) { # match date
			   echo "<td>".substr($res[$j], 0, 4)."-".substr($res[$j], 4, 2)."-".substr($res[$j], 6, 2)."</td>";
			} elseif ($j == 13) { # scorecard link
			   echo "<td><a href=\"scorecard.php?matchFormat=$matchFormat&matchId=".$res[$j]."\">$matchFormat #".$res[$j]."</a></td>";
			} else {
			   echo "<td>$res[$j]</td>";
			}    
		    } else if ($disc == "Win Shares") {
			if ($j == 2 || $j == 3 || $j == 4 || $j == 5) { # win shares
			    echo "<td>".round($res[$j], 3)."</td>";
			}  elseif ($j == 6) { # team and opposition
			   if ($matchFormat == "FT20") {
			      if (strrpos($res[$j], $res[$j+1]) === false) {
				 echo "<td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\">".$res[$j+2]."</a></td><td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td>";		
			      } else {
				 echo "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\">".$res[$j+1]."</a></td><td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\">".$res[$j+2]."</a></td>";
			      }  
			   } else {
			      if ($res[$j] == $res[$j+1]) {
				 echo "<td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td><td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+2].".png\" border=1px/></a></td>";
			      } else {
				 echo "<td><a href=\"team.php?team=".$res[$j+2]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+2].".png\" border=1px/></a></td><td><a href=\"team.php?team=".$res[$j+1]."&matchFormat=$matchFormat\"><img src=\"images/".$res[$j+1].".png\" border=1px/></a></td>";
			      }
			   }		     		  		    
			   $j = $j + 2;
			} elseif ($j == 10) { # match date
			   echo "<td>".substr($res[$j], 0, 4)."-".substr($res[$j], 4, 2)."-".substr($res[$j], 6, 2)."</td>";
			} elseif ($j == 11) { # scorecard link
			   echo "<td><a href=\"scorecard.php?matchFormat=$matchFormat&matchId=".$res[$j]."\">$matchFormat #".$res[$j]."</a></td>";
			} else {
			   echo "<td>$res[$j]</td>";
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
    echo "<div class=\"col-lg-5\">";     
    echo "<ul class=\"list-group\">";
    echo "<li class=\"list-group-item\">";
    
    if ($disc == "Batting") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	    $xVals = array("Average"=>"average", "Runs"=>"runs", "Strike Rate"=>"strikeRate", "Rating"=>"rating", "Innings"=>"innings");
	    $yVals = array("Strike Rate"=>"strikeRate", "Average"=>"average", "Runs"=>"runs", "Rating"=>"rating", "Innings"=>"innings");   
	} else {
	    $xVals = array("Runs"=>"runs", "Strike Rate"=>"strikeRate", "Balls"=>"balls", "Rating"=>"rating");
	    $yVals = array("Strike Rate"=>"strikeRate", "Runs"=>"runs", "Balls"=>"balls", "Rating"=>"rating");    
	}	
    } else if ($disc == "Bowling") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {	    
	    $xVals = array("Average"=>"average", "Strike Rate"=>"strikeRate", "Wickets"=>"wickets", "Runs"=>"runs", "Balls"=>"balls", "Econ Rate"=>"econRate", "Rating"=>"rating", "Innings"=>"innings");
	    $yVals = array("Strike Rate"=>"strikeRate", "Average"=>"average", "Wickets"=>"wickets", "Runs"=>"runs", "Balls"=>"balls", "Econ Rate"=>"econRate", "Rating"=>"rating", "Innings"=>"innings");
	} else {
	    $xVals = array("Wickets"=>"wickets", "Runs"=>"runs", "Balls"=>"balls", "Rating"=>"rating");
	    $yVals = array("Runs"=>"runs", "Wickets"=>"wickets", "Balls"=>"balls", "Rating"=>"rating"); 
	}
    } else if ($disc == "All-Round") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {	    
	    $xVals = array("Batting Average"=>"battingAverage", "Bowling Average"=>"bowlingAverage", "Runs"=>"runs", "Wickets"=>"wickets", "Rating"=>"rating", "Matches"=>"matches");
	    $yVals = array("Bowling Average"=>"bowlingAverage", "Batting Average"=>"battingAverage", "Runs"=>"runs", "Wickets"=>"wickets", "Rating"=>"rating", "Matches"=>"matches");
	} else {
	    $xVals = array("Runs"=>"runs", "Wickets"=>"wickets", "Rating"=>"rating");
	    $yVals = array("Wickets"=>"wickets", "Runs"=>"runs", "Rating"=>"rating"); 
	}	
    } else if ($disc == "Fielding") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {	    
	    $xVals = array("Catches"=>"catches", "Dropped Catches"=>"droppedCatches", "Drop Rate"=>"dropRate", "Great Catches"=>"greatCatches", "Direct Hits"=>"directHits", "Runs Saved"=>"runsSaved", "Rating"=>"rating", "Innings"=>"innings");
	    $yVals = array("Dropped Catches"=>"droppedCatches", "Catches"=>"catches", "Drop Rate"=>"dropRate", "Great Catches"=>"greatCatches", "Direct Hits"=>"directHits", "Runs Saved"=>"runsSaved", "Rating"=>"rating", "Innings"=>"innings");	
	} else {
	    $xVals = array("Catches"=>"catches", "Dropped Catches"=>"droppedCatches", "Great Catches"=>"greatCatches", "Direct Hits"=>"directHits", "Runs Saved"=>"runsSaved", "Rating"=>"rating");
	    $yVals = array("Dropped Catches"=>"droppedCatches", "Catches"=>"catches", "Great Catches"=>"greatCatches", "Direct Hits"=>"directHits", "Runs Saved"=>"runsSaved", "Rating"=>"rating");
	}	
    } else if ($disc == "Win Shares") {
	if ($groupBy == "Player" || $groupBy == "Ground" || $groupBy == "Opposition") {
	    $xVals = array("Batting WSAvg"=>"battingWSAvg", "Bowling WSAvg"=>"bowlingWSAvg", "Total WSAvg"=>"totalWSAvg", "Fielding WSAvg"=>"fieldingWSAvg", "Innings"=>"innings");
	    $yVals = array("Bowling WSAvg"=>"bowlingWSAvg", "Batting WSAvg"=>"battingWSAvg", "Total WSAvg"=>"totalWSAvg", "Fielding WSAvg"=>"fieldingWSAvg", "Innings"=>"innings");
	} else {
	    $xVals = array("Batting WS"=>"battingWS", "Bowling WS"=>"bowlingWS", "Total WS"=>"totalWS", "Fielding WS"=>"fieldingWS");
	    $yVals = array("Bowling WS"=>"bowlingWS", "Batting WS"=>"battingWS", "Total WS"=>"totalWS", "Fielding WS"=>"fieldingWS");
	}	
    }

    echo "<form class=\"form-inline\" role=\"form\" name=\"chartForm\" method=\"get\" action=\"cricinsight.php\">";	
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
    echo "<div id=\"chartB\"></div>";
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
    echo "<input type=\"hidden\" name=\"league\" value=\"$league\">";
    echo "<input type=\"hidden\" name=\"player\" value=\"$player\">";
    echo "<input type=\"hidden\" name=\"homeAway\" value=\"$homeAway\">";
    echo "<input type=\"hidden\" name=\"batFieldFirst\" value=\"$batFieldFirst\">";
    echo "<input type=\"hidden\" name=\"ground\" value=\"$ground\">";
    echo "<input type=\"hidden\" name=\"groupBy\" value=\"$groupBy\">";
    echo "<input type=\"hidden\" name=\"matchType\" value=\"$matchType\">";
    echo "<input type=\"hidden\" name=\"startDate\" value=\"$startDate\">";
    echo "<input type=\"hidden\" name=\"endDate\" value=\"$endDate\">";
    echo "<input type=\"hidden\" name=\"resultQual\" value=\"$resultQual\">";
    echo "<input type=\"hidden\" name=\"resultQualFrom\" value=\"$resultQualFrom\">";
    echo "<input type=\"hidden\" name=\"resultQualTo\" value=\"$resultQualTo\">";
    if(isset($_GET['teams'])) {
	foreach($_GET['teams'] as $team) {
	    echo "<input type=\"hidden\" name=\"teams[]\" value=\"$team\">";
	}
    }
    if(isset($_GET['oppositions'])) {
	foreach($_GET['oppositions'] as $opp) {
	    echo "<input type=\"hidden\" name=\"oppositions[]\" value=\"$opp\">";
	}
    }
    if(isset($_GET['winLoss'])) {
	foreach($_GET['winLoss'] as $winLoss) {
	    echo "<input type=\"hidden\" name=\"winLoss[]\" value=\"$winLoss\">";
	}
    }
    if(isset($_GET['innings'])) {
	foreach($_GET['innings'] as $inn) {
	    echo "<input type=\"hidden\" name=\"innings[]\" value=\"$inn\">";
	}
    }
    if(isset($_GET['hosts'])) {
	foreach($_GET['hosts'] as $host) {
	    echo "<input type=\"hidden\" name=\"hosts[]\" value=\"$host\">";
	}
    }
    echo "<input type=\"hidden\" name=\"sortBy\" value=\"$sortBy\">";
    echo "<input type=\"hidden\" name=\"histVal\" value=\"$histVal\">";
    echo "<input type=\"hidden\" name=\"Submit\" value=\"submit\">";
    echo "</form>";
    echo "</li>";
    echo "</ul>";
    echo "</div>";    
    echo "</div>";
    echo "</div>";
}
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