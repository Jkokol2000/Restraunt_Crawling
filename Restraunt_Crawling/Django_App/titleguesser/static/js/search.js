const searchBar = document.getElementById('search-bar');
const suggestionsBox = document.getElementById('suggestions');

searchBar.addEventListener('input', function() {
    const query = searchBar.value.trim();
    if (query.length > 0) {
        fetch(`/search/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                suggestionsBox.innerHTML = ''; // Clear previous suggestions
                data.suggestions.forEach(suggestion => {
                    const suggestionDiv = document.createElement('div');
                    suggestionDiv.textContent = suggestion;
                    suggestionDiv.addEventListener('click', () => {
                        searchBar.value = suggestion;
                        suggestionsBox.innerHTML = ''; // Clear suggestions
                    });
                    suggestionsBox.appendChild(suggestionDiv);
                });
            })
            .catch(error => console.error('Error fetching suggestions:', error));
    } else {
        suggestionsBox.innerHTML = ''; // Clear suggestions if search is empty
    }
});

// Close suggestions box when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-container')) {
        suggestionsBox.innerHTML = '';
    }
});
