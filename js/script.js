/* ===== Tourly — front-end (Fetch -> rotas Flask, com fallback de demonstração) ===== */

const DESTINOS = [
  { id: "rio", img: "rio.png", nome: "Rio de Janeiro", uf: "RJ", emoji: "🏖️", cor: "c1",
    desc: "Cristo Redentor, Pão de Açúcar e praias que fazem parte do cartão-postal do Brasil.",
    tags: ["Praia", "Cultura"], preco: "a partir de R$ 1.290" },
  { id: "sp", img: "sao-paulo.png", nome: "São Paulo", uf: "SP", emoji: "🌆", cor: "c2",
    desc: "A cidade que não para: gastronomia de classe mundial, museus e vida noturna.",
    tags: ["Urbano", "Gastronomia"], preco: "a partir de R$ 890" },
  { id: "noronha", img: "fernando-de-noronha.png", nome: "Fernando de Noronha", uf: "PE", emoji: "🐢", cor: "c3",
    desc: "Um paraíso na Terra: mergulho, tartarugas e o pôr do sol mais famoso do país.",
    tags: ["Ecoturismo", "Mergulho"], preco: "a partir de R$ 3.490" },
  { id: "salvador", img: "salvador.png", nome: "Salvador", uf: "BA", emoji: "🥁", cor: "c4",
    desc: "Pelourinho, axé, acarajé e uma cultura afro-brasileira vibrante.",
    tags: ["Cultura", "Praia"], preco: "a partir de R$ 1.150" },
  { id: "foz", img: "foz-do-iguacu.png", nome: "Foz do Iguaçu", uf: "PR", emoji: "🌊", cor: "c5",
    desc: "As Cataratas do Iguaçu, uma das sete maravilhas naturais do mundo.",
    tags: ["Natureza", "Aventura"], preco: "a partir de R$ 980" },
  { id: "gramado", img: "gramado.png", nome: "Gramado", uf: "RS", emoji: "🏔️", cor: "c6",
    desc: "Charme europeu na serra gaúcha, com chocolate quente e muito aconchego.",
    tags: ["Serra", "Romântico"], preco: "a partir de R$ 1.420" },
];

/* ---------- utilidades ---------- */
const RAIZ = location.pathname.includes("/pages/") ? "../" : "./";
const imgDestino = (nome) => (DESTINOS.find((d) => d.nome === nome) || DESTINOS[0]).img;

const esc = (s) => String(s).replace(/[&<>"']/g, (c) =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

const fmtData = (iso) => {
  const [y, m, d] = String(iso).split("-");
  return y && m && d ? `${d}/${m}/${y}` : iso;
};

function toast(msg, tipo = "ok") {
  let box = document.getElementById("toasts");
  if (!box) { box = document.createElement("div"); box.id = "toasts"; document.body.appendChild(box); }
  const t = document.createElement("div");
  t.className = `toast ${tipo}`;
  t.textContent = msg;
  box.appendChild(t);
  setTimeout(() => t.classList.add("out"), 3200);
  setTimeout(() => t.remove(), 3700);
}

/* ---------- camada de API ---------- */
const API = (() => {
  const isLocal = ["localhost", "127.0.0.1", ""].includes(location.hostname);
  const base = (window.TOURLY_API_URL || (isLocal ? "" : null));
  let demo = base === null; // sem API configurada (ex.: GitHub Pages puro)

  const LS = { reservas: "tourly_reservas", contatos: "tourly_contatos", seq: "tourly_seq" };
  const lerLS = (k) => { try { return JSON.parse(localStorage.getItem(k)) || []; } catch { return []; } };
  const gravarLS = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} };
  const proxId = () => {
    let n = 1; try { n = (parseInt(localStorage.getItem(LS.seq)) || 0) + 1; localStorage.setItem(LS.seq, n); } catch {}
    return n;
  };

  async function http(path, opts = {}) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 8000);
    try {
      const res = await fetch(base + path, {
        ...opts, signal: ctrl.signal,
        headers: { "Content-Type": "application/json" },
      });
      const body = await res.json().catch(() => ({}));
      if (!res.ok) { const e = new Error(body.error || "Erro no servidor"); e.http = true; throw e; }
      return body;
    } finally { clearTimeout(timer); }
  }

  // Tenta a API; se o servidor estiver inacessível, cai para o modo demonstração.
  async function tentar(apiFn, demoFn) {
    if (!demo) {
      try { return await apiFn(); }
      catch (e) { if (e.http) throw e; demo = true; atualizarBadge(); }
    }
    return demoFn();
  }

  function atualizarBadge() {
    let b = document.getElementById("modoBadge");
    if (!b) {
      b = document.createElement("div"); b.id = "modoBadge";
      document.body.appendChild(b);
    }
    b.className = demo ? "demo" : "online";
    b.innerHTML = demo
      ? '<span class="dot"></span> Modo demonstração · dados salvos neste navegador'
      : '<span class="dot"></span> Conectado ao servidor Flask';
    b.title = demo ? "O servidor Flask não está acessível; usando armazenamento local." : "";
  }

  const api = {
    get demo() { return demo; },
    badge: atualizarBadge,

    listarReservas: () => tentar(
      () => http("/api/reservas"),
      () => lerLS(LS.reservas).sort((a, b) => a.data_viagem.localeCompare(b.data_viagem))
    ),
    criarReserva: (d) => tentar(
      () => http("/api/reservas", { method: "POST", body: JSON.stringify(d) }),
      () => { const l = lerLS(LS.reservas); l.push({ id: proxId(), ...d }); gravarLS(LS.reservas, l); return { message: "Reserva salva!" }; }
    ),
    atualizarReserva: (id, d) => tentar(
      () => http(`/api/reservas/${id}`, { method: "PUT", body: JSON.stringify(d) }),
      () => { gravarLS(LS.reservas, lerLS(LS.reservas).map((r) => r.id === id ? { id, ...d } : r)); return {}; }
    ),
    excluirReserva: (id) => tentar(
      () => http(`/api/reservas/${id}`, { method: "DELETE" }),
      () => { gravarLS(LS.reservas, lerLS(LS.reservas).filter((r) => r.id !== id)); return {}; }
    ),
    enviarContato: (d) => tentar(
      () => http("/api/contatos", { method: "POST", body: JSON.stringify(d) }),
      () => { const l = lerLS(LS.contatos); l.push({ id: proxId(), ...d }); gravarLS(LS.contatos, l); return { message: "Contato salvo!" }; }
    ),
  };
  return api;
})();

