const gruposEstrelas = document.querySelectorAll(".estrelas");

let notas = {};

gruposEstrelas.forEach(function(grupo) {

    const estrelas = grupo.querySelectorAll("span");
    const categoria = grupo.getAttribute("data-categoria");
    const resultado = grupo.nextElementSibling;

    estrelas.forEach(function(estrela) {

        estrela.addEventListener("click", function() {

            const nota = Number(estrela.getAttribute("data-nota"));

            notas[categoria] = nota;

            resultado.textContent = categoria + ": " + nota + "/5 ⭐";

            let soma = 0;
            let quantidade = 0;

            for (let categoria in notas) {

                soma = soma + notas[categoria];
                quantidade = quantidade + 1;

            }

            const media = soma / quantidade;

            document.getElementById("notaGeral").textContent = media.toFixed(1);

        });

    });

});