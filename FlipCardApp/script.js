document.addEventListener('DOMContentLoaded', () => {
    fetch('professional_practices.json')
        .then(response => response.json())
        .then(data => renderCard(data))
        .catch(error => console.error('Error loading card data:', error));
});

function renderCard(cardData) {
    const container = document.getElementById('card-container');

    // Create card element
    const card = document.createElement('div');
    card.className = 'card';

    // Front Face
    const frontFace = document.createElement('div');
    frontFace.className = 'card-face card-front';
    frontFace.style.backgroundColor = cardData.frontBackgroundColor || '#fff';

    frontFace.innerHTML = `
        <div class="flip-button" title="Flip">⟳</div>
        <div class="card-title">${cardData.title}</div>
        ${cardData.card_image ? `<img src="${cardData.card_image}" alt="${cardData.title}" class="card-image">` : ''}
    `;

    // Back Face
    const backFace = document.createElement('div');
    backFace.className = 'card-face card-back';

    backFace.innerHTML = `
        <div class="flip-button" title="FlipBack">⟳</div>
        <textarea class="card-description-input" placeholder="Enter description..." readonly>${cardData.description}</textarea>
        <div class="checkbox-container">
            <label class="checkbox-label">
                <input type="checkbox" id="pdf-checkbox" name="pdf">
                <span>PDF</span>
            </label>
            <label class="checkbox-label">
                <input type="checkbox" id="graphic-checkbox" name="graphic">
                <span>Graphic</span>
            </label>
        </div>
        <button class="explore-btn" disabled>View</button>
    `;

    // Append faces to card
    card.appendChild(frontFace);
    card.appendChild(backFace);

    // Append card to container
    container.appendChild(card);

    // Add Event Listeners for Flip
    const flipButtons = card.querySelectorAll('.flip-button');
    flipButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            card.classList.toggle('flip');
        });
    });

    // Add Event Listeners for Checkboxes to control Explore button
    const pdfCheckbox = card.querySelector('#pdf-checkbox');
    const graphicCheckbox = card.querySelector('#graphic-checkbox');
    const exploreBtn = card.querySelector('.explore-btn');

    function updateExploreButton() {
        if (pdfCheckbox.checked || graphicCheckbox.checked) {
            exploreBtn.disabled = false;
        } else {
            exploreBtn.disabled = true;
        }
    }

    pdfCheckbox.addEventListener('change', updateExploreButton);
    graphicCheckbox.addEventListener('change', updateExploreButton);
}
