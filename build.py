# -*- coding: utf-8 -*-
"""Gera o site estático do blog Minuto de Reflexão."""
import os, re, json, html, datetime, shutil

SITE = "https://minutodereflexao.com"
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
IG = "https://www.instagram.com/minutodereflexao.comm/"
FB = "https://www.facebook.com/search/top?q=Minuto%20de%20Reflex%C3%A3o"
YT = "https://www.youtube.com/@minutodereflexaoBr"
EBOOK = "https://pay.hotmart.com/W107585689S"
EBOOK2 = "https://go.hotmart.com/J108088170D"
BRAND = "Minuto de Reflexão"
HANDLE = "@minutodereflexao.comm"
GA_ID = "G-F8THCF6TXM"

def load_articles():
    d = os.path.join(ROOT, "content", "articles")
    items = []
    for fn in os.listdir(d):
        if fn.endswith(".json"):
            with open(os.path.join(d, fn), encoding="utf-8") as f:
                items.append(json.load(f))
    items.sort(key=lambda x: (x["date"], x.get("seq", 0)), reverse=True)
    covers = ["c1", "c2", "c3"]
    for i, it in enumerate(items):
        it.setdefault("cover", covers[i % 3])
        it.setdefault("read", max(3, round(len(re.sub(r"<[^>]+>", " ", it["body"]).split()) / 200)))
    return items

ARTICLES = load_articles()

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]

def data_br(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} de {MESES[d.month-1]} de {d.year}"

ICONS = {
    "ig": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.3" cy="6.7" r="1.2" fill="currentColor"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.8 1.4-3.8 3.9v2.3H8v3h2.5V21h3z" fill="currentColor"/></svg>',
    "yt": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.6 7.2a2.5 2.5 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4A2.5 2.5 0 0 0 2.4 7.2 26 26 0 0 0 2 12a26 26 0 0 0 .4 4.8 2.5 2.5 0 0 0 1.8 1.8C5.8 19 12 19 12 19s6.2 0 7.8-.4a2.5 2.5 0 0 0 1.8-1.8A26 26 0 0 0 22 12a26 26 0 0 0-.4-4.8zM10 15V9l5.2 3L10 15z" fill="currentColor"/></svg>',
}

def social_links():
    return (f'<a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{ICONS["ig"]}</a>'
            f'<a href="{YT}" target="_blank" rel="noopener" aria-label="YouTube">{ICONS["yt"]}</a>')

def page(path, title, desc, body, active="", og_type="website", extra_head=""):
    canonical = SITE + path
    full_title = title if title == BRAND else f"{title} | {BRAND}"
    nav = [("/", "Início", "inicio"), ("/blog/", "Blog", "blog"),
           ("/sobre/", "Sobre", "sobre"), ("/contato/", "Contato", "contato")]
    nav_html = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if k == active else ""}>{t}</a>' for h, t, k in nav)
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:locale" content="pt_BR">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1D3B82">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Italiana&family=Sora:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
<script>
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
var mdrConsent=null;try{{mdrConsent=localStorage.getItem('mdr_consent');}}catch(e){{}}
gtag('consent','default',{{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:mdrConsent==='granted'?'granted':'denied'}});
gtag('js',new Date());gtag('config','{GA_ID}');
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
{extra_head}
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '2184221455784624');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=2184221455784624&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="logo" href="/" aria-label="{BRAND}, página inicial">
      <span class="logo-mark" aria-hidden="true">M</span>
      <span class="logo-text">{BRAND}</span>
    </a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="menu" aria-label="Abrir menu"><span></span><span></span></button>
    <nav id="menu" class="nav" aria-label="Principal">
      {nav_html}
      <a class="btn btn-small" href="/guias/">Guias digitais</a>
    </nav>
  </div>
