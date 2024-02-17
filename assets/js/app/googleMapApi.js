var map;
var directionsRenderer;
var directionsService;
var distanceMatrixService;
var iconBase;
var icons;
var features;
var titles;
var mapRequests;
var markersArray = [];
var infowindowsArray = [];

function initMap() {
  // Instantiate a directions service.
  directionsService = new google.maps.DirectionsService();
  distanceMatrixService = new google.maps.DistanceMatrixService();

  var tsmc12 = new google.maps.LatLng(24.77040602925178, 121.01221589102596);
  var mapOptions = {
    zoom: 12,
    center: tsmc12,
    disableDefaultUI: true,
    styles: [{
      featureType: "poi",
      elementType: "labels",
      stylers: [
        { visibility: "off" }
      ]
    }],
  };
  map = new google.maps.Map(document.getElementById("googleMap"), mapOptions);

  // Create a renderer for directions and bind it to the map.
  directionsRenderer = new google.maps.DirectionsRenderer();
  directionsRenderer.setMap(map);
  directionsRenderer.setPanel(document.getElementById('directionsPanel'));
  iconBase = "https://developers.google.com/maps/documentation/javascript/examples/full/images/";
  icons = {
    parking: {
      icon: iconBase + "parking_lot_maps.png",
    },
  };
  titles = ["停車場 A", "停車場 B", "停車場 C", "停車場 D"];
  features = [
    {
      //台積電五廠
      position: new google.maps.LatLng(24.774288870613738, 120.99776290354495),
      type: 'parking',
    },
    {
      //台積電十二廠P8西二停車場
      position: new google.maps.LatLng(24.76622815305906, 121.008697373479),
      type: 'parking',
    },
    {
      //台積電八廠
      position: new google.maps.LatLng(24.76308236526949, 121.02037163428783),
      type: 'parking',
    },
    {
      //台積電 Parking
      position: new google.maps.LatLng(24.778357076464278, 120.98946387556606),
      type: 'parking',
    },
  ];
  mapRequests = {
    travelMode: 'DRIVING',
    drivingOptions: {
      departureTime: new Date(Date.now()),
      //bestguess, pessimistic, optimistic
      trafficModel: 'bestguess',
    },
    unitSystem: google.maps.UnitSystem.METRIC,
  };
  // 計算距離與時間並繪製圖標
  getDistanceMatrix(map.center, features);

  const currentMarker = new google.maps.Marker({
    position: map.center,
    map: map,
    draggable: true,
  });
  currentMarker.addListener('dragend', (event) => {
    map.setCenter(event['latLng']);
    getDistanceMatrix(map.center, features);
  });


};

function getDistanceMatrix(start, features) {
  var destinationsArray = [];
  for(var i = 0; i<features.length; i++){
    destinationsArray.push(features[i].position);
  }
  const distanceMatrixRequests = {
    origins: [start],
    destinations: destinationsArray,
  };
  var totalRequests = [distanceMatrixRequests, mapRequests].reduce(function (r, o) {
    Object.keys(o).forEach(function (k) { r[k] = o[k]; });
    return r;
  }, {});
  console.log(totalRequests);
  distanceMatrixService.getDistanceMatrix(totalRequests, (response, status) => {
    if (status == 'OK') {
      const origins = response.originAddresses;
      const destinations = response.destinationAddresses;
      for (var i = 0; i < origins.length; i++) {
        var results = response.rows[i].elements;
      }
      createMarkers(start, features, results);
    } else { console.log('The Distance Matrix service failed.'); }
  });
};

function createMarkers(start, features, results) {
  // Create markers.
  for (let i = 0; i < features.length; i++) {
    const contentString =
      '<div id="mapContent">' +
      '<div id="mapSiteNotice">' +
      "</div>" +
      '<h6 id="mapfirstHeading">' + titles[i] + '</h6>' +
      '<div id="mapBodyContent">' +
      '<p>' + results[i]['duration_in_traffic']['text'] + ' 可達，' +
      '距離' + results[i]['distance']['text'] + ' </p>' +
      '</div>' +
      '</div>';
    const infowindow = new google.maps.InfoWindow({
      content: contentString,
      ariaLabel: titles[i],
    });

    const marker = new google.maps.Marker({
      position: features[i].position,
      icon: icons[features[i].type].icon,
      map: map,
      title: titles[i],
    });

    infowindow.open({
      anchor: marker,
      map,
    });
    marker.addListener("click", () => {
      for(let i=0; i<markersArray.length;i++){
        // markersArray[i].setVisible(false);
        infowindowsArray[i].close();
      }
      // marker.setVisible(true);
      infowindow.open({
        anchor: marker,
        map,
      });
      calcRoute(start, marker.position);
    });

    infowindowsArray.push(infowindow);
    markersArray.push(marker);
  };
};

function calcRoute(start, end) {
  const directionsRequests = {
    origin: start,
    destination: end,
  }
  var totalRequests = [directionsRequests, mapRequests].reduce(function (r, o) {
    Object.keys(o).forEach(function (k) { r[k] = o[k]; });
    return r;
  }, {});

  // Route the directions and pass the response to a
  // function to create markers for each step.
  directionsService.route(totalRequests, function (response, status) {
    if (status == "OK") {
      directionsRenderer.setDirections(response);
    }
  });
};