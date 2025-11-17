export function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

export const username = getCookie("username") || "user_demo";

export function initUserDisplay() {
  document.getElementById("usernameDisplay").innerText = username;
}
