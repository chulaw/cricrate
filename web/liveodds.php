<!DOCTYPE html>
<?php
session_start();
if(isset($_GET['match'])) {
   $match = $_GET['match'];
} else {
  $csvFile = file('https://s3-eu-west-1.amazonaws.com/cricrate/liveOdds.csv');
  $maxDateTime = "";
  foreach ($csvFile as $line) {
      $data = str_getcsv($line);
      $matchFormat = $data[1];
      if ($matchFormat == "Format") {
        continue;
      }

      $dateTime = explode(" ", $data[0]);
      $matchDate = $dateTime[0];
      $currentDate = date('Y-m-d');
      if ($currentDate != $matchDate) {
        continue;
      }

      $currentTime = str_replace(":", "", $dateTime[1]);
      if ($maxDateTime == "") {
        $maxDateTime = $currentTime;
      } else {
        if ($currentTime > $maxDateTime) {
          $maxDateTime = $currentTime;
          $team1 = $data[2];
          $team2 = $data[3];
          $inn = $data[4];
          $mat = $matchDate . ": " . $team1 . " vs " . $team2 . " " . $matchFormat;
          $mat2nd = $matchDate . ": " . $team2 . " vs " . $team1 . " " . $matchFormat;
        }
      }
  }

  if ($inn == 1) {
    $match = $mat;
  } else {
    $match = $mat2nd;
  }
}

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

if(isset($_SESSION['screen_width']) AND isset($_SESSION['screen_height'])){
} else if(isset($_REQUEST['width']) AND isset($_REQUEST['height'])) {
    $_SESSION['screen_width'] = $_REQUEST['width'];
    $_SESSION['screen_height'] = $_REQUEST['height'];

    header("Location: liveodds.php?match=".$match."&matchFormat=".$matchFormat."&inn=".$inn."&runs=".$runs."&overs=".$overs."&wkts=".$wkts);
} else {
    echo '<script type="text/javascript">window.location = "' . $_SERVER['PHP_SELF'] . '?match='.$match.'&matchFormat='.$matchFormat.'&inn='.$inn.'&runs='.$runs.'&overs='.$overs.'&wkts='.$wkts.'&width="+screen.width+"&height="+screen.height;</script>';
}

