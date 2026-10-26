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
AUTHOR = "Thiago Fernandes"
AUTHOR_BIO = ("Escritor e fundador da Editora Prumo e do Minuto de Reflexão. Escreve sobre propósito, foco e "
              "desenvolvimento pessoal com linguagem simples e aplicável ao dia a dia. É autor dos e-books "
              "O labirinto do propósito e Gestão do tempo.")
TEMAS = {
    "Motivação": ("motivacao", "Como começar, e principalmente como continuar quando a vontade some."),
    "Propósito": ("proposito", "Encontrar direção e sentido mesmo quando tudo parece confuso."),
    "Superação": ("superacao", "Levantar depois das quedas e transformar dor em aprendizado."),
    "Desenvolvimento pessoal": ("desenvolvimento-pessoal", "Pequenos ajustes diários que mudam quem você é ao longo do tempo."),
}

def tema_url(tag):
    return f"/blog/tema/{TEMAS[tag][0]}/" if tag in TEMAS else "/blog/"

def article_img(a):
    """Imagem do artigo feita no Canva, se já existir em static/assets/artigos/."""
    rel = f"assets/artigos/{a['slug']}.jpg"
    return "/" + rel if os.path.exists(os.path.join(ROOT, "static", rel)) else ""

def temas_nav(atual=""):
    links = [f'<a href="/blog/"{" aria-current=\"page\"" if not atual else ""}>Todos</a>']
    for tag, (slug, _) in TEMAS.items():
        cur = ' aria-current="page"' if tag == atual else ""
        links.append(f'<a href="/blog/tema/{slug}/"{cur}>{tag}</a>')
    return '<nav class="temas" aria-label="Temas">' + "".join(links) + "</nav>"

def load_articles():
    d = os.path.join(ROOT, "content", "articles")
    items = []
    for fn in os.listdir(d):
        if fn.endswith(".json"):
            with open(os.path.join(d, fn), encoding="utf-8") as f:
                it = json.load(f)
            if not it.get("time"):
                it["time"] = git_time(os.path.join("content", "articles", fn))
            items.append(it)
    items.sort(key=lambda x: (x["date"], x.get("time") or "", x.get("seq", 0)), reverse=True)
    covers = ["c1", "c2", "c3"]
    for i, it in enumerate(items):
        it.setdefault("cover", covers[i % 3])
        it.setdefault("read", max(3, round(len(re.sub(r"<[^>]+>", " ", it["body"]).split()) / 200)))
    return items

ARTICLES = load_articles()

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]

def git_time(rel):
    """Horário (BRT) do commit que adicionou o arquivo, usado quando o JSON não traz "time"."""
    try:
        import subprocess
        out = subprocess.run(["git", "log", "--diff-filter=A", "--date=format-local:%H:%M", "--format=%cd", "--", rel],
                             cwd=ROOT, capture_output=True, text=True, env={**os.environ, "TZ": "America/Sao_Paulo"}).stdout.split()
        return out[-1] if out else ""
    except Exception:
        return ""

def hora_br(hhmm):
    h, m = hhmm.split(":")
    return f"{int(h)}h{m}"

def data_curta(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day:02d}/{d.month:02d}/{d.year}"

def iso_dt(a):
    return f"{a['date']}T{a['time']}:00-03:00" if a.get("time") else a["date"]

def publicado(a, curto=False):
    d = data_curta(a["date"]) if curto else data_br(a["date"])
    return d

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

