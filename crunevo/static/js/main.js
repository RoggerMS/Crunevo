// Lógica para el menú offcanvas y su integración con el botón atrás
function initOffcanvasMenu() {
    const offcanvasEl = document.getElementById("mobileMenu");
    if (!offcanvasEl) return;
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

// Lógica para el Modal de Búsqueda Global
function initGlobalSearch() {
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
}


function initFloatingSidebar() {
    const toggleBtn = document.getElementById("toggleFloatingSidebar");
    const content = document.getElementById("floatingSidebarContent");

    if (toggleBtn && content) {
        toggleBtn.addEventListener("click", () => {
            content.classList.toggle("d-none");
            const expanded = !content.classList.contains("d-none");
            toggleBtn.setAttribute("aria-expanded", expanded);
        });
    }
}

function initActionButtons() {
    const allActionButtons = document.querySelectorAll(
        ".note-actions .action-btn"
    );
    allActionButtons.forEach((btn) => {
        const action = btn.dataset.action;
        const id = btn.dataset.id;
        const storageKey = id ? `action-${action}-${id}` : null;
        if (storageKey && localStorage.getItem(storageKey) === "1") {
            btn.classList.add("active");
        }
        btn.addEventListener("click", () => {
            btn.classList.toggle("active");
            if (storageKey) {
                if (btn.classList.contains("active")) {
                    localStorage.setItem(storageKey, "1");
                } else {
                    localStorage.removeItem(storageKey);
                }
            }
        });
    });
}

function initTooltips() {
  document
    .querySelectorAll('[data-bs-toggle="tooltip"]')
    .forEach((el) => new bootstrap.Tooltip(el));
}

function initTagify(selector) {
  const el = typeof selector === "string" ? document.querySelector(selector) : selector;
  if (!el) return null;
  const suggestions = window.TAG_SUGGESTIONS || [];
  return new Tagify(el, {
    whitelist: suggestions,
    dropdown: { maxItems: 20, enabled: 0, closeOnSelect: false },
  });
}

function initImagePreview(fileSelector, previewSelector, labelSelector) {
  const fileInput = document.querySelector(fileSelector);
  const preview = document.querySelector(previewSelector);
  const label = labelSelector ? document.querySelector(labelSelector) : null;
  if (!fileInput) return;
  fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (label) label.textContent = `📎 ${file?.name || "Seleccionar archivo"}`;
    if (!file) {
      if (preview) preview.innerHTML = "";
      return;
    }
    const url = URL.createObjectURL(file);
    if (file.type === "application/pdf") {
      preview.innerHTML = `<embed src="${url}#page=1" type="application/pdf" class="w-100" style="height:180px; object-fit:cover;">`;
    } else if (file.type.startsWith("image/")) {
      preview.innerHTML = `<img src="${url}" class="img-fluid mx-auto d-block rounded" style="max-height:180px; object-fit:cover;">`;
    } else {
      preview.innerHTML = `<div class="text-center mt-2">${file.name}</div>`;
    }
  });
}

