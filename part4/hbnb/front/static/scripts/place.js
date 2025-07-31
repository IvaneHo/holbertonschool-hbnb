document.addEventListener('DOMContentLoaded', async () => {
    const token = getTokenFromCookie();
    const placeId = getPlaceIdFromURL();

    // Affichage complet (place + reviews + formulaire)
    await fetchAndDisplayPlaceAndReviews(token, placeId);
});


function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}
function getTokenFromCookie() {
    const match = document.cookie.match(/(?:^|;\s*)access_token=([^;]+)/);
    return match ? match[1] : null;
}
function isAuthenticated() {
    return !!getTokenFromCookie();
}


function showReviewSuccess(msg) {
    const box = document.getElementById('review-message');
    box.innerHTML = `<span style="color:#22e082;font-weight:bold;">${msg}</span>`;
    box.style.display = 'block';
    setTimeout(() => {
        box.innerHTML = '';
        box.style.display = 'none';
    }, 3500);
}
function showReviewError(msg) {
    const box = document.getElementById('review-message');
    box.innerHTML = `<span style="color:#f55;font-weight:bold;">${msg}</span>`;
    box.style.display = 'block';
    setTimeout(() => {
        box.innerHTML = '';
        box.style.display = 'none';
    }, 5000);
}

// Fetch et rendu
async function fetchAndDisplayPlaceAndReviews(token, placeId) {
    const headers = {};
    if (token) headers['Authorization'] = 'Bearer ' + token;

    let place = null, reviews = [];
    try {
        const res = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, { headers });
        if (!res.ok) throw new Error("not found");
        place = await res.json();
    } catch { document.getElementById('place-details').innerHTML = '<div style="color:#f55;">Erreur chargement lieu.</div>'; return; }

    try {
        const res = await fetch(`http://127.0.0.1:5000/api/v1/reviews/by_place/${placeId}`, { headers });
        reviews = res.ok ? await res.json() : [];
    } catch { reviews = []; }

    displayPlaceDetails(place, reviews);
}