</header>
<main id="conteudo">
{body}
</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <p class="footer-brand">{BRAND}</p>
      <p class="footer-tag">Encontre sua força interior.</p>
      <p class="mono footer-handle">{HANDLE}</p>
    </div>
    <div>
      <p class="mono footer-title">Navegue</p>
      <a href="/blog/">Blog</a><a href="/sobre/">Sobre</a><a href="/contato/">Contato</a><a href="/privacidade/">Privacidade</a>
    </div>
    <div>
      <p class="mono footer-title">Acompanhe</p>
      <div class="social">{social_links()}</div>
    </div>
  </div>
  <div class="wrap footer-bottom mono">© 2026 {BRAND} · Inspire-se e reflita</div>
</footer>
<div class="cookie-bar" id="cookie-bar" hidden>
  <p>Usamos cookies de análise (Google Analytics) para entender como o site é usado e melhorar o conteúdo. Saiba mais na <a href="/privacidade/">política de privacidade</a>.</p>
  <div class="cookie-actions">
    <button type="button" class="btn btn-small-ghost" data-consent="denied">Recusar</button>
    <button type="button" class="btn btn-primary" data-consent="granted">Aceitar</button>
  </div>
</div>
<script>
(function(){{var bar=document.getElementById('cookie-bar');if(!bar)return;var c=null;try{{c=localStorage.getItem('mdr_consent');}}catch(e){{}}
if(!c)bar.hidden=false;
bar.addEventListener('click',function(e){{var v=e.target.getAttribute('data-consent');if(!v)return;try{{localStorage.setItem('mdr_consent',v);}}catch(err){{}}
gtag('consent','update',{{analytics_storage:v}});bar.hidden=true;}});}})();
</script>
<script>
(function(){{var b=document.querySelector('.menu-toggle'),n=document.getElementById('menu');
if(!b)return;b.addEventListener('click',function(){{var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o);}});}})();
</script>
</body>
</html>
"""

def guide_cards():
    return f"""<div class="guides">
  <article class="guide">
    <div class="ebook-cover" aria-hidden="true">
      <span class="mono">Guia</span>
      <span class="ebook-cover-title">O labirinto do propósito</span>
      <span class="mono ebook-cover-brand">{BRAND}</span>
    </div>
    <div>
      <p class="mono kicker">Propósito</p>
      <h3>O labirinto do propósito</h3>
      <p>Como identificar seu chamado em meio ao caos. Um guia de leitura leve, com linguagem simples e exercícios práticos para você sair da dúvida e dar o próximo passo com clareza.</p>
      <a class="btn btn-light" href="{EBOOK}" target="_blank" rel="noopener">Quero o guia</a>
    </div>
  </article>
  <article class="guide">
    <div class="ebook-cover alt" aria-hidden="true">
      <span class="mono">Leitura 360</span>
      <span class="ebook-cover-title">Gestão do tempo</span>
      <span class="mono ebook-cover-brand">Foco no essencial</span>
    </div>
    <div>
      <p class="mono kicker">Produtividade</p>
      <h3>Gestão do tempo</h3>
      <p>Produtividade com foco no que é essencial. Descubra como recuperar o controle da sua agenda e viver com mais foco, propósito e paz, mesmo em meio à correria do dia a dia.</p>
      <a class="btn btn-light" href="/guias/gestao-do-tempo/">Conhecer o guia</a>
      <a class="guide-link" href="{EBOOK2}" target="_blank" rel="noopener">Comprar agora <span aria-hidden="true">→</span></a>
    </div>
  </article>
</div>"""

def card(a):
    return f"""<article class="card">
  <a class="card-cover {a['cover']}" href="/blog/{a['slug']}/" aria-hidden="true" tabindex="-1">
    <span class="mono card-cover-tag">{a['tag']}</span>
    <span class="card-cover-quote">“{a['quote']}”</span>
  </a>
  <div class="card-body">
    <p class="mono meta">{a['tag']} · {a['read']} min de leitura</p>
    <h3><a href="/blog/{a['slug']}/">{a['title']}</a></h3>
    <p>{a['desc']}</p>
    <a class="link-arrow" href="/blog/{a['slug']}/">Ler artigo <span aria-hidden="true">→</span></a>
  </div>
