// ---  LEAFLET Basemap Tiles
var map = L.map('map', {
    center: [40.7019, 28.2848],
    zoom: 9,
    gestureHandling: true
})

//This is for executing <script> tag in the twitter embed HTML code.
// I am generating the Script tag since it repeats. 
map.on('popupopen', function() {

    var tag = document.createElement("script");
    tag.src = "https://platform.twitter.com/widgets.js";
    tag.charset = "utf-8"

    document.getElementsByTagName("head")[0].appendChild(tag);
});

// Collapse Accordion when map is touched or dragged
map.on('mousedown', function(e) {
    console.log("on map");
    $('.collapse').removeClass('show')
    $('.d-block').addClass('collapsed')
    $('.d-block').attr('aria-expanded', 'false')
});

$('#map').on('touchstart', function(e) {
    $('.collapse').removeClass('show')
    $('.d-block').addClass('collapsed')
    $('.d-block').attr('aria-expanded', 'false')
})

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: '© <a href="https://www.mapbox.com/about/maps/" style="color:#ffe000">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright"  style="color:#ffe000">OpenStreetMap</a> <strong><a  style="color:#ffe000" href="https://www.mapbox.com/map-feedback/" target="_blank">Improve this map</a></strong>',
    tileSize: 512,
    maxZoom: 14,
    minZoom: 8,
    zoomOffset: -1,
    id: 'mapbox/dark-v10',
    accessToken: 'pk.eyJ1IjoiY2Fua2FkaXIiLCJhIjoiY2pteXplNnEzMHF3YTNrcGx0dGd4MmJrdiJ9.zbhQ39YIdfZufTljuTSl1w'
}).addTo(map);

// Style Object for the general Polygon Styline
function style(data) {
    return {
        fillColor: '#ffe000', // Here is the categorical coloring.
        color: '#ffffff',
        weight: 0.15,
        opacity: 1,
        fillOpacity: 0.7
    };
}

// Style Object for the Mask Style
function style_mask() {
    return {
        fillColor: 'white', // Here is the categorical coloring.
        color: '#ffffff',
        weight: 0.05,
        opacity: 1,
        fillOpacity: 0.5
    };
}

// Polygons
function generatePolygon(date, L) {

    api_path = `https://prattsavi.github.io/Musilaj/apis/${date}.geojson`

    //Open 
    let geoJsonLayer = $.getJSON(api_path, function(data) {

        let geoJsonLayer = L.geoJSON(data, {
            style: style,
        }).addTo(map);

        //assign id = feature to polygons
        geoJsonLayer.eachLayer(function(layer) {
            layer._path.id = 'feature-select';
        });
        return geoJsonLayer;
    });
    return geoJsonLayer;
};

// Points
function del_all() {
    $("#feature-select").remove()
    $("#mask-select").remove()
};


// Generate Tweeter
function generateTws(data, L) {

    var div_circle = L.divIcon({
        className: 'circle',
    });

    data.forEach(function(d, i) {

        var popup_content = d.embed.split('<script')[0]; //Remove script tag

        var marker = L.marker([d.lat, d.lon], {
            icon: div_circle,
        }).addTo(map);

        marker.bindPopup(popup_content);
    });
};

function maskLayer(mask, pos, L) {

    data = mask.features.filter(d => d.properties.taraf != pos);

    let geoJsonLayer = L.geoJSON(data, {
        style: style_mask,
    }).addTo(map);

    //assign id = feature to polygons
    geoJsonLayer.eachLayer(function(layer) {
        layer._path.id = 'mask-select';
    });
}

let github = 'https://raw.githubusercontent.com/PrattSAVI/Musilaj/main';

let twit_path = `${github}/Data/tw/Tweets.json`;
let mask_path = `${github}/Data/mask_3.geojson`;
let date_pos = `${github}/apis/dates.json`;


// ------------------- WORK WITH DATA STARTS HERE--------------------------


$.getJSON(date_pos, function(data) { // Dates JSON
    $.getJSON(mask_path, function(mask) { // Mask geoJSON

        //extract unique dates from the json file
        let dates = data.map(({
            date: value
        }) => value);

        //Insert  dates into dropdown & select first
        dates.forEach(function(d, i) {
            $('#date-selector').append(`<option value="${d}">${d}</option>`);
            $("#date-selector").prop("selectedIndex", dates.length - 1); // Select first
        });

        //Create Initial musilaj  polygon
        let sdate = dates[dates.length - 1];
        let geoJsonLayer = generatePolygon(sdate, L);

        //Initial Mask polygon
        /*
        let pos = data.filter(d => d.date == sdate)[0].pos;
        //maskLayer(mask, pos, L);
        */


        // Add Twitter Points -> This will not be removed.
        $.getJSON(twit_path, function(twit) {
            generateTws(twit, L);
        });

        // Create the filter -> Filter data based on dropdown.
        $('#date-selector').change(function() {

            //Delete all musilaj & mask geometry
            del_all()

            //If that fails, delete all paths. 
            var feats = document.getElementById('feature-select')
            if (feats != null) {
                $('path').remove()
            }

            //Generate Polygon with new dates
            this_date = $(this).val();
            geoJsonLayer = generatePolygon(this_date, L);

            //Generate mask
            /*
            let pos = data.filter(d => d.date == this_date)[0].pos;
            maskLayer(mask, pos, L);
            */

        });
    });
})