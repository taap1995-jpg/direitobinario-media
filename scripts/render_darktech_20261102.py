#!/usr/bin/env python3
"""Generate the approved 02-08 Nov 2026 campaign; original vector art and soundtrack."""
import os, json, math, random, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
OUT=Path(os.environ.get("CAMPAIGN_OUTPUT","artifacts/darktech-20261102"))
OUT.mkdir(parents=True,exist_ok=True)
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
C="#36e4ee"; P="#a67cff"; G="#e2bc64"; WHITE="#f3f5f8"
DATA=[
{"id":"01-deepfake","date":"2026-11-02","label":"VOZ CLONADA","kind":"phone",
"reel":[["É A VOZ DO SEU FILHO.\nMAS É ELE?",""],["A IA PODE IMITAR\nQUEM VOCÊ AMA.","UM PEDIDO DE PIX URGENTE PODE SER FRAUDE."],["O GOLPE É DIGITAL.\nO CRIME É REAL.","A FRAUDE PODE CONFIGURAR ESTELIONATO, CONFORME O CASO."],["ANTES DO PIX,\nCONFIRME POR OUTRO CANAL.","SE HOUVE GOLPE: AVISE O BANCO E GUARDE AS PROVAS."],["ENVIE PARA\nSEUS PAIS.","A VOZ SOZINHA NÃO PROVA A IDENTIDADE."]],
"slides":[["GOLPE DA\nDEEPFAKE","COMO O DIREITO TE PROTEGE — E ONDE EXIGE CUIDADO."],["PARECE REAL.\nPODE SER IA.","DEEPFAKES IMITAM VOZ OU IMAGEM. O REALISMO NÃO COMPROVA QUEM ESTÁ DO OUTRO LADO."],["TECNOLOGIA NOVA.\nFRAUDE CONHECIDA.","ENGANAR PARA OBTER VANTAGEM ILÍCITA E CAUSAR PREJUÍZO PODE CONFIGURAR ESTELIONATO. O ENQUADRAMENTO DEPENDE DA CONDUTA."],["O BANCO RESPONDE\nEM TODO CASO?","NÃO AUTOMATICAMENTE. FALHAS DE SEGURANÇA E OPERAÇÕES ATÍPICAS PODEM GERAR RESPONSABILIDADE. SÚMULA 479/STJ."],["PRESERVE.\nDENUNCIE.\nPEÇA A REMOÇÃO.","GUARDE ÁUDIOS ORIGINAIS, LINKS, DATAS E COMPROVANTES. REGISTRE B.O. CONTEÚDO ILÍCITO PODE SER QUESTIONADO; NÃO HÁ DIREITO GERAL AO ESQUECIMENTO."]],
"caption":"A voz parece familiar. A urgência, também. É exatamente aí que o golpe tenta te pegar.\nConfirme a identidade por outro canal antes de transferir. Se já houve fraude, contate imediatamente o banco pelos canais oficiais, peça análise do MED quando for Pix e preserve áudios originais, links, comprovantes e protocolos.\nO estelionato e a responsabilidade civil dependem dos fatos. Banco ou plataforma não respondem automaticamente por todo golpe.\nEnvie para seus pais e salve este alerta.",
"sources":["https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm","https://www.stj.jus.br/sites/portalp/Paginas/Comunicacao/Noticias/2025/21102025-Bancos-e-instituicoes-de-pagamento-devem-indenizar-clientes-por-falhas-que-viabilizam-golpe-da-falsa-central.aspx","https://portal.stf.jus.br/jurisprudenciarepercussao/tema.asp?num=786"]},
{"id":"02-vigilancia","date":"2026-11-03","label":"VIGILÂNCIA NO TRABALHO","kind":"eye",
"reel":[["SEU CHEFE PODE\nLER SEU WHATSAPP?",""],["O COMPUTADOR\nÉ DA EMPRESA.","ISSO NÃO TORNA SUAS CONVERSAS PESSOAIS PÚBLICAS."],["MONITORAR NÃO É\nDEVASSAR A VIDA PRIVADA.","O CONTROLE CORPORATIVO EXIGE FINALIDADE, TRANSPARÊNCIA E LIMITES."],["AVISO PRÉVIO NÃO\nAUTORIZA TODO ACESSO.","A INTIMIDADE CONTINUA PROTEGIDA, MESMO NO EQUIPAMENTO DA FIRMA."],["SALVE ANTES DE\nABRIR O WHATSAPP.","ENCERRE SESSÕES PESSOAIS EM COMPUTADORES COMPARTILHADOS."]],
"slides":[["SEU CHEFE VÊ\nTUDO O QUE\nVOCÊ DIGITA?","MONITORAMENTO TEM LIMITES. ENTENDA A DIFERENÇA."],["O PODER DIRETIVO\nNÃO É ILIMITADO.","A EMPRESA PODE FISCALIZAR O TRABALHO, RESPEITANDO INTIMIDADE, NECESSIDADE E PROPORCIONALIDADE."],["CORPORATIVO NÃO\nSIGNIFICA SEM LIMITES.","E-MAILS E CHATS DE TRABALHO PODEM TER CONTROLE COM FINALIDADE LEGÍTIMA E TRANSPARÊNCIA. ISSO NÃO LIBERA TODA LEITURA."],["WHATSAPP PESSOAL\nCONTINUA PESSOAL.","DEIXAR A CONTA ABERTA NO COMPUTADOR DA FIRMA NÃO AUTORIZA LEITURA OU DIVULGAÇÃO ABUSIVA. CÂMERAS NO HOME OFFICE TAMBÉM EXIGEM LIMITES."],["SUA PRIVACIDADE\nFOI VIOLADA?","GUARDE POLÍTICAS INTERNAS, AVISOS E REGISTROS DO ACESSO. PROCURE O ENCARREGADO DE DADOS, SINDICATO OU ORIENTAÇÃO JURÍDICA. SALVE ESTE GUIA."]],
"caption":"O equipamento é corporativo. A sua intimidade não vira propriedade da empresa.\nO monitoramento de ferramentas profissionais exige finalidade legítima, transparência, necessidade e proporcionalidade. Um aviso genérico não autoriza devassa em conversas pessoais.\nO TRT-MG manteve indenização em caso de leitura, fotografia e compartilhamento interno de WhatsApp pessoal aberto no computador do trabalho. É uma decisão sobre fatos específicos, não autorização para generalizar qualquer situação.\nSalve e confira as políticas do seu trabalho.",
"sources":["https://portal.trt3.jus.br/internet/conheca-o-trt/comunicacao/noticias-juridicas/trt-mg-mantem-indenizacao-por-acesso-a-mensagens-privadas-de-empregada-e-divulgacao-no-ambiente-de-trabalho","https://www2.camara.leg.br/legin/fed/lei/2018/lei-13709-14-agosto-2018-787077-normaatualizada-pl.html"]},
{"id":"03-pix","date":"2026-11-04","label":"FRAUDE BANCÁRIA","kind":"pix",
"reel":[["SEU PIX SUMIU.\nQUEM PAGA?",""],["A DEVOLUÇÃO\nNÃO É AUTOMÁTICA.","É PRECISO ANALISAR COMO A FRAUDE ACONTECEU."],["OPERAÇÕES ATÍPICAS\nACENDEM O ALERTA.","FALHAS DO SERVIÇO PODEM GERAR RESPONSABILIDADE DO BANCO."],["AVISE O BANCO AGORA.\nPEÇA ANÁLISE DO MED.","NO PIX, O MECANISMO NÃO GARANTE RECUPERAÇÃO."],["GUARDE AS PROVAS.\nCOMPARTILHE O ALERTA.","FORNECER SENHA NÃO DEFINE, SOZINHO, QUEM RESPONDE."]],
"slides":[["SEU PIX SUMIU.\nE AGORA?","UM GUIA PRÁTICO PARA AGIR DEPOIS DA FRAUDE."],["BANCO PRIMEIRO.\nNÃO ESPERE 24H.","USE OS CANAIS OFICIAIS. CONTESTE AS TRANSAÇÕES E PEÇA ANÁLISE DO MED NO PIX. REGISTRE B.O. EM PARALELO."],["MED NÃO É\nDEVOLUÇÃO GARANTIDA.","O PEDIDO PODE SER FEITO EM ATÉ 80 DIAS, MAS AJA IMEDIATAMENTE. A RECUPERAÇÃO DEPENDE DA ANÁLISE E DE RECURSOS DISPONÍVEIS."],["QUANDO O BANCO\nPODE RESPONDER?","O CDC, ART. 14, E A SÚMULA 479/STJ AMPARAM A ANÁLISE DE FALHAS DO SERVIÇO. TRANSAÇÕES FORA DO PERFIL SÃO UM ALERTA."],["QUANDO O PEDIDO\nPODE SER NEGADO?","AUSÊNCIA DE FALHA DO SERVIÇO OU CULPA EXCLUSIVA COMPROVADA PODEM AFASTAR A RESPONSABILIDADE. CADA CASO EXIGE PROVA."],["MONTE SUA\nPASTA DE PROVAS.","EXTRATOS, COMPROVANTES, HORÁRIOS, MENSAGENS E PROTOCOLOS. SEM SOLUÇÃO, PROCURE OUVIDORIA, PROCON OU ORIENTAÇÃO JURÍDICA."]],
"caption":"Caiu em golpe? Não espere o dia seguinte para agir.\nContate o banco pelos canais oficiais, conteste as operações e solicite análise do MED se a transferência foi Pix. Registre B.O. em paralelo e preserve todos os comprovantes.\nO MED pode ser solicitado em até 80 dias, mas agir rápido importa. Ele não garante devolução: há análise e dependência de recursos recuperáveis.\nA responsabilidade bancária também não é automática. Falhas de segurança e operações incompatíveis com o perfil do cliente são relevantes; entregar senha não encerra, sozinho, a discussão.\nSalve este passo a passo.",
"sources":["https://www.bcb.gov.br/estabilidadefinanceira/pix-seguranca","https://www.stj.jus.br/sites/portalp/Paginas/Comunicacao/Noticias/2026/15072026-Sem-transacoes-incompativeis-com-perfil-de-cliente--banco-nao-responde-por-golpe-da-falsa-central.aspx","https://www.stj.jus.br/sites/portalp/Paginas/Comunicacao/Noticias/2025/21102025-Bancos-e-instituicoes-de-pagamento-devem-indenizar-clientes-por-falhas-que-viabilizam-golpe-da-falsa-central.aspx"]},
{"id":"04-dados","date":"2026-11-05","label":"VAZAMENTO DE DADOS","kind":"lock",
"reel":[["VAZOU DADOS.\nQUEM PAGA A CONTA?",""],["A LGPD PREVÊ\nSANÇÕES.","A MULTA PODE CHEGAR A R$ 50 MILHÕES POR INFRAÇÃO."],["MAS A MULTA\nNÃO É AUTOMÁTICA.","DEPENDE DE PROCESSO ADMINISTRATIVO E DOS CRITÉRIOS LEGAIS."],["INCIDENTE RELEVANTE\nEXIGE COMUNICAÇÃO.","A REGRA GERAL DA ANPD É DE 3 DIAS ÚTEIS, NOS CASOS APLICÁVEIS."],["JÁ AVISARAM QUE\nSEUS DADOS VAZARAM?","CONTE NOS COMENTÁRIOS, SEM EXPOR DADOS PESSOAIS."]],
"slides":[["VAZAMENTO:\nQUEM PAGA\nA CONTA?","O QUE EMPRESAS E USUÁRIOS PRECISAM SABER."],["INCIDENTE NÃO É\nSÓ ATAQUE HACKER.","PERDA, ACESSO INDEVIDO OU DIVULGAÇÃO ACIDENTAL PODEM AFETAR DADOS PESSOAIS. CONTER E DOCUMENTAR É ESSENCIAL."],["AVISAR É PARTE\nDA RESPOSTA.","HAVENDO RISCO OU DANO RELEVANTE, O CONTROLADOR DEVE COMUNICAR ANPD E TITULARES. REGRA GERAL: 3 DIAS ÚTEIS, COM EXCEÇÕES."],["R$ 50 MILHÕES?\nENTENDA O LIMITE.","MULTA SIMPLES: ATÉ 2% DO FATURAMENTO NO BRASIL, EXCLUÍDOS TRIBUTOS, LIMITADA A R$ 50 MILHÕES POR INFRAÇÃO. EXIGE PROCESSO."],["SEUS DIREITOS\nCONTINUAM VALENDO.","PEÇA INFORMAÇÕES, ACESSO E CORREÇÃO. ELIMINAÇÃO TEM HIPÓTESES E EXCEÇÕES. RESPONSABILIDADE, SOLIDARIEDADE E INDENIZAÇÃO DEPENDEM DO CASO."]],
"caption":"Vazamento não gera automaticamente multa máxima nem indenização para todo mundo.\nA LGPD prevê multa simples de até 2% do faturamento da pessoa jurídica de direito privado, grupo ou conglomerado no Brasil no último exercício, excluídos os tributos, limitada a R$ 50 milhões por infração. A aplicação exige processo administrativo e critérios legais.\nIncidentes que possam ocasionar risco ou dano relevante aos titulares devem ser comunicados pelo controlador à ANPD e aos afetados. O prazo geral é de 3 dias úteis a partir do conhecimento de que o incidente afetou dados pessoais, ressalvadas as regras específicas e exceções aplicáveis.\nPeça informações ao controlador e guarde protocolos. Direitos de eliminação e responsabilidade solidária têm requisitos, não são universais.\nJá recebeu aviso de vazamento? Comente sem publicar seus dados.",
"sources":["https://www2.camara.leg.br/legin/fed/lei/2018/lei-13709-14-agosto-2018-787077-normaatualizada-pl.html","https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca-cis"]},
{"id":"05-fakes","date":"2026-11-06","label":"PERFIS FALSOS","kind":"fake",
"reel":[["PERFIL FAKE:\nÉ SÓ BRINCADEIRA?",""],["UM PSEUDÔNIMO\nNÃO É CRIME POR SI SÓ.","O QUE VOCÊ FAZ COM ELE É DECISIVO."],["FINGIR SER OUTRO\nPODE TER CONSEQUÊNCIAS.","A FALSA IDENTIDADE EXIGE OS ELEMENTOS DO ART. 307 DO CÓDIGO PENAL."],["EXPOSIÇÃO E OFENSAS\nPODEM GERAR RESPONSABILIDADE.","CRIMES CONTRA A HONRA E DANOS CIVIS DEPENDEM DO CASO."],["NÃO APAGUE\nAS PROVAS.","GUARDE LINKS E DATAS. ENVIE PARA QUEM ACHA QUE VALE TUDO."]],
"slides":[["PERFIL FAKE:\nOPINIÃO OU\nCRIME?","A CONDUTA IMPORTA MAIS QUE O NOME DO PERFIL."],["NEM TODO NOME\nFICTÍCIO É CRIME.","PSEUDÔNIMO, HUMOR E CRÍTICA NÃO SE CONFUNDEM AUTOMATICAMENTE COM FALSA IDENTIDADE OU OFENSA."],["FALSA IDENTIDADE\nTEM REQUISITOS.","O ART. 307 DO CP TRATA DE ATRIBUIR FALSA IDENTIDADE PARA OBTER VANTAGEM OU CAUSAR DANO. O RESULTADO NÃO PRECISA SE CONCRETIZAR."],["LIBERDADE NÃO\nELIMINA RESPONSABILIDADE.","CALÚNIA, DIFAMAÇÃO E INJÚRIA TÊM ELEMENTOS DISTINTOS. AMEAÇAS E DISCRIMINAÇÃO TAMBÉM PODEM SER ILÍCITAS."],["COMO REAGIR\nSEM PERDER PROVAS?","GUARDE URLS, DATAS E CONTEXTO ANTES DE DENUNCIAR. IDENTIFICAÇÃO PODE EXIGIR ORDEM JUDICIAL E DADOS TÉCNICOS. IP SOZINHO NÃO PROVA AUTORIA."]],
"caption":"Criar um perfil com nome fictício não torna alguém criminoso automaticamente. Usá-lo para se passar por outra pessoa, ofender, ameaçar ou fraudar pode mudar completamente o cenário.\nO art. 307 do Código Penal exige atribuição de falsa identidade com finalidade de obter vantagem ou causar dano. O STJ esclarece que a obtenção efetiva da vantagem ou a ocorrência do prejuízo não são necessárias para a consumação.\nGuarde URLs, datas, contexto e arquivos antes de denunciar. A identificação pode exigir medidas judiciais e cruzamento de registros: endereço IP não equivale, sozinho, a autoria comprovada.\nSalve para consultar e não confunda crítica com licença para ofender.",
"sources":["https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm","https://scon.stj.jus.br/jurisprudencia/externo/informativo/?acao=pesquisar&aplicacao=informativo&b=INFJ&i=151&l=50&livre=%2707&p=true&refinar=S.DISP.&t="]},
{"id":"06-heranca","date":"2026-11-07","label":"HERANÇA DIGITAL","kind":"vault",
"reel":[["VOCÊ MORRE.\nE SEU BITCOIN?",""],["PATRIMÔNIO DIGITAL\nPODE ENTRAR NA HERANÇA.","MAS NEM TODA CONTA OU MENSAGEM É TRANSMISSÍVEL."],["HERDAR NÃO É\nGANHAR ACESSO A TUDO.","A INTIMIDADE DO FALECIDO E DE TERCEIROS CONTINUA IMPORTANDO."],["SEM ACESSO,\nO RISCO AUMENTA.","EM AUTOCUSTÓDIA, PERDER AS CHAVES PODE IMPEDIR A RECUPERAÇÃO."],["ORGANIZE HOJE.\nPROTEJA QUEM FICA.","COMPARTILHE COM QUEM TEM CRIPTO. NÃO ENVIE SENHAS POR COMENTÁRIOS."]],
"slides":[["QUEM HERDA\nSUA VIDA\nDIGITAL?","FOTOS, CONTAS E CRIPTOMOEDAS NÃO TÊM A MESMA REGRA."],["SEPARE PATRIMÔNIO\nDE INTIMIDADE.","ATIVOS ECONÔMICOS PODEM INTEGRAR A SUCESSÃO. MENSAGENS E DADOS PRIVADOS EXIGEM PROTEÇÃO DO FALECIDO E DE TERCEIROS."],["BITCOIN SEM CHAVE:\nUM RISCO REAL.","EM AUTOCUSTÓDIA, SEM CHAVE OU MECANISMO DE RECUPERAÇÃO O ACESSO PODE SER IMPOSSÍVEL. EM CORRETORAS, HÁ PROCEDIMENTOS PRÓPRIOS."],["PLANEJAMENTO\nNÃO É COMPARTILHAR SENHA.","INVENTARIE ATIVOS, DEFINA ACESSO SEGURO E USE CONTATOS DE LEGADO QUANDO DISPONÍVEIS. TESTAMENTO EXIGE FORMALIDADES LEGAIS."],["HERDAR NÃO É\nACESSAR TUDO.","O STJ ADMITIU INCIDENTE PRÓPRIO NO INVENTÁRIO PARA IDENTIFICAR BENS DIGITAIS, PRESERVANDO A INTIMIDADE. BUSQUE ORIENTAÇÃO SUCESSÓRIA."]],
"caption":"Seu patrimônio digital pode sobreviver a você. Acesso e herança, porém, são questões diferentes.\nCriptoativos com valor econômico podem integrar a sucessão. Mensagens, fotos privadas e contas pessoais exigem atenção à intimidade do falecido e de terceiros, às regras da plataforma e ao caso concreto.\nO STJ admitiu incidente associado ao inventário, com profissional especializado, para identificar e classificar bens digitais protegidos por senha, preservando conteúdos privados.\nOrganize um inventário de ativos e um plano seguro de acesso. Em autocustódia, perder chaves sem recuperação pode impedir o acesso; em corretoras, os procedimentos são diferentes. Um arquivo chamado 'testamento digital' não substitui as formalidades legais.\nEnvie para quem tem cripto e ainda não organizou isso.",
"sources":["https://www.stj.jus.br/sites/portalp/Paginas/Comunicacao/Noticias/2025/01102025-Acesso-a-heranca-digital-protegida-por-senha-exige-incidente-processual-proprio--decide-Terceira-Turma.aspx"]},
{"id":"07-eleicoes","date":"2026-11-08","label":"IA E MANIPULAÇÃO","kind":"ballot",
"reel":[["QUEM FORMOU\nSUA OPINIÃO?",""],["UM VÍDEO REALISTA\nPODE SER FALSO.","A IA CONSEGUE IMITAR IMAGEM E VOZ."],["NA PROPAGANDA ELEITORAL,\nHÁ LIMITES.","O TSE PROÍBE DEEPFAKES PARA FAVORECER OU PREJUDICAR CANDIDATURAS."],["O AVISO 'FEITO COM IA'\nNÃO LIBERA TUDO.","ROTULAGEM NÃO TORNA UM CONTEÚDO PROIBIDO PERMITIDO."],["CONFIRA A ORIGEM\nANTES DE COMPARTILHAR.","VOCÊ CONFIA NA REGULAÇÃO DA IA? COMENTE."]],
"slides":[["IA NAS ELEIÇÕES:\nO AVISO\nBASTA?","ROTULAR NÃO LIBERA TODA MANIPULAÇÃO."],["O QUE EXIGE\nTRANSPARÊNCIA?","A PROPAGANDA COM CONTEÚDO SINTÉTICO DEVE INFORMAR O USO DE IA DE FORMA EXPLÍCITA, DESTACADA E ACESSÍVEL, CONFORME AS REGRAS DO TSE."],["DEEPFAKE NÃO\nVIRA LÍCITA COM AVISO.","É PROIBIDO USAR DEEPFAKE NA PROPAGANDA PARA FAVORECER OU PREJUDICAR CANDIDATURA. A VEDAÇÃO TEM REQUISITOS ESPECÍFICOS."],["CHATBOT NÃO PODE\nFINGIR SER CANDIDATO.","A COMUNICAÇÃO DE CAMPANHA COM IA EXIGE TRANSPARÊNCIA. SIMULAR INTERLOCUÇÃO COM CANDIDATO OU OUTRA PESSOA REAL É VEDADO."],["VIU MANIPULAÇÃO?\nPRESERVE E DENUNCIE.","GUARDE LINK, DATA E ARQUIVO. CONSULTE OS CANAIS OFICIAIS DA JUSTIÇA ELEITORAL. SANÇÕES DEPENDEM DA CONDUTA E DO PROCESSO."]],
"caption":"O aviso 'feito com IA' não é um passe livre na propaganda eleitoral.\nA Resolução TSE 23.610/2019, com alterações inclusive da Resolução 23.755/2026, exige transparência no uso de conteúdo sintético e prevê vedações específicas.\nDeepfakes usadas na propaganda para favorecer ou prejudicar candidaturas são proibidas. Chatbots de campanha não podem simular conversa com candidato ou outra pessoa real. Há também restrições temporais específicas que precisam ser observadas.\nEste é um guia das regras, sem afirmação sobre resultado eleitoral ou prazo para uma próxima eleição. Sanções não são automáticas: dependem da infração e do devido processo.\nConfira a origem, preserve o link e consulte os canais oficiais da Justiça Eleitoral. Você confia na regulação da IA?",
"sources":["https://www.tse.jus.br/legislacao/compilada/res/2019/resolucao-no-23-610-de-18-de-dezembro-de-2019","https://www.tse.jus.br/legislacao/compilada/res/2026/resolucao-no-23-755-de-2-de-marco-de-2026"]}]
HASHTAGS="\n\n#Direito #Tecnologia #InteligenciaArtificial #DireitoDigital #LGPD #SegurancaDigital #DireitoETecnologia #DireitoBinario #CidadaniaDigital"
def font(n,bold=True): return ImageFont.truetype(FONT if bold else REG,n)
def wrap(text,f,width):
    result=[]
    for paragraph in text.split("\n"):
        line=""
        for word in paragraph.split():
            test=(line+" "+word).strip()
            if f.getlength(test)>width and line: result.append(line);line=word
            else: line=test
        result.append(line)
    return result
