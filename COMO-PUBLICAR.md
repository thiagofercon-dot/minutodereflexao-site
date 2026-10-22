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
  "time": "HH:MM (horário de Brasília da publicação, aparece no site como \"Publicado em ... às 9h55\")",
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

O tempo de leitura e a cor da capa são calculados sozinhos.

Guias digitais (e-books) que podem ser divulgados no fim do artigo, com o bloco `<div class="callout">`:

- "O labirinto do propósito": use `EBOOK_URL` no href. Para artigos de Propósito.
- "Gestão do tempo: produtividade com foco no que é essencial": use `EBOOK2_URL` no href.
  Para artigos sobre tempo, produtividade, foco, disciplina, rotina, procrastinação ou equilíbrio
  entre trabalho e descanso. A página do guia no site é `/guias/gestao-do-tempo/`.

Use no máximo um bloco de guia por artigo, o que tiver mais relação com o tema.

Teste localmente com `python3 build.py` e faça commit + push na `main`.

## Estilo de escrita (obrigatório)

Todo texto do blog, e tudo o que for escrito para os canais do Minuto de Reflexão
(Instagram, YouTube, e-books, legendas, stories), segue a skill
`estilo-de-escrita-minuto-de-reflexao`. Carregue a skill antes de escrever.

Resumo do estilo:

- Tom acolhedor, otimista e instrutivo, de quem quer ajudar a pessoa a dar o próximo passo.
- Fala direto com o leitor em segunda pessoa ("você", "sua vida"); "nós" só na abertura e no fechamento.
- Linguagem simples, sem jargão, sem gírias, sem emojis e sem tom de sermão.
- Construções da marca: "é importante...", "é preciso...", "lembre-se de que...", "tente...",
  "que tal começar hoje mesmo?". Conectivos que dão ritmo: "Além disso,", "Por isso,", "Em resumo,".
- Parágrafos de 3 a 4 frases. Cada bloco traz uma ideia e termina com uma orientação prática
  no imperativo ("Divida as tarefas em partes pequenas").
- Sempre que possível, um exemplo concreto do cotidiano ou uma pergunta que faça refletir.
  Nada de generalidades vagas e nenhuma frase repetida em partes diferentes do texto.
- Fechamento começando com "Em resumo", retomando os pontos principais e terminando com
  uma pergunta que convida à ação hoje.

No blog, o tamanho continua entre 800 e 1.200 palavras e as regras de SEO abaixo continuam
valendo. O pedido de inscrição e curtida da skill é só para vídeo; no blog o convite final
leva para outro artigo, para o Instagram ou para o guia "O labirinto do propósito".

## Identidade

Azul-marinho (#1D3B82 / #132A63) com azul-claro (#9FD8EF), títulos em Italiana maiúsculas,
textos em Sora, detalhes em Space Mono. Marca "Minuto de Reflexão", Instagram @minutodereflexao.comm.
Não incluir link para a página do Facebook.
