export function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

// ZAMIANA user_demo → null
export const username = getCookie("username"); 

export function initUserDisplay() {
  if (!username) return; // jeśli nie ma ciasteczka, nie wyświetlaj lub ukryj
  document.getElementById("usernameDisplay").innerText = username;
}
//Obsługa ciasteczek do pobrania username. 

//Funkcja initUserDisplay() wyświetla nazwę użytkownika. 