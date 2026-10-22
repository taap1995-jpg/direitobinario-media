#!/usr/bin/env python3
"""Gera peças simples e editáveis para @direitobinario: JPG para Feed/Stories e MP4 vertical para Reels."""
from PIL import Image, ImageDraw, ImageFont
import os, subprocess, textwrap, json, math

OUT = "campanha-outubro-2026/gerados"
os.makedirs(OUT, exist_ok=True)
NAVY = (8,26,51); GOLD = (214,177,94); WHITE=(248,247,242); MUTED=(184,196,210)
FONT_BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
TOPICS = [
 {"n":"01","slug":"01-jurisprudencia","title":"A IA INVENTOU UMA JURISPRUDÊNCIA?","hook":"A resposta parece perfeita.\nMas o processo citado nem existe.","feed":"Confira processo, tribunal, relatoria, data e inteiro teor em fonte oficial.","story":"A IA citou uma decisão.\nEla existe mesmo?","voice":"A inteligência artificial pode apresentar uma decisão judicial que não existe. Antes de citar qualquer precedente, confira o número do processo, o tribunal, a data, o relator e o inteiro teor em fonte oficial. Se não conseguir confirmar, não use como jurisprudência. IA ajuda na pesquisa; não substitui a conferência jurídica."},
 {"n":"02","slug":"02-dados-ia","title":"O QUE A IA PODE FAZER COM SEUS DADOS?","hook":"Você sabe o que acontece com o que digita numa IA?","feed":"Minimize dados. Evite documentos sigilosos. Confira retenção, compartilhamento e acesso.","story":"Vai colar um documento\nna IA? Pare e confira.","voice":"Antes de colar um documento numa ferramenta de IA, pare e confira. Ele pode conter dados pessoais, informações confidenciais ou segredos profissionais. Use apenas o necessário, remova identificadores quando possível e verifique as regras de tratamento, retenção e acesso da ferramenta. Conveniência não elimina deveres de privacidade e sigilo."},
 {"n":"03","slug":"03-direitos-autorais","title":"CONTEÚDO DE IA É DE USO LIVRE?","hook":"Criado por IA significa sem direitos autorais? Não é tão simples.","feed":"Considere contribuição humana, direitos de terceiros, licenças e termos de uso.","story":"IA criou.\nPosso usar livremente?","voice":"Conteúdo gerado por inteligência artificial não significa automaticamente uso livre. É preciso considerar a contribuição humana, a obra ou material usado como referência, os termos da ferramenta, os direitos de terceiros e o contexto de utilização. Antes de publicar ou comercializar, verifique a origem e as permissões aplicáveis."},
 {"n":"04","slug":"04-deepfakes","title":"DEEPFAKES: E SE O VÍDEO FOR FALSO?","hook":"Pode parecer real. Isso não prova que aconteceu.","feed":"Imagem, honra, privacidade e fraude podem estar em jogo — depende do caso.","story":"Parece real.\nMas aconteceu?","voice":"Um vídeo sintético pode afetar imagem, honra, privacidade e reputação. Se for usado para enganar alguém e obter vantagem ilícita, o caso também pode envolver fraude, conforme as circunstâncias. Não compartilhe só porque parece real: confirme a origem, preserve evidências e denuncie pelos canais adequados."},
 {"n":"05","slug":"05-lgpd-erros","title":"LGPD: 3 HÁBITOS PARA REVISAR","hook":"Pequenos hábitos digitais podem trazer riscos.","feed":"1. Compartilhar demais. 2. Não revisar permissões. 3. Guardar arquivos sem controle de acesso.","story":"3 hábitos digitais\npara revisar hoje.","voice":"Três hábitos para revisar: primeiro, compartilhar dados além do necessário; segundo, deixar permissões de aplicativos sem revisão; terceiro, armazenar documentos sensíveis sem controle de acesso. A LGPD prevê princípios como necessidade e segurança. Pequenas revisões ajudam a reduzir riscos, mas cada organização deve avaliar seu contexto."},
 {"n":"08","slug":"08-clonagem-voz","title":"A VOZ PARECE FAMILIAR. E AGORA?","hook":"Isso não prova que o pedido é verdadeiro.","feed":"Confirme por outro canal. Não envie dinheiro, códigos ou dados sob pressão.","story":"Pedido urgente de dinheiro\ncom voz conhecida? Confirme.","voice":"Clonagem de voz pode fazer uma mensagem parecer vir de alguém conhecido. Se houver pedido urgente de dinheiro, código ou dado pessoal, não confie só na voz. Desligue e ligue para um número que você já conhece, confirme por outro canal e combine uma palavra de verificação com pessoas próximas."},
 {"n":"09","slug":"09-quiz-risco","title":"QUIZ: VOCÊ IDENTIFICARIA ESTE RISCO?","hook":"Você tem 5 segundos: pode ou não pode?","feed":"Caso fictício: colar contrato com nome, CPF e valores de cliente numa IA gratuita. Está tudo certo?","story":"QUIZ • 5 segundos\nPode ou não pode?\n\nContrato com CPF numa IA gratuita.","voice":"Quiz jurídico: uma equipe cola numa IA gratuita um contrato com nome, CPF e valores de um cliente para resumir mais rápido. Está tudo certo? Não dá para afirmar sem avaliar finalidade, necessidade, base legal, segurança, regras da ferramenta e deveres de confidencialidade. Minimize ou anonimize dados quando possível."},
 {"n":"10","slug":"10-checklist-ia","title":"5 PERGUNTAS ANTES DE CONFIAR NA IA","hook":"Antes de copiar e colar, confira estes pontos.","feed":"Fonte? Atualização? Dados pessoais? Possíveis erros? Revisão humana?","story":"Antes de confiar na IA,\nfaça estas 5 perguntas.","voice":"Antes de confiar numa resposta de IA, faça cinco perguntas: qual é a fonte? A informação está atualizada? Estou expondo dados pessoais? A resposta pode conter erros ou referências inventadas? E alguém responsável revisou? Use a IA como apoio, confirme o que importa e mantenha a revisão humana."}
]
def font(size,bold=False): return ImageFont.truetype(FONT_BOLD if bold else FONT_REG,size)
def wrap(text, maxchars):
    return "\n".join(textwrap.wrap(text.replace("\\n"," "), maxchars, break_long_words=False))