?>
<html>
<head>
    <title>cricrate | Live Odds</title>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="120">
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
       $('#similarTable').DataTable( {
       "lengthMenu": [[18, 25, 50, 100, -1], [18, 25, 50, 100, "All"]],
       "bFilter":   false,
       "pageLength": 18,
       "order": [[ 0, "desc" ]],
    } );
    } );

    submitForms = function(){
      window.document.selectForm.submit();
    }

    // function enterSubmit(ele) {
    //   if(event.keyCode == 13) {
    //     window.document.selectForm.submit();
    //   }
    // }
    //
    var isMobile = false; //initiate as false
     // device detection
     if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent)
     || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))) isMobile = true;

     var chartWidth = screen.width * 0.45;
     var chartHeight = screen.height * 0.4;
     var chartHeightB = screen.height * 0.25;

     if (isMobile == true) {
 	     chartWidth = chartWidth * 2;
     }

    var match = <?php echo json_encode($match) ?>;
    var inn = <?php echo json_encode($inn); ?>;
    var runs = <?php echo json_encode($runs); ?>;
    var overs = <?php echo json_encode($overs); ?>;
    var wkts = <?php echo json_encode($wkts); ?>;
    var hAxis = "Run Rate";
    if (inn == 2) {
        hAxis = "Required Run Rate";
    }

     google.charts.load('current', {'packages':['corechart']});
     google.charts.setOnLoadCallback(drawChartLine);
    //  google.charts.setOnLoadCallback(drawChartBubble);

    function drawChartLine() {
       var jsonData = $.ajax({
 	  url: "charts/liveoddsLine.php?match="+match,
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
 	  colors:['#2c518d','#ff3232','#87ce00'],
 	  width: chartWidth,
 	    height: chartHeight,
 	  vAxis: {
 		  title: "Live Odds %",
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
 		  title: "Overs",
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

    function drawChartBubble() {
       var jsonData = $.ajax({
     url: "charts/liveOddsBubble.php?matchFormat="+matchFormat+"&inn="+inn+"&runs="+runs+"&overs="+overs+"&wkts="+wkts,
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
                            <li><a href="peaks.php?matchFormat=Test&disc=Player">&nbsp;&nbsp;Peaks</a></li>
                            <li><a href="career.php?matchFormat=Test&disc=Team">&nbsp;&nbsp;Overall</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=ODI&disc=Team"><b>ODI</b></a></li>
                            <li><a href="current.php?matchFormat=ODI&disc=Team">&nbsp;&nbsp;Current</a></li>
                            <li><a href="peaks.php?matchFormat=ODI&disc=Player">&nbsp;&nbsp;Peaks</a></li>
                            <li><a href="career.php?matchFormat=ODI&disc=Team">&nbsp;&nbsp;Overall</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=T20I&disc=Team"><b>T20I</b></a></li>
                            <li><a href="current.php?matchFormat=T20I&disc=Team">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=T20I&disc=Team">&nbsp;&nbsp;Overall</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=Team"><b>FT20</b></a></li>
                            <li><a href="current.php?matchFormat=FT20&disc=Team">&nbsp;&nbsp;Current</a></li>
                            <li><a href="peaks.php?matchFormat=FT20&disc=Player">&nbsp;&nbsp;Peaks</a></li>
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
		                <li><a href="insight.php">Insight</a></li>
                    <li class="active">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Odds <span class="caret"></span></a>
                    <ul class="dropdown-menu">
                          <li class="active"><a href="liveodds.php">Live <span class="label label-warning">new</span></a></li>
                          <li><a href="customodds.php">Custom</a></li>
                      </ul>
                    </li>
                    <li><a href="blog.php">Blog <span class="label label-warning">new</span></a></li>
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
$csvFile = file('https://s3-eu-west-1.amazonaws.com/cricrate/liveOdds.csv');
$data = [];
$matches = [];
foreach ($csvFile as $line) {
    $data = str_getcsv($line);
    $matchF = $data[1];
    if ($matchF == "Format") {
      continue;
    }
    $dateTime = explode(" ", $data[0]);
    $matchDate = $dateTime[0];
    $currentDate = date('Y-m-d');
    $team1 = $data[2];
    $team2 = $data[3];
    $inn = $data[4];
    $match = $matchDate . ": " . $team1 . " vs " . $team2 . " " . $matchF;
    $match2nd = $matchDate . ": " . $team2 . " vs " . $team1 . " " . $matchF;
    if (!in_array($match, $matches) && !in_array($match2nd, $matches) && $currentDate == $matchDate) {
      if ($inn == 1) {
        array_push($matches, $match);
      } else {
        array_push($matches, $match2nd);
      }
    }
}

if (count($matches) == 0) {
  echo "<h3>No live matches found.</h3>";
  echo "<h4>Click <a href=\"customodds.php\">here</a> for custom match scenario analysis.</h4>";
} else {
  echo "<h3><b>Live Odds&nbsp;&nbsp;<small>&nbsp;&nbsp;<a href=\"blog.php?title=odds\">Methodology</a></small></b></h3>";
  echo "<ul class=\"list-group\">";
  echo "<li class=\"list-group-item\">";
  echo "<form class=\"form-inline\" role=\"form\" name=\"selectForm\" method=\"get\" action=\"liveodds.php\">";
  echo "<div class=\"form-group\">";
  echo "&nbsp;&nbsp;&nbsp;&nbsp;<b>Match:</b>&nbsp;&nbsp;";
  echo "<select class=\"form-control\" name=\"match\" onChange=\"submitForms()\">";
  if(isset($_GET['match'])) {
    $match = $_GET['match'];
    foreach ($matches as $m) {
      $matchSplit = explode(":", $m);
      if ($match == $m) {
          echo "<option selected=\"selected\" value=\"$m\">".trim($matchSplit[1])."</option>";
      } else {
          echo "<option value=\"$m\">".trim($matchSplit[1])."</option>";
      }
    }
  } else {
    $count = 0;
    foreach ($matches as $m) {
      $matchSplit = explode(":", $m);
      if ($count == 0) {
          echo "<option selected=\"selected\" value=\"$m\">".trim($matchSplit[1])."</option>";
          $match = $m;
      } else {
          echo "<option value=\"$m\">".trim($matchSplit[1])."</option>";
      }
      $count = $count + 1;
    }
  }
  echo "</select>";
  echo "</div>";
  echo "</form>";
  echo "</li>";
  $data = [];
  $overs = [];
  $oversAdj = [];
  $betOdds = [];
  $crOdds = [];
  $crMLOdds = [];
  $inn1stOvers = 0;
  $inn1stRuns = 0;
  $inn1stWkts = 0;
  $inns = [];
  $runsReqs = [];
  $wkts = [];
  $runRates = [];
  $team1Mod = "";
  $team2Mod = "";
  $matchFormat = "";
  # set max first innings overs
  foreach ($csvFile as $line) {
      $data = str_getcsv($line);
      $dateTime = explode(" ", $data[0]);
      $matchDate = $dateTime[0];
      $matchF = $data[1];
      $team1 = $data[2];
      $team2 = $data[3];
      $inn = $data[4];
      $matchSt = $matchDate . ": " . $team1 . " vs " . $team2 . " " . $matchF;
      if ($inn == 2) {
          $matchSt = $matchDate . ": " . $team2 . " vs " . $team1 . " " . $matchF;
      }
      if ($match == $matchSt) {
        $matchFormat = $matchF;
        $team1Mod = $team1;
        $team2Mod = $team2;
        if ($inn == 2) {
          $team1Mod = $team2;
          $team2Mod = $team1;
        }
        $runsReq = $data[5];
        $wkt = $data[6];
        $ov = $data[7];
        if ($inn == 1 && $ov > $inn1stOvers) {
          $inn1stOvers = $ov;
        }
        if ($inn == 1 && $wkt > $inn1stWkts) {
          $inn1stWkts = $wkt;
        }
        if ($inn == 1 && $runsReq > $inn1stRuns) {
          $inn1stRuns = $runsReq;
        }
      }
  }

  foreach ($csvFile as $line) {
      $data = str_getcsv($line);
      $dateTime = explode(" ", $data[0]);
      $matchDate = $dateTime[0];
      $matchF = $data[1];
      $team1 = $data[2];
      $team2 = $data[3];
      $inn = $data[4];
      $matchSt = $matchDate . ": " . $team1 . " vs " . $team2 . " " . $matchF;
      if ($inn == 2) {
          $matchSt = $matchDate . ": " . $team2 . " vs " . $team1 . " " . $matchF;
      }
      if ($match == $matchSt) {
        $runsReq = $data[5];
        $wkt = $data[6];
        $ov = $data[7];
        $runRate = $data[8];
        $betO = $data[9];
        $crO = $data[10];
        $crMLO = $data[11];
        if ($inn == 2) {
          $inn2ndOvers = $inn1stOvers + $ov;
          array_push($oversAdj, $inn2ndOvers);
          $crOdds[$inn2ndOvers] = 100 - $crO;
          $crMLOdds[$inn2ndOvers] = 100 - $crMLO;
          $betOdds[$inn2ndOvers] = 100 - $betO;
          $overs[$inn2ndOvers] = $ov;
          $inns[$inn2ndOvers] = $inn;
          $runsReqs[$inn2ndOvers] = $runsReq;
          $wkts[$inn2ndOvers] = $wkt;
          $runRates[$inn2ndOvers] = $runRate;
         } else {
          array_push($oversAdj, $ov);
          $crOdds[$ov] = $crO;
          $crMLOdds[$ov] = $crMLO;
          $betOdds[$ov] = $betO;
          $overs[$ov] = $ov;
          $inns[$ov] = $inn;
          $runsReqs[$ov] = $runsReq;
          $wkts[$ov] = $wkt;
          $runRates[$ov] = $runRate;
        }
      }
  }

  sort($oversAdj);
  $latOv = max($oversAdj);
  $runs = $runsReqs[$latOv];
  $overs = $overs[$latOv];
  $inn = $inns[$latOv];
  $wkts = $wkts[$latOv];
  $cricOdds = $crOdds[$latOv];
  $cricMLOdds = $crMLOdds[$latOv];
  $bettingOdds = $betOdds[$latOv];

  if ($matchFormat == "One-Day") {
    $matchFormat = "ODI";
  } else {
    $matchFormat = "T20";
  }
  $matchFormatLower = strtolower($matchFormat);
  if ($matchFormat == "ODI") {
    $ballsRem = 300 - $overs * 6;
  } else {
    $ballsRem = 120 - $overs * 6;
  }

  echo "<li class=\"list-group-item\">";
  echo "<table class=\"table table-hover table-condensed\" id=\"ratingsTable\">";
  echo "<thead><tr>";
  echo "<th>Team</th>";
  echo "<th>Innings</th>";
  echo "<th>Score</th>";
  echo "<th>Overs</th>";
  echo "<th>Betting Site Odds (%)</th>";
  echo "<th>cricrate Base Odds (%)</th>";
  echo "<th>cricrate ML Odds (%)</th>";
  echo "</tr></thead>";
  echo "<tr>";
  $odiTeams = array("Afghanistan", "Australia", "Bangladesh", "England", "India", "New Zealand", "Pakistan", "South Africa", "Sri Lanka", "West Indies", "Zimbabwe", "Ireland", "P.N.G.", "Hong Kong", "Scotland", "U.A.E.");
  if ($matchFormat == "ODI") {
    if (in_array($team1Mod, $odiTeams)) {
      echo "<td><a href=\"team.php?team=".$team1Mod."&matchFormat=$matchFormat\">$team1Mod</a>&nbsp;&nbsp;<a href=\"team.php?team=".$team1Mod."&matchFormat=$matchFormat\"><img src=\"images/".$team1Mod.".png\" alt=\"$team1Mod\" style='border:1px solid #A9A9A9'/></a></td>";
    } else {
      echo "<td>".$team1Mod."</td>";
    }
  } else {
    echo "<td><a href=\"team.php?team=".$team1Mod."&matchFormat=FT20\">".$team1Mod."</a></td>";
  }
  echo "<td>1st</td>";
  echo "<td>".$inn1stRuns."/".$inn1stWkts."</td>";
  if (strpos($inn1stOvers, ".")) {
    $oversBalls = explode(".", $inn1stOvers);
    $inn1stOversOnly = $oversBalls[0];
    $balls = round($oversBalls[1] * 6 / 100);
  } else {
    $inn1stOversOnly = $inn1stOvers;
    $balls = 0;
  }
  echo "<td>".$inn1stOversOnly.".".$balls."</td>";
  if ($bettingOdds > 55) {
    echo "<td><b><font color='green'>$bettingOdds</font></b></td>";
  } elseif ($bettingOdds <= 55 && $bettingOdds >= 45) {
    echo "<td><b><font color='orange'>$bettingOdds</font></b></td>";
  } else {
    echo "<td><b><font color='red'>$bettingOdds</font></b></td>";
  }
  if ($cricOdds > 55) {
    echo "<td><b><font color='green'>$cricOdds</font></b></td>";
  } elseif ($cricOdds <= 55 && $cricOdds >= 45) {
    echo "<td><b><font color='orange'>$cricOdds</font></b></td>";
  } else {
    echo "<td><b><font color='red'>$cricOdds</font></b></td>";
  }
  if ($cricMLOdds > 55) {
    echo "<td><b><font color='green'>$cricMLOdds</font></b></td>";
  } elseif ($cricMLOdds <= 55 && $cricMLOdds >= 45) {
    echo "<td><b><font color='orange'>$cricMLOdds</font></b></td>";
  } else {
    echo "<td><b><font color='red'>$cricMLOdds</font></b></td>";
  }
  echo "</tr>";
  echo "<tr>";
  if ($matchFormat == "ODI") {
    if (in_array($team1Mod, $odiTeams)) {
      echo "<td><a href=\"team.php?team=".$team2Mod."&matchFormat=$matchFormat\">$team2Mod</a>&nbsp;&nbsp;<a href=\"team.php?team=".$team2Mod."&matchFormat=$matchFormat\"><img src=\"images/".$team2Mod.".png\" alt=\"$team2Mod\" style='border:1px solid #A9A9A9'/></a></td>";
    } else {
      echo "<td>".$team2Mod."</td>";
    }
  } else {
    echo "<td><a href=\"team.php?team=".$team2Mod."&matchFormat=FT20\">".$team2Mod."</a></td>";
  }

  if ($inn == 2) {
    echo "<td>2nd</td>";
    $team2Runs = $inn1stRuns - $runsReq + 1;
    echo "<td>".$team2Runs."/".$wkts."</td>";

    if (strpos($overs, ".")) {
      $oversBalls = explode(".", $overs);
      $inn2ndOversOnly = $oversBalls[0];
      $balls = round($oversBalls[1] * 6 / 100);
    } else {
      $inn2ndOversOnly = $overs;
      $balls = 0;
    }
    echo "<td>".$inn2ndOversOnly.".".$balls."</td>";
  } else {
    echo "<td></td>";
    echo "<td></td>";
    echo "<td></td>";
  }
  if ((100 - $bettingOdds) > 55) {
    echo "<td><b><font color='green'>".(100 - $bettingOdds)."</font></b></td>";
  } elseif ((100 - $bettingOdds) <= 55 && (100 - $bettingOdds) >= 45) {
    echo "<td><b><font color='orange'>".(100 - $bettingOdds)."</font></b></td>";
  } else {
    echo "<td><b><font color='red'>".(100 - $bettingOdds)."</font></b></td>";
  }
  if ((100 - $cricOdds) > 55) {
    echo "<td><b><font color='green'>".(100 - $cricOdds)."</font></b></td>";
  } elseif ((100 - $cricOdds) <= 55 && (100 - $cricOdds) >= 45) {
    echo "<td><b><font color='orange'>".(100 - $cricOdds)."</font></b></td>";
  } else {
    echo "<td><b><font color='red'>".(100 - $cricOdds)."</font></b></td>";
  }
  if ((100 - $cricMLOdds) > 55) {
    echo "<td><b><font color='green'>".(100 - $cricMLOdds)."</font></b></td>";
  } elseif ((100 - $cricMLOdds) <= 55 && (100 - $cricMLOdds) >= 45) {
    echo "<td><b><font color='orange'>".(100 - $cricMLOdds)."</font></b></td>";
  } else {
    echo "<td><b><font color='red'>".(100 - $cricMLOdds)."</font></b></td>";
  }
  echo "</tr>";
  echo "</table>";
  echo "</li>";
  echo "</ul>";

  echo "<ul class=\"list-group\">";
  echo "<li class=\"list-group-item\">";
  echo "<h4>Odds Timeline: $team1Mod</h4>";
  echo "<div class=\"chart\">";
  echo "<div id=\"chart\"></div></div>";
  echo "<div class=\"text-center\">Betting Site Odds <img src=\"images/player1.png\"/>&nbsp;&nbsp;cricrate Base Odds <img src=\"images/player2.png\"/>&nbsp;&nbsp;cricrate ML Odds <img src=\"images/player3.png\"/></div>";
  echo "</li>";

  echo "</ul>";
  echo "</div>";

  echo "<div class=\"col-lg-6\">";
  echo "<ul class=\"list-group\">";

  // $runs = 50;
  // $over = 15;
  // $wkts = 5;
  // $ballsRem = 30;
  if ($matchFormat == "ODI") {
    if ($inn == 1) {
      if ($runs < 50) {
        $sql = 'select o.'.$matchFormatLower.'Id, avg(o.runs), avg(o.overs), avg(o.runRate), avg(o.wkts), o.teamBat, t.team1, t.team2, t.ground, t.startDate, avg(o.result) from overComparisonODI o, '.$matchFormatLower.'Info t where o.'.$matchFormatLower.'Id=t.'.$matchFormatLower.'Id and o.innings=1 and o.overs>='.($overs-1).' and o.overs<'.($overs+1).' and o.runs<=1 and o.wkts='.$wkts.' group by o.'.$matchFormatLower.'Id';
      } else {
        $sql = 'select o.'.$matchFormatLower.'Id, avg(o.runs), avg(o.overs), avg(o.runRate), avg(o.wkts), o.teamBat, t.team1, t.team2, t.ground, t.startDate, avg(o.result) from overComparisonODI o, '.$matchFormatLower.'Info t where o.'.$matchFormatLower.'Id=t.'.$matchFormatLower.'Id and o.innings=1 and o.overs>='.($overs-1).' and o.overs<'.($overs+1).' and o.runs<='.($runs*1.1).' and o.runs>'.($runs*0.9).' and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1).' group by o.'.$matchFormatLower.'Id';
      }
    } else if ($inn == 2) {
      if ($ballsRem < 60) {
        $sql = 'select o.'.$matchFormatLower.'Id, avg(o.runsReq), avg(o.ballsRem), avg(o.reqRate), avg(o.wkts), o.teamBat, t.team1, t.team2, t.ground, t.startDate, avg(o.result) from overComparisonODI o, '.$matchFormatLower.'Info t where o.'.$matchFormatLower.'Id=t.'.$matchFormatLower.'Id and o.innings=2 and o.ballsRem>'.($ballsRem*0.75).' and o.ballsRem<='.($ballsRem*1.25).' and o.runsReq<'.($runs*1.25).' and o.runsReq>='.($runs*0.75).' and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1).' group by o.'.$matchFormatLower.'Id';
      } else {
        $sql = 'select o.'.$matchFormatLower.'Id, avg(o.runsReq), avg(o.ballsRem), avg(o.reqRate), avg(o.wkts), o.teamBat, t.team1, t.team2, t.ground, t.startDate, avg(o.result) from overComparisonODI o, '.$matchFormatLower.'Info t where o.'.$matchFormatLower.'Id=t.'.$matchFormatLower.'Id and o.innings=2 and o.ballsRem>'.($ballsRem*0.9).' and o.ballsRem<='.($ballsRem*1.1).' and o.runsReq<'.($runs*1.1).' and o.runsReq>='.($runs*0.9).' and o.wkts>='.($wkts-1).' and o.wkts<='.($wkts+1).' group by o.'.$matchFormatLower.'Id';
      }
    }
  } else {
    if ($inn == 1) {
      if ($runs < 50) {
        $sql = 'select o.ocId, avg(o.runs), avg(o.overs), avg(o.runRate), avg(o.wkts), o.teamBat, avg(o.result) from overComparison o where o.innings=1 and o.overs>='.($overs-1).' and o.overs<'.($overs+1).' and o.runs<=1 and o.wkts='.$wkts.' group by o.ocId';
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

  echo "<li class=\"list-group-item\">";
  echo "<h4>Similar Scenario History</h4>";
  echo "<table class=\"table table-hover table-condensed\" id=\"similarTable\">";
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
    echo "<td>".round($res[1])."</td>";
    if ($inn == 1) {
      echo "<td>".$res[2]."</td>";
    } elseif ($inn == 2) {
      echo "<td>".round($res[2]/6)."</td>";
    }
    echo "<td>".round($res[3], 2)."</td><td>".round($res[4])."</td>";
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
}

echo "</div>";
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
