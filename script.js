async function carregarNoticias() {
    const container = document.getElementById("noticias-container");

    try {
        const resposta = await fetch("noticias.json");
        const noticias = await resposta.json();

        container.innerHTML = "";

        noticias.forEach(n => {
            container.innerHTML += `
                <div class="noticia">
                    <img src="${n.imagem}" alt="Imagem da notícia">
                    <h2>${n.titulo}</h2>
                    <p>${n.descricao}</p>
                    <a href="${n.link}" target="_blank">Ler mais</a>
                </div>
            `;
        });

    } catch (error) {
        container.innerHTML = "<p>Erro ao carregar notícias.</p>";
    }
}

carregarNoticias();