def draw_piece(path, topic, size, mode="feed", slide=1):
    w,h=size; im=Image.new("RGB",size,NAVY); d=ImageDraw.Draw(im)
    # quiet geometric accents and gold rule
    d.ellipse((w-230,-160,w+80,150), outline=GOLD, width=3)
    d.ellipse((w-190,-120,w+40,110), outline=(65,84,110), width=2)
    d.rectangle((0,0,18,h),fill=GOLD)
    margin=int(w*.075); top=int(h*.09)
    d.text((margin,top),"DIREITO BINÁRIO",font=font(int(w*.034),True),fill=GOLD)
    d.text((margin,top+int(h*.045)),"DIREITO DIGITAL  •  IA",font=font(int(w*.018),True),fill=MUTED)
    if mode=="carousel":
        title = [topic["title"], "O QUE CONFERIR", "NA PRÁTICA"][slide-1]
        body = [topic["hook"], topic["feed"], "Confira a fonte oficial. Minimize dados. Faça revisão humana."][slide-1]
    elif mode=="story":
        title=topic["story"]; body=topic["feed"]
    else:
        title=topic["title"]; body=topic["hook"]+"\n\n"+topic["feed"]
    titlefont=font(int(w*(.052 if mode!="story" else .061)),True)
    bodyfont=font(int(w*(.031 if mode!="story" else .033)))
    y=int(h*.30)
    for line in title.split("\n"):
        for ln in textwrap.wrap(line, max(16,int(w/ (titlefont.size*.58))), break_long_words=False):
            d.text((margin,y),ln,font=titlefont,fill=WHITE,stroke_width=0); y+=int(titlefont.size*1.35)
        y+=int(titlefont.size*.35)
    y+=int(h*.035)
    for line in body.split("\n"):
        for ln in textwrap.wrap(line, max(20,int(w/(bodyfont.size*.56))), break_long_words=False):
            d.text((margin,y),ln,font=bodyfont,fill=GOLD if line==body.split("\n")[0] else MUTED); y+=int(bodyfont.size*1.45)
        y+=int(bodyfont.size*.3)
    # Footer
    d.line((margin,h-int(h*.105),w-margin,h-int(h*.105)),fill=(56,75,103),width=2)
    d.text((margin,h-int(h*.08)),"INFORMAÇÃO JURÍDICA • CONFIRA AS FONTES",font=font(int(w*.018),True),fill=MUTED)
    d.text((margin,h-int(h*.045)),"@direitobinario",font=font(int(w*.025),True),fill=GOLD)
    if mode=="carousel": d.text((w-margin-int(w*.07),h-int(h*.045)),f"{slide}/3",font=font(int(w*.024),True),fill=GOLD)
    im.save(path,"JPEG",quality=90,optimize=True)
