# ************************************************************
#
# A file with HTML and Javascript chuncks for audiovideocours
# (to help create an html/flash export)
#
#    (c) ULP Multimedia 2006 - 2007 
#     Developer : francois.schnell [AT ulpmm.u-strasbg.fr]
#
#*************************************************************
"""
Nothing special. HTML chunks used in generating recordings.html in particular. 
"""

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
        div#title
          {
          align:center;
          }
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
          left:30%;
          height:70%;
          }
        div#thumbs
          {
          position:absolute;
          bottom:10px;
          width:97%;
          height:100px;
          overflow:scroll;
          }        
    </style>

<!-- Load swfobject, necessary for JW Player--> 
<script type="text/javascript" src="thirdparty/swfobject.js"></script>

<script>    
"""
def tail(delayMediaSlides=0,message=""):
    """ Returns HTML tails depending on arguments (delay for media/slides)"""
    tail="""
        // a global reference to the JW Player
        var player
        var current_slide=1;
        var total_slides=timecode.length;
        delay="""+str(delayMediaSlides)+"""; //estimated delay between encoder startup and slides
        
        function initialize(){
          document.getElementById("slide").src="screenshots/D1.jpg";
          var thumbsCode=""
          for (var i = 1; i <= timecode.length+1; i++) {
            thumbsCode += "<img src='screenshots/D"+i+"-thumb.jpg' width='100' onclick='goToSlide("+eval(i-1)+")' onMouseOver='slideTooltip("+i+")'  onMouseOut='JSFX.zoomOut(this),slideTooltipOff()' >"
            
            }
          document.getElementById("thumbs").innerHTML=thumbsCode;
          <!-- document.getElementById("thumbInfo").innerHTML=title; -->
          document.getElementById("title").innerHTML=title;
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
          for (var i = 0; i < timecode.length; i++) {
            if ((obj.position > (timecode[i]+delay)) && (obj.position < (timecode[i+1]+delay))){
              document.getElementById("slide").src="screenshots/D"+(i+2)+".jpg";
              current_slide=i+1;
            }
            else if (obj.position>timecode[timecode.length-1]+delay){document.getElementById("slide").src="screenshots/D"+(i+2)+".jpg";current_slide=i+1;}
           }
        }  
        function goToSlide(slideNumber){
          //alert("You want slide number "+slideNumber);
          player.sendEvent('SEEK',timecode[slideNumber-1]+delay); 
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
          <!-- document.getElementById("thumbInfo").innerHTML="N "+ thumbHovered +" (t="+timecode[thumbHovered-1]+" s)"; -->
          }
        function slideTooltipOff()
          {
          <!-- document.getElementById("thumbInfo").innerHTML=title; -->
          }
        function hello(){
          alert("Current slide: " + current_slide);
          }
    </script>
    
       
    </head>
    <body onload="initialize()">
    <!-- <p>Warnning: doesn't work locally, needs a server (at least http://localhost in URL)</p> -->
    <!--  <h3 id="titre">Media (audio or video) :</h3> -->
    <p style="color:white; background-color: #CC0000; text-align:center;padding: 5px; border: 1px solid black; "> 
    Pr&eacute;visualisation des m&eacute;dias avant publication et mise en forme. 
    Appuyez sur le bonton "publier" du logiciel client AudioVideoCours si vous souhaitez mettre en ligne cet enregistrement.</p>
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
        """+message+"""
        </div>
        </div>
        
        <div id="screenshots">
        <img id="slide"  width="95%"  src="screenshots/D1.jpg">
        </div>
        
        <div id="thumbs" style="width:90%; overflow:scroll;">
        
        </div>
    
        
    </body>
    </html>
    """
    return tail