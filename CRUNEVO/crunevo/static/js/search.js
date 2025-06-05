// static/js/search.js
document.addEventListener("DOMContentLoaded", () => {
  const input = document.querySelector("#global-search");
  const resultsBox = document.querySelector("#search-results");

  if (input) {
    input.addEventListener("input", async () => {
      const query = input.value.trim();
      if (query.length > 1) {
        const res = await fetch(`/buscar?q=${encodeURIComponent(query)}`);
        const data = await res.json();
        resultsBox.innerHTML = "";
        data.resultados.forEach(item => {
          const div = document.createElement("div");
          div.className = "result-item";
          div.innerHTML = `<a href="${item.url}">${item.texto}</a>`;
          resultsBox.appendChild(div);
        });
      } else {
        resultsBox.innerHTML = "";
      }
    });
  }
});