function initFeedForms() {
  const openNoteBtn = document.getElementById("openNoteModalBtn");
  const noteModalEl = document.getElementById("uploadNoteModal");
  const noteForm = document.getElementById("noteForm");
  const tagInput = document.getElementById("note-tags");

  let noteModal;
  if (openNoteBtn && noteModalEl) {
    noteModal = new bootstrap.Modal(noteModalEl);
    openNoteBtn.addEventListener("click", () => noteModal.show());
  }

  const tagify = initTagify(tagInput);
  initImagePreview("#uploadImage", ".preview-img", "#fileLabelText");

  const uploadForm = document.getElementById("uploadForm");
  const uploadTagInput = document.getElementById("upload-tags");
  const uploadTagify = initTagify(uploadTagInput);
  initImagePreview("#noteFile", ".preview-note", "#noteFileLabel");

  if (uploadForm) {
    uploadForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!uploadForm.checkValidity()) {
        uploadForm.classList.add("was-validated");
        return;
      }
      const formData = new FormData(uploadForm);
      try {
        const resp = await fetch(uploadForm.action, {
          method: "POST",
          body: formData,
          headers: { "X-Requested-With": "XMLHttpRequest" },
        });
        if (!resp.ok) throw new Error("error");
        uploadForm.reset();
        if (uploadTagify) uploadTagify.removeAllTags();
        showToast("✅ Apunte subido con éxito");
      } catch (err) {
        showToast("❌ Error al subir el apunte");
      }
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
        showToast("❌ Error al publicar");
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
        showToast("❌ Error al publicar");
      }
    });
  }

  function addPostToFeed(post) {
    const container = document.querySelector(".feed-container");
    const article = document.createElement("article");
    article.className = "post-card card animate-fade mb-3";
    const imgPart = post.image_url
      ? `<div class="text-center mt-2"><img src="${post.image_url}" class="img-fluid rounded" style="max-height: 300px; object-fit: contain;" alt="imagen"></div>`
      : "";
    const career = post.user_career || 'Carrera';
    article.innerHTML = `
      <div class="card-body">
        <div class="post-header d-flex align-items-center mb-2">
          <img src="${post.user_avatar}" class="avatar me-2" alt="avatar">
          <div>
            <strong>${post.user_name}</strong><br>
            <small class="text-muted">${career}</small>
          </div>
        </div>
        <p class="post-content">${post.content}</p>
        ${imgPart}
      </div>
      <div class="note-actions post-actions card-footer bg-white">
        <div class="action-row d-flex">
          <button class="action-btn" data-action="like" data-bs-toggle="tooltip" title="Me gusta"><i class="fas fa-heart me-1"></i>Me gusta</button>
          <button class="action-btn comment-toggle" data-bs-toggle="tooltip" title="Comentar"><i class="fas fa-comment me-1"></i>Comentar</button>
          <button class="action-btn" data-action="save" data-bs-toggle="tooltip" title="Guardar"><i class="fas fa-bookmark me-1"></i>Guardar</button>
          <button class="action-btn" data-action="share" data-bs-toggle="tooltip" title="Compartir"><i class="fas fa-share me-1"></i>Compartir</button>
        </div>
      </div>
      <div class="comment-area mt-2" style="display:none;">
        <input type="text" class="form-control comment-input" placeholder="Escribe un comentario..." />
      </div>`;
    container.insertBefore(article, container.querySelector(".create-post").nextSibling);
    initActionButtons();
    initCommentInputs(article);
  }

function addNoteToFeed(note) {
    const container = document.querySelector(".feed-container");
    const article = document.createElement("article");
    article.className = "note-card card animate-fade";
    const preview = `<embed src="${note.file_url}#page=1" type="application/pdf" class="w-100" style="height:180px; object-fit:cover;" />`;
    const career = note.user_career || 'Carrera';
    article.innerHTML = `
      <div class="note-image">${preview}</div>
      <div class="card-body">
        <h5 class="note-title">${note.title}</h5>
        <p class="note-desc">${note.description}</p>
        <p class="note-meta mb-1"><i class="fas fa-user me-1"></i>${note.user_name} – ${career}</p>
      </div>`;
  const target = container.querySelector(".create-post").nextSibling;
  container.insertBefore(article, target);
  }


  initCommentInputs();
}

function initCommentInputs(scope = document) {
  scope.querySelectorAll('.comment-toggle').forEach((btn) => {
    const area = scope.querySelector(`.comment-area[data-id="${btn.dataset.id}"]`);
    if (!area) return;
    const input = area.querySelector('.comment-input');
    btn.addEventListener('click', () => {
      area.style.display = area.style.display === 'none' ? 'block' : 'none';
      if (area.style.display !== 'none') input.focus();
    });
    input.addEventListener('keydown', async (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        const text = input.value.trim();
        if (!text) return;
        const formData = new FormData();
        formData.append('content', text);
        let resp;
        if (btn.dataset.type === 'note') {
          formData.append('note_id', btn.dataset.id);
          resp = await fetch('/comments/add', {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
          });
        } else {
          resp = await fetch(`/posts/${btn.dataset.id}/comment`, {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
          });
        }
        if (resp.ok) {
          input.value = '';
          area.style.display = 'none';
          showToast('✅ Comentario publicado');
        } else {
          showToast('❌ Error al comentar');
        }
      }
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initOffcanvasMenu();
  initGlobalSearch();
  initFloatingSidebar();
  initActionButtons();
  initFeedForms();
  initCommentInputs();
  initTooltips();
});
