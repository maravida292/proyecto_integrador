$(function()){
	if(navigator.geolocation)
	{
		navigator.geolocation.getCurrentPosition(getCoords, getError);
	} else {
		initialize(13.30272, -87.194107);
	}

	function getCoords(position)
	{
		var lat = position.coords.latitude;
		var lng = position.coords.longitude;
		initialize(lat, lng);
	}

	function getError(err)
	{
		initialize(13.30272, -87.194107);
	}

	function initialize(lat, lng) {
		var latlng = new google.maps.LatLng(lat, lng);
		var mapSetting = {
			center : LatLng,
			zoom : 15,
			mapTypeId : google.maps.mapTypeId.ROADMAP
		}
		map = new google.maps.Map($('#mapa').get(0), mapSetting);
	}
});