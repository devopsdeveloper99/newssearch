document.getElementById("search-input").addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    event.preventDefault(); // Prevent default form submission (if any)
    document.getElementById("search-button").click(); // Trigger the search button
  }
});

function getCSRFToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


function callSearch() {
  alert("callSearch---");
  return;
  const inputValue = document.getElementById("search-input").value;
  if (inputValue == "") {
    alert("please input a keyword")
    return;
  }
  const searchButton = document.getElementById('search-button');
  const loadingOverlay = document.getElementById('loadingOverlay');

  // Show full-page loading spinner
  searchButton.style.display = 'none';
  loadingOverlay.style.display = 'flex';


  const csrftoken = getCookie('csrftoken');


  fetch("/search/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify({ query: inputValue })
  })
    .then(async (response) => {

      if (!response.ok) {
        const errorText = await response.text(); // get raw text instead of json
        console.error("Server error:", errorText);
        alert("Server returned an error:\n" + errorText);
        return;
      }
      return response.json();
    })
    .then(data => {
      loadingOverlay.style.display = 'none';
      searchButton.style.display = 'inline-block';

      callResult(data);
      if (data) {
        //      alert("Result: " + data.result);
      }
    })
    .catch(error => {
      console.error("Fetch error:", error);
    });
}

function callResult(data) {
  const csrftoken = getCookie('csrftoken');
  fetch("/results/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify(data)
  })
    .then(res => res.text())
    .then(html => {
      document.getElementById("search").style.display = 'none';
      document.getElementById("resultsContainer").innerHTML = html;
    })
    .catch(err => console.error("Error:", err));
}
