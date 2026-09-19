const gruposEstrelas = document.querySelectorAll(".estrelas");

let notas = {};

gruposEstrelas.forEach(function(grupo) {

    const estrelas = grupo.querySelectorAll("span");
    const categoria = grupo.getAttribute("data-categoria");

    // O <p> que mostra a nota
    const resultado = grupo.nextElementSibling;

    estrelas.forEach(function(estrela) {

        estrela.addEventListener("click", function() {

            const nota = Number(
                estrela.getAttribute("data-nota")
            );

            // Guarda a nota da categoria
            notas[categoria] = nota;

            // Mostra a nota escolhida
            resultado.textContent =
                categoria + ": " + nota + "/5 ⭐";


            // Coloca a nota no input escondido
            if (categoria === "elenco") {
                document.getElementById("notaElenco").value = nota;
            }

            if (categoria === "direcao") {
                document.getElementById("notaDirecao").value = nota;
            }

            if (categoria === "roteiro") {
                document.getElementById("notaRoteiro").value = nota;
            }

            if (categoria === "figurino") {
                document.getElementById("notaFigurino").value = nota;
            }

            if (categoria === "trilha_sonora") {
                document.getElementById("notaTrilha").value = nota;
            }


            // =========================
            // CALCULAR A MÉDIA
            // =========================

            let soma = 0;
            let quantidade = 0;

            for (let categoria in notas) {

                soma = soma + notas[categoria];

                quantidade = quantidade + 1;

            }


            // Faz a média
            let media = soma / quantidade;


            // Mostra a média na tela
            document.getElementById("mediaCategorias").textContent =
                media.toFixed(1) + "/5 ⭐";


            console.log("Notas:", notas);
            console.log("Média:", media);

        });

    });

});