// Slider & Place Logic 
const minRange = document.getElementById('minRange');
const maxRange = document.getElementById('maxRange');
const sliderTrack = document.getElementById('slider-track');
const sliderMinLabel = document.getElementById('slider-min');
const sliderMaxLabel = document.getElementById('slider-max');
const thumbMinLabel = document.getElementById('thumb-min-label');
const thumbMaxLabel = document.getElementById('thumb-max-label');
const inputMin = document.getElementById('input-min');
const inputMax = document.getElementById('input-max');
const minBound = document.getElementById('min-bound');
const maxBound = document.getElementById('max-bound');
const sliderReset = document.getElementById('slider-reset');
const resultCount = document.getElementById('result-count');

let allPlaces = [];

const SLIDER_MIN = 0;
const SLIDER_MAX = 10000;

function setSliderBounds(min, max) {
  minRange.min = inputMin.min = SLIDER_MIN;
  maxRange.min = inputMin.min = SLIDER_MIN;
  minRange.max = inputMax.max = SLIDER_MAX;
  maxRange.max = inputMax.max = SLIDER_MAX;
  minBound.textContent = `${SLIDER_MIN} $`;
  maxBound.textContent = `${SLIDER_MAX} $`;
}

// Affiche le nombre de résultats
function updateResultCount(count) {
  resultCount.textContent = `${count} place${count > 1 ? "s" : ""} correspondent à votre recherche`;
}


function updateSlider(fromInput = false) {
  let min = Math.min(Number(minRange.value), Number(maxRange.value));
  let max = Math.max(Number(minRange.value), Number(maxRange.value));
  minRange.value = min;
  maxRange.value = max;
  inputMin.value = min;
  inputMax.value = max;
  sliderMinLabel.textContent = min;
  sliderMaxLabel.textContent = max;
  thumbMinLabel.textContent = min + " $";
  thumbMaxLabel.textContent = max + " $";

  // Positionne les tooltips
  const minPercent = ((min - SLIDER_MIN) / (SLIDER_MAX - SLIDER_MIN));
  const maxPercent = ((max - SLIDER_MIN) / (SLIDER_MAX - SLIDER_MIN));
  thumbMinLabel.style.left = `calc(${minPercent * 100}% - 24px)`;
  thumbMaxLabel.style.left = `calc(${maxPercent * 100}% - 24px)`;

  // Track color
  sliderTrack.style.background = `
    linear-gradient(
      to right,
      #232f38 ${minPercent * 100}%,
      #14fff4 ${minPercent * 100}%,
      #14fff4 ${maxPercent * 100}%,
      #232f38 ${maxPercent * 100}%
    )`;

  // Filtre les places et met à jour le DOM
  const filtered = allPlaces.filter(pl => {
    const priceVal = Number(pl.price);
    return !isNaN(priceVal) && priceVal >= min && priceVal <= max;
  });
  displayPlaces(filtered);
  updateResultCount(filtered.length);
}

// Synchronise les inputs et le slider
function syncInputs() {
  let min = parseInt(inputMin.value, 10);
  let max = parseInt(inputMax.value, 10);
  if (isNaN(min)) min = SLIDER_MIN;
  if (isNaN(max)) max = SLIDER_MAX;
  min = Math.max(SLIDER_MIN, Math.min(min, SLIDER_MAX, max));
  max = Math.min(SLIDER_MAX, Math.max(max, min));
  minRange.value = min;
  maxRange.value = max;
  updateSlider(true);
}

// Empêche les croisements
minRange.addEventListener('input', () => {
  if (+minRange.value > +maxRange.value) minRange.value = maxRange.value;
  updateSlider();
});
maxRange.addEventListener('input', () => {
  if (+maxRange.value < +minRange.value) maxRange.value = minRange.value;
  updateSlider();
});
inputMin.addEventListener('input', syncInputs);
inputMax.addEventListener('input', syncInputs);

// Keyboard accessibility
[minRange, maxRange].forEach(el => {
  el.addEventListener('keydown', e => {
    if (["ArrowLeft", "ArrowDown"].includes(e.key)) el.stepDown();
    if (["ArrowRight", "ArrowUp"].includes(e.key)) el.stepUp();
    updateSlider();
  });
});

// Reset
sliderReset.addEventListener('click', () => {
  minRange.value = SLIDER_MIN;
  maxRange.value = SLIDER_MAX;
  inputMin.value = SLIDER_MIN;
  inputMax.value = SLIDER_MAX;
  updateSlider();
});

// Récupère les places depuis l'API
async function fetchPlaces() {
  const token = window.getTokenFromCookie ? window.getTokenFromCookie() : null;
  let headers = {};
  if (token) headers['Authorization'] = 'Bearer ' + token;
  try {
    const res = await fetch('http://127.0.0.1:5000/api/v1/places/', { headers });
    if (!res.ok) {
      document.querySelector('.places-container').innerHTML = "Erreur API";
      return;
    }
    allPlaces = await res.json();

    
    let minPrice = SLIDER_MIN, maxPrice = SLIDER_MAX;
    if (allPlaces.length) {
      minPrice = Math.floor(Math.min(...allPlaces.map(p => Number(p.price) || 0)));
      maxPrice = Math.ceil(Math.max(...allPlaces.map(p => Number(p.price) || 0)));
    }
    

    setSliderBounds(SLIDER_MIN, SLIDER_MAX);
    minRange.value = inputMin.value = minPrice;
    maxRange.value = inputMax.value = maxPrice;
    updateSlider();
  } catch (e) {
    document.querySelector('.places-container').innerHTML = "Erreur lors du chargement des places.";
  }
}

// Affiche les places
function displayPlaces(places) {
  const container = document.querySelector('.places-container');
  container.innerHTML = '';
  places.forEach(place => {
    let imgUrl = 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg';
    let caption = 'Aperçu de ' + (place.title ? place.title : 'Place');
    if (place.images && place.images.length > 0) {
      if (place.images[0].url) imgUrl = place.images[0].url;
      if (place.images[0].caption) caption = place.images[0].caption;
    }
    const card = document.createElement('div');
    card.className = 'glass-card place-card';
    card.innerHTML = `
      <img src="${imgUrl}" alt="${caption}" class="place-img-preview" />
      <div class="place-details">
        <h2>${place.title ? place.title : '(Sans titre)'}</h2>
        
        <p class="place-price">Price per night: $${place.price}</p>
        <a href="place.html?id=${place.id}" class="neon-button">View Details</a>
      </div>
    `;
    container.appendChild(card);
  });
}


document.addEventListener('DOMContentLoaded', () => {
  if (typeof window.updateUserNav === "function") window.updateUserNav();
  fetchPlaces();
  updateSlider();
});