def block(draw,text,xy,width,size,maxheight,color=WHITE,bold=True):
    while size>=24:
        f=font(size,bold);lines=wrap(text,f,width);step=round(size*1.22)
        if len(lines)*step<=maxheight:break
        size-=2
    if len(lines)*step>maxheight:raise ValueError("Text overflow: "+text)
    for i,line in enumerate(lines):draw.text((xy[0],xy[1]+i*step),line,font=f,fill=color)
    return len(lines)*step
def robot(d,x,y,s=1,mood=0):
    def box(b,r,fill,outline=None,w=3):d.rounded_rectangle(tuple(int(v*s) for v in (x+b[0],y+b[1],x+b[2],y+b[3])),radius=int(r*s),fill=fill,outline=outline,width=max(1,int(w*s)))
    # x,y are supplied in unscaled coordinates.
    box((0,0,148,112),30,"#172d46",C,4)
    box((12,22,136,85),20,"#07141e",None)
    for ex in (37,96):
        box((ex,38,ex+17,64),7,C)
    box((29,119,119,181),18,"#15243d",P)
    box((47,139,101,155),6,G)
    for ax in (-22,155):box((ax,128,ax+16,168),7,"#223a52",C)
    for lx in (35,88):box((lx,186,lx+27,204),6,"#223a52",C)
    d.line((int((x+74)*s),int((y-24)*s),int((x+74)*s),int(y*s)),fill=C,width=max(1,int(4*s)))
    d.ellipse((int((x+65)*s),int((y-40)*s),int((x+83)*s),int((y-22)*s)),fill=G)
