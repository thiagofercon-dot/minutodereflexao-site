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
  "keyword": "palavra-chave principal de cauda longa (não aparece no site, serve de controle)",
  "body": "<p>...</p><h2>...</h2><h3>...</h3><blockquote>...</blockquote>",
  "faq": [{"q": "Pergunta que as pessoas fazem no Google?", "a": "Resposta direta de 1 a 3 frases."}]
}
```

`faq` é opcional (3 perguntas recomendadas) e gera a seção "Perguntas frequentes" e a marcação FAQPage para o Google.
`updated` (AAAA-MM-DD) é opcional e indica a data da última revisão.

## Regras de SEO para cada artigo

- Uma palavra-chave principal de cauda longa por artigo, sem repetir a de outro artigo.
- A palavra-chave aparece no `title` (de preferência no início), na `desc`, no primeiro parágrafo (em <strong>), em pelo menos um <h2> e, se possível, no `slug`.
- `title` com até ~65 caracteres; `desc` com até ~155 caracteres.
- 1 ou 2 links internos no corpo para artigos relacionados (`<a href="/blog/slug/">texto descritivo</a>`).
- Os artigos relacionados no fim da página priorizam o mesmo tema automaticamente.

O tempo de leitura e a cor da capa são calculados sozinhos. O link do guia
"O labirinto do propósito" pode ser inserido no corpo com o texto `EBOOK_URL` no href.

Teste localmente com `python3 build.py` e faça commit + push na `main`.

## Identidade

Azul-marinho (#1D3B82 / #132A63) com azul-claro (#9FD8EF), títulos em Italiana maiúsculas,
textos em Sora, detalhes em Space Mono. Marca "Minuto de Reflexão", Instagram @minutodereflexao.comm.
Não incluir link para a página do Facebook.
