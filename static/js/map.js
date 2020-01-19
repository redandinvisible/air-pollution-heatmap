function makeGraphs(error, recordsJson) {

    var drawMap = function(data){
        alert("drawing map");

        var baseLayer = L.tileLayer(
            'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
                attribution: '...',
                maxZoom: 18
            }
        );

        var cfg = {
            // radius should be small ONLY if scaleRadius is true (or small radius is intended)
            // if scaleRadius is false it will be the constant radius used in pixels
            "radius": 2,
            "maxOpacity": .8,
            // scales the radius based on map zoom
            "scaleRadius": true,
            // if set to false the heatmap uses the global maximum for colorization
            // if activated: uses the data maximum within the current map boundaries
            //   (there will always be a red spot with useLocalExtremas true)
            "useLocalExtrema": true,
            // which field name in your data represents the latitude - default "lat"
            latField: 'lat',
            // which field name in your data represents the longitude - default "lng"
            lngField: 'lng',
            // which field name in your data represents the data value - default "value"
            valueField: 'count'
        };


        var heatmapLayer = new HeatmapOverlay(cfg);

        var map = new L.Map('map-canvas', {
            center: new L.LatLng(54.57206, -5.80078),
            zoom: 6,
            layers: [baseLayer, heatmapLayer]
        });

        heatmapLayer.setData(testData);

    };

    //Draw Map
    drawMap();
};