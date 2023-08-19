
////////////////////Please leave this notice////////////////////
//
//	DropDown Menu 1.1
//	By Evgeny Novikov (java@aladin.ru)
//	http://java.skyteam.ru
//	It works only with IE5.0(++) and Netscape6.0(++)
//	Free to use!
//
////////////////////Last modified 2002-06-07////////////////////

var ve=false;	// true - the main menu runs vertically, false - horizontally
//	After change, modify same values in your *.css file:
var tdColor="#FFFFFF";		// menu item text color
var tdBgColor="#993366";	// menu item background color
var hlColor="#000000";		// highlight text color
var hlBgColor="#FFFFBB";	// highlight background color
var md=250;
var ti=-1;
var oTd=new Object;
oTd=null;
function doMenu(td){
	clearTimeout(ti);
	td.style.backgroundColor=hlBgColor;
	td.style.color=hlColor;
	var i;
	var sT="";
	var tda=new Array();
	tda=td.id.split("_");
	if(oTd!=null){
		var tdo=new Array();
		tdo=oTd.id.split("_");
		for(i=1;i<tdo.length;i++){
			sT+="_"+tdo[i];
			if(tdo[i]!=tda[i]){
				document.getElementById("td"+sT).style.backgroundColor=tdBgColor;
				document.getElementById("td"+sT).style.color=tdColor;
				if(document.getElementById("tbl"+sT)!=null)
					document.getElementById("tbl"+sT).style.visibility="hidden";
			}
		}			
	}
	oTd=td;
	sT="tbl";
	for(i=1;i<tda.length;i++)
		sT+="_"+tda[i];
	if(document.getElementById(sT)!=null)
           // Вывод подменю для второго ряда
           // Добавлено 04.01.2016
           if (sT.localeCompare("tbl_9")==0) // 9-й пункт меню (начало 2-го ряда)
               { // document.getElementById(sT).style = "position:relative; top:2px; left:5px; visibility:visible;";
                 document.getElementById(sT).style.position = "relative";
                 document.getElementById(sT).style.top = "2px";
                 document.getElementById(sT).style.left = "5px";
 		 document.getElementById(sT).style.visibility="visible";
                  }   
           else 
           // Конец добавления
           if (sT.localeCompare("tbl_10")==0) // 10-й пункт меню (начало 2-го ряда)
               { // document.getElementById(sT).style = "position:relative; top:2px; left:5px; visibility:visible;";
                 document.getElementById(sT).style.position = "absulute";
                 document.getElementById(sT).style.top = "32px";
                 document.getElementById(sT).style.left = "115px";
 		 document.getElementById(sT).style.visibility="visible";
                  }   
           else 
           // Конец добавления
		document.getElementById(sT).style.visibility="visible";

}
function clearMenu(){
	if(oTd!=null){
		var tdo=new Array();
		tdo=oTd.id.split("_");
		var sT="";
		for(var i=1;i<tdo.length;i++){
			sT+="_"+tdo[i];
			document.getElementById("td"+sT).style.backgroundColor=tdBgColor;
			document.getElementById("td"+sT).style.color=tdColor;
			if(document.getElementById("tbl"+sT)!=null)
				document.getElementById("tbl"+sT).style.visibility="hidden";
		}
		oTd=null;			
	}
}
function runMenu(strURL){
	location.href=strURL;
}
var tt="";
var sT="";
var pT=new Array();
var tA=new Array();
function getCoord(st){
	tA=st.split("_");
	if(tA.length>2){
		tA=tA.slice(0,-1);
		tt=tA.join("_");
		return (document.getElementById("tbl"+tt).offsetTop+document.getElementById("td"+st).offsetTop+4)+"px;left:"+
			(document.getElementById("tbl"+tt).offsetLeft+document.getElementById("td"+st).offsetWidth-2)+"px'>";
	}
	var p1=ve?document.getElementById("td"+st).offsetTop+4:document.getElementById("td"+st).offsetHeight-2;
	var p2=ve?document.getElementById("mainmenu").offsetWidth-4:document.getElementById("td"+st).offsetLeft+5;
	return (document.getElementById("mainmenu").offsetTop+p1)+"px;left:"+(document.getElementById("mainmenu").offsetLeft+p2)+"px'>";
}
if(document.getElementById){
var g1=ve?"":"<tr>";
var g2=ve?"":"</tr>";
var v1=ve?"<tr>":"";
var v2=ve?"</tr>":"";
var v3=ve?" style='float:left'>":">";
var sH="<table class='menu' id='mainmenu' cellspacing='0'"+v3+g1;
var p=0;
var j=0;
while(eval("typeof(td_"+ ++j +")!='undefined'")){
        if (j==9) //Если девятый элемент - добавлено (05.07.2005)
           { sH+="</tr><tr>"; } //Конец добавления
	sH+=v1+"<td id='td_"+j+"' onmouseover='doMenu(this)' onmouseout=\"ti=setTimeout('clearMenu()',md)\"";
	sH+=(eval("typeof(url_"+j+")!='undefined'"))?" onclick=\"runMenu('"+eval("url_"+j)+"')\">":">";
	sH+=eval("td_"+j)+"</td>"+v2;
	if (eval("typeof(td_"+j+"_1)!='undefined'"))
		pT[p++]="_"+j;
}
sH+=g2+"</table>";
document.write(sH);
for(var q=0;typeof(pT[q])!="undefined";q++){
	sT=pT[q];
	sH="";
	j=0;
	sH+="<table class='menu' id='tbl"+sT+"' cellspacing='0' style='top:"+getCoord(sT);
	while(eval("typeof(td"+sT+"_"+ ++j +")!='undefined'")){
		sH+="<tr><td id='td"+sT+"_"+j+"' onmouseover='doMenu(this)' onmouseout=\"ti=setTimeout('clearMenu()',md)\"";
		sH+=(eval("typeof(url"+sT+"_"+j+")!='undefined'"))?" onclick=\"runMenu('"+eval("url"+sT+"_"+j)+"')\">":">";
		sH+=eval("td"+sT+"_"+j)+"</td></tr>";
		if (eval("typeof(td"+sT+"_"+j+"_1)!='undefined'"))
			pT[p++]=sT+"_"+j;
	}
	sH+="</table>";
	document.write(sH);
}
//document.getElementById("mainmenu").style.visibility="visible";
}
else document.write("<p>This page uses DHTML and DOM, but your browser doesn't support them.</p>");

