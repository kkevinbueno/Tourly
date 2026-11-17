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