def page(path, title, desc, body, active="", og_type="website", extra_head="", og_image=""):
    canonical = SITE + path
    full_title = title if title == BRAND else f"{title} | {BRAND}"
    nav = [("/", "Início", "inicio"), ("/blog/", "Artigos", "blog"),
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
<meta property="og:image" content="{SITE}{og_image or "/assets/og.jpg"}">
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
      <a class="btn btn-small" href="/guias/">E-books</a>
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
      <a href="/blog/">Artigos</a><a href="/sobre/">Sobre</a><a href="/contato/">Contato</a><a href="/privacidade/">Privacidade</a>
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
(function(){{var pr=document.querySelector('[data-product]');
if(pr&&window.fbq)fbq('track','ViewContent',{{content_name:pr.getAttribute('data-product'),content_type:'product'}});
document.addEventListener('click',function(e){{var a=e.target.closest&&e.target.closest('a[data-checkout]');if(!a)return;var n=a.getAttribute('data-checkout');
if(window.fbq)fbq('track','InitiateCheckout',{{content_name:n}});
if(window.gtag)gtag('event','begin_checkout',{{items:[{{item_name:n}}]}});}});}})();
</script>
<script>
(function(){{var b=document.querySelector('.menu-toggle'),n=document.getElementById('menu');
if(!b)return;b.addEventListener('click',function(){{var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o);}});}})();
</script>
</body>
</html>
"""

def load_guides():
    d = os.path.join(ROOT, "content", "guias")
    out = []
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".json"):
            with open(os.path.join(d, fn), encoding="utf-8") as f:
                out.append(json.load(f))
    return out

GUIDES = load_guides()

def checkout_btn(g, label, cls="btn btn-light"):
    url = EBOOK2 if g["ebook_var"] == "EBOOK2" else EBOOK
    return (f'<a class="{cls}" href="{url}" target="_blank" rel="noopener" '
            f'data-checkout="{html.escape(g["title"])}">{label}</a>')

def sales_page(g):
    e = html.escape
    path = f"/guias/{g['slug']}/"
    cover = f"""<div class="ebook-cover {g.get('cover','')}" aria-hidden="true">
      <span class="mono">{e(g['cover_top'])}</span>
      <span class="ebook-cover-title">{e(g['title'])}</span>
      <span class="mono ebook-cover-brand">{e(g['cover_bottom'])}</span>
    </div>"""
    trust = '<p class="mono sp-trust">E-book digital · Acesso pela Hotmart · 7 dias de garantia</p>'
    problem = "".join(f"<p>{e(x)}</p>" for x in g["problem"])
    cite = f'<cite class="mono">{e(g["quote_cite"])}</cite>' if g.get("quote_cite") else ""
    chapters = "".join(
        f'<div class="sp-chapter"><span class="mono">{i:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
        for i, (t, d) in enumerate(g["chapters"], 1))
    fmt = "".join(f"<p>{e(x)}</p>" for x in g["format"])
    fit = "".join(f"<li>{e(x)}</li>" for x in g["for"])
    nofit = "".join(f"<li>{e(x)}</li>" for x in g["not_for"])
    faq = "".join(f"<details><summary>{e(f['q'])}</summary><p>{e(f['a'])}</p></details>" for f in g["faq"])
    body = f"""
<section class="page-hero sp-hero" data-product="{e(g['title'])}">
  <div class="wrap sp-hero-inner">
    <p class="mono kicker"><a href="/guias/">E-books</a> · {e(g['kicker'].split(' · ')[-1])}</p>
    <h1 class="display">{e(g['title'])}</h1>
    <p class="sp-subtitle">{e(g['subtitle'])}</p>
    <img class="sp-cover" src="{g['cover_img']}" alt="Capa do e-book {e(g['title'])}" width="{g['cover_size'][0]}" height="{g['cover_size'][1]}">
    <p class="lead">{e(g['hero_lead'])}</p>
    {checkout_btn(g, "Quero o meu exemplar")}
    {trust}
  </div>
</section>

<section class="section">
  <div class="wrap narrow prose">
    <h2 class="sp-h2">{e(g['problem_title'])}</h2>
    {problem}
    <blockquote>{e(g['quote'])}{cite}</blockquote>
  </div>
</section>

<section class="section section-mist">
  <div class="wrap">
    <div class="narrow sp-head">
      <p class="mono kicker dark">Conteúdo</p>
      <h2 class="sp-h2">{e(g['chapters_title'])}</h2>
      <p>{e(g['chapters_intro'])}</p>
    </div>
    <div class="sp-chapters">{chapters}</div>
  </div>
</section>

<section class="section">
  <div class="wrap narrow prose">
    <h2 class="sp-h2">{e(g['format_title'])}</h2>
    {fmt}
  </div>
  <div class="wrap sp-fit">
    <div class="sp-fit-box yes">
      <p class="mono kicker dark">Este e-book é para você se</p>
      <ul>{fit}</ul>
    </div>
    <div class="sp-fit-box no">
      <p class="mono kicker dark">Talvez não seja para você se</p>
      <ul>{nofit}</ul>
    </div>
  </div>
</section>

<section class="section ebook">
  <div class="wrap narrow sp-cta">
    <p class="mono kicker">Uma reflexão para hoje</p>
    <p class="sp-summary">{e(g['summary'])}</p>
    {checkout_btn(g, "Quero o meu exemplar")}
    {trust}
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <div class="sp-guarantee">
      <p class="mono kicker dark">Garantia de 7 dias</p>
      <p>Você pode ler com tranquilidade. Se o e-book não fizer sentido para você nos primeiros 7 dias, é só pedir o reembolso pela própria Hotmart, sem complicação.</p>
    </div>
    <div class="sp-author">
      <img class="author-photo" src="/assets/thiago-fernandes.jpg" alt="Foto de Thiago Fernandes" width="72" height="72" loading="lazy">
      <div>
        <p class="mono kicker dark">Sobre o autor</p>
        <p>{e(g['author'])}</p>
      </div>
    </div>
    <div class="sp-faq">
      <h2 class="sp-h2">Perguntas frequentes</h2>
      {faq}
    </div>
    <p class="sp-related">Quer começar agora? Leia também <a href="{g['related'][0]}">{e(g['related'][1])}</a>.</p>
    <p class="center">{checkout_btn(g, "Quero o meu exemplar", "btn btn-primary")}</p>
  </div>
