<!DOCTYPE html>
<?php
session_start();
if(isset($_GET['matchFormat'])) {
   $matchFormat = $_GET['matchFormat'];
} else {
   $matchFormat = "ODI";
}
if(isset($_GET['inn'])) {
   $inn = $_GET['inn'];
} else {
   $inn = 2;
}
if(isset($_GET['runs'])) {
   $runs = $_GET['runs'];
} else {
  $runs = 80;
}
if(isset($_GET['overs'])) {
   $overs = $_GET['overs'];
} else {
  $overs = 10;
}
if(isset($_GET['wkts'])) {
   $wkts = $_GET['wkts'];
} else {
  $wkts = 4;
}
if(isset($_GET['battingTeam'])) {
   $battingTeam = $_GET['battingTeam'];
} else {
   $battingTeam = "Not Set";
}
if(isset($_GET['bowlingTeam'])) {
   $bowlingTeam = $_GET['bowlingTeam'];
} else {
   $bowlingTeam = "Not Set";
}
if(isset($_GET['startDate'])) {
   $startDate = $_GET['startDate'];
} else {
  if ($matchFormat == "T20") {
    $startDate = "20050101";
  } else {
    $startDate = "19710101";
  }
}
if(isset($_GET['endDate'])) {
   $endDate = $_GET['endDate'];
} else {
   $endDate = "20991231";
}

if(isset($_SESSION['screen_width']) AND isset($_SESSION['screen_height'])){
} else if(isset($_REQUEST['width']) AND isset($_REQUEST['height'])) {
    $_SESSION['screen_width'] = $_REQUEST['width'];
    $_SESSION['screen_height'] = $_REQUEST['height'];

    header("Location: cricodds.php?matchFormat=".$matchFormat."&inn=".$inn."&runs=".$runs."&overs=".$overs."&wkts=".$wkts."&startDate=".$startDate."&endDate=".$endDate."&battingTeam=".$battingTeam."&bowlingTeam=".$bowlingTeam);
} else {
    echo '<script type="text/javascript">window.location = "' . $_SERVER['PHP_SELF'] . '?matchFormat='.$matchFormat.'&inn='.$inn.'&runs='.$runs.'&overs='.$overs.'&wkts='.$wkts.'&startDate='.$startDate.'&endDate='.$endDate.'&battingTeam='.$battingTeam.'&bowlingTeam='.$bowlingTeam.'&width="+screen.width+"&height="+screen.height;</script>';
}