def illustration(kind,size=650,variant=0):
    # Original code-native vector illustration, rendered at 2x.
    ss=2
    im=Image.new("RGBA",(800*ss,480*ss))
    d=ImageDraw.Draw(im)
    def line(points,fill=C,width=4):d.line([(int(x*ss),int(y*ss)) for x,y in points],fill=fill,width=width*ss,joint="curve")
    def rect(b,fill="#0b192b",outline=C,r=20,w=3):d.rounded_rectangle(tuple(int(z*ss) for z in b),r*ss,fill,outline,w*ss)
    def ell(b,fill=None,outline=C,w=3):d.ellipse(tuple(int(z*ss) for z in b),fill,outline,w*ss)
    # orbital circuitry
    ell((175,20,605,450),outline="#193d57",w=2)
    ell((203,48,577,422),outline="#27334d",w=2)
    for i in range(12):
        a=i*math.pi/6
        x,y=390+230*math.cos(a),235+210*math.sin(a)
        line([(x,y),(x+45*math.cos(a),y+30*math.sin(a)),(x+90*math.cos(a),y+30*math.sin(a))],fill=P if i%3==0 else "#24606c",width=2)
        ell((x-5,y-5,x+5,y+5),fill=C,outline=None)
    if kind=="phone":
        rect((278,20,512,443),r=36,w=5)
        rect((292,38,498,420),outline="#275271",r=25)
        rect((350,42,442,57),fill="#29425d",outline=None,r=6)
        ell((346,91,448,193),fill="#183d58")
        ell((378,109,414,145),fill="#6899b3",outline=None)
        d.pieslice((357*ss,142*ss,436*ss,215*ss),180,360,fill="#6899b3")
        for j in range(18):
            h=12+abs(math.sin(j*1.4))*55
            line([(310+j*9,258-h/2),(310+j*9,258+h/2)],C if j%2 else P,4)
        ell((316,333,367,384),fill="#113e40",outline=C)
        ell((423,333,474,384),fill="#491c38",outline="#fa718a")
        line([(335,350),(348,365)],G,6)
        rect((458,142,573,219),fill="#362039",outline=G,r=12)
        d.text((491*ss,151*ss),"!",font=font(48*ss),fill=G)
    elif kind=="eye":
        # Eye lens over a perspective keyboard
        d.polygon([(225*ss,319*ss),(545*ss,319*ss),(630*ss,427*ss),(140*ss,427*ss)],fill="#10223b",outline=C,width=4*ss)
        for j in range(5):line([(199-j*12,340+j*17),(568+j*11,340+j*17)],"#345d80",2)
        for j in range(10):line([(225+j*33,326),(170+j*44,418)],"#345d80",2)
        d.polygon([(160*ss,160*ss),(265*ss,65*ss),(500*ss,65*ss),(610*ss,160*ss),(500*ss,250*ss),(265*ss,250*ss)],fill="#10273d",outline=C,width=5*ss)
        ell((292,64,478,250),fill="#183750",outline=P,w=5)
        ell((318,90,452,224),fill="#164d60",outline=C,w=5)
        ell((354,126,416,188),fill="#04101c",outline=G,w=4)
        ell((352,115,371,134),fill=WHITE,outline=None)
        for x in (262,510):line([(x,260),(x,291),(385,291),(385,309)],G,2)
    elif kind=="pix":
        for px,py in [(380,95),(240,235),(520,235),(380,375)]:
            d.rounded_rectangle(((px-70)*ss,(py-70)*ss,(px+70)*ss,(py+70)*ss),radius=22*ss,fill="#144550",outline=C,width=4*ss)
        line([(245,235),(320,160),(380,220),(440,160),(515,235),(440,310),(380,250),(320,310),(245,235)],G,5)
        for j in range(14):
            xx=550+j*12; yy=130+(j*41)%220
            rect((xx,yy,xx+10,yy+10),fill=P,outline=None,r=1)
        line([(590,62),(652,62),(652,115)],"#fa718a",6)
        line([(630,96),(652,118),(674,96)],"#fa718a",6)
    elif kind=="lock":
        d.arc((272*ss,32*ss,504*ss,284*ss),180,340,fill=C,width=25*ss)
        line([(480,88),(452,132),(484,163)],G,13)
        rect((247,195,530,413),fill="#152b42",outline=P,r=25,w=5)
        ell((361,258,418,315),fill=G,outline=None)
        rect((379,301,401,345),fill=G,outline=None,r=5)
        for j in range(5):
            line([(543,225+j*34),(608,225+j*34),(633,200+j*34),(683,200+j*34)],C,2)
            ell((679,196+j*34,687,204+j*34),fill=C,outline=None)
    elif kind=="fake":
        rect((228,47,544,426),fill="#15233c",outline=P,r=30,w=5)
        ell((306,93,466,253),fill="#0b1728",outline=C,w=4)
        # mask
        d.polygon([(315*ss,147*ss),(386*ss,165*ss),(458*ss,147*ss),(443*ss,208*ss),(386*ss,231*ss),(330*ss,208*ss)],fill="#244a60",outline=G,width=3*ss)
        for x in (338,404):rect((x,176,x+29,190),fill="#04111c",outline=C,r=5,w=2)
        for y in (286,315,344):rect((270,y,502,y+10),fill="#33506a",outline=None,r=4)
        rect((322,376,450,400),fill="#173740",outline=C,r=10,w=2)
        line([(550,61),(597,108),(550,155)],"#fa718a",5)
    elif kind=="vault":
        rect((222,46,562,424),fill="#1b2641",outline=P,r=24,w=5)
        rect((248,72,536,399),fill="#102235",outline=C,r=17,w=3)
        ell((318,144,479,305),fill="#1b4250",outline=G,w=5)
        ell((364,190,432,258),fill="#102032",outline=C,w=4)
        for i in range(6):
            a=i*math.pi/3
            line([(398+40*math.cos(a),224+40*math.sin(a)),(398+70*math.cos(a),224+70*math.sin(a))],G,7)
        for y in (125,330):rect((235,y,262,y+43),fill="#41566c",outline=C,r=5,w=2)
        ell((517,301,650,434),fill="#47351c",outline=G,w=5)
        d.text((552*ss,315*ss),"B",font=font(70*ss),fill=G)
        line([(575,309),(575,416)],G,3)
    else:
        # stylized voting terminal, no official logo or purported ballot
        d.polygon([(205*ss,92*ss),(558*ss,92*ss),(615*ss,379*ss),(145*ss,379*ss)],fill="#16253b",outline=C,width=4*ss)
        rect((217,132,419,290),fill="#061925",outline=P,r=8,w=3)
        for i in range(4):line([(240,160+i*29),(395-i*24,160+i*29)],G if i==0 else "#37748a",5)
        for yy in range(3):
            for xx in range(3):rect((452+xx*35,151+yy*41,478+xx*35,181+yy*41),fill="#375064",outline="#4f8793",r=4,w=2)
        for i in range(7):
            d.text(((155+i*65)*ss,25*ss),str(i%2),font=font(26*ss),fill=C if i%2 else P)
        line([(255,401),(525,401)],G,6)
    robot(d,640,280,ss,variant)
    glow=im.filter(ImageFilter.GaussianBlur(9*ss))
    glow.putalpha(glow.getchannel("A").point(lambda a:int(a*.55)))
    combined=Image.alpha_composite(glow,im)
    return combined.resize((size,round(size*.6)),Image.Resampling.LANCZOS)
