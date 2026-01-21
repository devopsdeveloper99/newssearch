document.addEventListener("DOMContentLoaded", function () {

  console.log("search.js loaded");

  const searchInput = document.getElementById("search-input");
  const searchButton = document.getElementById("search-button");
  const loadingOverlay = document.getElementById("loadingOverlay");

  if (!searchInput) {
    console.error("search-input not found in DOM");
    return;
  }

  searchInput.addEventListener("keydown", function (event) {

    if (event.key === "Enter") {
      event.preventDefault();
      searchButton.click();
    }
  });

  window.callSearch = function () {
    const inputValue = searchInput.value.trim();
    if (inputValue === "") {
      alert("please input a keyword");
      return;
    }

    searchButton.style.display = "none";
    loadingOverlay.style.display = "flex";

    const csrftoken = getCookie("csrftoken");

    fetch("/newssearch/search/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({ query: inputValue }),
    })
      .then(async (response) => {
        if (!response.ok) {
          const errorText = await response.text();

          loadingOverlay.style.display = "none";
          searchButton.style.display = "inline-block";

          if (response.status === 503) {
            alert(
              "Server is temporarily unavailable.\n\n" +
              "Check:\n1. Python app running in cPanel\n2. Django app configured\n3. Try again later"
            );
          } else {
            alert(
              "Server error (" +
              response.status +
              "):\n" +
              errorText.substring(0, 200)
            );
          }
          throw new Error("Server error");
        }
        return response.json();
      })
      .then((data) => {
        loadingOverlay.style.display = "none";
        searchButton.style.display = "inline-block";
        callResult(data);
      })
      .catch((error) => {
        console.error("Fetch error:", error);
        loadingOverlay.style.display = "none";
        searchButton.style.display = "inline-block";
        alert("Network error: " + error.message);
      });
  };
});

/* ---------- CSRF helpers ---------- */

function getCSRFToken() {
  const metaTag = document.querySelector('meta[name="csrf-token"]');
  if (metaTag) return metaTag.getAttribute("content");
  return getCookie("csrftoken");
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie) {
    document.cookie.split(";").forEach((cookie) => {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
      }
    });
  }
  return cookieValue;
}

function callResult(data) {
  const csrftoken = getCookie("csrftoken");

  fetch("/newssearch/results/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(data),
  })
    .then((res) => res.text())
    .then((html) => {
      document.getElementById("search").style.display = "none";
      document.getElementById("resultsContainer").innerHTML = html;
    })
    .catch((err) => console.error("Error:", err));
}