function displayPlaceDetails(place, reviews) {
    const container = document.getElementById('place-details');
    container.innerHTML = ''; // Clear

    // GALERIE D'IMAGES 
    let images = (place.images && place.images.length > 0)
      ? place.images
      : [{url: 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'}];

    const gallery = document.createElement('div');
    gallery.className = 'place-image-gallery';

    // Image principale
    const mainImg = document.createElement('img');
    mainImg.src = images[0].url;
    mainImg.className = 'place-detail-img';
    mainImg.tabIndex = 0;
    mainImg.alt = place.title || 'Photo';
    mainImg.onclick = () => showModalImage(mainImg.src);
    gallery.appendChild(mainImg);

    // Miniatures
    if (images.length > 1) {
        const thumbs = document.createElement('div');
        thumbs.className = 'place-thumbs';
        images.forEach((img, idx) => {
            const t = document.createElement('img');
            t.src = img.url;
            t.className = 'thumb-img' + (idx === 0 ? ' selected' : '');
            t.tabIndex = 0;
            t.onclick = () => {
                mainImg.src = img.url;
                thumbs.querySelectorAll('.thumb-img').forEach(th => th.classList.remove('selected'));
                t.classList.add('selected');
            };
            t.onkeydown = (e) => { if (e.key === "Enter") t.onclick(); };
            thumbs.appendChild(t);
        });
        gallery.appendChild(thumbs);
    }
    container.appendChild(gallery);

    // INFOS 
    const title = document.createElement('h1');
    title.textContent = place.title || '(No Title)';
    container.appendChild(title);

    const desc = document.createElement('p');
    desc.innerHTML = `<b>Description:</b> ${place.description || ''}`;
    container.appendChild(desc);

    const price = document.createElement('p');
    price.innerHTML = `<b>Price:</b> $${place.price}`;
    container.appendChild(price);

    if (place.amenities && place.amenities.length > 0) {
        const amenities = document.createElement('div');
        amenities.className = 'amenities-list';
        amenities.innerHTML = '<b>Amenities:</b> ' +
            place.amenities.map(a => `<span class="tag">${a}</span>`).join(' ');
        container.appendChild(amenities);
    }

    // REVIEWS
    const reviewsSection = document.createElement('section');
    reviewsSection.className = 'reviews-section';
    reviewsSection.innerHTML = '<h2>Reviews</h2>';
    if (reviews && reviews.length > 0) {
        reviews.forEach(rv => {
            let name = "Utilisateur";
            if (rv.user_first_name) {
                name = rv.user_first_name;
                if (rv.user_last_name) name += " " + rv.user_last_name[0].toUpperCase() + ".";
            }
            const review = document.createElement('div');
            review.className = 'review-item';
            review.innerHTML = `
                <span class="review-author">${name}</span>
                <span class="review-rating">${'★'.repeat(rv.rating)}</span><br>
                <span>${rv.text}</span>
            `;
            reviewsSection.appendChild(review);
        });
    } else {
        reviewsSection.innerHTML += '<p style="text-align:center;">No reviews yet.</p>';
    }
    container.appendChild(reviewsSection);

    // FORMULAIRE ADD REVIEW 
    if (isAuthenticated()) {
        if (document.getElementById('add-review-form')) document.getElementById('add-review-form').remove();
        const addReviewSection = document.createElement('section');
        addReviewSection.className = 'add-review-section';
        addReviewSection.innerHTML = `
          <form id="add-review-form" class="form-card">
            <h2>Add a Review</h2>
            <label for="review">Your Review:</label>
            <textarea id="review" name="review" rows="4" required></textarea>
            <label for="rating">Rating:</label>
            <select id="rating" name="rating" required>
              <option value="" disabled selected>Select rating</option>
              <option value="5">⭐️⭐️⭐️⭐️⭐️</option>
              <option value="4">⭐️⭐️⭐️⭐️</option>
              <option value="3">⭐️⭐️⭐️</option>
              <option value="2">⭐️⭐️</option>
              <option value="1">⭐️</option>
            </select>
            <button type="submit">Submit Review</button>
            <div id="review-message" style="margin-top:12px;"></div>
          </form>
        `;
        container.appendChild(addReviewSection);

        document.getElementById('add-review-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const data = {
        text: this.review.value.trim(),
        rating: Number(this.rating.value),
        place_id: getPlaceIdFromURL()
    };
    try {
        const res = await fetch(`http://127.0.0.1:5000/api/v1/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + getTokenFromCookie()
            },
            body: JSON.stringify(data)
        });
        if (res.ok) {
    showReviewSuccess('Review added! Thank you for your feedback.');
    this.reset();
    // NE RECONSTRUIT PAS IMMEDIATEMENT — attend 2 secondes avant de refresh !
    setTimeout(() => {
        fetchAndDisplayPlaceAndReviews(getTokenFromCookie(), getPlaceIdFromURL());
    }, 3500); // laisse le message visible !
        } else {
            const err = await res.json();
            showReviewError(err.error || err.message || 'Error');
        }
    } catch {
        showReviewError('Network error.');
    }
});

    }
}

// ZOOM IMAGE
function showModalImage(url) {
    let modal = document.createElement('div');
    modal.style.cssText = `
      position:fixed; z-index:9999; inset:0; background:rgba(12,22,31,0.97);
      display:flex; align-items:center; justify-content:center;
      animation:fadeIn .18s;
    `;
    modal.innerHTML = `
      <img src="${url}" style="max-width:98vw; max-height:96vh; border-radius:18px; box-shadow:0 4px 38px #00f7ff88;">
      <span style="position:absolute;top:30px;right:45px;font-size:2.7rem;color:#fff;cursor:pointer;z-index:99;" id="close-modal-img">&times;</span>
    `;
    document.body.appendChild(modal);
    function close() { document.body.removeChild(modal); }
    modal.onclick = close;
    document.getElementById('close-modal-img').onclick = close;
    modal.querySelector('img').onclick = (e) => e.stopPropagation();
}