</section>
"""
    ld_book = {"@context": "https://schema.org", "@type": "Book", "name": f"{g['title']}: {g['subtitle']}",
               "author": {"@type": "Person", "name": "Thiago Fernandes"},
               "publisher": {"@type": "Organization", "name": "Editora Prumo"},
               "bookFormat": "https://schema.org/EBook", "inLanguage": "pt-BR",
               "url": SITE + path, "description": g["seo_desc"]}
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in g["faq"]]}
    head = (f'<script type="application/ld+json">{json.dumps(ld_book, ensure_ascii=False)}</script>\n'
            f'<script type="application/ld+json">{json.dumps(ld_faq, ensure_ascii=False)}</script>')
    write(f"guias/{g['slug']}/index.html", page(path, g["seo_title"], g["seo_desc"], body, "guias", "website", head))

def guide_cards():
    return f"""<div class="guides">
  <article class="guide">
    <a href="/guias/o-labirinto-do-proposito/" class="guide-cover" tabindex="-1" aria-hidden="true"><img src="/assets/ebooks/o-labirinto-do-proposito.jpg" alt="" width="800" height="800" loading="lazy"></a>
    <div>
      <p class="mono kicker">Propósito</p>
      <h3>O labirinto do propósito</h3>
      <p>Como identificar seu chamado em meio ao caos. Um e-book de leitura leve, com linguagem simples e exercícios práticos para você sair da dúvida e dar o próximo passo com clareza.</p>
      <a class="btn btn-light" href="/guias/o-labirinto-do-proposito/">Conhecer o e-book</a>
      <a class="guide-link" href="{EBOOK}" target="_blank" rel="noopener" data-checkout="O labirinto do propósito">Comprar agora <span aria-hidden="true">→</span></a>
    </div>
  </article>
  <article class="guide">
    <a href="/guias/gestao-do-tempo/" class="guide-cover" tabindex="-1" aria-hidden="true"><img src="/assets/ebooks/gestao-do-tempo.jpg" alt="" width="400" height="566" loading="lazy"></a>
    <div>
      <p class="mono kicker">Produtividade</p>
      <h3>Gestão do tempo</h3>
      <p>Produtividade com foco no que é essencial. Descubra como recuperar o controle da sua agenda e viver com mais foco, propósito e paz, mesmo em meio à correria do dia a dia.</p>
      <a class="btn btn-light" href="/guias/gestao-do-tempo/">Conhecer o e-book</a>
      <a class="guide-link" href="{EBOOK2}" target="_blank" rel="noopener" data-checkout="Gestão do tempo">Comprar agora <span aria-hidden="true">→</span></a>
    </div>
  </article>
</div>"""

def card(a):
    img = article_img(a)
    if img:
        cover = (f'<a class="card-cover card-img" href="/blog/{a["slug"]}/" aria-hidden="true" tabindex="-1">'
                 f'<img src="{img}" alt="" loading="lazy" width="1200" height="630"></a>')
    else:
        cover = f"""<a class="card-cover {a['cover']}" href="/blog/{a['slug']}/" aria-hidden="true" tabindex="-1">
    <span class="mono card-cover-tag">{a['tag']}</span>
    <span class="card-cover-quote">“{a['quote']}”</span>
  </a>"""
    return f"""<article class="card">
  {cover}
  <div class="card-body">
    <p class="mono meta"><a href="{tema_url(a['tag'])}">{a['tag']}</a> · <time datetime="{a['date']}">{publicado(a, True)}</time></p>
    <h3><a href="/blog/{a['slug']}/">{a['title']}</a></h3>
    <p>{a['desc']}</p>
    <a class="link-arrow" href="/blog/{a['slug']}/">Ler artigo <span aria-hidden="true">→</span></a>
  </div>