def base(h,seed):
    w=1080
    yy,xx=np.mgrid[0:h,0:w]
    glow=np.exp(-(((xx-820)/650)**2+((yy-h*.63)/550)**2))
    glow2=np.exp(-(((xx-40)/540)**2+((yy-h*.85)/600)**2))
    a=np.zeros((h,w,3),dtype=np.uint8)
    for k,(b,v,z) in enumerate([(7,9,7),(10,16,4),(17,32,20)]):a[:,:,k]=(b+v*glow+z*glow2).astype("uint8")
    im=Image.fromarray(a);d=ImageDraw.Draw(im)
    # Fine perspective floor and circuit traces
    for x in range(-600,1800,120):d.line((540,h*.55,x,h),fill="#122438",width=1)
    for y in range(int(h*.7),h,50):d.line((0,y,w,y),fill="#142438",width=1)
    rng=random.Random(seed)
    for i in range(26):
        x=rng.randrange(25,1050);y=rng.randrange(int(h*.53),h-110)
        d.ellipse((x,y,x+3,y+3),fill="#2f6179")
    d.rounded_rectangle((65,69,1015,119),radius=24,outline="#27536b",width=2)
    d.text((89,82),"DIREITO BINÁRIO  /  O LADO SOMBRIO DA TECNOLOGIA",font=font(23),fill=C)
    d.line((68,h-110,1012,h-110),fill="#31506c",width=2)
    d.text((70,h-83),"@DIREITOBINARIO",font=font(28),fill=WHITE)
    return im
