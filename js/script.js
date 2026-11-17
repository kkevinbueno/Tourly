
// Fix for tabs
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
        tabcontent[i].classList.remove("active");
    }
    tablinks = document.getElementsByClassName("tab-button");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }
    document.getElementById(tabName).style.display = "block";
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}

// Contato form submission
const formContato = document.getElementById("formContato");
if (formContato) {
    formContato.addEventListener("submit", async (e) => {
        e.preventDefault();
        const data = {
            nome: document.getElementById("nome").value,
            email: document.getElementById("email").value,
            mensagem: document.getElementById("mensagem").value
        };
        await fetch('/api/contatos', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        alert("Contato enviado!");
        formContato.reset();
    });
}

// Reserva logic
const formReserva = document.getElementById("formReserva");
const listaReservas = document.getElementById("listaReservas");

async function carregarReservas() {
    if (!listaReservas) return;
    listaReservas.innerHTML = "";
    const res = await fetch('/api/reservas');
    const reservas = await res.json();
    reservas.forEach(r => {
        const div = document.createElement("div");
        div.className = "reserva-item";
        div.innerHTML = `
            <span><strong>${r.nome_cliente}</strong> - ${r.destino} (${r.data_viagem})</span>
            <button onclick="deletarReserva(${r.id})">Excluir</button>
        `;
        listaReservas.appendChild(div);
    });
}

if (formReserva) {
    formReserva.addEventListener("submit", async (e) => {
        e.preventDefault();
        const data = {
            nome_cliente: document.getElementById("nome_cliente").value,
            destino: document.getElementById("destino").value,
            data_viagem: document.getElementById("data_viagem").value
        };
        await fetch('/api/reservas', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        formReserva.reset();
        carregarReservas();
    });
    carregarReservas(); // load initially
}
async function deletarReserva(id) {
    await fetch(`/api/reservas/${id}`, { method: 'DELETE' });
    carregarReservas();
}
