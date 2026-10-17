# Site Minuto de Reflexão (minutodereflexao.com)

Site estático gerado por `build.py` (Python 3, sem dependências) e publicado pelo Netlify
a cada commit na branch `main` (comando `python3 build.py`, pasta publicada `site/`).

## Publicar um artigo novo

Crie um arquivo em `content/articles/AAAA-MM-DD-slug.json`:

```json
{
  "slug": "titulo-curto-com-hifens",
  "title": "Título do artigo",
  "desc": "Resumo de 1 a 2 frases (até ~160 caracteres), usado no Google e nos cards.",
  "tag": "Motivação | Propósito | Superação | Desenvolvimento pessoal",
  "date": "AAAA-MM-DD",
  "quote": "Frase de destaque curta (até ~60 caracteres), aparece na capa do card.",
  "body": "<p>...</p><h2>...</h2><h3>...</h3><blockquote>...</blockquote>"
}
```

O tempo de leitura e a cor da capa são calculados sozinhos. O link do guia
"O labirinto do propósito" pode ser inserido no corpo com o texto `EBOOK_URL` no href.

Teste localmente com `python3 build.py` e faça commit + push na `main`.

## Identidade

Azul-marinho (#1D3B82 / #132A63) com azul-claro (#9FD8EF), títulos em Italiana maiúsculas,
textos em Sora, detalhes em Space Mono. Marca "Minuto de Reflexão", Instagram @minutodereflexao.comm.
Não incluir link para a página do Facebook.
