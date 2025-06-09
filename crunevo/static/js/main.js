// Lógica para el menú offcanvas y su integración con el botón atrás
document.addEventListener("DOMContentLoaded", () => {
    const offcanvasEl = document.getElementById("mobileMenu");
    if (offcanvasEl) {
        const offcanvas = new bootstrap.Offcanvas(offcanvasEl);
        offcanvasEl.addEventListener("shown.bs.offcanvas", () => {
            history.pushState({ offcanvas: true }, "");
        });
        offcanvasEl.addEventListener("hidden.bs.offcanvas", () => {
            if (history.state && history.state.offcanvas) {
                history.back();
            }
        });

        window.addEventListener("popstate", (evt) => {
            if (evt.state && evt.state.offcanvas) {
                offcanvas.hide();
            }
        });
    }
});

// Lógica para el Modal de Búsqueda Global
document.addEventListener("DOMContentLoaded", () => {
    const openSearchBtn = document.getElementById("openGlobalSearchBtn");
    const closeSearchBtn = document.getElementById("closeGlobalSearchBtn");
    const globalSearchModal = document.getElementById("globalSearchModal");
    const globalSearchInput = document.getElementById("globalSearchInput");
    
    const searchInitialState = document.getElementById("searchInitialState");
    const searchResultsContent = document.getElementById("searchResultsContent");
    const noResultsFoundMsg = document.getElementById("noResultsFound");

    const apuntesResultsContainer = document.getElementById("apuntesResults");
    const tiendaResultsContainer = document.getElementById("tiendaResults");
    const temasSugeridosContainer = document.getElementById("temasSugeridosResults");

    const recentSearchesList = document.getElementById("recentSearchesList");
    const noRecentSearchesMsg = document.getElementById("noRecentSearches");
    const popularTopicsContainer = document.getElementById("popularTopics");

    const viewAllApuntesLink = document.querySelector("#apuntesResultsSection .view-all-link");
    const viewAllTiendaLink = document.querySelector("#tiendaResultsSection .view-all-link");

    let searchDebounceTimer;

    const resetSearchState = () => {
        searchInitialState.classList.remove("d-none");
        searchResultsContent.classList.add("d-none");
        noResultsFoundMsg.classList.add("d-none");
        apuntesResultsContainer.innerHTML = "";
        tiendaResultsContainer.innerHTML = "";
        temasSugeridosContainer.innerHTML = "";
        if(viewAllApuntesLink) viewAllApuntesLink.classList.add("d-none");
        if(viewAllTiendaLink) viewAllTiendaLink.classList.add("d-none");
    };

    const openSearch = () => {
        globalSearchModal.classList.remove("d-none");
        globalSearchInput.focus();
        displayRecentSearches(); 
        displayPopularTopics(); 
        if (!globalSearchInput.value) {
            resetSearchState();
        }
    };

    const closeSearch = () => {
        globalSearchModal.classList.add("d-none");
        globalSearchInput.value = ""; 
        resetSearchState();
    };

    if(openSearchBtn) openSearchBtn.addEventListener("click", openSearch);
    if(closeSearchBtn) closeSearchBtn.addEventListener("click", closeSearch);
    if(globalSearchModal) {
        globalSearchModal.addEventListener("click", (event) => {
            if (event.target === globalSearchModal) { 
                closeSearch();
            }
        });
    }
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && globalSearchModal && !globalSearchModal.classList.contains("d-none")) {
            closeSearch();
        }
    });

    const displayResults = (data) => {
        const currentQuery = globalSearchInput.value.trim();
        searchInitialState.classList.add("d-none");
        searchResultsContent.classList.remove("d-none");
        noResultsFoundMsg.classList.add("d-none");

        apuntesResultsContainer.innerHTML = "";
        tiendaResultsContainer.innerHTML = "";
        temasSugeridosContainer.innerHTML = "";
        if(viewAllApuntesLink) viewAllApuntesLink.classList.add("d-none");
        if(viewAllTiendaLink) viewAllTiendaLink.classList.add("d-none");

        let hasResults = false;

        if (data.apuntes && data.apuntes.length > 0) {
            hasResults = true;
            document.getElementById("apuntesResultsSection").classList.remove("d-none");
            data.apuntes.forEach(apunte => {
                const card = `
                    <div class="card card-apunte mb-2">
                        <div class="card-body">
                            <h5 class="card-title"><a href="${apunte.url}">${apunte.title}</a></h5>
                            <p class="card-text"><i class="fas ${getIconForFileType(apunte.file_type)} file-type-icon"></i> ${apunte.course || ''} - ${apunte.faculty || ''}</p>
                            <p class="card-text text-muted">${apunte.description_snippet || ''}</p>
                        </div>
                    </div>`;
                apuntesResultsContainer.innerHTML += card;
            });
            if(viewAllApuntesLink) {
                viewAllApuntesLink.href = `/search_results?q=${encodeURIComponent(currentQuery)}&category=apuntes`;
                viewAllApuntesLink.classList.remove("d-none");
            }
        } else {
            document.getElementById("apuntesResultsSection").classList.add("d-none");
        }

        if (data.tienda && data.tienda.length > 0) {
            hasResults = true;
            document.getElementById("tiendaResultsSection").classList.remove("d-none");
            data.tienda.forEach(producto => {
                const card = `
                    <div class="card card-producto mb-2">
                        <div class="card-body d-flex">
                            <img src="${producto.image_url || '/static/images/default_product.png'}" alt="${producto.name}" style="width: 60px; height: 60px; object-fit: cover; margin-right: 10px;">
                            <div>
                                <h5 class="card-title"><a href="${producto.url}">${producto.name}</a></h5>
                                <p class="card-text price">S/ ${producto.price ? producto.price.toFixed(2) : 'N/A'}</p>
                                <p class="card-text text-muted">${producto.type || ''}</p>
                            </div>
                        </div>
                    </div>`;
                tiendaResultsContainer.innerHTML += card;
            });
            if(viewAllTiendaLink) {
                viewAllTiendaLink.href = `/search_results?q=${encodeURIComponent(currentQuery)}&category=tienda`;
                viewAllTiendaLink.classList.remove("d-none");
            }
        } else {
            document.getElementById("tiendaResultsSection").classList.add("d-none");
        }

        if (data.temas_sugeridos && data.temas_sugeridos.length > 0) {
            hasResults = true;
            document.getElementById("temasSugeridosResultsSection").classList.remove("d-none");
            data.temas_sugeridos.forEach(tema => {
                const button = `<button class="btn btn-sm btn-outline-info popular-topic-btn me-1 mb-1" data-search-term="${tema.text}">${tema.text}</button>`;
                temasSugeridosContainer.innerHTML += button;
            });
        } else {
            document.getElementById("temasSugeridosResultsSection").classList.add("d-none");
        }

        if (!hasResults) {
            noResultsFoundMsg.classList.remove("d-none");
            noResultsFoundMsg.textContent = "No se encontraron resultados para tu búsqueda.";
        }
    };

    const getIconForFileType = (fileType) => {
        if (!fileType) return 'fa-file';
        const type = fileType.toLowerCase();
        if (type.includes('pdf')) return 'fa-file-pdf';
        if (type.includes('doc') || type.includes('word')) return 'fa-file-word';
        if (type.includes('ppt') || type.includes('powerpoint')) return 'fa-file-powerpoint';
        if (type.includes('xls') || type.includes('excel')) return 'fa-file-excel';
        if (type.includes('zip') || type.includes('rar')) return 'fa-file-archive';
        if (type.includes('txt')) return 'fa-file-alt';
        if (type.includes('jpg') || type.includes('jpeg') || type.includes('png') || type.includes('gif')) return 'fa-file-image';
        return 'fa-file';
    };

    const executeSearch = async (query) => {
        if (query.length < 2 && query.length !==0) { 
            resetSearchState();
            return;
        }
        if (query.length === 0) {
             resetSearchState();
             displayRecentSearches();
             displayPopularTopics();
             return;
        }

        try {
            const response = await fetch(`/api/search?q=${encodeURIComponent(query)}&limit=5`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            displayResults(data);
            addSearchToHistory(query);
        } catch (error) {
            console.error("Error al realizar la búsqueda:", error);
            searchInitialState.classList.add("d-none");
            searchResultsContent.classList.add("d-none");
            noResultsFoundMsg.classList.remove("d-none");
            noResultsFoundMsg.textContent = "Error al cargar resultados. Inténtalo de nuevo.";
        }
    };

    if(globalSearchInput) {
        globalSearchInput.addEventListener("input", () => {
            clearTimeout(searchDebounceTimer);
            const query = globalSearchInput.value.trim();
            searchDebounceTimer = setTimeout(() => {
                executeSearch(query);
            }, 300); 
        });
    }

    const MAX_RECENT_SEARCHES = 5;
    const getRecentSearches = () => JSON.parse(localStorage.getItem("recentSearchesCantuta")) || [];
    const saveRecentSearches = (searches) => localStorage.setItem("recentSearchesCantuta", JSON.stringify(searches));

    const addSearchToHistory = (term) => {
        if (!term) return;
        let searches = getRecentSearches();
        
        searches = searches.filter(s => s.toLowerCase() !== term.toLowerCase());
        searches.unshift(term); 
        if (searches.length > MAX_RECENT_SEARCHES) {
            searches.pop(); 
        }
        saveRecentSearches(searches);
    };

    const displayRecentSearches = () => {
        const searches = getRecentSearches();
        if(recentSearchesList) recentSearchesList.innerHTML = "";
        if (searches.length > 0) {
            if(noRecentSearchesMsg) noRecentSearchesMsg.classList.add("d-none");
            searches.forEach(term => {
                const li = document.createElement("li");
                const a = document.createElement("a");
                a.href = "#";
                a.classList.add("recent-search-item");
                a.textContent = term;
                a.addEventListener("click", (e) => {
                    e.preventDefault();
                    globalSearchInput.value = term;
                    executeSearch(term);
                });
                li.appendChild(a);
                if(recentSearchesList) recentSearchesList.appendChild(li);
            });
        } else {
            if(noRecentSearchesMsg) noRecentSearchesMsg.classList.remove("d-none");
        }
    };
    
    const SIMULATED_POPULAR_TOPICS = ["Cálculo I", "Marketing Digital", "Derecho Penal", "Programación Web", "Física Básica"];
    const displayPopularTopics = () => {
        if(popularTopicsContainer) popularTopicsContainer.innerHTML = "";
        SIMULATED_POPULAR_TOPICS.forEach(topic => {
            const button = document.createElement("button");
            button.classList.add("btn", "btn-sm", "btn-outline-secondary", "popular-topic-btn", "me-1", "mb-1");
            button.textContent = topic;
            button.dataset.searchTerm = topic;
            button.addEventListener("click", () => {
                globalSearchInput.value = topic;
                executeSearch(topic);
            });
            if(popularTopicsContainer) popularTopicsContainer.appendChild(button);
        });
    };

    if(searchResultsContent) {
        searchResultsContent.addEventListener('click', function(event) {
            if (event.target.matches('.popular-topic-btn')) {
                const searchTerm = event.target.dataset.searchTerm;
                if (searchTerm) {
                    globalSearchInput.value = searchTerm;
                    executeSearch(searchTerm);
                }
            }
        });
    }
});