def main():
  manifest=[]
  for t in TOPICS:
    base=f"{OUT}/{t['slug']}"; os.makedirs(base,exist_ok=True)
    # Feed cover or single image
    feed=f"{base}/feed.jpg"; draw_piece(feed,t,(1080,1350),"feed"); manifest.append(feed)
    if t["n"] in ("02","05","10"):
      for s in (2,3):
        p=f"{base}/feed-{s}.jpg"; draw_piece(p,t,(1080,1350),"carousel",s); manifest.append(p)
    story=f"{base}/story.jpg"; draw_piece(story,t,(1080,1920),"story"); manifest.append(story)
    # Reel: 3 sequential vertical slides with voice narration and subtitles/labels
    frames=[]
    chunks=[t["title"],t["hook"],t["feed"]]
    for i,txt in enumerate(chunks):
      p=f"{base}/frame-{i+1}.jpg"; draw_piece(p,t,(720,1280),"story" if i==0 else "feed")
      frames.append(p); manifest.append(p)
    # create narrated voice track with espeak, using Portuguese voice when available
    voice=f"{base}/narracao.txt"
    open(voice,"w",encoding="utf-8").write(t["voice"])
    wav=f"{base}/voice.wav"
    subprocess.run(["espeak","-v","pt-br","-s","145","-w",wav,t["voice"]],check=True)
    # Hold each visual for equal portions; encode H264 with audio. A simple gentle zoom/pan is intentionally avoided for reliable rendering.
    durations=[3.2,3.2,3.2]
    concat=f"{base}/frames.txt"
    with open(concat,"w",encoding="utf-8") as f:
      for p,dur in zip(frames,durations):
        f.write("file '"+os.path.abspath(p)+"'\n")
        f.write(f"duration {dur}\n")
      f.write("file '"+os.path.abspath(frames[-1])+"'\n")
    mp4=f"{base}/reels.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",concat,"-i",wav,"-vf","scale=720:1280,format=yuv420p","-c:v","libx264","-preset","veryfast","-crf","29","-r","24","-c:a","aac","-b:a","96k","-shortest","-movflags","+faststart",mp4],check=True)
    manifest.extend([voice,wav,mp4])
  with open(f"{OUT}/manifest.json","w",encoding="utf-8") as f: json.dump({"files":manifest,"topics":[t["slug"] for t in TOPICS]},f,ensure_ascii=False,indent=2)
  print(f"Gerados {len(manifest)} arquivos em {OUT}")
if __name__=="__main__": main()
