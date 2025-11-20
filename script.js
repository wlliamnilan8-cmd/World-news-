let noticias = [];

async function carregarNoticias() {
    try {
        const resposta = await fetch("noticias.json?cache=" + Date.now());
        if (!resposta.ok) throw new Error("HTTP " + resposta.status);
        noticias = await resposta.json();

        if (!Array.isArray(noticias)) noticias = [];

        montarCarrossel();
        montarUltimas();
        montarTodas(noticias);
        ativarFiltros();
    } catch (e) {
        console.error("Erro ao carregar noticias.json:", e);
        document.getElementById("noticias").innerHTML =
            "<p style='color:red;text-align:center;padding:20px;'>Erro ao carregar notícias.</p>";
    }
}

function montarCarrossel() {
    const carrossel = document.getElementById("carrossel");
    if (!noticias.length) {
        carrossel.innerHTML = "<div class='carrossel-empty'>Nenhuma notícia disponível</div>";
        return;
    }
    let index = 0;
    carrossel.innerHTML = `<img src="${noticias[0].imagem}" alt="${escapeHtml(noticias[0].titulo)}">`;

    setInterval(() => {
        index = (index + 1) % noticias.length;
        carrossel.innerHTML = `<img src="${noticias[index].imagem}" alt="${escapeHtml(noticias[index].titulo)}">`;
    }, 4000);
}

function montarUltimas() {
    const ult = document.getElementById("ultimas");
    ult.innerHTML = "";
    noticias.slice(0, 5).forEach(n => {
        ult.innerHTML += gerarCard(n, true);
    });
}

function montarTodas(lista) {
    const container = document.getElementById("noticias");
    container.innerHTML = "";
    if (!lista.length) {
        container.innerHTML = "<p style='text-align:center;padding:20px;'>Sem notícias.</p>";
        return;
    }
    lista.forEach(n => container.innerHTML += gerarCard(n, false));
}

function gerarCard(n, compacto=false) {
    const titulo = escapeHtml(n.titulo || "Sem título");
    const desc = escapeHtml(n.descricao || "");
    const img = n.imagem || "https://via.placeholder.com/800x400";
    const link = n.link || "#";
    if (compacto) {
        return `
          <div class="noticia-card compact">
            <a href="${link}" target="_blank" rel="noopener">
              <div class="compact-left"><img src="${img}" alt="${titulo}"></div>
              <div class="compact-right"><h4>${titulo}</h4></div>
            </a>
          </div>`;
    }
    return `
      <div class="noticia-card">
        <img src="${img}" alt="${titulo}">
        <h3>${titulo}</h3>
        <p>${desc}</p>
        <a href="${link}" target="_blank" rel="noopener">Ler mais →</a>
      </div>`;
}

function ativarFiltros() {
    const botoes = document.querySelectorAll(".menu-btn");
    botoes.forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelector(".menu-btn.active")?.classList.remove("active");
            btn.classList.add("active");
            const filtro = btn.dataset.filter;
            if (filtro === "all") montarTodas(noticias);
            else montarTodas(noticias.filter(n => (n.categoria || "").toLowerCase() === filtro));
        });
    });
}

function escapeHtml(text) {
    return text.replace(/[&<>"']/g, function(m) { return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[m]; });
}

carregarNoticias();
