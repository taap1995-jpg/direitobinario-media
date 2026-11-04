"""Renderiza o Reel aprovado: suspensoes de contas pela Meta e ANPD.
Reutiliza o renderizador Dark Tech validado deste repositorio.
"""
from pathlib import Path

TEMPLATE = Path("reels/engenharia-reversa-tv-openai-20261026/render.py")
source = TEMPLATE.read_text(encoding="utf-8")
scenes = [
    (5, "CONTA SUSPENSA", "SEM EXPLICAÇÃO?",
     ["SEU PERFIL SUMIU DE REPENTE?",
      "VOCÊ TEM DIREITO A UMA RESPOSTA?"], "BLOQUEIO DE PERFIL"),
    (8, "A ANPD COBROU", "EXPLICAÇÕES DA META",
     ["A AUTORIDADE PEDIU INFORMAÇÕES",
      "SOBRE DENÚNCIAS DE SUSPENSÕES",
      "E REMOÇÕES DE CONTEÚDO."], "FISCALIZAÇÃO • 19/10/2026"),
    (8, "QUEM DECIDE?", "ALGORITMO OU PESSOA?",
     ["UMA SUSPENSÃO PODE RESULTAR",
      "DE SISTEMAS AUTOMATIZADOS",
      "OU DE ANÁLISE HUMANA."], "APURAÇÃO NÃO É CONDENAÇÃO"),
    (9, "BASE JURÍDICA", "O QUE DIZ A LGPD?",
     ["O ART. 20 PREVÊ REVISÃO DE",
      "DECISÕES TOMADAS UNICAMENTE",
      "POR TRATAMENTO AUTOMATIZADO."], "NEM TODO BLOQUEIO SE ENQUADRA"),
    (8, "SE ISSO ACONTECER", "GUARDE AS PROVAS",
     ["REGISTRE AVISOS E DATAS.",
      "PEÇA A JUSTIFICATIVA.",
      "USE OS CANAIS DE RECURSO."], "PROTEJA SEUS DIREITOS"),
    (7, "E VOCÊ?", "JÁ FOI BLOQUEADO?",
     ["A PLATAFORMA DEVERIA EXPLICAR",
      "POR QUE SUSPENDEU UMA CONTA?",
      "COMENTE E COMPARTILHE."], "SIGA @direitobinario"),
]
assert sum(s[0] for s in scenes) == 45
start = source.index("scenes=[")
end = source.index("\nB='/usr/share/fonts", start)
source = source[:start] + "scenes=" + repr(scenes) + source[end:]
original = "OUT=Path('media/reels/engenharia-reversa-tv-openai-20261026')"
assert original in source
source = source.replace(original, "OUT=Path('media/reels/anpd-meta-conta-20261104')")
exec(compile(source, str(TEMPLATE), "exec"), {"__name__":"__main__"})
