import { initUserDisplay } from "./user.js";
import { initLayerSelector } from "./mapControls.js";
import { initSearch } from "./search.js";
import { initPanel } from "./panel.js";
import {loadForecast} from "./forecast.js";
import { autoLoadLastCities } from "./search.js";
import { loadAlertsForCities } from "./alerts.js";


initUserDisplay();
initLayerSelector();
initSearch();
initPanel();
autoLoadLastCities();
//punkt startowy modułu