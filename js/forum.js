


document.getElementById("inputt").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const username = document.getElementById("username").value;
    const message = document.getElementById("message").value;
    
  

    fetch("../php/forum.php", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `username=${encodeURIComponent(username)}&message=${encodeURIComponent(message)}`
    })
    .then((response) => {
        return response.json();
      })// Falls `forum.php` eine fehlerhafte JSON-Antwort gibt
    .then(data => {
        if (data.success) {
            document.getElementById("inputt").reset();
            loadPosts(); // Beiträge neu laden
        }
    })
    .catch(error => console.error("Fehlermeldung", error)); // Falls `fetch()` fehlschlägt
});



function loadPosts() {
    fetch("../php/forum.php")
        .then((response) => response.json())
        .then(posts => {
            let postsDiv = document.getElementById("posts");
            postsDiv.innerHTML = ""; // Vorherige Beiträge leeren

            posts.forEach(post => {
                let postDiv = document.createElement("div");
                postDiv.classList.add("post");

                postDiv.innerHTML = `
                 <strong>${post.username}:</strong>
                 <p class="comment-text">${post.message}</p>
                 <span class="timestamp">${post.timestamp}</span><button class="analyze-btn" onclick="analyze(this)">🧠 analysieren</button>
                 <div class="result"></div>
`;

                postsDiv.prepend(postDiv);
            });
        })
        .catch(error => console.error("Fehler beim Laden der Beiträge:", error));
    }
    
    loadPosts();
   
async function analyze(button) {
    const post = button.closest(".post");
    const text = post.querySelector(".comment-text").innerText;

    try {
        const response = await fetch("https://asemo.pythonanywhere.com/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();
        post.querySelector(".result").innerText = `Stimmung: ${data.label || "Unbekannt"}`;
    } catch (err) {
        post.querySelector(".result").innerText = "❌ Fehler bei Analyse";
        console.error(err);
    }

    alert("Danke für deinen Beitrag");
    if (loadPosts()) {
        alert("Danke für deinen Beitrag");
    }
  
}

