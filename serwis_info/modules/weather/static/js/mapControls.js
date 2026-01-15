import { layers, legends, baseLayer } from "./mapLayers.js";

export const map = L.map("map", { center: [52.0, 19.0], zoom: 6, layers: [baseLayer] });


//aktualizuje mapę, gdy użytkownik zaznacza / odznacza checkboxy.
export function updateLayers() {
  //usuwamy by było tylko to co zaznaczone
  Object.values(layers).forEach(layer => map.removeLayer(layer));

  //sprawdzamy co zaznaczone
  const checked = Array.from(document.querySelectorAll('input[name="weatherLayer"]:checked'));
  //przygotowanie legendy
  const legendContainer = document.getElementById("legendContainer");

  legendContainer.innerHTML = "";

  checked.forEach(chk => {
    const layer = layers[chk.value];
    if (layer) map.addLayer(layer);
    legendContainer.innerHTML += legends[chk.value] + "<br/>";
  });
}




//panel wyboru warstw
export function initLayerSelector() {
  document.getElementById("layerSelector").innerHTML = `
    <label><input type="checkbox" name="weatherLayer" value="temp"> Temperatura</label>
    <label><input type="checkbox" name="weatherLayer" value="rain"> Opady</label>
    <label><input type="checkbox" name="weatherLayer" value="clouds"> Zachmurzenie</label>
    <label><input type="checkbox" name="weatherLayer" value="wind"> Wiatr</label>
  `;

  //eventy
  document.querySelectorAll('input[name="weatherLayer"]').forEach(chk => {
    chk.addEventListener("change", updateLayers);
  });

  updateLayers();
}
