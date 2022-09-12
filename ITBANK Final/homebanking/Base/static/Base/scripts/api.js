let cotizacionLista = [
  "dolarOficial",
  "dolarBlue",
  "dolarSoja",
  "dolarContadoConLiqui",
  "dolarBolsa",
  "bitcoin",
  "dolarTurista",
];

const date = new Date();
let isRequestPerformed = false

function api_request() {
  if (!isRequestPerformed) {
    fetch("https://www.dolarsi.com/api/api.php?type=valoresprincipales")
    .then((response) => response.json())
    .then((data) => {
      for (let index in cotizacionLista) {
        let element = document.getElementById(cotizacionLista[index]);

        let body = document.createElement("div");

        body.setAttribute("class", "card bg-light mb-3");

        let cardHeader = document.createElement("div");

        cardHeader.setAttribute(
          "class",
          "card-header bg-secondary text-white text-center"
        );
        cardHeader.innerText = data[index].casa.nombre;

        let cardBody = document.createElement("div");

        let transactionLabel = document.createElement("div");

        transactionLabel.setAttribute(
          "class",
          "row justify-content-md-center d-flex w-100"
        );

        let buyLabel = document.createElement("div");

        buyLabel.setAttribute("class", "col-6 text-center");
        buyLabel.style.fontSize = '80%';
        buyLabel.innerText = "Precio Compra:";

        let sellLabel = document.createElement("div");

        sellLabel.setAttribute("class", "col-6 text-center");
        sellLabel.style.fontSize = '80%';
        sellLabel.innerText = "Precio Venta:";

        transactionLabel.appendChild(buyLabel);
        transactionLabel.appendChild(sellLabel);

        let transactionValue = document.createElement("div");

        transactionValue.setAttribute("class", "row justify-content-md-center");

        let buyValue = document.createElement("div");

        buyValue.setAttribute("class", "col-6");
        buyValue.style.fontSize = '120%';
        buyValue.style.padding = '5%';
        buyValue.innerText =
          data[index].casa.compra == "No Cotiza"? "-": `$${data[index].casa.compra}`;

        let sellValue = document.createElement("div");

        sellValue.setAttribute("class", "col-6");
        sellValue.style.fontSize = '120%';
        sellValue.style.padding = '5%';
        sellValue.innerText =
          data[index].casa.venta == 0 ? "-" : `$${data[index].casa.venta}`;

        transactionValue.appendChild(buyValue);
        transactionValue.appendChild(sellValue);

        cardBody.appendChild(transactionLabel);
        cardBody.appendChild(transactionValue);

        let cardFooter = document.createElement("div");

        cardFooter.setAttribute("class", "card-footer text-muted fs-6");
        cardFooter.innerText = `última Actualización: ${date.getDate()}/${date.getMonth() + 1} ${date.getHours()}:${date.getMinutes()}'hs`;

        body.appendChild(cardHeader);
        body.appendChild(cardBody);
        body.appendChild(cardFooter);

        element.appendChild(body);
      }
    });
  }
  isRequestPerformed = true
}
function main() {
  setInterval(() => {
    api_request();
  }, 50000);
}

function toggleCurrencies() {
  api_request();

  let section = document.getElementById('seccionCotizaciones');
  let button = document.getElementById('botonDivisas')
  if (section.style.display == 'block') {
    section.style.display = 'none';
    button.innerText = 'Ver Detalles »'
  } else {
    section.style.display = 'block';
    button.innerText = 'Ocultar Detalles »'
  }
}