</article>"""

def sanitize_html(h):
    """Remove do corpo dos artigos qualquer coisa que possa executar código (defesa extra)."""
    h = re.sub(r"(?is)<\s*(script|iframe|object|embed|style|form|input|button|link|meta)\b.*?(</\s*\1\s*>|/?>)", "", h)
    h = re.sub(r"(?i)\s+on[a-z]+\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+)", "", h)
    h = re.sub(r"(?i)(href|src)\s*=\s*([\"'])\s*(javascript|data|vbscript):[^\"']*\2", r'\1="#"', h)
    return h

def write_security_files():
    """Gera os cabeçalhos de segurança (_headers) com a política de conteúdo baseada nos scripts do site."""
    import hashlib, base64
    hashes = set()
    for root, _, files in os.walk(OUT):
        for fn in files:
            if fn.endswith(".html"):
                txt = open(os.path.join(root, fn), encoding="utf-8").read()
                for attrs, code in re.findall(r"(?is)<script([^>]*)>(.*?)</script>", txt):
                    if "src=" in attrs or "ld+json" in attrs:
                        continue
                    hashes.add("'sha256-" + base64.b64encode(hashlib.sha256(code.encode("utf-8")).digest()).decode() + "'")
    csp = "; ".join([
        "default-src 'self'",
        "script-src 'self' " + " ".join(sorted(hashes)) + " https://www.googletagmanager.com https://connect.facebook.net",
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
        "font-src 'self' https://fonts.gstatic.com",
        "img-src 'self' data: https://*.google-analytics.com https://*.googletagmanager.com https://www.google.com https://www.facebook.com",
        "connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com https://*.googletagmanager.com https://www.google.com https://www.facebook.com https://connect.facebook.net",
        "frame-src https://www.facebook.com",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "frame-ancestors 'none'",
        "upgrade-insecure-requests",
    ])
    headers = f"""/*
  Content-Security-Policy: {csp}
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), magnetometer=(), gyroscope=(), accelerometer=()
  Cross-Origin-Opener-Policy: same-origin
  X-Permitted-Cross-Domain-Policies: none

/assets/*
  Cache-Control: public, max-age=604800
"""
    write("_headers", headers)
    write("_redirects", "https://effervescent-madeleine-77e208.netlify.app/* https://minutodereflexao.com/:splat 301!\n"
                        "http://effervescent-madeleine-77e208.netlify.app/* https://minutodereflexao.com/:splat 301!\n")

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
      <a class="btn btn-light" href="/blog/">Ler os artigos</a>
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
    <p class="mono kicker">E-books</p>
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
    <p class="mono kicker">Artigos</p>
    <h1 class="display">Reflexões para<br>o seu dia</h1>
    <p class="lead">Textos curtos para ler em poucos minutos e levar para a vida.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">{temas_nav()}<div class="grid">{all_cards}</div></div>
</section>
"""
    write("blog/index.html", page("/blog/", "Artigos",
        "Artigos sobre motivação, propósito, superação e desenvolvimento pessoal do Minuto de Reflexão.", blog, "blog"))

    for tag, (tslug, tdesc) in TEMAS.items():
        itens = [a for a in ARTICLES if a["tag"] == tag]
        cards = "".join(card(a) for a in itens) or '<p class="muted">Em breve, novos artigos sobre este tema.</p>'
        n = len(itens)
        tbody = f"""
<section class="page-hero">
  <div class="wrap">
    <p class="mono kicker"><a href="/blog/">Artigos</a> · Tema</p>
    <h1 class="display">{tag}</h1>
    <p class="lead">{tdesc}</p>
    <p class="mono sp-trust">{n} artigo{'s' if n != 1 else ''}</p>
  </div>
</section>
<section class="section">
  <div class="wrap">{temas_nav(tag)}<div class="grid">{cards}</div></div>
</section>
"""
        write(f"blog/tema/{tslug}/index.html", page(f"/blog/tema/{tslug}/", f"Artigos sobre {tag.lower()}",
              f"Artigos do Minuto de Reflexão sobre {tag.lower()}: {tdesc}", tbody, "blog"))

    for i, a in enumerate(ARTICLES):
        rest = [x for x in ARTICLES if x is not a]
        others = ([x for x in rest if x["tag"] == a["tag"]] + [x for x in rest if x["tag"] != a["tag"]])[:2]
        body_html = (sanitize_html(a["body"])
            .replace('href="EBOOK2_URL" target="_blank" rel="noopener"', 'href="/guias/gestao-do-tempo/"')
            .replace('href="EBOOK_URL" target="_blank" rel="noopener"', 'href="/guias/o-labirinto-do-proposito/"')
            .replace("EBOOK2_URL", "/guias/gestao-do-tempo/").replace("EBOOK_URL", "/guias/o-labirinto-do-proposito/"))
        faq = a.get("faq") or []
        faq_html = ""
        if faq:
            faq_html = '<section class="faq">\n<h2>Perguntas frequentes</h2>\n' + "\n".join(
                f"<h3>{html.escape(f['q'])}</h3>\n<p>{html.escape(f['a'])}</p>" for f in faq) + "\n</section>"
        ld = {
            "@context": "https://schema.org", "@type": "BlogPosting",
            "headline": a["title"], "description": a["desc"],
            "datePublished": iso_dt(a), "dateModified": a.get("updated", iso_dt(a)),
            "inLanguage": "pt-BR",
            "author": {"@type": "Person", "name": AUTHOR, "url": SITE + "/sobre/", "image": SITE + "/assets/thiago-fernandes.jpg"},
            "publisher": {"@type": "Organization", "name": BRAND,
                          "logo": {"@type": "ImageObject", "url": SITE + "/assets/og.jpg"}},
            "mainEntityOfPage": f"{SITE}/blog/{a['slug']}/",
            "image": SITE + (article_img(a) or "/assets/og.jpg"),
        }
        art = f"""
<article class="post">
  <header class="post-hero {a['cover']}">
    <div class="wrap narrow">
      <p class="mono kicker"><a href="/blog/">Artigos</a> · <a href="{tema_url(a['tag'])}">{a['tag']}</a></p>
      <h1 class="post-title">{a['title']}</h1>
      <p class="mono post-meta">Por {AUTHOR} · Publicado em <time datetime="{a['date']}">{publicado(a)}</time>{(' · Atualizado em ' + data_br(a['updated'])) if a.get('updated') else ''} · {a['read']} min de leitura</p>
    </div>
  </header>
  <div class="wrap narrow post-body">
    {(f'<figure class="post-img"><img src="{article_img(a)}" alt="{html.escape(a["title"])}" width="1200" height="630"></figure>') if article_img(a) else ''}
    {body_html}
    {faq_html}
    <aside class="author-box">
      <img class="author-photo" src="/assets/thiago-fernandes.jpg" alt="Foto de Thiago Fernandes" width="72" height="72" loading="lazy">
      <div>
        <p class="mono author-kicker">Escrito por</p>
        <p class="author-name">{AUTHOR}</p>
        <p>{AUTHOR_BIO}</p>
        <p class="author-links"><a href="/sobre/">Sobre o Minuto de Reflexão</a> · <a href="/guias/">Conheça os e-books</a></p>
      </div>
    </aside>
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
        write(f"blog/{a['slug']}/index.html", page(f"/blog/{a['slug']}/", a["title"], a["desc"], art, "blog", "article", og_image=article_img(a), extra_head=
              f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
              + (f'\n<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faq]}, ensure_ascii=False)}</script>' if faq else "")))

    guias = f"""
<section class="page-hero">
  <div class="wrap">
    <p class="mono kicker">E-books</p>
    <h1 class="display">Para ir<br>mais fundo</h1>
    <p class="lead">Leituras práticas para quem quer transformar reflexão em atitude no dia a dia.</p>
  </div>
</section>
<section class="section ebook">
  <div class="wrap">{guide_cards()}</div>
</section>
"""
    write("guias/index.html", page("/guias/", "E-books",
        "E-books do Minuto de Reflexão: O labirinto do propósito e Gestão do tempo, leituras práticas para viver com mais foco e propósito.", guias, "guias"))

    for g in GUIDES:
        sales_page(g)

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
    <p>Além do blog, publicamos reflexões todos os dias no Instagram <a href="{IG}" target="_blank" rel="noopener">{HANDLE}</a> e no canal do YouTube. Também criamos e-books, como <a href="/guias/o-labirinto-do-proposito/">O labirinto do propósito</a> e <a href="/guias/gestao-do-tempo/">Gestão do tempo</a>, para quem quer ir mais fundo.</p>
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
          <option>Sugestão de tema</option><option>Dúvida sobre o e-book</option><option>Parceria</option><option>Outro</option>
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
    <a class="btn btn-light" href="/blog/">Ir para os artigos</a>
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

    urls = ["/", "/blog/", "/guias/", "/guias/o-labirinto-do-proposito/", "/guias/gestao-do-tempo/", "/sobre/", "/contato/", "/privacidade/"] + [f"/blog/tema/{v[0]}/" for v in TEMAS.values()] + [f"/blog/{a['slug']}/" for a in ARTICLES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>2026-10-17</lastmod></url>\n" for u in urls)
    sm += "</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write_security_files()
    write("versao.txt", (os.environ.get("COMMIT_REF") or "local") + "\n")

if __name__ == "__main__":
    build()
    print("ok", OUT)
