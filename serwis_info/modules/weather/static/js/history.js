import { username } from "./user.js";

export async function loadHistory() {
  console.log("USERNAME:", username);

  const res = await fetch(`/weather/api/history/${username}`);
  if (!res.ok) return;

  const data = await res.json();
  const ul = document.getElementById("historyList");
  ul.innerHTML = "";

  data.forEach(item => {
    const li = document.createElement("li");
    li.innerText = item.city;
    ul.appendChild(li);
  });
}


//Ładuje historię wyszukiwań z backendu i wstawia do <ul id="historyList">. 
//integracje- uzywane przez panel.js i search.js