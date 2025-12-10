/* ===========================
   THEME TOGGLE - Dark/Light Mode
   Obsługa przełączania trybu jasnego i ciemnego
   =========================== */

(function() {
  'use strict';

  // Funkcja do ustawiania trybu
  function setTheme(theme) {
    if (theme === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
      document.body.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
      document.body.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
    updateThemeButtonIcon(theme);
  }

  // Funkcja do pobierania aktualnego trybu
  function getTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      return savedTheme;
    }
    // Sprawdź preferencje systemowe
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light';
  }

  // Funkcja do aktualizacji ikony przycisku
  function updateThemeButtonIcon(theme) {
    const buttons = document.querySelectorAll('.theme-toggle-btn');
    buttons.forEach(button => {
      const moonIcon = button.querySelector('.bi-moon');
      const sunIcon = button.querySelector('.bi-sun');
      
      if (theme === 'dark') {
        if (moonIcon) moonIcon.style.setProperty('display', 'none', 'important');
        if (sunIcon) sunIcon.style.setProperty('display', 'inline-block', 'important');
      } else {
        if (moonIcon) moonIcon.style.setProperty('display', 'inline-block', 'important');
        if (sunIcon) sunIcon.style.setProperty('display', 'none', 'important');
      }
    });
  }

  // Funkcja do przełączania trybu
  function toggleTheme() {
    const currentTheme = getTheme();
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
  }

  // Sprawdź czy jesteśmy na stronie auth (logowanie, rejestracja, ustawienia)
  function isAuthPage() {
    const body = document.body;
    return body.classList.contains('login-page') ||
           body.classList.contains('account-settings-page') ||
           body.classList.contains('account-more-options-page') ||
           body.classList.contains('change-password-page');
  }

  // Inicjalizacja przy załadowaniu strony
  document.addEventListener('DOMContentLoaded', function() {
    // Jeśli jesteśmy na stronie auth, wymuś jasny styl i nie inicjalizuj przełącznika
    if (isAuthPage()) {
      // Wymuś jasny styl
      document.documentElement.setAttribute('data-theme', 'light');
      document.body.classList.remove('dark');
      return; // Wyjdź wcześniej, nie inicjalizuj przełącznika
    }
    
    console.log('Theme toggle script loaded');
    
    // Ustaw początkowy tryb
    const initialTheme = getTheme();
    console.log('Initial theme:', initialTheme);
    setTheme(initialTheme);

    // Dodaj event listenery do przycisków
    const themeButtons = document.querySelectorAll('.theme-toggle-btn');
    console.log('Found theme buttons:', themeButtons.length);
    
    themeButtons.forEach(button => {
      button.addEventListener('click', function() {
        // Sprawdź ponownie czy nie jesteśmy na stronie auth
        if (isAuthPage()) {
          return;
        }
        console.log('Theme toggle button clicked');
        toggleTheme();
      });
      
      // Usuń disabled po załadowaniu
      button.disabled = false;
    });

    // Nasłuchuj zmian preferencji systemowych
    if (window.matchMedia) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      mediaQuery.addEventListener('change', function(e) {
        // Nie reaguj na zmiany preferencji systemowych na stronach auth
        if (isAuthPage()) {
          return;
        }
        // Tylko jeśli użytkownik nie ustawił ręcznie preferencji
        if (!localStorage.getItem('theme')) {
          setTheme(e.matches ? 'dark' : 'light');
        }
      });
    }
  });

  // Eksport funkcji dla użycia w innych skryptach
  window.themeToggle = {
    setTheme: setTheme,
    getTheme: getTheme,
    toggleTheme: toggleTheme
  };
})();

