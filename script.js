async function carregarNoticias() {
    const container = document.getElementById("noticias-container");

    try {
        const resposta = await fetch("noticias.json");
        const noticias = await resposta.json();

        window.todasNoticias = noticias;
        exibirNoticias("all");

    } catch (err) {
        container.innerHTML = "<p>Erro ao carregar notícias.</p>";
    }
}

function exibirNoticias(filtro) {
    const container = document.getElementById("noticias-container");
    container.innerHTML = "";

    const lista = filtro === "all"
        ? window.todasNoticias
        : window.todasNoticias.filter(n => n.categoria === filtro);

    lista.forEach(n => {
        container.innerHTML += `
            <div class="noticia">
                <img src="${n.imagem}" alt="">
                <h2>${n.titulo}</h2>
                <p>${n.descricao}</p>
                <a href="${n.link}" target="_blank">Ler mais</a>
            </div>
        `;
    });
}

document.querySelectorAll(".menu button").forEach(btn => {
    btn.addEventListener("click", () => {
        document.querySelector(".menu .active")?.classList.remove("active");
        btn.classList.add("active");
        exibirNoticias(btn.dataset.filter);
    });
});

carregarNoticias();
