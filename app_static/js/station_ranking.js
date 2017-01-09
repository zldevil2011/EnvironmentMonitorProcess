// if (typeof jQuery === 'undefined') {
//   throw new Error('Ranking\'s JavaScript requires jQuery')
// }
var xhr = new XMLHttpRequest();
var url = "/station_ranking/";
loadXMLDoc(url);
function loadXMLDoc(url) {
    xmlhttp=null;
    try{
        xmlhttp=new XMLHttpRequest1();
    }catch (e){
        try{
            xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }catch (e){

        }
    }
    if (xmlhttp!=null)
    {
        xmlhttp.onreadystatechange=state_Change;
        xmlhttp.open("GET",url,true);
        xmlhttp.send(null);
    }
    else {
        postMessage("error");
    }
}

function state_Change(){
    if (xmlhttp.readyState==4){// 4 = "loaded"
        if (xmlhttp.status==200){// 200 = OK
            // ...our code here...
            var text = xmlhttp.responseText;
            // console.log(JSON.parse(text));
            postMessage(JSON.parse(text));
        }
        else{
            console.log("Problem retrieving XML data");
            // alert("Problem retrieving XML data");
        }
    }
}