</article>"""

def write(rel, content):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

def build():
    shutil.rmtree(OUT, ignore_errors=True)
    shutil.copytree(os.path.join(ROOT, "static"), OUT)
    cards = "\n".join(card(a) for a in ARTICLES[:3])
    all_cards = "\n".join(card(a) for a in ARTICLES)

    home = f"""
<section class="hero">
  <div class="hero-waves" aria-hidden="true"></div>
  <div class="wrap hero-inner">
    <p class="mono kicker">Encontre sua força interior</p>
    <h1 class="display">Um minuto para pensar.<br>Uma vida para mudar.</h1>
    <p class="lead">Reflexões curtas e práticas sobre motivação, propósito, superação e desenvolvimento pessoal, para você seguir em frente, um dia de cada vez.</p>
    <div class="hero-actions">
      <a class="btn btn-light" href="/blog/">Ler o blog</a>
      <a class="btn btn-ghost" href="{IG}" target="_blank" rel="noopener">Seguir no Instagram</a>
    </div>
    <p class="mono hero-handle">{BRAND} {HANDLE}</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="mono kicker dark">Últimas reflexões</p>
      <h2 class="title">Do blog</h2>
    </div>
    <div class="grid">{cards}</div>
    <p class="center"><a class="btn btn-primary" href="/blog/">Ver todos os artigos</a></p>
  </div>
</section>

<section class="section section-mist">
  <div class="wrap pillars">
    <div class="section-head">
      <p class="mono kicker dark">Sobre o que falamos</p>
      <h2 class="title">Quatro caminhos para evoluir</h2>
    </div>
    <div class="pillar-grid">
      <div class="pillar"><span class="mono">01</span><h3>Motivação</h3><p>Como começar, e principalmente como continuar quando a vontade some.</p></div>
      <div class="pillar"><span class="mono">02</span><h3>Propósito</h3><p>Encontrar direção e sentido mesmo quando tudo parece confuso.</p></div>
      <div class="pillar"><span class="mono">03</span><h3>Superação</h3><p>Levantar depois das quedas e transformar dor em aprendizado.</p></div>
      <div class="pillar"><span class="mono">04</span><h3>Desenvolvimento pessoal</h3><p>Pequenos ajustes diários que mudam quem você é ao longo do tempo.</p></div>
    </div>
  </div>
</section>

<section class="section ebook" id="guias">
  <div class="wrap">
    <p class="mono kicker">Guias digitais</p>
    <h2 class="title light">Para ir mais fundo</h2>
    {guide_cards()}
  </div>
</section>

<section class="section">
  <div class="wrap community">
    <p class="mono kicker dark">Reflexão do dia</p>
    <p class="big-quote">“Não espere a motivação. Comece, e ela aparece no caminho.”</p>
    <p>Todos os dias tem uma reflexão nova no nosso Instagram e no canal do YouTube. Venha fazer parte.</p>
    <div class="social social-big">{social_links()}</div>
  </div>
</section>
"""
    write("index.html", page("/", BRAND,
        "Reflexões curtas e práticas sobre motivação, propósito, superação e desenvolvimento pessoal. Encontre sua força interior.",
        home, "inicio"))

    blog = f"""
<section class="page-hero">
  <div class="wrap">
    <p class="mono kicker">Blog</p>
    <h1 class="display">Reflexões para<br>o seu dia</h1>
    <p class="lead">Textos curtos para ler em poucos minutos e levar para a vida.</p>
  </div>
</section>
<section class="section">
  <div class="wrap"><div class="grid">{all_cards}</div></div>
