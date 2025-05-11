
const NO_FLY_ZONES = [
    { min_lon: 13.182460, max_lon: 13.214460, min_lat: 55.702952, max_lat: 55.720952 },
    { min_lon: 13.197878, max_lon: 13.229878, min_lat: 55.708623, max_lat: 55.726623 }
];

function mapToSVGCoords(lon, lat) {
  const x_osm_lim = [13.143390664, 13.257501336];
  const y_osm_lim = [55.678138854000004, 55.734680845999996];

  const x_svg_lim = [212.155699, 968.644301];
  const y_svg_lim = [103.68, 768.96];

  const x_ratio = (x_svg_lim[1] - x_svg_lim[0]) / (x_osm_lim[1] - x_osm_lim[0]);
  const y_ratio = (y_svg_lim[1] - y_svg_lim[0]) / (y_osm_lim[1] - y_osm_lim[0]);

  const x = x_ratio * (lon - x_osm_lim[0]) + x_svg_lim[0];
  const y = y_ratio * (y_osm_lim[1] - lat) + y_svg_lim[0]; // Notice: y is flipped for SVG

  return { x, y };
}

function halve_zone(zone) {
  const center_lon = (zone["min_lon"] + zone["max_lon"])/2;
  const center_lat = (zone["min_lat"] + zone["max_lat"])/2;

  const half_width = (zone["max_lon"] - zone["min_lon"])/4;
  const half_height = (zone["max_lat"] - zone["min_lat"])/4;

  return {
    "min_lon": center_lon - half_width,
    "max_lon": center_lon + half_width,
    "min_lat": center_lat - half_height,
    "max_lat": center_lat + half_height,
  }

}

function drawAllNoFlyZones() {
  const doc = document.getElementById("map");
  const doc_svg = doc.getSVGDocument();
  const svg = doc_svg.getElementById("map-svg");

  NO_FLY_ZONES.forEach(zones => {
    const zone = halve_zone(zones);
    const topLeft = mapToSVGCoords(zone.min_lon, zone.max_lat);
    const bottomRight = mapToSVGCoords(zone.max_lon, zone.min_lat);

    const width = bottomRight.x - topLeft.x;
    const height = bottomRight.y - topLeft.y;

    const rect = doc_svg.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("x", topLeft.x);
    rect.setAttribute("y", topLeft.y);
    rect.setAttribute("width", width);
    rect.setAttribute("height", height);
    rect.setAttribute("fill", "orange");
    rect.setAttribute("opacity", "0.5");
    rect.setAttribute("stroke", "red");
    rect.setAttribute("stroke-width", "1");
    svg.appendChild(rect);
  });
}

document.getElementById("map").addEventListener("load", () => {
    drawAllNoFlyZones();
});