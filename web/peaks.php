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
   $disc = "Player";
}
if(isset($_GET['team'])) {
   $team = $_GET['team'];
} else {
   $team = "All teams";
}

$matchFormatLower = strtolower($matchFormat);
$disciplineLower = strtolower($disc);

$dbName = "ccr.db";
if ($matchFormat == "ODI") {
  $dbName = "ccrODI.db";
} elseif ($matchFormat == "T20I") {
  $dbName = "ccrT20I.db";
} elseif ($matchFormat == "FT20") {
  $dbName = "ccrFT20.db";
}

$db = new SQLite3($dbName);

if(isset($_SESSION['screen_width']) AND isset($_SESSION['screen_height'])){
} else if(isset($_REQUEST['width']) AND isset($_REQUEST['height'])) {
    $_SESSION['screen_width'] = $_REQUEST['width'];
    $_SESSION['screen_height'] = $_REQUEST['height'];

    header("Location: peaks.php?matchFormat=".$matchFormat."&disc=".$disc."&team=".$team);
} else {
    echo '<script type="text/javascript">window.location = "' . $_SERVER['PHP_SELF'] . '?matchFormat='.$matchFormat.'&disc='.$disc."&team=".$team.'&width="+screen.width+"&height="+screen.height;</script>';
}

$db->close();

?>
<html>
<head>
   <title>cricrate | Peak Ratings - <?php echo($matchFormat." ".$disc); ?></title>
   <meta charset="UTF-8">
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

   $(document).ready(function() {
       $('#ratingsTable').DataTable( {
       "lengthMenu": [[15, 25, 50, 100, -1], [15, 25, 50, 100, "All"]],
       "pageLength": 15,
       "order": [[ 0, "asc" ]],
   } );

      $('#ratingsTable2').DataTable( {
       "lengthMenu": [[15, 25, 50, 100, -1], [15, 25, 50, 100, "All"]],
       "pageLength": 15,
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
                    <li class="active">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Team <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="methodology.php?matchFormat=Test&disc=Team"><b>Test</b></a></li>
                            <li><a href="current.php?matchFormat=Test&disc=Team">&nbsp;&nbsp;Current</a></li>
                            <?php if ($matchFormat == "Test") { echo "<li class=\"active\"><a href=\"peaks.php?matchFormat=Test&disc=Player\">&nbsp;&nbsp;Peaks<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"peaks.php?matchFormat=Test&disc=Player\">&nbsp;&nbsp;Peaks</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=Test&disc=Team">&nbsp;&nbsp;Overall</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=ODI&disc=Team"><b>ODI</b></a></li>
                            <li><a href="current.php?matchFormat=ODI&disc=Team">&nbsp;&nbsp;Current</a></li>
                            <?php if ($matchFormat == "ODI") { echo "<li class=\"active\"><a href=\"peaks.php?matchFormat=ODI&disc=Player\">&nbsp;&nbsp;Peaks<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"peaks.php?matchFormat=ODI&disc=Player\">&nbsp;&nbsp;Peaks</a></li>"; } ?>
                            <li><a href="career.php?matchFormat=ODI&disc=Team">&nbsp;&nbsp;Overall</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=T20I&disc=Team"><b>T20I</b></a></li>
                            <li><a href="current.php?matchFormat=T20I&disc=Team">&nbsp;&nbsp;Current</a></li>
                            <li><a href="career.php?matchFormat=T20I&disc=Team">&nbsp;&nbsp;Overall</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="methodology.php?matchFormat=FT20&disc=Team"><b>FT20</b></a></li>
                            <li><a href="current.php?matchFormat=FT20&disc=Team">&nbsp;&nbsp;Current</a></li>
                            <?php if ($matchFormat == "FT20") { echo "<li class=\"active\"><a href=\"peaks.php?matchFormat=FT20&disc=Player\">&nbsp;&nbsp;Peaks<span class=\"sr-only\">(current)</span></a></li>"; } else { echo "<li><a href=\"peaks.php?matchFormat=FT20&disc=Player\">&nbsp;&nbsp;Peaks</a></li>"; } ?>
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
                    <li class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Odds <span class="caret"></span></a>
                    <ul class="dropdown-menu">
                          <li><a href="liveodds.php">Live</a></li>
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

   $discMod = "Team";
   if ($disc == "Player") {
     $discMod = "Team";
   } else {
     $discMod = $disc;
   }
   echo "<div class=\"panel panel-inverse\">";
   echo "<div class=\"panel-body\">";
   echo "<div class=\"row\">";
   echo "<div class=\"col-lg-10\">";
   echo "<h2><b>Peak Ratings&nbsp;&nbsp;<small>&nbsp;&nbsp;<a href=\"methodology.php?matchFormat=$matchFormat&disc=$discMod\">Methodology</a></small></b></h2>";
   $matchFormat = "Test";
   $disc = "Player";
   $team = "All teams";
   echo "<form class=\"form-inline\" role=\"form\" name=\"selectForm\" method=\"get\" action=\"peaks.php\">";
   echo "<div class=\"form-group\">";
   echo "<select class=\"form-control\" name=\"matchFormat\" onChange=\"submitForms()\">";
   $matchFormats = array("Test", "ODI", "FT20");
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
   $discs = array("Player", "Team", "Batting", "Bowling");
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
   if ($team == "All teams") {
     $sql = "select team, playerList, rating, startDate, ".$matchFormatLower."Id from team".$matchFormat."Peaks where ratingType='".$disc."' order by rating desc";
   } else {
     $sql = "select team, playerList, rating, startDate, ".$matchFormatLower."Id from team".$matchFormat."Peaks where ratingType='".$disc."' and team='".$team."' order by rating desc";
   }

   $result = $db->query($sql);
   if (!$result) die("Cannot execute query.");
   echo "<ul class=\"list-group\">";
   echo "<li class=\"list-group-item\">";
   echo "<table class=\"table table-hover table-condensed\" id=\"ratingsTable\">";
   echo "<thead><tr>";
   echo "<th>Rank</th>";
   echo "<th>Team</th>";
   if ($matchFormat != "FT20") {
    echo "<th>Flag</th>";
   }
   if ($disc != "Team") {
     echo "<th>Players</th>";
   }
   echo "<th>Rating</th>";
   echo "<th>Date</th>";
   echo "<th>Scorecard</th>";
   echo "</tr></thead>";

   $k = 1;
   while($res = $result->fetchArray(SQLITE3_NUM)) {
	    echo "<td>$k</td>";
      echo "<td><a href=\"team.php?team=".$res[0]."&matchFormat=$matchFormat&disc=$disc\">".$res[0]."</a></td>";
      if ($matchFormat != "FT20") {
        echo "<td><a href=\"team.php?team=".$res[0]."&matchFormat=$matchFormat&disc=$disc\"><img src=\"images/".$res[0].".png\" alt=\"$res[0]\" style='border:1px solid #A9A9A9'/></a></td>";
      }
      if ($disc != "Team") {
        echo "<td>".$res[1]."</td>";
      }
      echo "<td><b>".round($res[2], 0)."</b></td>";
      echo "<td>".substr($res[3], 0, 4)."-".substr($res[3], 4, 2)."-".substr($res[3], 6, 2)."</td>";
      echo "<td><a href=\"scorecard.php?matchFormat=$matchFormat&matchId=".$res[4]."\">$matchFormat #".$res[4]."</a></td>";
      echo "</tr>";
      $k++;
   }
   echo "</table>";
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
