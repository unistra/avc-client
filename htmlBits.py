# ************************************************************
#
# A file with HTML and Javascript chuncks for audiovideocours
# (to help create an html/flash export)
#
#    (c) ULP Multimedia 2006 - 2007 
#     Developer : francois.schnell [AT ulpmm.u-strasbg.fr]
#
#*************************************************************

head= """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>AudioVideoCours http playback</title>
    <style type="text/css">
        body 
          { 
            background: white url(bg-bluegrad.png) repeat-x top right; 
            padding: 0 20px;
            color:#000;
            font: 13px/18px Arial, sans-serif;
             }
        a { color: #360; }
        h3 { padding-top: 20px; }
        ol { margin:5px 0 15px 16px; padding:0; list-style-type:square; }
        div#media
          {
          position:absolute;
          bottom:150px;
          left:30px;
          }
        div#controls
          {
          margin-top:10px;
          margin-bottom:10px;
          }
        div#screenshots
          {
          position:absolute;
          top:50px;
          left:400px;
          }
        div#thumbs
          {
          position:absolute;
          bottom:30px;
          }
        
    </style>

<!-- Load swfobject, necessary for JW Player--> 
<script type="text/javascript" src="thirdparty/swfobject.js"></script>
<script type="text/javascript" src="thirdparty/JSFX_ImageZoom.js"></script>
<!--<script type="text/javascript" src="http://www.jeroenwijering.com/embed/swfobject.js"></script> -->
<!--<script type="text/javascript" src="http://www.javascript-fx.com/navigation/buttongroup/javascript/JSFX_ImageZoom.js"></script>-->

<script>    
"""

tail="""
    // a global reference to the JW Player
    var player
    var current_slide=1
    var total_slides=timecode.length
    
    function initialize(){
      document.getElementById("slide").src="screenshots/D1.jpg";
      var thumbsCode=""
      for (var i = 1; i < timecode.length+1; i++) {
        thumbsCode += "<img src='screenshots/D"+i+"-thumb.jpg' width='100' onclick='goToSlide("+i+")' onMouseOver='JSFX.zoomIn(this),slideTooltip("+i+")'  onMouseOut='JSFX.zoomOut(this),slideTooltipOff()' >"
        
        }
      document.getElementById("thumbs").innerHTML=thumbsCode;
      document.getElementById("thumbInfo").innerHTML=title;
      }
    
    // will be called when the playe is ready and give us a reference to var player
    function playerReady(obj) {
      var id = obj['id'];
      var version = obj['version'];
      var client = obj['client'];
      //alert('player '+id+' has been instantiated');
      player = document.getElementById(id);
      player.addModelListener("TIME","timeMonitor");
      //player.sendEvent("PLAY");
      };
              
    //Each 1/10s, get time position and decide what to do        
    function timeMonitor(obj){
      //alert(obj.position);
      for (var i = 0; i < timecode.length+1; i++) {
        if ((obj.position > timecode[i]) && (obj.position < timecode[i+1])){
          document.getElementById("slide").src="screenshots/D"+(i+1)+".jpg";
          current_slide=i+1;
        }
       }
    }  
    function goToSlide(slideNumber){
      //alert("You want slide number "+slideNumber);
      player.sendEvent('SEEK',timecode[slideNumber-1]); 
      }
    function nextSlide()
    {
    if (current_slide < total_slides)
      {
      document.getElementById("slide").src="screenshots/D"+(current_slide+1)+".jpg";
      try {goToSlide(current_slide+1)} catch(e) {/*pass*/}
      current_slide ++;
      }
    }
    function previousSlide()
    {
    if (current_slide > 1)
      {
      document.getElementById("slide").src="screenshots/D"+(current_slide-1)+".jpg";
      try {goToSlide(current_slide-1)} catch(e) {/*pass*/}
      current_slide --;
      }
    }
    function slideTooltip(thumbHovered)
      {
      document.getElementById("thumbInfo").innerHTML="N� "+ thumbHovered +" (t="+timecode[thumbHovered-1]+" s)";
      }
    function slideTooltipOff()
      {
      document.getElementById("thumbInfo").innerHTML=title;
      }
    function hello(){
      alert("Current slide: " + current_slide);
      }
</script>

   
</head>
<body onload="initialize()">
<!-- <p>Warnning: doesn't work locally, needs a server (at least http://localhost in URL)</p> -->
<!--  <h3 id="titre">Media (audio or video) :</h3> -->
  
    <div id="media">
    <!-- <embed  src="player.swf"  id="flashvideo" name="flashvideo" /> -->
    <a href="http://www.macromedia.com/go/getflashplayer">Get the Flash Player</a> to see this player.
    <script type="text/javascript">
        var jwplayer = new SWFObject("thirdparty/player.swf","flashvideo","328",playerHeight,"9","#FFFFFF");
        jwplayer.addParam("allowfullscreen","true");
        jwplayer.addParam("enablejs","true");
        jwplayer.addParam("allowscriptaccess","always");
        jwplayer.addParam("flashvars","file="+media+"&stretching=fill&autostart=true");
        jwplayer.write("media");    
    </script>  
    <div id="controls">
     <!-- <button type="button" onClick="hello()"> Action </button> -->
     <button type="button" onClick="previousSlide()"> << </button> 
     <button type="button" onClick="nextSlide()"> >> </button>
     <p id="thumbInfo"></p>
    </div>
    <div id="description">
    </div>
    </div>
    
    <div id="screenshots">
    <img id="slide"  width="95%"  src="ac-splash.png">
    </div>
    
    <div id="thumbs">
    </div>
    
</body>
</html>
"""