/* ---------- navegação ---------- */
(function nav() {
  const btn = document.getElementById("menuBtn");
  const nav = document.querySelector("header nav");
  if (btn && nav) btn.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    btn.setAttribute("aria-expanded", open);
  });
  const atual = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("header nav a").forEach((a) => {
    if (a.getAttribute("href").split("/").pop() === atual) a.classList.add("ativo");
  });
  const h = document.querySelector("header");
  const onScroll = () => h && h.classList.toggle("scrolled", window.scrollY > 10);
  onScroll(); window.addEventListener("scroll", onScroll, { passive: true });

  // revelar ao rolar
  const io = "IntersectionObserver" in window && new IntersectionObserver((es) => {
    es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach((el) => io ? io.observe(el) : el.classList.add("in"));
})();

/* ---------- Home: destinos em destaque ---------- */
const destaques = document.getElementById("destaques");
if (destaques) {
  destaques.innerHTML = DESTINOS.slice(0, 3).map(cardDestino).join("");
}

function cardDestino(d) {
  return `
  <article class="card-destino">
    <div class="card-img"><img src="${RAIZ}png/${d.img}" alt="Ilustração de ${esc(d.nome)}" loading="lazy"><span class="uf">${esc(d.uf)}</span></div>
    <div class="card-body">
      <div class="tags">${d.tags.map((t) => `<span>${esc(t)}</span>`).join("")}</div>
      <h3>${esc(d.nome)}</h3>
      <p>${esc(d.desc)}</p>
      <div class="card-foot">
        <strong>${esc(d.preco)}</strong>
        <a class="btn btn-sm" href="${RAIZ}pages/reservas.html?destino=${encodeURIComponent(d.nome)}">Reservar</a>
      </div>
    </div>
  </article>`;
}

/* ---------- Destinos: grade com filtro ---------- */
const gradeDestinos = document.getElementById("gradeDestinos");
if (gradeDestinos) {
  const filtros = document.getElementById("filtros");
  const tags = ["Todos", ...new Set(DESTINOS.flatMap((d) => d.tags))];
  filtros.innerHTML = tags.map((t, i) =>
    `<button class="chip${i === 0 ? " active" : ""}" data-tag="${esc(t)}">${esc(t)}</button>`).join("");
  const render = (tag) => {
    const lista = tag === "Todos" ? DESTINOS : DESTINOS.filter((d) => d.tags.includes(tag));
    gradeDestinos.innerHTML = lista.map(cardDestino).join("");
    gradeDestinos.querySelectorAll(".reveal").forEach((el) => el.classList.add("in"));
  };
  filtros.addEventListener("click", (e) => {
    const b = e.target.closest(".chip"); if (!b) return;
    filtros.querySelectorAll(".chip").forEach((c) => c.classList.toggle("active", c === b));
    render(b.dataset.tag);
  });
  render("Todos");
}

/* ---------- Contato (somente alert) ---------- */
const formContato = document.getElementById("formContato");
if (formContato) {
  formContato.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      await API.enviarContato({
        nome: document.getElementById("nome").value,
        email: document.getElementById("email").value,
        mensagem: document.getElementById("mensagem").value,
      });
      alert("Contato enviado!");
      formContato.reset();
    } catch (err) { alert("Erro ao enviar: " + err.message); }
  });
}