def card(day,pair,index,total,reel=False):
    h=1920 if reel else 1350
    im=base(h,index);d=ImageDraw.Draw(im)
    label=f"{day['label']}  /  {index+1:02d}"
    d.text((70,154 if not reel else 236),label,font=font(25),fill=G)
    title_y=203 if not reel else 300
    title_h=330 if not reel else 390
    # consistent large headlines, fit checked
    used=block(d,pair[0],(65,title_y),940,76 if not reel else 82,title_h)
    # Full illustrative field separates heading and supporting text.
    art_y=590 if reel else 540
    art_size=970 if reel else 900
    art=illustration(day["kind"],art_size,index)
    im.paste(art,((1080-art.width)//2,art_y),art)
    d=ImageDraw.Draw(im)
    body_y=1250 if reel else 1090
    # carousel body below title and above illustration, room 190
    if not reel:
        body_y=title_y+used+28
        max_body=min(260,535-body_y)
        # If heading uses 3+ lines, put body in bottom panel.
        if max_body<165:
            body_y=1030
            max_body=180
        else:max_body=535-body_y
        block(d,pair[1],(70,body_y),925,32,max_body,color="#cbd5e3",bold=False)
    elif pair[1]:
        d.rounded_rectangle((65,1215,1015,1505),radius=24,fill="#101e31",outline="#26475b",width=2)
        block(d,pair[1],(92,1250),875,43,215,color="#d6e0ec",bold=False)
    if reel:
        d.text((70,1625),"SALVE • COMPARTILHE • SIGA",font=font(29),fill=G)
        d.text((70,1678),"CONTEÚDO EDUCATIVO  /  FONTES NA LEGENDA",font=font(23),fill="#8ba3bc")
    else:
        d.text((70,1190),"ARRASTE  →" if index<total-1 else "SALVE E COMPARTILHE",font=font(25),fill=G)
    d.text((905,h-83),f"{index+1}/{total}",font=font(26),fill=C)
    return im
def make_contact(paths,target):
    thumbw=270; thumbh=338
    grid=Image.new("RGB",(thumbw*7,thumbh*2),"#080e17")
    for j,path in enumerate(paths):
        im=Image.open(path); im.thumbnail((thumbw,thumbh))
        grid.paste(im,((j%7)*thumbw,(j//7)*thumbh))
    grid.save(target)
def main():
    manifest=[]
    sample=[]
    for day in DATA:
        folder=OUT/day["id"];folder.mkdir(exist_ok=True)
        slides=[]
        for i,pair in enumerate(day["slides"]):
            path=folder/f"slide-{i+1:02d}.jpg"
            card(day,pair,i,len(day["slides"])).save(path,quality=95,subsampling=0)
            slides.append(str(path))
        frames=[]
        for i,pair in enumerate(day["reel"]):
            path=folder/f"scene-{i+1:02d}.png"
            card(day,pair,i,5,True).save(path)
            frames.append(path)
        sample.extend([slides[0],str(frames[0])])
        # 30 seconds, five scenes; distinct original ambient electronic score.
        listing=folder/"scenes.ffconcat"
        durations=[3,7,7,7,6]
        listing.write_text("ffconcat version 1.0\n"+"".join(f"file '{p.name}'\nduration {dur}\n" for p,dur in zip(frames,durations))+f"file '{frames[-1].name}'\n")
        video=folder/"reel.mp4"
        if "--images-only" not in sys.argv:
            cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-safe","0","-i",str(listing),
                 "-f","lavfi","-i","aevalsrc=0.08*(sin(2*PI*110*t)+0.5*sin(2*PI*164.81*t)+0.35*sin(2*PI*220*t))*(0.55+0.45*sin(2*PI*1.5*t)*sin(2*PI*1.5*t)):s=48000:d=30",
                 "-vf","fps=24,fade=t=in:st=0:d=0.25,fade=t=out:st=29.65:d=0.35,format=yuv420p",
                 "-af","afade=t=in:d=1,afade=t=out:st=28:d=2","-t","30","-c:v","libx264","-preset","veryfast","-crf","21","-threads","2","-c:a","aac","-b:a","128k","-movflags","+faststart",str(video)]
            subprocess.run(cmd,check=True)
        source_lines="\n".join(day["sources"])
        for typ,hr,files in [("REELS","08:00",[str(video)]),("CAROUSEL","17:00",slides)]:
            caption=day["caption"]+"\n\nFontes:\n"+source_lines+HASHTAGS
            if len(caption)>2200:raise ValueError(f"Caption too long {day['id']}: {len(caption)}")
            manifest.append({"id":day["id"]+"-"+typ.lower(),"date":day["date"]+"T"+hr+":00-03:00","type":typ,"files":files,"caption":caption,"sources":day["sources"],"status":"ready"})
        print("GENERATED",day["id"],flush=True)
    (OUT/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    (OUT/"roteiros.json").write_text(json.dumps(DATA,ensure_ascii=False,indent=2))
    # 14-thumbnail review sheet: carousels first row, reels second.
    ordered=sample[::2]+sample[1::2]
    make_contact(ordered,OUT/"preview.jpg")
    print("COMPLETE",OUT,flush=True)
if __name__=="__main__":main()
