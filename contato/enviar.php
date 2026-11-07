<?php
// Recebe o formulário de contato do Minuto de Reflexão e envia por e-mail.
// Proteções: só aceita POST, campo-armadilha contra robôs, tempo mínimo de preenchimento,
// limite simples por IP, validação e limpeza de todos os campos (sem quebra de cabeçalho).

$DESTINO   = 'thiagofercon@gmail.com';
$REMETENTE = 'contato@minutodereflexao.com';

function voltar($status) {
    header('Location: ' . ($status === 'ok' ? '/obrigado/' : '/contato/?erro=1'), true, 303);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { http_response_code(405); exit; }

// Robôs costumam preencher o campo escondido "empresa"
if (!empty($_POST['empresa'])) { voltar('ok'); }

// Envio rápido demais (menos de 3 segundos depois de abrir a página) é tratado como robô
$inicio = (int)($_POST['t'] ?? 0);
if ($inicio > 0 && (time() - $inicio) < 3) { voltar('ok'); }

// No máximo 5 mensagens por hora por endereço IP
$ip   = $_SERVER['REMOTE_ADDR'] ?? '0';
$arq  = sys_get_temp_dir() . '/mdr_contato_' . md5($ip);
$hist = array_filter(array_map('intval', @file($arq, FILE_IGNORE_NEW_LINES) ?: []), fn($t) => $t > time() - 3600);
if (count($hist) >= 5) { voltar('erro'); }

$limpa = fn($v, $max) => mb_substr(trim(str_replace(["\r", "\n", "\0"], ' ', (string)$v)), 0, $max);
$nome     = $limpa($_POST['nome'] ?? '', 120);
$email    = $limpa($_POST['email'] ?? '', 160);
$assunto  = $limpa($_POST['assunto'] ?? 'Contato', 80);
$mensagem = mb_substr(trim(str_replace("\0", '', (string)($_POST['mensagem'] ?? ''))), 0, 5000);
$aceite   = !empty($_POST['aceite']);

if ($nome === '' || $mensagem === '' || !$aceite || !filter_var($email, FILTER_VALIDATE_EMAIL)) { voltar('erro'); }

$corpo = "Nova mensagem pelo site minutodereflexao.com\n\n"
       . "Nome: $nome\nE-mail: $email\nAssunto: $assunto\n\nMensagem:\n$mensagem\n\n"
       . "---\nEnviado em " . date('d/m/Y H:i') . " (IP $ip)\n";
$cabecalhos = "From: Minuto de Reflexão <$REMETENTE>\r\n"
            . "Reply-To: $email\r\n"
            . "Content-Type: text/plain; charset=UTF-8\r\n";

$ok = mail($DESTINO, '=?UTF-8?B?' . base64_encode("[Site] $assunto - $nome") . '?=', $corpo, $cabecalhos, "-f$REMETENTE");
if ($ok) { $hist[] = time(); @file_put_contents($arq, implode("\n", $hist)); }
voltar($ok ? 'ok' : 'erro');