document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("toggleFloatingSidebar");
    const content = document.getElementById("floatingSidebarContent");

    if (toggleBtn && content) {
        toggleBtn.addEventListener("click", () => {
            content.classList.toggle("d-none");
            const expanded = !content.classList.contains("d-none");
            toggleBtn.setAttribute("aria-expanded", expanded);
        });
    }
});

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".note-actions .action-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            btn.classList.toggle("active");
            const action = btn.dataset.action;
            console.log(`Action: ${action}`);
        });
    });
    document.querySelectorAll('.post-actions button').forEach((btn) => {
        btn.addEventListener('click', () => {
            btn.classList.toggle('active');
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
  const openNoteBtn = document.getElementById("openNoteModalBtn");
  const noteModalEl = document.getElementById("uploadNoteModal");
  const noteForm = document.getElementById("noteForm");
  const tagInput = document.getElementById("note-tags");
  const tagSuggestions = [
    "álgebra",
    "álgebra lineal",
    "derivadas",
    "integrales",
    "ecuaciones diferenciales",
    "geometría analítica",
    "trigonometría",
    "límites",
    "matrices",
    "probabilidad",
    "estadística",
    "combinatoria",
    "números complejos",
    "fórmulas matemáticas",
    "lógica matemática",
    "física clásica",
    "cinemática",
    "leyes de Newton",
    "ondas",
    "termodinámica",
    "química orgánica",
    "química inorgánica",
    "tabla periódica",
    "reacciones químicas",
    "enlaces químicos",
    "biología celular",
    "genética",
    "anatomía",
    "evolución",
    "microbiología",
    "historia del Perú",
    "historia universal",
    "revolución francesa",
    "independencia de América",
    "filosofía moderna",
    "ética",
    "ciudadanía",
    "derechos humanos",
    "arte precolombino",
    "historia del arte",
    "psicología",
    "sociología",
    "antropología",
    "redacción",
    "ortografía",
    "tipos de texto",
    "análisis literario",
    "figuras literarias",
    "comprensión lectora",
    "técnicas de exposición",
    "ensayos",
    "argumentación",
    "citas APA",
    "referencias bibliográficas",
    "programación",
    "pseudocódigo",
    "Python",
    "HTML",
    "CSS",
    "JavaScript",
    "redes",
    "algoritmos",
    "base de datos",
    "ciberseguridad",
    "sistemas operativos",
    "informática educativa",
    "Excel",
    "resumen",
    "apuntes",
    "separata",
    "práctica resuelta",
    "solución paso a paso",
    "clase grabada",
    "guía de estudio",
    "tips de examen",
    "examen anterior",
    "ciclo regular",
    "sustitutorio",
    "exoneración",
    "educación inicial",
    "educación secundaria",
    "matemáticas y física",
    "ingeniería industrial",
    "derecho",
    "medicina humana",
    "enfermería",
    "contabilidad",
    "administración",
    "psicología",
    "arquitectura",
    "agronomía",
    "UNMSM",
    "La Cantuta",
    "San Marcos",
    "UNI",
    "CEPRE",
    "EBA",
    "CEBA",
    "simulacro",
    "preuniversitario",
    "resumen gráfico",
    "infografía",
    "cuadro comparativo",
    "mapa mental",
    "ficha técnica",
    "esquema",
    "línea de tiempo",
    "guía de laboratorio",
    "rúbrica",
    "portafolio",
  ];

  let noteModal;
  if (openNoteBtn && noteModalEl) {
    noteModal = new bootstrap.Modal(noteModalEl);
    openNoteBtn.addEventListener("click", () => noteModal.show());
  }

  let tagify;
  if (tagInput) {
    tagify = new Tagify(tagInput, {
      whitelist: tagSuggestions,
      dropdown: { maxItems: 20, enabled: 0, closeOnSelect: false },
    });
  }

  const imageInput = document.getElementById("uploadImage");
  if (imageInput) {
    imageInput.addEventListener("change", (e) => {
      const file = e.target.files[0];
      const label = document.getElementById("fileLabelText");
      label.textContent = `📎 ${file?.name || "Seleccionar imagen"}`;
      if (!file) {
        document.querySelector(".preview-img").innerHTML = "";
        return;
      }
      const reader = new FileReader();
      reader.onload = (ev) => {
        document.querySelector(
          ".preview-img"
        ).innerHTML = `<img src="${ev.target.result}" alt="Preview">`;
      };
      reader.readAsDataURL(file);
    });
  }

  const postForm = document.getElementById("postForm");
  if (postForm) {
    postForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(postForm);
      try {
        const resp = await fetch("/crear_post", {
          method: "POST",
          body: formData,
          headers: { "X-Requested-With": "XMLHttpRequest" },
        });
        if (!resp.ok) throw new Error("error");
        const data = await resp.json();
        addPostToFeed(data.post);
        postForm.reset();
        document.querySelector(".preview-img").innerHTML = "";
      } catch (err) {
        alert("Ocurrió un error al publicar");
      }
    });
  }

  if (noteForm) {
    noteForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!noteForm.checkValidity()) {
        noteForm.classList.add("was-validated");
        return;
      }
      const formData = new FormData(noteForm);
      try {
        const resp = await fetch("/quick_note", {
          method: "POST",
          body: formData,
          headers: { "X-Requested-With": "XMLHttpRequest" },
        });
        if (!resp.ok) throw new Error("error");
        const data = await resp.json();
        addNoteToFeed(data.note);
        noteForm.reset();
        if (tagify) tagify.removeAllTags();
        if (noteModal) noteModal.hide();
        showToast("✅ Apunte subido con éxito");
      } catch (err) {
        alert("Ocurrió un error al publicar");
      }
    });
  }

  function addPostToFeed(post) {
    const container = document.querySelector(".feed-container");
    const article = document.createElement("article");
    article.className = "note-card post-card card animate-fade";
    const imgPart = post.image_url
      ? `<div class="text-center mt-2"><img src="${post.image_url}" class="img-fluid mx-auto d-block rounded shadow-sm" style="max-height: 300px; object-fit: contain;" alt="imagen"></div>`
      : "";
    article.innerHTML = `
      <div class="card-body">
        <p class="note-meta mb-1">
          <i class="fas fa-user me-1"></i>${post.user_name} — ${post.user_career}
        </p>
        <p class="note-desc">${post.content}</p>
        ${imgPart}
      </div>
      <div class="d-flex justify-content-around border-top pt-2 post-actions">
        <button class="btn btn-light btn-sm"><i class="fas fa-heart me-1 text-danger"></i>Me gusta</button>
        <button class="btn btn-light btn-sm"><i class="fas fa-comment-alt me-1 text-secondary"></i>Comentar</button>
        <button class="btn btn-light btn-sm"><i class="fas fa-bookmark me-1 text-primary"></i>Guardar</button>
        <button class="btn btn-light btn-sm"><i class="fas fa-share me-1 text-info"></i>Compartir</button>
      </div>`;
    container.insertBefore(article, container.querySelector(".post-toggle").nextSibling);
    article.querySelectorAll('.post-actions button').forEach((btn) => {
      btn.addEventListener('click', () => {
        btn.classList.toggle('active');
      });
    });
  }

  function addNoteToFeed(note) {
    const container = document.querySelector(".feed-container");
    const article = document.createElement("article");
    article.className = "note-card card animate-fade";
    const preview = `<embed src="${note.file_url}#page=1" type="application/pdf" class="w-100" style="height:180px; object-fit:cover;" />`;
    article.innerHTML = `
      <div class="note-image">${preview}</div>
      <div class="card-body">
        <h5 class="note-title">${note.title}</h5>
        <p class="note-desc">${note.description}</p>
        <p class="note-meta mb-1"><i class="fas fa-user me-1"></i>${note.user_name} – ${note.user_career}</p>
      </div>`;
    const marker = container.querySelector("h2.fw-bold");
    container.insertBefore(article, marker.nextSibling);
  }
});