</section>
"""
    write("blog/index.html", page("/blog/", "Blog",
        "Artigos sobre motivação, propósito, superação e desenvolvimento pessoal do Minuto de Reflexão.", blog, "blog"))

    for i, a in enumerate(ARTICLES):
        rest = [x for x in ARTICLES if x is not a]
        others = ([x for x in rest if x["tag"] == a["tag"]] + [x for x in rest if x["tag"] != a["tag"]])[:2]
        body_html = a["body"].replace("EBOOK2_URL", EBOOK2).replace("EBOOK_URL", EBOOK)
        faq = a.get("faq") or []
        faq_html = ""
        if faq:
            faq_html = '<section class="faq">\n<h2>Perguntas frequentes</h2>\n' + "\n".join(
                f"<h3>{html.escape(f['q'])}</h3>\n<p>{html.escape(f['a'])}</p>" for f in faq) + "\n</section>"
        ld = {
            "@context": "https://schema.org", "@type": "BlogPosting",
            "headline": a["title"], "description": a["desc"],
            "datePublished": a["date"], "dateModified": a.get("updated", a["date"]),
            "inLanguage": "pt-BR",
            "author": {"@type": "Organization", "name": BRAND},
            "publisher": {"@type": "Organization", "name": BRAND,
                          "logo": {"@type": "ImageObject", "url": SITE + "/assets/og.jpg"}},
            "mainEntityOfPage": f"{SITE}/blog/{a['slug']}/",
            "image": SITE + "/assets/og.jpg",
        }
        art = f"""
<article class="post">
  <header class="post-hero {a['cover']}">
    <div class="wrap narrow">
      <p class="mono kicker"><a href="/blog/">Blog</a> · {a['tag']}</p>
      <h1 class="post-title">{a['title']}</h1>
      <p class="mono post-meta">{data_br(a['date'])} · {a['read']} min de leitura</p>
    </div>
  </header>
  <div class="wrap narrow post-body">
    {body_html}
    {faq_html}
    <div class="share">
      <p class="mono">Gostou? Compartilhe esta reflexão</p>
      <div class="share-links">
        <a href="https://wa.me/?text={html.escape(a['title'])}%20{SITE}/blog/{a['slug']}/" target="_blank" rel="noopener">WhatsApp</a>
        <a href="https://www.facebook.com/sharer/sharer.php?u={SITE}/blog/{a['slug']}/" target="_blank" rel="noopener">Facebook</a>
        <a href="{IG}" target="_blank" rel="noopener">Instagram</a>
      </div>
    </div>
  </div>
</article>
<section class="section section-mist">
  <div class="wrap">
    <div class="section-head"><p class="mono kicker dark">Continue lendo</p><h2 class="title">Outras reflexões</h2></div>
    <div class="grid grid-2">{''.join(card(o) for o in others)}</div>
  </div>
</section>
"""
        write(f"blog/{a['slug']}/index.html", page(f"/blog/{a['slug']}/", a["title"], a["desc"], art, "blog", "article",
              f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
              + (f'\n<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faq]}, ensure_ascii=False)}</script>' if faq else "")))

    guias = f"""
<section class="page-hero">
  <div class="wrap">
    <p class="mono kicker">Guias digitais</p>
    <h1 class="display">Para ir<br>mais fundo</h1>
    <p class="lead">Leituras práticas para quem quer transformar reflexão em atitude no dia a dia.</p>
  </div>
</section>
<section class="section ebook">
  <div class="wrap">{guide_cards()}</div>
</section>
"""
    write("guias/index.html", page("/guias/", "Guias digitais",
        "Guias digitais do Minuto de Reflexão: O labirinto do propósito e Gestão do tempo, leituras práticas para viver com mais foco e propósito.", guias, "guias"))

    gestao = f"""