?>
<html>
<head>
    <title>cricrate | cricodds</title>
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
       "bFilter":   false,
       "pageLength": 10,
       "order": [[ 0, "desc" ]],
    } );
    } );

    submitForms = function(){
      window.document.selectForm.submit();
    }

    function enterSubmit(ele) {
      if(event.keyCode == 13) {
        window.document.selectForm.submit();
      }
    }

    var isMobile = false; //initiate as false
    // device detection
    if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent)
    || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))) isMobile = true;

    var matchFormat = <?php echo json_encode($matchFormat); ?>;

    var chartWidth = screen.width * 0.375;
    // if (matchFormat == "T20") {
    //   chartWidth = screen.width * 0.45;
    // }
    var chartHeight = screen.height * 0.2;
    var chartHeightB = screen.height * 0.4;

    if (isMobile == true) {
	     chartWidth = chartWidth * 2;
    }

    var inn = <?php echo json_encode($inn); ?>;
    var runs = <?php echo json_encode($runs); ?>;
    var overs = <?php echo json_encode($overs); ?>;
    var wkts = <?php echo json_encode($wkts); ?>;
    var startDate = <?php echo json_encode($startDate); ?>;
    var endDate = <?php echo json_encode($endDate); ?>;
    var hAxis = "Run Rate";
    if (inn == 2) {
        hAxis = "Required Run Rate"
    }
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChartStacked);
    google.charts.setOnLoadCallback(drawChartBubble);

    function drawChartStacked() {
      var jsonData = $.ajax({
       url: "charts/cricoddsColumn.php?matchFormat="+matchFormat+"&inn="+inn+"&runs="+runs+"&overs="+overs+"&wkts="+wkts+"&startDate="+startDate+"&endDate="+endDate,
       dataType:"json",
       async: false
       }).responseText;

      // Create our data table out of JSON data loaded from server.
      var data = new google.visualization.DataTable(jsonData);

      var showEvery = parseInt(data.getNumberOfRows() / 25);
    	var options = {
    	    fontName: "Lucida Sans Unicode",
          // isStacked: true,
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
    	    colors: ['#2c518d','#ff3232'],
    	    width: chartWidth,
    	    height: chartHeight,
    	    hAxis: {
            showTextEvery: showEvery,
    		    title: hAxis,
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
    	    bar: {
               gap: 0,
               groupWidth: '100%'
             },
          legend: 'none',
    	    animation: {
    			"startup": true,
    			duration: 1000,
    			easing: 'inAndOut',
    			},
            };

           var chart = new google.visualization.ColumnChart(document.getElementById('chart'));
           chart.draw(data, options);
        }

        function drawChartBubble() {
           var jsonData = $.ajax({
         url: "charts/cricoddsBubble.php?matchFormat="+matchFormat+"&inn="+inn+"&runs="+runs+"&overs="+overs+"&wkts="+wkts+"&startDate="+startDate+"&endDate="+endDate,
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
    	    height: chartHeightB,
          colors: ['#2c518d','#ff3232','#FFA500'],
    	   hAxis: {
    		   title: "Match #",
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
    		   title: hAxis,
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
                    <li class="active"><a href="cricodds.php" ><b>cricodds <span class="label label-warning">new</span><span class="sr-only">(current)</span></b></a></li>
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
if ($matchFormat == "ODI") {
  echo "<div class=\"col-lg-7\">";
} else {
  echo "<div class=\"col-lg-7\">";
}
echo "<ul class=\"list-group\">";
echo "<li class=\"list-group-item\">";
echo "<h4>Current Match Scenario</h4>";
echo "<form class=\"form-inline\" role=\"form\" name=\"selectForm\" method=\"get\" action=\"cricodds.php\">";
echo "<div class=\"form-group\">";
echo "&nbsp;&nbsp;&nbsp;&nbsp;<b>Match format:</b>&nbsp;&nbsp;";
echo "<select class=\"form-control\" name=\"matchFormat\" onChange=\"submitForms()\">";
$matchFormats = array("ODI", "T20");
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
echo "&nbsp;&nbsp;&nbsp;&nbsp;<b>Innings:</b>&nbsp;&nbsp;";
echo "<select class=\"form-control\" name=\"inn\" onChange=\"submitForms()\">";
$inns = array(1, 2);
if(isset($_GET['inn'])) {
  $inn = $_GET['inn'];
  foreach ($inns as $i) {
    if ($inn == $i) {
        echo "<option selected=\"selected\" value=\"$i\">$i</option>";
    } else {
        echo "<option value=\"$i\">$i</option>";
    }
  }
} else {
  $count = 0;
  foreach ($inns as $i) {
    if ($count == 0) {
        echo "<option selected=\"selected\" value=\"$i\">$i</option>";
        $inn = $i;
    } else {
        echo "<option value=\"$i\">$i</option>";
    }
  $count = $count + 1;
  }
}
echo "</select>";
echo "</div>";

if ($inn == 1) {
  echo "&nbsp;&nbsp;&nbsp;&nbsp;<b>Runs:</b> <input type=\"text\"  class=\"form-control\" size=\"5\" onkeypress='return event.charCode >= 48 && event.charCode <= 57' name=\"runs\" value=".$runs." onChange=\"submitForms()\" onKeyDown=\"enterSubmit(this)\">&nbsp;&nbsp;";
  echo "&nbsp;&nbsp;&nbsp;&nbsp;<b>Overs</b>: <input type=\"text\" class=\"form-control\" size=\"5\" onkeypress='return event.charCode >= 48 && event.charCode <= 57' name=\"overs\" value=".$overs." onChange=\"submitForms()\" onKeyDown=\"enterSubmit(this)\">&nbsp;&nbsp;";
} else {
  echo "&nbsp;&nbsp;&nbsp;&nbsp;<b>Runs Required</b>: <input type=\"text\"  class=\"form-control\" size=\"5\" onkeypress='return event.charCode >= 48 && event.charCode <= 57' name=\"runs\" value=".$runs." onChange=\"submitForms()\" onKeyDown=\"enterSubmit(this)\">&nbsp;&nbsp;";
  echo "&nbsp;&nbsp;&nbsp;&nbsp;<b>Overs Remaining</b>: <input type=\"text\" class=\"form-control\" size=\"5\" onkeypress='return event.charCode >= 48 && event.charCode <= 57' name=\"overs\" value=".$overs." onChange=\"submitForms()\" onKeyDown=\"enterSubmit(this)\">&nbsp;&nbsp;";
}

echo "&nbsp;&nbsp;&nbsp;&nbsp;<b>Wickets:</b>&nbsp;&nbsp;";
echo "<select class=\"form-control\" name=\"wkts\" onChange=\"submitForms()\">";
$wktsList = array(0, 1, 2, 3, 4, 5, 6, 7, 8, 9);

if(isset($_GET['wkts'])) {
  $wkts = $_GET['wkts'];
  foreach ($wktsList as $w) {
    if ($wkts == $w) {
  	   echo "<option selected=\"selected\" value=\"$w\">$w</option>";
    } else {
  	   echo "<option value=\"$w\">$w</option>";
    }
  }
} else {
  $count = 0;
  foreach ($wktsList as $w) {
      if ($count == 5) {
      	echo "<option selected=\"selected\" value=\"$w\">$w</option>";
      	$wkts = $w;
      } else {
      	echo "<option value=\"$w\">$w</option>";
      }
      $count = $count + 1;
  }
}
echo "</select>";

echo "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type=\"submit\" name=\"Submit\" class=\"btn btn-primary\" value=\"Submit\">";
echo "<br/><br/>";

if ($matchFormat == "ODI") {
  echo "&nbsp;&nbsp;&nbsp;&nbsp;<b>Date range:</b>&nbsp;&nbsp;";
  echo "<input type=\"date\" class=\"form-control\" name=\"startDate\" value=".$startDate." onChange=\"submitForms()\">&nbsp;to&nbsp;";
  echo "<input type=\"date\" class=\"form-control\" name=\"endDate\" value=".$endDate." onChange=\"submitForms()\">&nbsp;&nbsp;";
}

$dbName = "ccrODI.db";
if ($matchFormat == "T20") {
  $dbName = "ccrT20I.db";
}
$db = new SQLite3($dbName);

if ($matchFormat == "ODI") {
  $sql = "select distinct team from team".$matchFormat."Current order by team asc";
  $result = $db->query($sql);
  if (!$result) die("Cannot execute query.");

  echo "<div class=\"form-group\">";
  echo "&nbsp;&nbsp;&nbsp;&nbsp;<b>Batting Team:</b>&nbsp;&nbsp;";
  echo "<select class=\"form-control\" name=\"battingTeam\" onChange=\"submitForms()\">";
  $battingTeamSet = "Not Set";
  if (isset($_GET['battingTeam'])) {
    $battingTeamSet = $_GET['battingTeam'];
  }
  if ($battingTeamSet == "Not Set") {
    echo "<option selected=\"selected\" value=\"Not Set\">Not Set</option>";
  } else {
    echo "<option value=\"Not Set\">Not Set</option>";
  }

  while($res = $result->fetchArray(SQLITE3_NUM)) {
   $battingT = $res[0];
   if ($battingT == $battingTeamSet) {
      echo "<option selected=\"selected\" value=\"$battingT\">$battingT</option>";
   } else {
      echo "<option value=\"$battingT\">$battingT</option>";
   }
  }
  echo "</select>";
  echo "</div>";

  echo "<div class=\"form-group\">";
  echo "&nbsp;&nbsp;&nbsp;&nbsp;<b>Bowling Team:</b>&nbsp;&nbsp;";
  echo "<select class=\"form-control\" name=\"bowlingTeam\" onChange=\"submitForms()\">";
  $bowlingTeamSet = "Not Set";
  if (isset($_GET['bowlingTeam'])) {
    $bowlingTeamSet = $_GET['bowlingTeam'];
  }
  if ($bowlingTeamSet == "Not Set") {
    echo "<option selected=\"selected\" value=\"Not Set\">Not Set</option>";
  } else {
    echo "<option value=\"Not Set\">Not Set</option>";
  }

  while($res = $result->fetchArray(SQLITE3_NUM)) {
   $bowlingT = $res[0];
   if ($bowlingT == $bowlingTeamSet) {
      echo "<option selected=\"selected\" value=\"$bowlingT\">$bowlingT</option>";
   } else {
      echo "<option value=\"$bowlingT\">$bowlingT</option>";
   }
  }
  echo "</select>";
  echo "</div>";
}
 else {
  $sql = "select distinct team from teamT20ICurrent order by team asc";
  $result = $db->query($sql);
  if (!$result) die("Cannot execute query.");

  echo "<div class=\"form-group\">";
  echo "&nbsp;&nbsp;&nbsp;&nbsp;<b>Batting Team:</b>&nbsp;&nbsp;";
  echo "<select class=\"form-control\" name=\"battingTeam\" onChange=\"submitForms()\">";
  $battingTeamSet = "Not Set";
  if (isset($_GET['battingTeam'])) {
    $battingTeamSet = $_GET['battingTeam'];
  }
  if ($battingTeamSet == "Not Set") {
    echo "<option selected=\"selected\" value=\"Not Set\">Not Set</option>";
  } else {
    echo "<option value=\"Not Set\">Not Set</option>";
  }

  while($res = $result->fetchArray(SQLITE3_NUM)) {
   $battingT = $res[0];
   if ($battingT == $battingTeamSet) {
      echo "<option selected=\"selected\" value=\"$battingT\">$battingT</option>";
   } else {
      echo "<option value=\"$battingT\">$battingT</option>";
   }
  }

  $db = new SQLite3("ccrFT20.db");
  $sql = "select distinct team from teamFT20Current order by team asc";
  $result = $db->query($sql);
  if (!$result) die("Cannot execute query.");

  while($res = $result->fetchArray(SQLITE3_NUM)) {
   $battingT = $res[0];
   if ($battingT == $battingTeamSet) {
      echo "<option selected=\"selected\" value=\"$battingT\">$battingT</option>";
   } else {
      echo "<option value=\"$battingT\">$battingT</option>";
   }
  }
  echo "</select>";
  echo "</div>";

  $db = new SQLite3("ccrT20I.db");
  $sql = "select distinct team from teamT20ICurrent order by team asc";
  $result = $db->query($sql);
  if (!$result) die("Cannot execute query.");
  echo "<div class=\"form-group\">";
  echo "&nbsp;&nbsp;&nbsp;&nbsp;<b>Bowling Team:</b>&nbsp;&nbsp;";
  echo "<select class=\"form-control\" name=\"bowlingTeam\" onChange=\"submitForms()\">";
  $bowlingTeamSet = "Not Set";
  if (isset($_GET['bowlingTeam'])) {
    $bowlingTeamSet = $_GET['bowlingTeam'];
  }
  if ($bowlingTeamSet == "Not Set") {
    echo "<option selected=\"selected\" value=\"Not Set\">Not Set</option>";
  } else {
    echo "<option value=\"Not Set\">Not Set</option>";
  }

  while($res = $result->fetchArray(SQLITE3_NUM)) {
   $bowlingT = $res[0];
   if ($bowlingT == $bowlingTeamSet) {
      echo "<option selected=\"selected\" value=\"$bowlingT\">$bowlingT</option>";
   } else {
      echo "<option value=\"$bowlingT\">$bowlingT</option>";
   }
  }

  $db = new SQLite3("ccrFT20.db");
  $sql = "select distinct team from teamFT20Current order by team asc";
  $result = $db->query($sql);
  if (!$result) die("Cannot execute query.");

  while($res = $result->fetchArray(SQLITE3_NUM)) {
   $bowlingT = $res[0];
   if ($bowlingT == $bowlingTeamSet) {
      echo "<option selected=\"selected\" value=\"$bowlingT\">$bowlingT</option>";
   } else {
      echo "<option value=\"$bowlingT\">$bowlingT</option>";
   }
  }
  echo "</select>";
  echo "</div>";
}

echo "</form>";
echo "</li>";

$matchFormatLower = strtolower($matchFormat);

if (isset($_GET['runs'])) {
  $runs = $_GET['runs'];
} else {
  $runs = 50;
}

if (isset($_GET['overs'])) {
  $overs = $_GET['overs'];
} else {
  $overs = 10;
}
if (strpos($overs, ".")) {
  $oversBalls = explode(".", $overs);
  $ballsRem = $oversBalls[0] * 6 + $oversBalls[1];
} else {
  $ballsRem = $overs * 6;
}

if ($matchFormat == "ODI") {
  $startDate = "19710000";
} else if ($matchFormat == "T20") {
  $startDate = "20050000";
}
$endDate = "20999999";

if (isset($_GET['startDate'])) {
  if ($_GET['startDate'] != "") {
    if (strpos($_GET['startDate'], "-") == false) {
      $startDate = $_GET['startDate'];
    } else {
      $startDates = explode("-", $_GET['startDate']);
      $startDate = $startDates[0].$startDates[1].$startDates[2];
    }
  }
}

if (isset($_GET['endDate'])) {
  if ($_GET['endDate'] != "") {
    if (strpos($_GET['endDate'], "-") == false) {
      $endDate = $_GET['endDate'];
    } else {
      $endDates = explode("-", $_GET['endDate']);
      $endDate = $endDates[0].$endDates[1].$endDates[2];
    }
  }
}

if ($matchFormat == "ODI") {
  if ($inn == 1) {
    if ($runs == 0) {
      $sql = 'select o.'.$matchFormatLower.'Id, avg(o.runs), avg(o.overs), avg(o.runRate), avg(o.wkts), o.teamBat, t.team1, t.team2, t.ground, t.startDate, avg(o.result) from overComparisonODI o, '.$matchFormatLower.'Info t where o.'.$matchFormatLower.'Id=t.'.$matchFormatLower.'Id and o.innings=1 and t.startDate>='.$startDate.' and t.startDate<='.$endDate.' and o.overs>='.($overs-1).' and o.overs<'.($overs+1).' and o.runs<=1 and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1).' group by o.'.$matchFormatLower.'Id';
    } else {
      $sql = 'select o.'.$matchFormatLower.'Id, avg(o.runs), avg(o.overs), avg(o.runRate), avg(o.wkts), o.teamBat, t.team1, t.team2, t.ground, t.startDate, avg(o.result) from overComparisonODI o, '.$matchFormatLower.'Info t where o.'.$matchFormatLower.'Id=t.'.$matchFormatLower.'Id and o.innings=1 and t.startDate>='.$startDate.' and t.startDate<='.$endDate.' and o.overs>='.($overs-1).' and o.overs<'.($overs+1).' and o.runs<='.($runs*1.1).' and o.runs>'.($runs*0.9).' and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1).' group by o.'.$matchFormatLower.'Id';
    }
  } else if ($inn == 2) {
    if ($ballsRem < 60) {
      $sql = 'select o.'.$matchFormatLower.'Id, avg(o.runsReq), avg(o.ballsRem), avg(o.reqRate), avg(o.wkts), o.teamBat, t.team1, t.team2, t.ground, t.startDate, avg(o.result) from overComparisonODI o, '.$matchFormatLower.'Info t where o.'.$matchFormatLower.'Id=t.'.$matchFormatLower.'Id and o.innings=2 and t.startDate>='.$startDate.' and t.startDate<='.$endDate.' and o.ballsRem>'.($ballsRem*0.75).' and o.ballsRem<='.($ballsRem*1.25).' and o.runsReq<'.($runs*1.25).' and o.runsReq>='.($runs*0.75).' and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1).' group by o.'.$matchFormatLower.'Id';
    } else {
      $sql = 'select o.'.$matchFormatLower.'Id, avg(o.runsReq), avg(o.ballsRem), avg(o.reqRate), avg(o.wkts), o.teamBat, t.team1, t.team2, t.ground, t.startDate, avg(o.result) from overComparisonODI o, '.$matchFormatLower.'Info t where o.'.$matchFormatLower.'Id=t.'.$matchFormatLower.'Id and o.innings=2 and t.startDate>='.$startDate.' and t.startDate<='.$endDate.' and o.ballsRem>'.($ballsRem*0.9).' and o.ballsRem<='.($ballsRem*1.1).' and o.runsReq<'.($runs*1.1).' and o.runsReq>='.($runs*0.9).' and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1).' group by o.'.$matchFormatLower.'Id';
    }
  }
} else {
  if ($inn == 1) {
    if ($runs == 0) {
      $sql = 'select o.ocId, avg(o.runs), avg(o.overs), avg(o.runRate), avg(o.wkts), o.teamBat, avg(o.result) from overComparison o where o.innings=1 and o.overs>='.($overs-1).' and o.overs<'.($overs+1).' and o.runs<=1 and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1).' group by o.ocId';
    } else {
      $sql = 'select o.ocId, avg(o.runs), avg(o.overs), avg(o.runRate), avg(o.wkts), o.teamBat, avg(o.result) from overComparison o where o.innings=1 and o.overs>='.($overs-1).' and o.overs<'.($overs+1).' and o.runs<='.($runs*1.1).' and o.runs>'.($runs*0.9).' and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1).' group by o.ocId';
    }
  } else if ($inn == 2) {
    if ($ballsRem < 60) {
      $sql = 'select o.ocId, avg(o.runsReq), avg(o.ballsRem), avg(o.reqRate), avg(o.wkts), o.teamBat, avg(o.result) from overComparison o where o.innings=2 and o.ballsRem>'.($ballsRem*0.75).' and o.ballsRem<='.($ballsRem*1.25).' and o.runsReq<'.($runs*1.25).' and o.runsReq>='.($runs*0.75).' and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1).' group by o.ocId';
    } else {
      $sql = 'select o.ocId, avg(o.runsReq), avg(o.ballsRem), avg(o.reqRate), avg(o.wkts), o.teamBat, avg(o.result) from overComparison o where o.innings=2 and o.ballsRem>'.($ballsRem*0.9).' and o.ballsRem<='.($ballsRem*1.1).' and o.runsReq<'.($runs*1.1).' and o.runsReq>='.($runs*0.9).' and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1).' group by o.ocId';
    }
  }
}

$dbName = "ccrODI.db";
if ($matchFormat == "T20") {
  $dbName = "ccrT20I.db";
}

$db = new SQLite3($dbName);
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");

$count = 0;
$winCount = 0;
$lossCount = 0;
while($res = $result->fetchArray(SQLITE3_NUM)) {
  if ($matchFormat == "ODI") {
    if ($res[10] == 2) {
      $winCount = $winCount + 1;
    } elseif ($res[10] == 0) {
      $lossCount = $lossCount + 1;
    }
  } else {
    if ($res[6] == 2) {
      $winCount = $winCount + 1;
    } elseif ($res[6] == 0) {
      $lossCount = $lossCount + 1;
    }
  }

  $count = $count + 1;
}

$team1Rating = 100;
$team2Rating = 100;
if (($inn == 1 && $battingTeam != "Not Set") || ($inn == 2 && $bowlingTeam != "Not Set")) {
  if ($inn == 1) {
    $team1 = $battingTeam;
  } else {
    $team1 = $bowlingTeam;
  }

  if ($matchFormat == "ODI") {
    $sql = 'select rating from team'.$matchFormat.'Live where team="'.$team1.'" order by startDate desc limit 1';
    $resultT = $db->query($sql);
    if (!$resultT) die("Cannot execute query.");
    if (count($resultT) > 0) {
      while($resT = $resultT->fetchArray(SQLITE3_NUM)) {
        $team1Rating = $resT[0];
      }
    }
  } else {
    $sql = 'select rating from teamT20ILive where team="'.$team1.'" order by startDate desc limit 1';
    $resultT = $db->query($sql);
    if (!$resultT) die("Cannot execute query.");
    if (count($resultT) > 0) {
      while($resT = $resultT->fetchArray(SQLITE3_NUM)) {
        $team1Rating = $resT[0];
      }
    } else {
      $sql = 'select rating from teamFT20Live where team="'.$team1.'" order by startDate desc limit 1';
      $resultT = $db->query($sql);
      if (!$resultT) die("Cannot execute query.");
      if (count($resultT) > 0) {
        while($resT = $resultT->fetchArray(SQLITE3_NUM)) {
          $team1Rating = $resT[0];
        }
      }
    }
  }
}

if (($inn == 2 && $battingTeam != "Not Set") || ($inn == 1 && $bowlingTeam != "Not Set")) {
  if ($inn == 2) {
    $team2 = $battingTeam;
  } else {
    $team2 = $bowlingTeam;
  }

  if ($matchFormat == "ODI") {
    $sql = 'select rating from team'.$matchFormat.'Live where team="'.$team2.'" order by startDate desc limit 1';
    $resultT = $db->query($sql);
    if (!$resultT) die("Cannot execute query.");
    if (count($resultT) > 0) {
      while($resT = $resultT->fetchArray(SQLITE3_NUM)) {
        $team2Rating = $resT[0];
      }
    }
  } else {
    $sql = 'select rating from teamT20ILive where team="'.$team2.'" order by startDate desc limit 1';
    $resultT = $db->query($sql);
    if (!$resultT) die("Cannot execute query.");
    if (count($resultT) > 0) {
      while($resT = $resultT->fetchArray(SQLITE3_NUM)) {
        $team2Rating = $resT[0];
      }
    } else {
      $sql = 'select rating from teamFT20Live where team="'.$team2.'" order by startDate desc limit 1';
      $resultT = $db->query($sql);
      if (!$resultT) die("Cannot execute query.");
      if (count($resultT) > 0) {
        while($resT = $resultT->fetchArray(SQLITE3_NUM)) {
          $team2Rating = $resT[0];
        }
      }
    }
  }
}

$team1StartingOdds = $team1Rating / ($team1Rating + $team2Rating);
$team2StartingOdds = 1 - $team1StartingOdds;

$teamAdjust = "N/A";
if ($count == 0) {
  $winOdds = "N/A";
  $winOddsAdj = "N/A";
  $winOddsText = "N/A";
} else {
  $winOdds = $winCount/$count;
  if ($inn == 2) {
    if ($runs == 0) {
      $winOdds = 1;
    }
    if ($overs == 0 && $runs != 0) {
      $winOdds = 0;
    }
  }

  $oddsDiff = $winOdds - (1 - $winOdds);
  $winOddsAdj = $winOdds;
  if ($inn == 1) {
      if ($team1StartingOdds >= 0.5) {
        $oddsAdj = $team1StartingOdds - 0.5;
        if ($winOdds >= 0.5) {
          $winOddsAdj = $winOdds - ($oddsAdj * $oddsDiff) + $oddsAdj;
        } else {
          $winOddsAdj = $winOdds + ($oddsAdj * $oddsDiff) + $oddsAdj;
        }
      } elseif ($team1StartingOdds < 0.5) {
        $oddsAdj = 0.5 - $team1StartingOdds;
        if ($winOdds >= 0.5) {
          $winOddsAdj = $winOdds + ($oddsAdj * $oddsDiff) - $oddsAdj;
        } else {
          $winOddsAdj = $winOdds - ($oddsAdj * $oddsDiff) - $oddsAdj;
        }
      }
  }

  if ($inn == 2) {
      if ($team2StartingOdds >= 0.5) {
        $oddsAdj = $team2StartingOdds - 0.5;
        if ($winOdds >= 0.5) {
          $winOddsAdj = $winOdds - ($oddsAdj * $oddsDiff) + $oddsAdj;
        } else {
          $winOddsAdj = $winOdds + ($oddsAdj * $oddsDiff) + $oddsAdj;
        }
      } elseif ($team2StartingOdds < 0.5) {
        $oddsAdj = 0.5 - $team2StartingOdds;
        if ($winOdds >= 0.5) {
          $winOddsAdj = $winOdds + ($oddsAdj * $oddsDiff) - $oddsAdj;
        } else {
          $winOddsAdj = $winOdds - ($oddsAdj * $oddsDiff) - $oddsAdj;
        }
      }
  }

  $winOdds = $winOdds * 100;
  $winOddsAdj = $winOddsAdj * 100;
  $teamAdjust = round($winOddsAdj - $winOdds, 2);
  $winOddsText = round($winOddsAdj, 2)."%";
}

echo "<li class=\"list-group-item\">";
if ($winOddsAdj > 55) {
  echo "<h3><b>Win Odds: <font color='green'>$winOddsText</font></b></h3>";
} elseif ($winOddsAdj <= 55 && $winOddsAdj >= 45) {
  echo "<h3><b>Win Odds: <font color='orange'>$winOddsText</font></b></h3>";
} else {
  echo "<h3><b>Win Odds: <font color='red'>$winOddsText</font></b></h3>";
}
if ($battingTeam != "Not Set" || $bowlingTeam != "Not Set") {
  if ($teamAdjust > 0) {
    echo "<b>Team Ratings Adjustment: <font color='green'>+$teamAdjust%</font></b><br/>";
  } else {
    echo "<b>Team Ratings Adjustment: <font color='red'>$teamAdjust%</font></b><br/>";
  }
}
echo "<b>Similar Count: $count&nbsp;&nbsp;&nbsp;&nbsp;Win Count: $winCount&nbsp;&nbsp;&nbsp;&nbsp;Loss Count: $lossCount</b>";
echo "</li>";
echo "</ul>";
echo "</div>";

if ($matchFormat == "ODI") {
  echo "<div class=\"col-lg-5\">";
} else {
  echo "<div class=\"col-lg-5\">";
}
echo "<ul class=\"list-group\">";
echo "<li class=\"list-group-item\">";
if ($inn == 1) {
  echo "<h4>Win/Loss Count by Run Rate</h4>";
} elseif ($inn == 2) {
  echo "<h4>Win/Loss Count by Required Run Rate</h4>";
}
echo "<div class=\"chart\">";
echo "<div id=\"chart\"></div></div>";
echo "</li>";
echo "</ul>";
echo "</div>";
echo "</div>";

echo "<div class=\"row\">";
if ($matchFormat == "ODI") {
  echo "<div class=\"col-lg-7\">";
} else {
  echo "<div class=\"col-lg-7\">";
}
echo "<ul class=\"list-group\">";
echo "<li class=\"list-group-item\">";
echo "<h4>Similar Scenario History</h4>";

echo "<table class=\"table table-hover table-condensed\" id=\"ratingsTable\">";
echo "<thead><tr>";
echo "<th>Match #</th>";
if ($inn == 1) {
  echo "<th>Runs</th>";
  echo "<th>Overs</th>";
  echo "<th>RunRate</th>";
} else if ($inn == 2) {
  echo "<th>Runs Req</th>";
  echo "<th>Overs Rem</th>";
  echo "<th>ReqRunRate</th>";
}
echo "<th>Wickets</th>";
if ($matchFormat == "ODI") {
  echo "<th>Team</th>";
  echo "<th>Vs</th>";
  echo "<th>Ground</th>";
  echo "<th>Date</th>";
} else {
  echo "<th>Batting Team</th>";
}
echo "<th>Result</th>";
echo "</tr></thead>";

while($res = $result->fetchArray(SQLITE3_NUM)) {
  $t20Type = "F";
  echo "<tr>";
  if ($matchFormat == "ODI") {
      echo "<td><a href=\"scorecard.php?matchFormat=$matchFormat&matchId=".$res[0]."\">$matchFormat #".$res[0]."</a></td>";
  } else {
    if (strpos($res[0], "F") === false) {
      $t20Type = "I";
      $t20Split = explode("I", $res[0]);
      $matchId = str_replace("u'","",$t20Split[0]);
      echo "<td><a href=\"scorecard.php?matchFormat=T20I&matchId=".$matchId."\">T20I #".$matchId."</a></td>";
    } else {
      $t20Type = "F";
      $t20Split = explode("F", $res[0]);
      $matchId = str_replace("u'","",$t20Split[0]);
      echo "<td><a href=\"scorecard.php?matchFormat=FT20&matchId=".$matchId."\">FT20 #".$matchId."</a></td>";
    }
  }
  echo "<td>".$res[1]."</td>";
  if ($inn == 1) {
    echo "<td>".$res[2]."</td>";
  } elseif ($inn == 2) {
    echo "<td>".round($res[2]/6)."</td>";
  }
  echo "<td>".$res[3]."</td><td>".$res[4]."</td>";
  if ($matchFormat == "ODI") {
    if ($res[5] == $res[6]) {
      echo "<td><a href=\"team.php?team=".$res[6]."&matchFormat=$matchFormat\"><img src=\"images/".$res[6].".png\" alt=\"$res[6]\" style='border:1px solid #A9A9A9'/></a></td>";
      echo "<td><a href=\"team.php?team=".$res[7]."&matchFormat=$matchFormat\"><img src=\"images/".$res[7].".png\" alt=\"$res[7]\" style='border:1px solid #A9A9A9'/></a></td>";
    } else {
      echo "<td><a href=\"team.php?team=".$res[7]."&matchFormat=$matchFormat\"><img src=\"images/".$res[7].".png\" alt=\"$res[7]\" style='border:1px solid #A9A9A9'/></a></td>";
      echo "<td><a href=\"team.php?team=".$res[6]."&matchFormat=$matchFormat\"><img src=\"images/".$res[6].".png\" alt=\"$res[6]\" style='border:1px solid #A9A9A9'/></a></td>";
    }
    echo "<td>".$res[8]."</td>";
    echo "<td>".substr($res[9], 0, 4)."-".substr($res[9], 4, 2)."-".substr($res[9], 6, 2)."</td>";
    if ($res[10] == 2) {
      echo "<td><font color='green'><b>Win</b></font></td>";
    } elseif ($res[10] == 1) {
      echo "<td><font color='orange'><b>Tie/NR</b></font></td>";
    } else {
      echo "<td><font color='red'><b>Loss</b></font></td>";
    }
  } else {
    if ($t20Type == "I") {
      echo "<td><a href=\"team.php?team=".$res[5]."&matchFormat=T20I\"><img src=\"images/".$res[5].".png\" alt=\"$res[5]\" style='border:1px solid #A9A9A9'/></a></td>";
    } else {
      echo "<td><a href=\"team.php?team=".$res[5]."&matchFormat=FT20\">".$res[5]."</a></td>";
    }

    if ($res[6] == 2) {
      echo "<td><font color='green'><b>Win</b></font></td>";
    } elseif ($res[6] == 1) {
      echo "<td><font color='orange'><b>Tie/NR</b></font></td>";
    } else {
      echo "<td><font color='red'><b>Loss</b></font></td>";
    }
  }

  echo "</tr>";
}
echo "</table>";
echo "</li>";
echo "</ul>";
echo "</div>";
if ($matchFormat == "ODI") {
  echo "<div class=\"col-lg-5\">";
} else {
  echo "<div class=\"col-lg-5\">";
}
echo "<ul class=\"list-group\">";
echo "<li class=\"list-group-item\">";
if ($inn == 1) {
  echo "<h4>Win/Loss by Run Rate Timeline</h4>";
} elseif ($inn == 2) {
  echo "<h4>Win/Loss by Required Run Rate Timeline</h4>";
}
echo "<div class=\"chart\">";
echo "<div id=\"chartB\"></div></div>";
echo "</li>";

echo "</ul>";
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
