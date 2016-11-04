var highlightColor = '#a9fcff';
var marriageColor = '#A9FFBD';
var selectedColor = '#f442dc';

// For interactive map
var disableClusterZoomLevel = 8;
var markerOpacity = 0.35;

queue()
    .defer(d3.csv, 'data/final_dataset_v5.csv')
    .await(makeMap);

function makeMap(error, single_entries) {

    var nested_data = d3.nest()
        .key(function(d) { return d.location_current; })
        .entries(single_entries);

    for (var i=0; i<nested_data.length; i++) {
        nested_data[i].latitude = nested_data[i].values[0].location_latitude;
        nested_data[i].longitude = nested_data[i].values[0].location_longitude;
        year_array = [];
        for (var c=0; c<nested_data[i].values.length; c++) {
            year_array.push(nested_data[i].values[c].time_year);
            nested_data[i].year_list = year_array.join();
        }
    }


    ////////////// Map Parameters //////////////
    var centreLatitude = 51.5;
    var centreLongitude = 0.12;
    var initialZoom = 10;


    var map = L.map('map', {
        zoomControl:true,
        maxZoom: 21,
        minZoom: 2,
    }).setView([centreLatitude, centreLongitude], initialZoom);


    // add basemap url here
    var mbUrl = ''

    var darkMap = L.tileLayer(mbUrl).addTo(map);
    $.getJSON("data/london_districts_latlong_with_centroids.json",function(borough_outlines){
        boroughLayer = L.geoJson( borough_outlines, {
          style: function(feature){
            return {
                color: "white",
                weight: 1,
                fillColor: 'none',
                fillOpacity: 0 };
            }
        }).addTo(map);
    });

    radiusScale = d3.scale.sqrt().domain([1, 20]).range([5, 20])
    marriageradiusScale = d3.scale.sqrt().domain([1, 20]).range([0, 20])

    function radius(){
        return radiusScale(d.values.length)
    }

    var MarriageCount = 0

    function marriageRadius(){
        d.Marriage = 0;
        for (var h=0; h<d.values.length; h++) {
            if(d.values[h].classification_wasTheMarriedWomensWorkDiscussedIncontextOfMotherhood === 'Yes'){
                d.Marriage += 1;

            }
        }
        return marriageradiusScale(d.Marriage);
    }

    allmarkers = new L.layerGroup();
    marriageGroup = new L.layerGroup();

    for (var i=0; i<nested_data.length; i++) {
        var d = nested_data[i];

        var marker = L.circleMarker(new L.LatLng(d.latitude, d.longitude), {
            radius: radius(),
            color: highlightColor,
            fillOpacity: markerOpacity,
        });

        var marker02 = L.circleMarker(new L.LatLng(d.latitude, d.longitude), {
            radius: marriageRadius(),
            color: marriageColor,
            fillOpacity: markerOpacity,
        });

        var tooltipContentDiv;
        function tooltipContent(){
            tooltipContentDiv = '<h2 id="tooltipContentDiv">Borough: '+d.key+'</h2>'+
                                '<p id="tooltipContentDiv">Records: '+ d.values.length+'</p>'+
                                '<p id="tooltipContentDiv">Years: '+ d.year_list+'</p>';

            return tooltipContentDiv;
        }

        marker.data = d

        marker02.on('click', function(){

        })

        marker.on('click', function(e){
            // marker.setStyle({color:'blue'})
            e.target.setStyle({color:selectedColor})
            $('.infoWindow').css('opacity', '0.9');
            $('.infoWindow').css('height', 'auto');
            $('.infoWindow').html(function(){
                sidebarContent = '<h1 id="tooltipContentDiv">'+e.target.data.key+'</h1>';

                for (var m=0; m< e.target.data.values.length; m++) {
                    sidebarContent +=
                                    "<h2>REPORT #"+ (m + 1) +"</h2>"+
                                    "<p>Location "+e.target.data.values[m].location_mohPlace+"</p>"+
                                    '<p id="years">'+ e.target.data.values[m].time_year +'</p>'+
                                    "<h3>Occupation tags:</h3>"+
                                    "<p>"+e.target.data.values[m].classification_occupation+"</p>"+
                                    "<p><a href='"+ e.target.data.values[m].source_url +"' target='_blank'>Link to report</a></p>"+
                                    "<p>"+e.target.data.values[m].contextText+"</p>"+
                                    '<hr>';

                };
                return sidebarContent;
            });
        })

        marker.on('popupclose', function(e){
            e.target.setStyle({color:highlightColor})
        })
        marker.bindPopup(tooltipContent());
        allmarkers.addLayer(marker);
        marriageGroup.addLayer(marker02);
    }
    map.addLayer(allmarkers);

    // Infowindow
    var infoContainer = L.Control.extend({
        options: {
            position: 'topright',
        },
        onAdd: function (map) {
            // create the control container with a particular class name
            var infoContainer = L.DomUtil.create('div', 'infoWindow');
            return infoContainer;
        }
    });
    map.addControl(new infoContainer());

    // Define base map layers
    var baseMaps = {
        "All": allmarkers,
        'Motherhood mentioned in the context of marriage': marriageGroup
    };

    layer_names = ["All", 'Marriage'];
    layer_urls = [allmarkers, marriageGroup];

    var overlayMaps = {};
    for (i=0; i<layer_names.length; i++) {
        var layer_name = layer_names[i];
        var overlayLayer = layer_urls[i];
        overlayDiv = ('<span style="width: 10px; ' +
        'height: 10px; -moz-border-radius: 5px; -webkit-border-radius: 5px; border-radius: 5px; border: 1px solid #FFF; float: left; margin-right: 0px; margin-left: 0px;' +
        'margin-top: 3px;"></span>' + layer_name);
        overlayMaps[overlayDiv] = overlayLayer;
    }

    // Add controls
    L.control.layers(
        baseMaps, null, {collapsed:false, position:"bottomleft"}
    ).addTo(map);

    // Add legend title
    jQuery(function($){$('.leaflet-control-layers-expanded').prepend(
        '<h3 style="color:white"; margin-top:0px !important>' + 'Layers' + '</h3>');
    });

}