<section class="page-hero">
  <div class="wrap guide-hero">
    <div>
      <p class="mono kicker"><a href="/guias/">Guias digitais</a> · Leitura 360</p>
      <h1 class="display">Gestão<br>do tempo</h1>
      <p class="lead">Produtividade com foco no que é essencial. Descubra como recuperar o controle da sua agenda e viver com mais foco, propósito e paz, mesmo em meio à correria do dia a dia.</p>
      <a class="btn btn-light" href="{EBOOK2}" target="_blank" rel="noopener">Quero o meu exemplar</a>
    </div>
    <div class="ebook-cover alt" aria-hidden="true">
      <span class="mono">Leitura 360</span>
      <span class="ebook-cover-title">Gestão do tempo</span>
      <span class="mono ebook-cover-brand">Foco no essencial</span>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap narrow prose">
    <p class="lead dark">Você termina o dia cansado, com a sensação de que esteve ocupado o tempo todo, mas não avançou no que realmente importa? Se a sua lista de tarefas nunca acaba, este guia foi escrito para você.</p>
    <p>O e-book <strong>Gestão do tempo: produtividade com foco no que é essencial</strong> une descobertas da ciência sobre foco e planejamento a princípios de sabedoria atemporal. A proposta é olhar para o tempo não apenas como um recurso a ser administrado, mas como algo a ser vivido com sentido. Por isso, mais do que encaixar tarefas na agenda, você vai aprender a escolher o que merece o seu tempo.</p>

    <h2>Para quem é este guia</h2>
    <p>Ele foi pensado para profissionais, empreendedores, líderes e qualquer pessoa que sente que está sempre ocupada, mas sem avançar no que realmente importa. É para quem busca produtividade com propósito, e não apenas uma lista maior de tarefas cumpridas. Se você quer sair do modo automático e voltar a decidir como usa as suas horas, este é um bom ponto de partida.</p>

    <h2>O que você vai aprender nos 9 capítulos</h2>
    <p>A seguir, veja os principais caminhos que o guia percorre com você.</p>
    <h3>O tempo do relógio e o tempo do propósito</h3>
    <p>Entenda a diferença entre Chronos, o tempo que o relógio mede, e Kairós, o tempo que tem significado. É essa distinção que muda a forma como você enxerga a sua agenda.</p>
    <h3>O essencial primeiro</h3>
    <p>Aprenda a escolher o que realmente importa e a dizer não, com tranquilidade, ao que não importa.</p>
    <h3>Foco profundo em meio às distrações</h3>
    <p>Descubra como treinar a atenção para trabalhar de forma concentrada, mesmo cercado de notificações e interrupções.</p>
    <h3>Energia, e não apenas horas</h3>
    <p>Lembre-se de que uma hora com energia vale mais do que três horas no cansaço. O guia mostra como gerenciar a sua energia ao longo do dia.</p>
    <h3>Planejamento realista</h3>
    <p>Saia da armadilha do "vai dar tempo" e aprenda a planejar com os pés no chão.</p>
    <h3>Rotinas que trabalham a seu favor</h3>
    <p>Crie hábitos e rotinas que sustentam o que é importante, sem depender da força de vontade a cada manhã.</p>
    <h3>Descanso sem culpa</h3>
    <p>Entenda por que o descanso faz parte do trabalho, e não é um prêmio que só vem depois dele.</p>

    <h2>Um caderno de práticas para aplicar no dia a dia</h2>
    <p>Além do conteúdo, o guia traz um caderno de práticas com exercícios simples para você aplicar cada conceito na sua rotina. É importante transformar leitura em ação, e é exatamente para isso que esses exercícios existem. Tente fazer um por dia, no seu ritmo, e observe como a sua relação com o tempo começa a mudar.</p>

    <blockquote>O tempo não é só para administrar. É para viver com sentido.</blockquote>

    <h2>Em resumo</h2>
    <p>Em resumo, este guia ajuda você a separar o urgente do essencial, proteger o seu foco, cuidar da sua energia, planejar com realismo e descansar sem culpa. São escolhas pequenas que, somadas, devolvem a você o controle da própria agenda. Que tal começar hoje mesmo a viver o seu tempo com mais foco, propósito e paz?</p>

    <div class="callout">
      <p class="callout-kicker">Guia digital · e-book</p>
      <p><strong>Gestão do tempo: produtividade com foco no que é essencial.</strong> Garanta o seu exemplar e comece a aplicar as estratégias ainda hoje.</p>
      <p><a class="btn btn-primary" href="{EBOOK2}" target="_blank" rel="noopener">Quero o meu exemplar</a></p>
    </div>
    <p>Quer começar agora? Leia também <a href="/blog/motivacao-ou-disciplina/">como ter disciplina quando a motivação acaba</a>.</p>
  </div>
