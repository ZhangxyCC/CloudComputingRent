var apigClient = apigClientFactory.newClient({
	accessKey: '',
    secretKey: ''
 });
var Words = document.getElementById("words");
var TalkWords = document.getElementById("talkwords");
var TalkSub = document.getElementById("talksub");
var res;
var contactBtn = document.getElementById("contactButton");
var chooseIndex = 0;
TalkSub.onclick = function(){

    var params = {
        'Origin' : "https://frontend-hw3.s3.amazonaws.com",
    };
    var body = {
        
    };
    var additionalParams = {
        queryParams:{
            'q': TalkWords.value
        }
    };
           
    apigClient.propertySearchGet(params, body, additionalParams).then( function(result){
        // console.log(result);
                    
        res = result['data'];
       var fulfilled = res.includes("House");
        if(fulfilled){
        	res = JSON.parse(res)["Houses"];
        	for (i = 0; i < res.length; i++) {
  				str += "<div class='atalk'>";
  				// <button onlick="houseButton($index)>street_name</button>"
  				str += "<button onclick=\"houseButton(" + i + ")\" >" + res[i]["_source"]["street"] + "</button>";
  				str += "</div>";
			}

        }else{
            str = '<div class="atalk"><span>' + res +'</span></div>';
        }
                   // console.log(res)
                   // str = '<div class="atalk"><span>' + res +'</span></div>';

        Words.innerHTML = Words.innerHTML + str;

            }).catch( function(result){
               //Add error callback code here.
              res = "Sorry, API Gateway is not responding";
            });
        // var str = "";
        if(TalkWords.value == ""){
            alert("Not null");
            return;
        }
        var str = '<div class="btalk"><span>' + TalkWords.value +'</span></div>';
        Words.innerHTML = Words.innerHTML + str;
        TalkWords.value = "";
    }       
console.log("aa");
document.onkeyup = function(e) {
  // 兼容FF和IE和Opera
  var event = e || window.event;
  var key = event.which || event.keyCode || event.charCode;
  if (key == 13) {
    TalkSub.click();
  }
};
var showButton = document.getElementById("bt1");
// var submitButton = document.getElementById("bt2");
// var clearButton = document.getElementById("bt3");
// var submitDiv = document.getElementById("submitProperty");
// var clearDiv = document.getElementById("welcome");
// showButton.onclick = function(){
// 	showDiv.style.visibility="visible";
// 	submitDiv.style.visibility="hidden";
// 	clearDiv.style.visibility="hidden";
// };

// submitButton.onclick = function(){
// 	showDiv.style.visibility="hidden";
// 	submitDiv.style.visibility="visible";
// 	clearDiv.style.visibility="hidden";
// };

// clearButton.onclick = function(){
// 	showDiv.style.visibility="hidden";
// 	submitDiv.style.visibility="hidden";
// 	clearDiv.style.visibility="visible";
// };

//google map
function nice(lat, lng) {
	var map;
	var uluru = {lat: parseFloat(lat), lng: parseFloat(lng)};
  // The map, centered at Uluru
  	var map = new google.maps.Map(
      document.getElementById('map_canvas'), {zoom: 10, center: uluru});
  // The marker, positioned at Uluru
  	var marker = new google.maps.Marker({position: uluru, map: map});
}

function houseButton(index){
	chooseIndex = index;
	var propertyDiv = document.getElementById("showProperty");
	propertyDiv.style.display = "inline";	
	//render the right part of page


	//render DescriptionP
	var DescriptionP = document.getElementById("DescriptionP");
	var innterVal = res[index]["_source"]["homeDescription"];
	DescriptionP.innerHTML = innterVal;

	//render image
	var img = document.getElementById("propertyImg");
	img.src = res[index]["_source"]["images"][0];

	//render bedroom number
	var bedroomSpan = document.getElementById("bedroomSpan");
	bedroomSpan.innerHTML = res[index]["_source"]["bedrooms"];

	//render bathroom number
	var bathroomSpan = document.getElementById("bathSpan");
	console.log("bathrooms:" + res[index]["_source"]["bathrooms"]);
	bathroomSpan.innerHTML = res[index]["_source"]["bathrooms"];

	//render property name(street)
	var property = document.getElementById("propertyN");
	console.log(res[index]["_source"]);
	console.log("property:" + res[index]["_source"]["street"]);
	property.innerHTML	= res[index]["_source"]["street"];

	//render appliances
	var appliance = res[index]["_source"]["appliances"];
	if(appliance != null){
		console.log("app");
		var appliancesList = appliance.split(",");
		var appliancesUL = document.getElementById("appliancesUL");
		for(var i = 0; i < appliancesList.length; i++){
			var li = document.createElement("li");
  			li.appendChild(document.createTextNode(appliancesList[i]));
  			appliancesUL.appendChild(li);
		}
	}
	console.log("appliance: " + appliancesList);
	console.log(res[index]["_source"]["latitude"]);
	console.log(res[index]["_source"]["longitude"]);
	var lat = res[index]["_source"]["latitude"];
	var lng = res[index]["_source"]["longitude"];
	nice(lat, lng);

	// change money
	var money = document.getElementById("moneySpan");
	money.innerHTML = "$" + res[index]["_source"]["rentzestimate"];
}

contactBtn.onclick = function(){
	var phoneN = prompt("Please enter your phone number", "+19876543"); //将输入的内容赋给变量 name ，

    if (phoneN)//如果返回的有内容
    {
        alert("The information of the owner has been sent to your phone");
    }

    var params = {
        'Origin' : "https://frontend-hw3.s3.amazonaws.com",
        'phonenum': phoneN,
         'aptid': res[chooseIndex]["_source"]["aptid"]
         
    };
    var body = {
        
    };
   
    var additionalParams = {
        queryParams:{
           'phonenum': phoneN,
           'aptid': res[chooseIndex]["_source"]["aptid"]
        }
    };
     console.log(additionalParams)
     apigClient.contactGet(params, body, additionalParams).then(function(result){
       
    }).catch( function(result){
                       //Add error callback code here.
          res = "Upload failed.";
    });
       

}