/* ---------- Reservas (tempo real: atualiza a cada 3s, edita e exclui) ---------- */
const formReserva = document.getElementById("formReserva");
const listaReservas = document.getElementById("listaReservas");
let reservasAtuais = [], assinatura = "", editandoId = null;

async function carregarReservas(forcar = false) {
  if (!listaReservas) return;
  let reservas;
  try { reservas = await API.listarReservas(); }
  catch (err) { if (forcar) toast(err.message, "erro"); return; }
  API.badge();
  const sig = JSON.stringify(reservas);
  if (!forcar && sig === assinatura) return; // nada mudou: evita piscar
  assinatura = sig; reservasAtuais = reservas;
  document.getElementById("contador").textContent = reservas.length;
  if (!reservas.length) {
    listaReservas.innerHTML = `<div class="vazio"><img src="${RAIZ}png/sem-reservas.png" alt=""><p>Nenhuma reserva ainda.<br>Faça a primeira ao lado!</p></div>`;
    return;
  }
  listaReservas.innerHTML = reservas.map((r) => `
    <div class="reserva-item${r.id === editandoId ? " editando" : ""}">
      <img class="thumb" src="${RAIZ}png/${imgDestino(r.destino)}" alt="">
      <div class="reserva-info"><strong>${esc(r.destino)}</strong><span>${esc(r.nome_cliente)}</span></div>
      <div class="reserva-data"><b>${esc(fmtData(r.data_viagem).slice(0, 5))}</b><small>${esc(fmtData(r.data_viagem).slice(6))}</small></div>
      <div class="acoes">
        <button class="btn-ico btn-edit" data-id="${Number(r.id)}" aria-label="Editar reserva" title="Editar">✎</button>
        <button class="btn-ico btn-del" data-id="${Number(r.id)}" aria-label="Excluir reserva" title="Excluir">🗑</button>
      </div>
    </div>`).join("");
}

if (formReserva) {
  const sel = document.getElementById("destino");
  const nome = document.getElementById("nome_cliente");
  const data = document.getElementById("data_viagem");
  const btnSalvar = document.getElementById("btnSalvar");
  const btnCancelar = document.getElementById("btnCancelar");
  const titulo = document.getElementById("tituloForm");

  sel.innerHTML = '<option value="" disabled selected>Escolha um destino…</option>' +
    DESTINOS.map((d) => `<option>${esc(d.nome)}</option>`).join("");
  data.min = new Date().toISOString().slice(0, 10);
  const pre = new URLSearchParams(location.search).get("destino");
  if (pre && DESTINOS.some((d) => d.nome === pre)) sel.value = pre;

  function sairEdicao() {
    editandoId = null; formReserva.reset();
    btnSalvar.textContent = "Agendar reserva"; titulo.textContent = "Fazer reserva";
    btnCancelar.hidden = true; carregarReservas(true);
  }
  btnCancelar.addEventListener("click", sairEdicao);

  formReserva.addEventListener("submit", async (e) => {
    e.preventDefault();
    btnSalvar.disabled = true;
    const dados = { nome_cliente: nome.value, destino: sel.value, data_viagem: data.value };
    try {
      if (editandoId) { await API.atualizarReserva(editandoId, dados); toast("Reserva atualizada! ✅"); sairEdicao(); }
      else { await API.criarReserva(dados); toast("Reserva confirmada! ✈️"); formReserva.reset(); await carregarReservas(true); }
    } catch (err) { toast(err.message, "erro"); }
    btnSalvar.disabled = false;
  });

  listaReservas.addEventListener("click", async (e) => {
    const b = e.target.closest(".btn-ico"); if (!b) return;
    const id = Number(b.dataset.id);
    if (b.classList.contains("btn-edit")) {
      const r = reservasAtuais.find((x) => x.id === id); if (!r) return;
      editandoId = id; nome.value = r.nome_cliente; sel.value = r.destino; data.value = r.data_viagem;
      data.min = ""; btnSalvar.textContent = "Salvar alterações"; titulo.textContent = "Editar reserva";
      btnCancelar.hidden = false; carregarReservas(true);
      formReserva.scrollIntoView({ behavior: "smooth", block: "center" }); nome.focus();
    } else {
      if (!confirm("Excluir esta reserva?")) return;
      try {
        await API.excluirReserva(id);
        if (editandoId === id) sairEdicao();
        toast("Reserva excluída."); carregarReservas(true);
      } catch (err) { toast(err.message, "erro"); }
    }
  });

  carregarReservas(true);
  setInterval(() => { if (!document.hidden) carregarReservas(); }, 3000);
  window.addEventListener("storage", () => carregarReservas());
  document.addEventListener("visibilitychange", () => { if (!document.hidden) carregarReservas(); });
}