</section>
"""
    write("guias/gestao-do-tempo/index.html", page("/guias/gestao-do-tempo/", "Gestão do tempo: produtividade com foco no essencial",
        "E-book Gestão do tempo: recupere o controle da sua agenda e viva com mais foco, propósito e paz, mesmo na correria do dia a dia.", gestao, "guias"))

    sobre = f"""
<section class="page-hero">
  <div class="wrap">
    <p class="mono kicker">Sobre</p>
    <h1 class="display">Um minuto pode<br>mudar o seu dia</h1>
  </div>
</section>
<section class="section">
  <div class="wrap narrow prose">
    <p class="lead dark">O <strong>{BRAND}</strong> nasceu de uma ideia simples: no meio da correria, todo mundo merece um minuto para parar, respirar e pensar no próprio caminho.</p>
    <p>Aqui você encontra reflexões curtas e práticas sobre motivação, propósito, superação e desenvolvimento pessoal. Nada de fórmulas mágicas ou promessas impossíveis, só ideias honestas, em linguagem simples, que você pode aplicar ainda hoje.</p>
    <blockquote>Evoluir não é virar outra pessoa. É continuar ajustando quem você já é.</blockquote>
    <p>Além do blog, publicamos reflexões todos os dias no Instagram <a href="{IG}" target="_blank" rel="noopener">{HANDLE}</a> e no canal do YouTube. Também criamos guias digitais, como <a href="{EBOOK}" target="_blank" rel="noopener">O labirinto do propósito</a> e <a href="/guias/gestao-do-tempo/">Gestão do tempo</a>, para quem quer ir mais fundo.</p>
    <p>Que cada visita aqui seja um pequeno passo na direção de quem você quer ser.</p>
    <div class="social social-big">{social_links()}</div>
  </div>
</section>
"""
    write("sobre/index.html", page("/sobre/", "Sobre",
        "Conheça o Minuto de Reflexão: reflexões curtas e práticas para encontrar sua força interior.", sobre, "sobre"))

    contato = f"""
<section class="page-hero">
  <div class="wrap">
    <p class="mono kicker">Contato</p>
    <h1 class="display">Fale com a gente</h1>
    <p class="lead">Dúvidas, sugestões de tema ou parcerias. Respondemos o mais rápido possível.</p>
  </div>
</section>
<section class="section">
  <div class="wrap narrow">
    <form class="form" name="contato" method="POST" action="/obrigado/" data-netlify="true" netlify-honeypot="empresa">
      <input type="hidden" name="form-name" value="contato">
      <p class="hidden"><label>Não preencha: <input name="empresa"></label></p>
      <label>Nome<input type="text" name="nome" required autocomplete="name"></label>
      <label>E-mail<input type="email" name="email" required autocomplete="email"></label>
      <label>Assunto
        <select name="assunto">
          <option>Sugestão de tema</option><option>Dúvida sobre o guia</option><option>Parceria</option><option>Outro</option>
        </select>
      </label>
      <label>Mensagem<textarea name="mensagem" rows="6" required></textarea></label>
      <label class="check"><input type="checkbox" name="aceite" required> Li e concordo com a <a href="/privacidade/">política de privacidade</a>.</label>
      <button class="btn btn-primary" type="submit">Enviar mensagem</button>
    </form>
    <p class="center muted">Prefere falar pelas redes? Mande uma mensagem no Instagram <a href="{IG}" target="_blank" rel="noopener">{HANDLE}</a>.</p>
  </div>
