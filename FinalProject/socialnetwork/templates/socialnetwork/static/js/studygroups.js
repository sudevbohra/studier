

function initialize() {
  var mapCanvas = document.getElementById('map-canvas');
    var mapOptions = {
      center: new google.maps.LatLng(40.4430939,-79.942309) //CMU Campus,
      zoom: 17,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    var map = new google.maps.Map(mapCanvas, mapOptions);
    map.set('styles', [
        
  {
    featureType: 'poi.school',
    elementType: 'geometry',
    stylers: [
      { hue: '#f29b10' },
      { lightness: -15 },
      { saturation: 99 }
    ]
  }
])};
  // Try HTML5 geolocation
document.getElementById("location").onclick = function() {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = new google.maps.LatLng(position.coords.latitude,
                                       position.coords.longitude);

      var marker = new google.maps.Marker({
      position: pos,
      map: map,
      icon:'http://cdn-img.easyicon.net/png/40/4058.png'
    });

     
    }, function() {
      handleNoGeolocation(true);
    });
  }
}

google.maps.event.addDomListener(window, 'load', initialize);