function smena(o, width, height, top){
	o.style.left = "0"; 
	o.style.right = "0"; 
	o.style.top = top; 
	o.style.margin = "0 auto";
	o.style.width = width; 
	o.style.height = height; 
}

window.onload=function() {
  /*if ((screen.width)>=1024)
        {
          D = screen.width;
          C = 575;
          switch (screen.width)
          {
            case 1024: C = 192; break;
            case 1152: C = 130; break;
            case 1280: C = 68; break;
            case 1360: C = 24; break;
          } 
          A = new String ((D-765)/2);
          B = (D)/2+C; //575;
          A1 = new String (B);
          mnu.style.left = A+"px"; 
          zag.style.left = A+"px"; 
          animate.style.left = A1+"px"; 
          document.getElementById("top").style.left = A+"px";
          bottom.style.left = A+"px"; 
        }                              */
	
  /* if (screen.width<=1360) 
      animate.style.visibility="visible"; */ 
	  	
	animate.style.left = "730px";
	smena(zag, "785px", "82px", "2px");
	smena(mnu, "785px", "32px", "87px");
	smena(document.getElementById("top"), "775px", "70px", "120px");
	smena(bottom, "775px", "auto", "192px");
		
	zag.style.visibility="visible"; 
	mnu.style.visibility="visible";
	document.getElementById("mainmenu").style.visibility="visible";
	animate.style.visibility="visible";
	document.getElementById("top").style.visibility="visible";
	bottom.style.visibility="visible"; 	
}