</section>
"""
    write("contato/index.html", page("/contato/", "Contato",
        "Entre em contato com o Minuto de Reflexão.", contato, "contato"))

    obrigado = f"""
<section class="page-hero tall">
  <div class="wrap">
    <p class="mono kicker">Mensagem enviada</p>
    <h1 class="display">Obrigado!</h1>
    <p class="lead">Recebemos sua mensagem e vamos responder em breve. Enquanto isso, que tal uma reflexão?</p>
    <a class="btn btn-light" href="/blog/">Ir para o blog</a>
  </div>
</section>
"""
    write("obrigado/index.html", page("/obrigado/", "Obrigado", "Mensagem enviada com sucesso.", obrigado,
          extra_head='<meta name="robots" content="noindex">'))

    priv = f"""
<section class="page-hero">
  <div class="wrap"><p class="mono kicker">Transparência</p><h1 class="display">Política de privacidade</h1></div>
</section>
<section class="section">
  <div class="wrap narrow prose">
    <p>Esta política explica como o {BRAND} trata as informações de quem visita o site {SITE.replace('https://','')}, em linha com a Lei Geral de Proteção de Dados (LGPD).</p>
    <h2>Dados que coletamos</h2>
    <p>Coletamos apenas os dados que você nos envia voluntariamente pelo formulário de contato (nome, e-mail e mensagem). Esses dados são usados exclusivamente para responder ao seu contato e não são vendidos nem compartilhados com terceiros para fins comerciais.</p>
    <h2>Cookies e estatísticas de uso</h2>
    <p>Usamos o Google Analytics para entender, de forma agregada, como as pessoas usam o site (páginas mais lidas, tempo de leitura, de onde vêm as visitas). Os cookies de análise só são ativados se você clicar em "Aceitar" no aviso de cookies; se recusar, o site continua funcionando normalmente. Você pode mudar sua escolha a qualquer momento limpando os dados de navegação deste site. Não usamos cookies de publicidade.</p>
    <h2>Links externos</h2>
    <p>O site contém links para Instagram, Facebook, YouTube e para a plataforma de pagamento Hotmart. Ao acessá-los, valem as políticas de privacidade dessas plataformas.</p>
    <h2>Seus direitos</h2>
    <p>Você pode pedir a qualquer momento acesso, correção ou exclusão dos seus dados, pelo formulário de <a href="/contato/">contato</a>.</p>
    <p class="muted">Última atualização: {data_br('2026-10-17')}.</p>
  </div>
</section>
"""
    write("privacidade/index.html", page("/privacidade/", "Política de privacidade",
        "Política de privacidade do Minuto de Reflexão.", priv))

    notfound = """
<section class="page-hero tall">
  <div class="wrap">
    <p class="mono kicker">Erro 404</p>
    <h1 class="display">Página não encontrada</h1>
    <p class="lead">Às vezes o caminho muda, e tudo bem. Volte para o início e siga em frente.</p>
    <a class="btn btn-light" href="/">Voltar ao início</a>
  </div>
</section>
"""
    write("404.html", page("/404", "Página não encontrada", "Página não encontrada.", notfound,
          extra_head='<meta name="robots" content="noindex">'))

    urls = ["/", "/blog/", "/guias/", "/guias/gestao-do-tempo/", "/sobre/", "/contato/", "/privacidade/"] + [f"/blog/{a['slug']}/" for a in ARTICLES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>2026-10-17</lastmod></url>\n" for u in urls)
    sm += "</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

if __name__ == "__main__":
    build()
    print("ok", OUT)
