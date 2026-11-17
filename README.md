# Tourly ✈️
Agência de viagens — Projeto Integrado (DWS + POO + BD).

**Stack:** HTML/CSS/JS (Fetch) · Python/Flask (POO: models, DAOs, rotas) · SQLite

## Rodar localmente
```bash
pip install -r requirements.txt
python app.py        # http://localhost:5000
```
O banco `banco.db` é criado sozinho a partir de `database/banco.sql`.

## API
| Método | Rota | Descrição |
|---|---|---|
| GET/POST | `/api/reservas` | listar / criar reserva |
| DELETE | `/api/reservas/<id>` | excluir reserva |
| GET/POST | `/api/contatos` | listar / enviar contato |

## GitHub Pages
Settings → Pages → Deploy from branch → `main` / `(root)`.
O Pages só hospeda arquivos estáticos, então o site detecta se o Flask está acessível:
- **Com servidor** (URL em `js/config.js` → `TOURLY_API_URL`): usa Fetch nas rotas Flask.
- **Sem servidor**: entra em *modo demonstração* (selo no canto da tela) e salva no navegador.

## Fotos dos destinos
As imagens dos destinos, do hero e do banner de contato são fotos reais do [Wikimedia Commons](https://commons.wikimedia.org), carregadas direto da internet (`Special:FilePath`). Os PNGs da pasta `png/` ficam só como reserva se a foto não carregar.

| Uso | Arquivo no Commons |
|---|---|
| Hero (topo do site) | [Rio de Janeiro, Pão de Açúcar from Cristo Redentor](https://commons.wikimedia.org/wiki/File:Rio_de_Janeiro,_P%C3%A3o_de_A%C3%A7%C3%BAcar_from_Cristo_Redentor_(15744316848).jpg) |
| Rio de Janeiro | [Rio de Janeiro - Cristo Redentor 01](https://commons.wikimedia.org/wiki/File:Rio_de_Janeiro_-_Cristo_Redentor_01.jpg) |
| São Paulo | [Cidade de São Paulo](https://commons.wikimedia.org/wiki/File:Cidade_de_S%C3%A3o_Paulo.jpg) |
| Fernando de Noronha | [FernandoDeNoronhaPraiaSancho](https://commons.wikimedia.org/wiki/File:FernandoDeNoronhaPraiaSancho.jpg) |
| Salvador | [Largo do Pelourinho 2019-6501](https://commons.wikimedia.org/wiki/File:Centro_Hist%C3%B3rico_de_Salvador_Bahia_Largo_do_Pelourinho_2019-6501.jpg) |
| Foz do Iguaçu | [Parque Nacional do Iguaçú (14116137781)](https://commons.wikimedia.org/wiki/File:Parque_Nacional_do_Igua%C3%A7%C3%BA_-_Igua%C3%A7u_National_Park_(14116137781).jpg) |
| Gramado | [Lagonegro3](https://commons.wikimedia.org/wiki/File:Lagonegro3.jpg) |
| Contato | [Fernando de Noronha Conceicao Beach](https://commons.wikimedia.org/wiki/File:Fernando_de_Noronha_Conceicao_Beach.jpg) |

Cada página de arquivo mostra o autor e a licença (CC) para dar o crédito certo.
