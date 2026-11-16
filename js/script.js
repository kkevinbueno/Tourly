(() => {
  'use strict';

  const raiz = document.body.dataset.raiz || '';
  const destinos = [
    { nome: 'Rio de Janeiro', regiao: 'Rio de Janeiro · Sudeste', resumo: 'Praias, paisagens icônicas e uma energia que contagia.', imagem: 'rio-de-janeiro.svg', tag: 'Praia e cidade' },
    { nome: 'Fernando de Noronha', regiao: 'Pernambuco · Nordeste', resumo: 'Mar cristalino, natureza preservada e experiências únicas.', imagem: 'fernando-de-noronha.svg', tag: 'Natureza' },
    { nome: 'Gramado', regiao: 'Rio Grande do Sul · Sul', resumo: 'Clima acolhedor, gastronomia e charme em cada estação.', imagem: 'gramado.svg', tag: 'Serra' },
    { nome: 'Bonito', regiao: 'Mato Grosso do Sul · Centro-Oeste', resumo: 'Rios transparentes, grutas e ecoturismo de tirar o fôlego.', imagem: 'bonito.svg', tag: 'Ecoturismo' },
    { nome: 'Lençóis Maranhenses', regiao: 'Maranhão · Nordeste', resumo: 'Dunas claras e lagoas que formam um cenário inesquecível.', imagem: 'lencois-maranhenses.svg', tag: 'Aventura' }
  ];

  const esc = (s) => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const card = (d) => `<article class="destino-card reveal"><a class="destino-card__imagem" href="${raiz}pages/destinos.html?q=${encodeURIComponent(d.nome)}"><img src="${raiz}img/destinos/${d.imagem}" alt="Paisagem de ${esc(d.nome)}" loading="lazy"><span>${esc(d.tag)}</span></a><div class="destino-card__corpo"><p class="destino-card__regiao">${esc(d.regiao)}</p><h3>${esc(d.nome)}</h3><p>${esc(d.resumo)}</p><a class="link-seta" href="${raiz}pages/destinos.html?q=${encodeURIComponent(d.nome)}">Explorar destino <span aria-hidden="true">→</span></a></div></article>`;

  const destaque = document.getElementById('destaques');
  if (destaque) destaque.innerHTML = destinos.slice(0, 3).map(card).join('');

  const gradeDestinos = document.getElementById('lista-destinos');
  const buscaDestinos = document.getElementById('busca-destinos');
  const filtro = (termo = '') => {
    if (!gradeDestinos) return;
    const q = termo.trim().toLocaleLowerCase('pt-BR');
    const encontrados = destinos.filter(d => `${d.nome} ${d.regiao} ${d.tag} ${d.resumo}`.toLocaleLowerCase('pt-BR').includes(q));
    gradeDestinos.innerHTML = encontrados.length ? encontrados.map(card).join('') : '<p class="sem-resultados">Não encontramos esse destino. Tente buscar por outra cidade ou região.</p>';
    observarReveals();
  };
  if (gradeDestinos) {
    const params = new URLSearchParams(location.search);
    const inicial = params.get('q') || '';
    if (buscaDestinos) buscaDestinos.value = inicial;
    filtro(inicial);
    buscaDestinos?.addEventListener('input', () => filtro(buscaDestinos.value));
  }

  const formBusca = document.getElementById('form-busca-hero');
  formBusca?.addEventListener('submit', e => {
    e.preventDefault();
    const termo = document.getElementById('busca-hero')?.value.trim() || '';
    location.href = `${raiz}pages/destinos.html?q=${encodeURIComponent(termo)}`;
  });

  const menuBtn = document.querySelector('.menu-btn');
  const menu = document.querySelector('.menu');
  menuBtn?.addEventListener('click', () => {
    const aberto = menuBtn.getAttribute('aria-expanded') === 'true';
    menuBtn.setAttribute('aria-expanded', String(!aberto));
    menu?.classList.toggle('menu--aberto', !aberto);
    menuBtn.setAttribute('aria-label', aberto ? 'Abrir menu' : 'Fechar menu');
  });
  menu?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    menu.classList.remove('menu--aberto');
    menuBtn?.setAttribute('aria-expanded', 'false');
  }));

  document.querySelectorAll('[data-nav]').forEach(link => {
    if (link.dataset.nav === document.body.dataset.pagina) link.setAttribute('aria-current', 'page');
  });
  document.querySelectorAll('[data-ano]').forEach(el => el.textContent = new Date().getFullYear());

  const status = document.getElementById('status-api');
  if (status) {
    fetch('/api/health').then(async response => {
      const data = await response.json();
      status.textContent = response.ok ? 'Servidor e banco conectados' : 'Servidor online · banco desconectado';
      status.title = data.detalhe || '';
      status.classList.toggle('status--erro', !response.ok);
    }).catch(() => {
      status.textContent = 'Não foi possível verificar a conexão';
      status.classList.add('status--erro');
    });
  }

  const formContato = document.getElementById('form-contato');
  formContato?.addEventListener('submit', async e => {
    e.preventDefault();
    const aviso = document.getElementById('aviso-contato');
    const botao = formContato.querySelector('button[type="submit"]');
    const campos = ['nome', 'email', 'mensagem'];
    let valido = true;
    campos.forEach(nome => {
      const campo = formContato.elements[nome];
      const erro = document.getElementById(`erro-${nome}`);
      let mensagem = '';
      if (!campo.value.trim()) mensagem = 'Este campo é obrigatório.';
      else if (nome === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(campo.value.trim())) mensagem = 'Informe um e-mail válido.';
      if (erro) erro.textContent = mensagem;
      campo.setAttribute('aria-invalid', String(Boolean(mensagem)));
      valido = valido && !mensagem;
    });
    if (!valido) {
      aviso.hidden = false; aviso.className = 'alerta alerta--erro'; aviso.textContent = 'Revise os campos destacados.';
      return;
    }
    const payload = Object.fromEntries(campos.map(nome => [nome, formContato.elements[nome].value.trim()]));
    botao.disabled = true; botao.textContent = 'Enviando…';
    aviso.hidden = true;
    try {
      const response = await fetch('/api/contatos', {
        method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.detalhes?.join(' ') || data.erro || 'Não foi possível enviar sua mensagem.');
      formContato.reset();
      campos.forEach(nome => { const erro = document.getElementById(`erro-${nome}`); if (erro) erro.textContent = ''; });
      aviso.className = 'alerta alerta--sucesso';
      aviso.textContent = 'Mensagem enviada com sucesso! Nossa equipe recebeu seu contato.';
    } catch (erro) {
      aviso.className = 'alerta alerta--erro';
      aviso.textContent = `${erro.message} Verifique se o servidor Flask e o MySQL estão funcionando.`;
    } finally {
      aviso.hidden = false; botao.disabled = false; botao.textContent = 'Enviar mensagem';
    }
  });

  function observarReveals() {
    const elementos = document.querySelectorAll('.reveal:not(.reveal--visivel)');
    if (!('IntersectionObserver' in window)) { elementos.forEach(el => el.classList.add('reveal--visivel')); return; }
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('reveal--visivel'); observer.unobserve(entry.target); }
    }), { threshold: 0.12 });
    elementos.forEach(el => observer.observe(el));
  }
  observarReveals();
})();
