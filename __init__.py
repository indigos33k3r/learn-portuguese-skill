from adapt.intent import IntentBuilder
from mycroft.skills.core import FallbackSkill, intent_handler, intent_file_handler
from mycroft.audio import wait_while_speaking, play_mp3
from mycroft.util.format import nice_date, pronounce_number
from mycroft.util.parse import extract_number, extract_datetime

import os
import random
from PyDictionary import PyDictionary
from mtranslate import translate


class LearnPortugueseSkill(FallbackSkill):
    path_translated_file = "/tmp/portuguese.mp3"
    intercepting = False
    puns = [
        {
            "pergunta": "Quais heróis se preocupam mais com as poses para fotos do que com salvar o seu planeta?",
            "resposta": "Os TumblrCats"
        }, {
            "pergunta": "Qual é a profissão do Homem Aranha?",
            "resposta": "Desenvolvedor Web"
        }, {
            "pergunta": "Qual é o estado dos EUA que te eletrifica?",
            "resposta": "Ohio."
        }, {
            "pergunta": "Por que o monge foi ao hospital?",
            "resposta": "Porque ele é paciente."
        }, {
            "pergunta": "Qual o time mais quente de todos?",
            "resposta": "Bota-fogo."
        }, {
            "pergunta": "Por que o cachorro ia pra escola todos os dias?",
            "resposta": "Porque ele tinha auaula."
        }, {
            "pergunta": "Qual o produto tensoativo que sabe de tudo?",
            "resposta": "Sabão."
        }, {
            "pergunta": "Quem é o rei dos produtos de espantar insetos?",
            "resposta": "É o Rei-pelente."
        }, {
            "pergunta": "Por que o magrelo tem que tomar banho com os braços abertos?",
            "resposta": "Para não ser engolido pelo ralo."
        }, {
            "pergunta": "Qual o ator que livra as pessoas das dores?",
            "resposta": "Malvino Salva-dor."
        }, {
            "pergunta": "Por que as vogais A, E, I e O foram rejeitadas pela banda Scorpions?",
            "resposta": "Porque eles Still Love U."
        }, {
            "pergunta": "Qual a carne que é cheia de panos?",
            "resposta": "Frango Empanado."
        }, {
            "pergunta": "Por que o Papai Noel não tem assadura?",
            "resposta": "Porque seu saco já é vermelho."
        }, {
            "pergunta": "Qual é a bebida que corre?",
            "resposta": "Rum."
        }, {
            "pergunta": "Você está em uma estrada e vê vários postos um perto do outro. Por que isso acontece?",
            "resposta": "Porque os-postos se atraem."
        }, {
            "pergunta": "Qual animal não gosta do amanhã?",
            "resposta": "Rinocer-ontem."
        }, {
            "pergunta": "O que acontece se um panda tiver vários filhotes?",
            "resposta": "Vira uma pandemia."
        }, {
            "pergunta": "Qual a fruta predileta da cigana?",
            "resposta": "O Li Mão."
        }, {
            "pergunta": "Qual é o tipo de música favorito dos mortos?",
            "resposta": "R.I.P-Hop."
        }, {
            "pergunta": "O que é que tem no meio do ovo?",
            "resposta": "A gema."
        }, {
            "pergunta": "Por que a loira entrou com muitos espelhos na faculdade de engenharia?",
            "resposta": "Porque ela é engenheira se-viu."
        }, {
            "pergunta": "Qual é a cantora que não se adapta ao meio urbano?",
            "resposta": "Vanessa da Mata."
        }, {
            "pergunta": "Qual é o super-herói que toma chá e depois dá um salto pequeno?",
            "resposta": "Chá-pulinho."
        }, {
            "pergunta": "Qual é a ave que está sempre enrijecida?",
            "resposta": "An-durinha."
        }, {
            "pergunta": "Qual é a ave que serve de automóvel para um parasita aracnídeo?",
            "resposta": "Carro-a-pato."
        }, {
            "pergunta": "Porque o principal narrador esportivo da Globo adora narrar jogos da Argentina?",
            "resposta": "Porque é Galvão Buenos-Aires."
        }, {
            "pergunta": "Que tipo de negócio abriram os ursos da China?",
            "resposta": "Uma pandaria."
        }, {
            "pergunta": "Qual o filósofo favorito do cavalo?",
            "resposta": "Trotsky."
        }, {
            "pergunta": "Qual é a ferramenta que sempre aponta onde as pessoas e coisas estão?",
            "resposta": "Ali-cate."
        }, {
            "pergunta": "O que o leitão foi fazer na loja de parafusos?",
            "resposta": "Foi procurar a porca."
        }, {
            "pergunta": "O que o boi respondeu para a vaca, quando ela o perguntou se ele gostava bastante dela?",
            "resposta": "Muuuuuuuuuuuuito!"
        }, {
            "pergunta": "Como se chama o campeonato de anedotas?",
            "resposta": "Olim-piadas."
        }, {
            "pergunta": "Qual a reação de um mecânico depois de contarem uma piada sem graça para ele?",
            "resposta": "Dizer que não achou graxa nenhuma."
        }, {
            "pergunta": "Qual o tipo de violência que o super-herói do martelo não admite?",
            "resposta": "A Thortura."
        }, {
            "pergunta": "Qual a doença do sacristão?",
            "resposta": "Sinus-ite."
        }, {
            "pergunta": "Por que temos vacas e bois próximos ao nosso estômago?",
            "resposta": "Porque temos o intestino deu-gado."
        }, {
            "pergunta": "Qual o tipo de pessoa o Papai Noel gosta?",
            "resposta": "De puxa-saco."
        }, {
            "pergunta": "Qual é o ramo da medicina que faz uma ligação para a irmã de sua mãe?",
            "resposta": "Alopatia."
        }, {
            "pergunta": "O que acontece se um panda tiver vários filhos?",
            "resposta": "Ele vira um pandeiro."
        }, {
            "pergunta": "Quando é que o Renato Aragão acorda?",
            "resposta": "Didi-a."
        }, {
            "pergunta": "O que é que, quando o pai nasce a filha já esta andando?",
            "resposta": "Fumaça."
        }, {
            "pergunta": "Qual é o time mais odiado pelo os bombeiros?",
            "resposta": "Botafogo"
        }, {
            "pergunta": "O que você deve fazer quando estiver triste?",
            "resposta": "Abraçar o sapato, porque o sapato com-sola."
        }, {
            "pergunta": "Qual o carro em que o Cebolinha manda as pessoas pararem?",
            "resposta": "Ô-Pala."
        }, {
            "pergunta": "Você sabe qual é a comida preferida do topógrafo?",
            "resposta": "Frângulo."
        }, {
            "pergunta": "Como se fala bombeiro em japonês?",
            "resposta": "Takágua Naxama."
        }, {
            "pergunta": "Qual a rede social que os mineiros mais usam?",
            "resposta": "Uaitsapp."
        }, {
            "pergunta": "Qual é o nome da pedra falante?",
            "resposta": "Sei lá, pergunta pra ela, ela fala!"
        }, {
            "pergunta": "Qual é a massa do caderno?",
            "resposta": "A massa folhada."
        }, {
            "pergunta": "Três mulheres estavam com picolés nas mãos. Uma estava chupando o picolé, outra estava mordendo o picolé e outra estava lambendo o picolé. Qual delas era a casada?",
            "resposta": "A que estava com anel no dedo."
        }, {
            "pergunta": "Qual o banco em que uma letra se transforma em outra letra?",
            "resposta": "É o I-tá-U."
        }, {
            "pergunta": "Qual a fruta que é parente da porta?",
            "resposta": "É a Maçã-Neta."
        }, {
            "pergunta": "Qual é a peça de roupa preferido do Thor?",
            "resposta": "PaleThor."
        }, {
            "pergunta": "Qual a cantora que é o primeiro alce do mundo?",
            "resposta": "Alce-One."
        }, {
            "pergunta": "Um bêbado estava na rua quando chegou um carro e buzinou. O que o bêbado respondeu?",
            "resposta": "Eu também bibi."
        }, {
            "pergunta": "Qual a diferença entre a cachaça e a mulher?",
            "resposta": "A cachaça dá dor de cabeça só um dia."
        }, {
            "pergunta": "Por que o português jogou o arroz inteiro do pacote dentro do pote de açúcar?",
            "resposta": "Para comer arroz doce."
        }, {
            "pergunta": "Por que os lustres não prestam atenção para escuridão?",
            "resposta": "Porque eles tem focos luminosos."
        }, {
            "pergunta": "O que é um cachorro afinado, que entende de música?",
            "resposta": "É um cãotor."
        }, {
            "pergunta": "O que é um objeto cortante em poder de um cachorro?",
            "resposta": "Um cão-nivete."
        }, {
            "pergunta": "Por que o maior dramaturgo de língua inglesa é considerado um cavalheiro quando tenta ir ao banheiro, mas está ocupado?",
            "resposta": "Porque quando ele bate e respondem que tem gente, ele diz em seguida: Shake-espera."
        }, {
            "pergunta": "Por que na cidade de Palmas as mulheres nunca conseguem molhar o cabelo?",
            "resposta": "Porque lá elas usam Touca-ntins."
        }, {
            "pergunta": "Por que a loira pediu um envelope redondo no escritório onde trabalha?",
            "resposta": "Porque seu chefe a pediu para entregar uma circular."
        }, {
            "pergunta": "Qual o veículo que é mulher do lanche?",
            "resposta": "Lancha."
        }, {
            "pergunta": "O tio de Pedro tem 4 filhas, Lala, Lele, Lili, Lolo. Qual falta?",
            "resposta": "Nenhuma, porque já tem 4."
        }, {
            "pergunta": "Qual o molho de tomate preferido dos gatos?",
            "resposta": "É o Cat-chup."
        }, {
            "pergunta": "Qual o eletrodoméstico do vulcão?",
            "resposta": "É a máquina de lava."
        }, {
            "pergunta": "Um homem levou um pedaço de queijo pro hospício e um dos pacientes subiu em cima do queijo. Qual o nome da série?",
            "resposta": "Um Maluco no Pedaço."
        }, {
            "pergunta": "O que pensaram os outros convidados quando viram o Zangado chegar na festa sem a Branca de Neve?",
            "resposta": "Ah, Não!"
        }, {
            "pergunta": "Qual o campeonato que tira as suas dores?",
            "resposta": "Liberta-dores"
        }, {
            "pergunta": "Qual é a vestimenta preferida do Batman?",
            "resposta": "Bat-ina."
        }, {
            "pergunta": "Por que um atleta dormiu na balança de uma farmácia?",
            "resposta": "Para que quando acordasse fizesse um levantamento de peso."
        }, {
            "pergunta": "Qual o peixe que é parceiro de todo mundo?",
            "resposta": "Truta."
        }, {
            "pergunta": "Por que as roupas amassadas se estenderam sobre o trilho?",
            "resposta": "Porque lá passa o Trem de Ferro."
        }, {
            "pergunta": "Qual o médico que as pessoas atiram compostos orgânicos?",
            "resposta": "Geraldo Álcool-Em-Mim."
        }, {
            "pergunta": "Como se diz veterinário em japonês?",
            "resposta": "Kuragato Nakasa."
        }, {
            "pergunta": "Qual é o alimento preferida do Thor no natal?",
            "resposta": "Pane-Thor-ne."
        }, {
            "pergunta": "Qual é o aparelho digital preferido do Thor?",
            "resposta": "LapTHORp."
        }, {
            "pergunta": "Por que a loira leva sabonete e shampoo pro pé de manga?",
            "resposta": "Porque ela gosta de tomar banho de mangueira."
        }, {
            "pergunta": "Qual a explosão que o Renato Aragão mais tem medo?",
            "resposta": "É a Didi-namite."
        }, {
            "pergunta": "O que a Oceania e a novela tem em comum?",
            "resposta": "Que a Oceania é O Outro Lado do Mundo e a novela é O Outro Lado do Paraíso."
        }, {
            "pergunta": "O menino estava assistindo desenho, e seu pai sem querer resvala na tomada e acaba desligando a TV. Qual o nome do desenho?",
            "resposta": "Pô-pai."
        }, {
            "pergunta": "Qual é a fruta que termina primeiro do que todas as outras?",
            "resposta": "Jabuti-acaba."
        }, {
            "pergunta": "Qual é o urso que nunca envelhece?",
            "resposta": "Peter-Panda."
        }, {
            "pergunta": "Porque o urso começou a se coçar de repente?",
            "resposta": "Porque ele era um urso empolar."
        }, {
            "pergunta": "Um americano perguntou para o bom velhinho do natal: Papai, o senhor está bem?",
            "resposta": "No well, respondeu o senhor..."
        }, {
            "pergunta": "O que disse uma pessoa após ter descoberto que havia comprado um óculos sem as lentes?",
            "resposta": "Cuidado, é armação..."
        }, {
            "pergunta": "Por que as senhoras que vão à piscina gostam tanto de Helmmans?",
            "resposta": "Porque elas só ficam de maiô-nesse."
        }, {
            "pergunta": "Porque todos os tipos de carne não toleram os bifes macios?",
            "resposta": "Porque elas são contra-filé."
        }, {
            "pergunta": "Qual o estado brasileiro que anda de trem?",
            "resposta": "Piauiiiiiiiiiiiiiiii."
        }, {
            "pergunta": "Como a família portuguesa que mora no Brasil parou de gastar com oftalmologista?",
            "resposta": "Mudando-se para Boa-Vista."
        }, {
            "pergunta": "Qual é a capital brasileira que ensina a irmã a latir?",
            "resposta": "Mana, au-aus."
        }, {
            "pergunta": "Qual a cidade mais amarela do mundo?",
            "resposta": "Yellows Angeles."
        }, {
            "pergunta": "Qual é o cantor que poderia ser ortopedista?",
            "resposta": "Caetano Vê-o-osso."
        }, {
            "pergunta": "Qual o carro mais azedo que existe?",
            "resposta": "Limão-zine."
        }, {
            "pergunta": "Por que um jardineiro estava cavando o chão da vila do Chaves?",
            "resposta": "Porque ele queria achar o tesouro."
        }, {
            "pergunta": "Qual o problema de saúde que nenhum anão terá?",
            "resposta": "Pressão alta."
        }, {
            "pergunta": "Qual é a fruta favorita dos maquinistas?",
            "resposta": "Kiwiiiiiiiiiiiiiii!!!"
        }, {
            "pergunta": "Qual é a fruta que ameniza o calor de Ana?",
            "resposta": "Abana-Ana."
        }, {
            "pergunta": "Por que o estádo do Grêmio tem muitas abelhas?",
            "resposta": "Porque Pedro Gerou-o-mel."
        }, {
            "pergunta": "Dois textos eram incompletos e estavam participando de alguns campeonatos de futebol, o que um disse pro outro?",
            "resposta": "Precisamos de título."
        }, {
            "pergunta": "Qual o apresentador que tem olfato de animal?",
            "resposta": "Rodrigo Faro."
        }, {
            "pergunta": "Qual é o carro do exército?",
            "resposta": "Kadett."
        }, {
            "pergunta": "Qual é a crença ou religião que está sempre conectada à internet?",
            "resposta": "A Umbanda Larga."
        }, {
            "pergunta": "Qual é o lugar da igreja que o Batman mais gosta?",
            "resposta": "Bat-istério."
        }, {
            "pergunta": "Qual é o animal preferido do Thor?",
            "resposta": "OrniThorrinco."
        }, {
            "pergunta": "Meu fim me leva ao começo ou o inexiste, sou um caminho sem fim, oque eu sou?",
            "resposta": "Um paradoxo."
        }, {
            "pergunta": "Estou à sua volta, moro em seu coração, mas não posso ser compartilhado. O que eu sou?",
            "resposta": "A solidão. Qualquer outro sentimento e até mesmo a sabedoria e conhecimento pode ser compartilhado."
        }, {
            "pergunta": "Por que a loira comeu o telhado da casa?",
            "resposta": "Porque ela era comi-lona."
        }, {
            "pergunta": "Por que o anão não escuta o outro?",
            "resposta": "Porque ele fala baixinho."
        }, {
            "pergunta": "Qual o time de futebol em que um chinês observa um jogo de sinuca?",
            "resposta": "Lee-ver-pool."
        }, {
            "pergunta": "Qual o animal preferido do Renato Aragão?",
            "resposta": "Didi-nossauro."
        }, {
            "pergunta": "Qual time de futebol larga na frente?",
            "resposta": "Na-Pole."
        }, {
            "pergunta": "Qual a atriz que faz cópias de imagens?",
            "resposta": "Gisele Print."
        }, {
            "pergunta": "Qual o lugar onde as pessoas mais fazem churros?",
            "resposta": "Na enxurrada."
        }, {
            "pergunta": "Qual é a função do Thor?",
            "resposta": "CorreThor."
        }, {
            "pergunta": "Qual país que se você pisar, será preso?",
            "resposta": "Cana-dá."
        }, {
            "pergunta": "Um jogador de futebol apareceu e virou líder de um time de um programa de domingo da Globo. Qual o nome do filme?",
            "resposta": "Capitão Fantástico."
        }, {
            "pergunta": "O que o goleiro utiliza para dormir?",
            "resposta": "Trave-sseiro."
        }, {
            "pergunta": "Qual o aparelho luminário preferido do Thor?",
            "resposta": "RefleThor."
        }, {
            "pergunta": "Qual o animal mais fuxiqueiro que existe?",
            "resposta": "A fo-foca."
        }, {
            "pergunta": "Qual é o animal peçonhento que trabalha com montaria?",
            "resposta": "É o escor-peão."
        }, {
            "pergunta": "Por que um determinado inseto voador não reclama de aterrissar nos piores locais possíveis?",
            "resposta": "Por que Mari-pousa em qualquer lugar."
        }, {
            "pergunta": "Qual é o nome da norma jurídica para pessoas com dificuldades de dicção por repetirem demais as sílabas das palavras?",
            "resposta": "Lei de Gaga."
        }, {
            "pergunta": "Tinham dez pessoas em cima de uma árvore jogando pastilhas garoto nas pessoas que passavam em baixo. Qual o nome do filme?",
            "resposta": "Os Dez Manda Menta."
        }, {
            "pergunta": "Qual o ovo mais escuro que existe?",
            "resposta": "Ovinho tinto."
        }, {
            "pergunta": "Por que nunca falta energia no fundo do rio?",
            "resposta": "Porque ele tem enguia elétrica."
        }, {
            "pergunta": "Qual artista você não pode convidar para sua casa?",
            "resposta": "O Eric... Claptomaniaco!"
        }, {
            "pergunta": "Do que as velhinhas mas sentem saudades?",
            "resposta": "Da Ditadura!"
        }, {
            "pergunta": "Qual a semelhança entre o Uruguai e o YouTube?",
            "resposta": "Que os dois tem um Monte-Vídeo."
        }, {
            "pergunta": "No trânsito, como fazer para as dores corporais passarem mais depressa?",
            "resposta": "É só pisar no acelera-dor."
        }, {
            "pergunta": "Por que o envelope é tão medroso jogando baralho?",
            "resposta": "Porque ele só guarda as cartas."
        }, {
            "pergunta": "Por que as roupas devem se pendurarem nos cabides?",
            "resposta": "Porque eles não tem mãos pra segurarem elas."
        }, {
            "pergunta": "Qual a vodka que da tiros para os dois lados?",
            "resposta": "Bala-lá-e-cá."
        }, {
            "pergunta": "Qual o chocolate que espanta que espanta a capital do Equador?",
            "resposta": "Xô-Quito."
        }, {
            "pergunta": "Como se chama mil políticos presos?",
            "resposta": "Um bom começo."
        }, {
            "pergunta": "O que desce chorando da escada?",
            "resposta": "Balde."
        }, {
            "pergunta": "Por que o carro jamais é eletrocutado?",
            "resposta": "Porque ele tem o para-choque."
        }, {
            "pergunta": "Qual é a versão de Dragon Ball que o Vasco, Fluminense e Botafogo mais gostam?",
            "resposta": "Kai."
        }, {
            "pergunta": "Qual é o mosquito que a vaca tem medo?",
            "resposta": "Muuuuriçoca."
        }, {
            "pergunta": "Por que um tigre auxiliava o idoso a andar?",
            "resposta": "Porque ele era um tigre de bengala."
        }, {
            "pergunta": "Quem é que, no Natal, anda com o saco cheio às costas subindo e descendo a rua?",
            "resposta": "O carteiro, ou você acredita em Papai Noel?"
        }, {
            "pergunta": "Como um escritor termina um caso de amor?",
            "resposta": "Com um ponto final."
        }, {
            "pergunta": "Por que é que 'na casa do ferreiro tem espeto de pau'?",
            "resposta": "Porque 'santo de casa não faz milagre'."
        }, {
            "pergunta": "Entre médicos, qual deveria ser considerado engenheiro?",
            "resposta": "Os que faz pontes de safena."
        }, {
            "pergunta": "Quem é que bate na porta sem estar chamando ninguém?",
            "resposta": "O marceneiro."
        }, {
            "pergunta": "Que fazem os grandes costureiros, quando não têm o que fazer?",
            "resposta": "Inventam moda."
        }, {
            "pergunta": "Que pista levou o policial à certeza de que aquele carro, parado no estacionamento, era roubado?",
            "resposta": "O motor estava quente, mas a placa fria."
        }, {
            "pergunta": "Qual a profissão que aborrece?",
            "resposta": "A de amolador."
        }, {
            "pergunta": "Como se chama o jornal do oculista?",
            "resposta": "O globo ocular."
        }, {
            "pergunta": "Qual a carta que melhora a vida do carteiro?",
            "resposta": "A carta de recomendação."
        }, {
            "pergunta": "Qual o produto alimentício preferido dos escritores?",
            "resposta": "A sopa de letrinhas."
        }, {
            "pergunta": "Que escritor escreve um livro em menos de um minuto?",
            "resposta": "Qualquer um: 'um livro'."
        }, {
            "pergunta": "Qual o lugar onde o pescador pode até escolher o peixe?",
            "resposta": "Na peixaria."
        }, {
            "pergunta": "Por que um astrônomo sempre se frusta quando tenta estudar os grandes grupos de estrelas do Universo?",
            "resposta": "Porque no telescópio, a visão é sempre nebulosa."
        }, {
            "pergunta": "Quem é que se encarrega pessoalmente de transmitir os nossos desabafos, as nossas alegrias, exigências e consulta sem jamais ter contato conosco?",
            "resposta": "O carteiro."
        }, {
            "pergunta": "Qual é a capital preferida do Thor?",
            "resposta": "PreTHORia."
        }, {
            "pergunta": "Qual a prótese que vive durante um longo período?",
            "resposta": "É a denta-dura."
        }, {
            "pergunta": "Qual a haste de metal que é uma operadora de TV?",
            "resposta": "É o Alfi-NET."
        }, {
            "pergunta": "Onde o Renato Aragão nasceu?",
            "resposta": "Na Didi-namarca."
        }, {
            "pergunta": "Qual o país que sai pegando tudo?",
            "resposta": "Catar."
        }, {
            "pergunta": "Por que a música foi na papelaria?",
            "resposta": "Porque ela queria um clipe."
        }, {
            "pergunta": "No salão de beleza, por que o português colocou uma grade sobre a cabeça?",
            "resposta": "Porque ele queria um de-gradê."
        }, {
            "pergunta": "Qual o jogador que trata água?",
            "resposta": "Aguero."
        }, {
            "pergunta": "Qual é o jogador que não toma tiro?",
            "resposta": "Dybala."
        }, {
            "pergunta": "Qual país do caribe é uma explosão?",
            "resposta": "Granada."
        }, {
            "pergunta": "Nas obras, como fazer para a parede de tijolo ser recarregada?",
            "resposta": "É só fazer um abaste-cimento."
        }, {
            "pergunta": "Qual o ator que os operários sobem em cima dele?",
            "resposta": "Vã-Andaime."
        }, {
            "pergunta": "O que acontece se o coqueiro beber demais?",
            "resposta": "Ele chapa o coco."
        }, {
            "pergunta": "Estou acima das pessoas mais posso ficar a baixo delas, sou sólido e essencial para um lar quem eu sou?",
            "resposta": "Terraço."
        }, {
            "pergunta": "O que um jogador de futebol falou pro outro na hora de dar um pré-datado?",
            "resposta": "Eu não tenho dinheiro, mas o Peter Cheque."
        }, {
            "pergunta": "O que a ponte pequena disse para outra que cresceu?",
            "resposta": "E agora, eu te vi-adulto."
        }, {
            "pergunta": "Por que o fio sentiu frio?",
            "resposta": "Porque ele estava desencapado."
        }, {
            "pergunta": "Qual é a cerveja favorita dos cachorros?",
            "resposta": "Glaciau-au."
        }, {
            "pergunta": "Qual é o animal mais preguiçoso que existe?",
            "resposta": "A dor-minhoca."
        }, {
            "pergunta": "Qual é o movimento que as próprias pessoas que curtem muito realizam?",
            "resposta": "Fã-farra."
        }, {
            "pergunta": "Por que o energético mais conhecido do mundo agora faz propaganda de marca de informática?",
            "resposta": "Porque Red Bull te dá Asus!"
        }, {
            "pergunta": "Qual é o pão que o Ursinho Pooh mais gosta?",
            "resposta": "Pão de Mel."
        }, {
            "pergunta": "Qual é o brinquedo preferido do Thor?",
            "resposta": "AuTHORama."
        }, {
            "pergunta": "Qual o conselho que o seu pai te dava para classificar as mulheres por tipo?",
            "resposta": "Cate-gurias."
        }, {
            "pergunta": "Qual é a fruta que é também é dois animais?",
            "resposta": "Jabuti-Cabra."
        }, {
            "pergunta": "Represento o amor, mas amor não posso ter, me desenham com 2 indicadores, mas como um punho da sua mão eu posso ser, que sou eu?",
            "resposta": "O coração."
        }, {
            "pergunta": "O que o pobre tem que se o rico comer ele morre?",
            "resposta": "Nada. O pobre tem nada, e se o rico comer nada ele morre de fome."
        }, {
            "pergunta": "Qual atriz é um peixe cartilaginoso?",
            "resposta": "Claudia Arraia."
        }, {
            "pergunta": "Qual a planta dos sentimentos imediatos?",
            "resposta": "Jacinto."
        }, {
            "pergunta": "O que é que diz um ratão de 100 quilos?",
            "resposta": "Vem, vem gatinho."
        }, {
            "pergunta": "O que é que se pede com o dedo?",
            "resposta": "Ligação telefônica."
        }, {
            "pergunta": "O que é que perdido uma vez nunca mais se acha?",
            "resposta": "O tempo."
        }, {
            "pergunta": "Para que homem todos os outros tiram o chapéu?",
            "resposta": "Para o barbeiro."
        }, {
            "pergunta": "Qual a palavra que você usa quando se esquece das outras?",
            "resposta": "Sinônimos."
        }, {
            "pergunta": "O que nasce grande e morre pequeno?",
            "resposta": "O sabão."
        }, {
            "pergunta": "O que é o que é entra na igreja de cabeça para baixo?",
            "resposta": "O prego do sapato."
        }, {
            "pergunta": "Qual o jogador de basquete que trabalha como faxineiro?",
            "resposta": "Anderson Varre Chão."
        }, {
            "pergunta": "Qual banda de rock que beija todo mundo?",
            "resposta": "Kiss."
        }, {
            "pergunta": "Qual o cantor que se compara com as leis marítimas?",
            "resposta": "Bob Mar-Lei."
        }, {
            "pergunta": "Qual o aplicativo preferido do Thor?",
            "resposta": "Play sThor."
        }, {
            "pergunta": "Qual a flor que diz estar se sentindo?",
            "resposta": "Jacinto."
        }, {
            "pergunta": "Qual ator é símbolo de países?",
            "resposta": "Antônio Bandeiras."
        }, {
            "pergunta": "Qual o planeta mais admirado do supermercado?",
            "resposta": "Uau-Marte."
        }, {
            "pergunta": "Qual a batata que todos devem respeitar?",
            "resposta": "Lays."
        }, {
            "pergunta": "Qual o hipermercado preferido do número 4?",
            "resposta": "Carre-Four."
        }, {
            "pergunta": "Qual a universidade particular que quase tira um dez?",
            "resposta": "Uni-nove."
        }, {
            "pergunta": "Qual a diferença entre um limão e o Mr. Bean?",
            "resposta": "Que o limão só faz careta quando é chupado."
        }, {
            "pergunta": "Qual a cerveja que os de menores não podem beber?",
            "resposta": "Proibida."
        }, {
            "pergunta": "Qual o salgadinho que mais vai no jogo de futebol?",
            "resposta": "A Torcida."
        }, {
            "pergunta": "O que um bolo com frio disse pro outro?",
            "resposta": "Precisamos de cobertura."
        }, {
            "pergunta": "Por que o armário estava lotado?",
            "resposta": "Porque todos queriam ver o jogo de panelas."
        }, {
            "pergunta": "Por que Bob Marley é folgado?",
            "resposta": "Porque ele quer que o arrasta-fari."
        }, {
            "pergunta": "Tenho 5 maçãs, roubo de Joãozinho 5, quantas tartarugas tem no pote de doce?",
            "resposta": "Duas, pois vassoura não assiste TV a noite."
        }, {
            "pergunta": "Qual animal mais gosta de cantar em grupo?",
            "resposta": "A cobra-coral."
        }, {
            "pergunta": "Por que os padres amam açúcar?",
            "resposta": "Porque eles abraçam um sacer-doce-o."
        }, {
            "pergunta": "Qual é a comida favorito da piranha?",
            "resposta": "Pirão."
        }, {
            "pergunta": "O que uma ave perguntou pra outra sobre o futebol?",
            "resposta": "Meu time é o Flamingo, e o seu?"
        }, {
            "pergunta": "Por que um dos maiores apresentadores da Rede Globo não queria uma fazenda?",
            "resposta": "Porque ele queria apenas uma Chacrinha."
        }, {
            "pergunta": "Qual a doença que mais incomoda os gaúchos?",
            "resposta": "Artri-tchê."
        }, {
            "pergunta": "Por que Angelina não é considerada uma atriz completa?",
            "resposta": "Porque para isso, Angelina além de Jô-Li, deveria ser Jô-Escrevi também."
        }, {
            "pergunta": "Por que o ex-marido de Angelina Jolie é considerado um cara muito chato?",
            "resposta": "Porque vive o Brad dando Pití."
        }, {
            "pergunta": "Qual é o veículo de comunicação que sempre obverva você?",
            "resposta": "É a Rede Te Vê."
        }, {
            "pergunta": "Por que nos montes mais altos e frios da Suíça tem cachorros?",
            "resposta": "Porque lá estão os au-aupes."
        }, {
            "pergunta": "Qual é o legume favorito do menino de madeira que cresce o nariz?",
            "resposta": "O Pepinóquio."
        }, {
            "pergunta": "Qual a fruta que tem título de nobreza?",
            "resposta": "Fruta-do-Conde."
        }, {
            "pergunta": "Por que o português colocou a cama no guarda-roupas?",
            "resposta": "Por que o médico o pediu para guardar leito."
        }, {
            "pergunta": "O que o mineirinho pediu ao saber que no cardápio de um determinado restaurante só servia frutos do mar?",
            "resposta": "Uma banana d'água."
        }, {
            "pergunta": "Qual é o país onde as pessoas mais praticam musculação?",
            "resposta": "Só-malha."
        }, {
            "pergunta": "Qual é o animal que mais sente quando a temperatura está alta?",
            "resposta": "A Calor-psita."
        }, {
            "pergunta": "Qual animal é o melhor dos dançarinos?",
            "resposta": "O tatu-re-bola."
        }, {
            "pergunta": "Qual o celular que deixa você fazer o que quiser com ele?",
            "resposta": "Ai pode."
        }, {
            "pergunta": "Por que a roupa saiu correndo e pulou na banheira d'água?",
            "resposta": "Porque ela só levava ferro."
        }, {
            "pergunta": "Por que um homem vivia cheio de velas em sua casa?",
            "resposta": "Porque ele era fã do Caetano Veloso."
        }, {
            "pergunta": "Por que a galinha gorda estava batendo a cabeça no bebedouro elétrico?",
            "resposta": "Porque ela queria um galão."
        }, {
            "pergunta": "Qual é a profissão agente do Thor?",
            "resposta": "CorreThor."
        }, {
            "pergunta": "O que o Thor mais gosta do banheiro?",
            "resposta": "Thor-alha."
        }, {
            "pergunta": "Qual é a função de autoridade do Thor?",
            "resposta": "PromoThor."
        }, {
            "pergunta": "Qual o jogador que larga as coisas de qualquer jeito?",
            "resposta": "Se-dane."
        }, {
            "pergunta": "Por que a vaca foi pra Alemanha?",
            "resposta": "Porque ela queria ver Muuuuu-nique."
        }, {
            "pergunta": "Por que a loira joga o relógio pela janela?",
            "resposta": "Porque a hora voa."
        }, {
            "pergunta": "Por que o Médico tem a letra feia?",
            "resposta": "Porque ele não sabe escrever, só prescrever."
        }, {
            "pergunta": "O que o gato faz quando está na rua?",
            "resposta": "Engatinha."
        }, {
            "pergunta": "Por que os cães da Austrália ficam roucos?",
            "resposta": "Porque a capital do país se chama cão-berra."
        }, {
            "pergunta": "Por que os papéis e as folhas tem medo do Rio de Janeiro?",
            "resposta": "Porque eles fazem picadinho."
        }, {
            "pergunta": "Qual a ave que quer matar as vacas imediatamente em busca de seu couro?",
            "resposta": "Couro-já."
        }, {
            "pergunta": "Qual é a Lua que nunca esta com fome?",
            "resposta": "Lua cheia."
        }, {
            "pergunta": "O que tem cara de um lado e animal do outro?",
            "resposta": "As notas."
        }, {
            "pergunta": "Segunda pessoa do singular; Água passa; Qual é o nome do animal?",
            "resposta": "TUcano."
        }, {
            "pergunta": "Eu tenho um cachorro que se chama Choco. O que Choco faz?",
            "resposta": "CHOCO-late."
        }, {
            "pergunta": "Ge estava andando de bicicleta, mas ele não viu a ladeira que estava à sua frente. O que falaram para ele?",
            "resposta": "Ge-Ladeira."
        }, {
            "pergunta": "O que o tempo e a novela tem em comum?",
            "resposta": "O tempo é o Senhor da Razão, e a novela é a Senhora do Destino."
        }, {
            "pergunta": "Por que parente e igual a dente?",
            "resposta": "Porque quanto mais afastado melhor pra não juntar sujeira."
        }, {
            "pergunta": "Qual o país dos touros?",
            "resposta": "Bull-Garia."
        }, {
            "pergunta": "Qual a cantora que abre todas as portas?",
            "resposta": "Kelly Key."
        }, {
            "pergunta": "Por que os torcedores estavam com a mão na cara?",
            "resposta": "Por que os atletas iam jogar tênis."
        }, {
            "pergunta": "Por que as abelhas não comem pão de sal?",
            "resposta": "Porque elas já têm o pão de mel."
        }, {
            "pergunta": "Nas novelas, como fazer para os atores vovôs falarem mais alto?",
            "resposta": "É só apertar o vô-lume."
        }, {
            "pergunta": "Por que os camaleões mudam de cor sozinho?",
            "resposta": "Porque eles não precisam de lápis de cor."
        }, {
            "pergunta": "Qual a comida que tem um grupo de soldados prontos para guerra?",
            "resposta": "Feijão Tropeiro."
        }, {
            "pergunta": "Por que os baianos não deixam nada aberto?",
            "resposta": "Porque eles tem o vatampá."
        }, {
            "pergunta": "Qual o ator que mais gosta de flores?",
            "resposta": "Tony Ramos."
        }, {
            "pergunta": "Qual a atriz mais enxuta?",
            "resposta": "Deborah Secco."
        }, {
            "pergunta": "Qual o santo do Rodrigo?",
            "resposta": "São Toro."
        }, {
            "pergunta": "Qual enfermidade tem o técnico da seleção brasileira de futebol quando entra em um labirinto?",
            "resposta": "Labirin-Tite."
        }, {
            "pergunta": "Qual o jogador que só vive com raiva?",
            "resposta": "Bravo."
        }, {
            "pergunta": "O que todo homem faz quando está no banheiro?",
            "resposta": "Sai do banheiro."
        }, {
            "pergunta": "Por que o nadador jogou a televisão na piscina?",
            "resposta": "Para fazer um nado sintonizado."
        }, {
            "pergunta": "Por que o italiano tem que se equilibrar jogando xadrez?",
            "resposta": "Porque senão ele perde sua torre."
        }, {
            "pergunta": "Por que a cama do sabão facilmente estoura?",
            "resposta": "Porque seu colchão é de espuma."
        }, {
            "pergunta": "Qual é o eletrodoméstico preferido do Batman?",
            "resposta": "Bat-deira."
        }, {
            "pergunta": "Qual comida que quase tira um 10?",
            "resposta": "Strogo-nove."
        }, {
            "pergunta": "Qual o brinquedo preferido do McDonald's?",
            "resposta": "McSteel."
        }, {
            "pergunta": "O que a vaca foi fazer na papelaria?",
            "resposta": "Comprar uma muuuuuuuu-chila."
        }, {
            "pergunta": "Qual o material escolar que mostra a parte de seu corpo que dói?",
            "resposta": "Aponta-dor."
        }, {
            "pergunta": "Qual a rede social mais gorda?",
            "resposta": "InstaGrama."
        }, {
            "pergunta": "Qual é o tipo de festa que os cegos frequentam?",
            "resposta": "O braille funk."
        }, {
            "pergunta": "Por que no Rio de Janeiro as pessoas não comem pão de sal?",
            "resposta": "Porque eles têm o Pão de Açúcar."
        }, {
            "pergunta": "Qual super herói tira foto no escuro?",
            "resposta": "Flash."
        }, {
            "pergunta": "Quando está apaixonado, como um sabão em pó se declara?",
            "resposta": "Eu te OMO."
        }, {
            "pergunta": "O que a mãe açaí disse para os outros açaís?",
            "resposta": "O último açaí feche a porta."
        }, {
            "pergunta": "Qual é o carro que gosta de fazer exercícios?",
            "resposta": "Cooper."
        }, {
            "pergunta": "Por que o pai do Thor é um ser pré-histórico?",
            "resposta": "Porque ele é Odinossauro."
        }, {
            "pergunta": "O que o Batman faz com o celular?",
            "resposta": "Bat-Selfie."
        }, {
            "pergunta": "Qual o contrário de futsal?",
            "resposta": "Fut-açúcar."
        }, {
            "pergunta": "Como seria o nome chinês do preguiçoso?",
            "resposta": "Kan-sei ou kochi-lin."
        }, {
            "pergunta": "Por que o relógio é popular?",
            "resposta": "Porque ele é da hora."
        }, {
            "pergunta": "Por que a piada da bola é a melhor?",
            "resposta": "Porque ela é bem bolada."
        }, {
            "pergunta": "Qual é o traficante que toma uma gelada no boteco?",
            "resposta": "Pablo Skol Bar."
        }, {
            "pergunta": "O que tem 5 cordas e uma cova?",
            "resposta": "Violão."
        }, {
            "pergunta": "Qual o santo da Ivete?",
            "resposta": "São Galo."
        }, {
            "pergunta": "Qual é o chocolate dos gatos?",
            "resposta": "Kit-Cat."
        }, {
            "pergunta": "Qual o esporte preferido dos gaúchos?",
            "resposta": "Basquetchê."
        }, {
            "pergunta": "Quem é o rei da farmácia?",
            "resposta": "Rei-médio."
        }, {
            "pergunta": "Qual o contrário de buscapé",
            "resposta": "Levamão."
        }, {
            "pergunta": "Qual o carro mais amado da Julieta?",
            "resposta": "Alfa-Romeu."
        }, {
            "pergunta": "Qual a cerveja preferida dos mineiros?",
            "resposta": "Bud-Uai-Zé."
        }, {
            "pergunta": "Por que a Holanda não cresce?",
            "resposta": "Porque ela é um País-Baixo."
        }, {
            "pergunta": "Qual o contrário de cachorro-quente?",
            "resposta": "Cadela fria."
        }, {
            "pergunta": "Por que o frango atravessou a rua?",
            "resposta": "Porque era dia de folga da galinha."
        }, {
            "pergunta": "Por que o Thor é rico?",
            "resposta": "Porque ele tem O-din-din."
        }, {
            "pergunta": "O que é o quê é e branco não é líquido e serve pra bebê?",
            "resposta": "Fralda."
        }, {
            "pergunta": "Qual é o veículo que lava roupas?",
            "resposta": "Tanque."
        }, {
            "pergunta": "Qual é a área de ensinamentos do Thor?",
            "resposta": "Or-THOR-grafia."
        }, {
            "pergunta": "O que o Thor mais gosta de contar?",
            "resposta": "His-THOR-ia."
        }, {
            "pergunta": "Qual é o veículo mais sacana?",
            "resposta": "Velo-troll."
        }, {
            "pergunta": "O que é um grande prédio com apenas uma janela?",
            "resposta": "Agulha."
        }, {
            "pergunta": "O que é que é que no interior é uma linda praia e fora um mato?",
            "resposta": "Coco."
        }, {
            "pergunta": "Qual é a parte mais feminina da casa?",
            "resposta": "JanELA."
        }, {
            "pergunta": "Por que o Batman é tão ruim nos jogos de carta?",
            "resposta": "Porque ele só pega coringa."
        }, {
            "pergunta": "Qual é o contrário de contramão?",
            "resposta": "Favorpé."
        }, {
            "pergunta": "Qual é o barco que sempre está aceso no escuro?",
            "resposta": "Barco a vela."
        }, {
            "pergunta": "Qual o contrário de papelada?",
            "resposta": "Pá vestida."
        }, {
            "pergunta": "Qual a ave que é marca de bicicleta?",
            "resposta": "Caloi-picita."
        }, {
            "pergunta": "Qual é o alimento mais sagrado do mundo?",
            "resposta": "Amén-doim."
        }, {
            "pergunta": "Como o Thor se comunica com os outros Vingadores?",
            "resposta": "Por Thor-pedo."
        }, {
            "pergunta": "Qual a parte mais sonora do corpo?",
            "resposta": "Rádio."
        }, {
            "pergunta": "Qual e o esporte mais salgado?",
            "resposta": "Fut-sal."
        }, {
            "pergunta": "Por que o vaso é o melhor presente para se ganhar?",
            "resposta": "Porque ele é de-coração!"
        }, {
            "pergunta": "O que o coelho disse quando se assustou?",
            "resposta": "Ah, minha nossa cenoura!"
        }, {
            "pergunta": "Qual é o hidrocarboneto da raiva?",
            "resposta": "Bicarbonato de ódio."
        }, {
            "pergunta": "Por que o macaco tem medo de martelo?",
            "resposta": "Porque ele é um macaco-prego."
        }, {
            "pergunta": "Por que o jogador não estava conseguindo ligar do campo?",
            "resposta": "Porque ele estava fora de área."
        }, {
            "pergunta": "Qual o maior órgão público de uma cidade?",
            "resposta": "Orelhão."
        }, {
            "pergunta": "O que o astronauta foi fazer no teclado?",
            "resposta": "Andar no espaço."
        }, {
            "pergunta": "Quais são os bandidos mais horríveis que existem?",
            "resposta": "Os ma-feiosos."
        }, {
            "pergunta": "Qual carro está sempre ligado?",
            "resposta": "On-ix."
        }, {
            "pergunta": "Por que um caminhoneiro nunca consegue pegar uma garota no deserto?",
            "resposta": "Porque é muita areia pro seu caminhão."
        }, {
            "pergunta": "Por que a chuva sempre cai sem nos avisar?",
            "resposta": "Porque ela é precipitada."
        }, {
            "pergunta": "O que é o que é que depois de ficar muito tempo na geladeira continua quente?",
            "resposta": "Pimenta."
        }, {
            "pergunta": "João tinha nove carrinhos, emprestou quatro para o Arthur. Com quantos carrinhos João ficou?",
            "resposta": "Continuou com nove, pois ele emprestou, ele não deu."
        }, {
            "pergunta": "O que é o que quando bate na pedra não quebra e quando cai na água se parte?",
            "resposta": "O papel."
        }, {
            "pergunta": "Qual é o tipo de bebida preferida dos animais?",
            "resposta": "As de garrafa PET."
        }, {
            "pergunta": "Qual é o prato preferido dos mecânicos?",
            "resposta": "Macarrão parafuso."
        }, {
            "pergunta": "Qual é a prisão, onde todos nós estamos condenados a passar?",
            "resposta": "Prisão de ventre."
        }, {
            "pergunta": "Um homem lá vinha com uma carroça, e na carroça tinha um burro, um capim e uma onça. A ponte estava quase quebrando, e ele tinha que atravessar uma coisa de cada vez, e sem deixar um comer ao outro. Que processo ele iria fazer?",
            "resposta": "Ele leva o burro e deixa ele lá, volta e busca a onça, traz o burro de volta e leva o capim, depois leva o burro de novo."
        }, {
            "pergunta": "Qual é a fruta preferida do Thor?",
            "resposta": "THORanja."
        }, {
            "pergunta": "Qual é o animal de estimação do Thor?",
            "resposta": "THOR-upeira."
        }, {
            "pergunta": "Qual é a comida mais devagar?",
            "resposta": "A po-lenta."
        }, {
            "pergunta": "Por que a menina doente foi pra a academia?",
            "resposta": "Pra ficar sarada."
        }, {
            "pergunta": "Com qual gênero a matemática combina?",
            "resposta": "Mulheres, pois são difíceis."
        }, {
            "pergunta": "O que o milho disse para a pipoca?",
            "resposta": "HuMILHO mesmo."
        }, {
            "pergunta": "Qual é o doce preferido do Thor?",
            "resposta": "Thorrone."
        }, {
            "pergunta": "Qual é o prato preferido do Thor?",
            "resposta": "Thorresmo."
        }, {
            "pergunta": "O que o Thor faz quando corta o dedo?",
            "resposta": "Thorniquete."
        }, {
            "pergunta": "O que acontece se o Thor assoprar?",
            "resposta": "THORnado."
        }, {
            "pergunta": "Quantas pata tem uma pata?",
            "resposta": "Somente uma, se fosse mais seria patapatapatapata..."
        }, {
            "pergunta": "Qual é a semelhança entre aranha e escorpião?",
            "resposta": "Com nenhum dos dois dá pra fazer bolo de abacate."
        }, {
            "pergunta": "Meu avô tem 4 filhos, cada filho tem 4 filhos. Quantos primos eu tenho?",
            "resposta": "12. Três são meus irmãos e um sou eu."
        }, {
            "pergunta": "Ela tinha 4 filhos. Janeiro, Fevereiro, Março. Qual é o nome do quarto filho.",
            "resposta": "O nome da criança e 'Qual'."
        }, {
            "pergunta": "Qual o esporte que os cientistas gostam?",
            "resposta": "Fórmula 1."
        }, {
            "pergunta": "Qual a profissão histórica do Thor?",
            "resposta": "His-THOR-iógrafo."
        }, {
            "pergunta": "Qual a catástrofe que o Thor tem medo?",
            "resposta": "TerremoTHOR."
        }, {
            "pergunta": "O que o gato faz quando está na rua?",
            "resposta": "Engata."
        }, {
            "pergunta": "Qual é a profissão do Thor?",
            "resposta": "Mo-THOR-ista."
        }, {
            "pergunta": "Qual a especialização do Thor?",
            "resposta": "PaTHORlogia."
        }, {
            "pergunta": "Qual a profissão secreta do Thor?",
            "resposta": "InspeThor."
        }, {
            "pergunta": "Qual é o frango que está sempre na mesa?",
            "resposta": "O frango alinamesa."
        }, {
            "pergunta": "Qual é a profissão do Thor?",
            "resposta": "Thoreiro."
        }, {
            "pergunta": "Qual o pão que o Thor mais come?",
            "resposta": "O THORrado."
        }, {
            "pergunta": "No carro estavam 1 avó, 2 pais, 2 filhos e 1 neto. Quantas pessoas estavam no carro?",
            "resposta": "3 pessoas."
        }, {
            "pergunta": "O que é surdo e mudo mas conta tudo?",
            "resposta": "Livro."
        }, {
            "pergunta": "Por que a fração não cabe em uma casa?",
            "resposta": "Por que ela tem 4 quarto."
        }, {
            "pergunta": "Qual a parte do corpo que Thor mais gosta?",
            "resposta": "Thornozelo."
        }, {
            "pergunta": "O que o zero disse para o seis?",
            "resposta": "Nossa, apertou tanto o cinto que abriu a boca."
        }, {
            "pergunta": "Qual e o animal que mais gosta de jogar futebol?",
            "resposta": "GOLfinho."
        }, {
            "pergunta": "Qual é o carro que só anda bem vestido?",
            "resposta": "Blazer."
        }, {
            "pergunta": "Por que guarda de trânsito é o ser mais forte do mundo?",
            "resposta": "Porque ele pode parar carros só com uma das mãos."
        }, {
            "pergunta": "Qual é o fenômeno que acontece no mar que o Thor tem medo?",
            "resposta": "Thormenta."
        }, {
            "pergunta": "Qual é o animal que mais gosta de jogar futebol?",
            "resposta": "O goooooooooolfinho."
        }, {
            "pergunta": "Tinha um pontinho verde no Xbox, qual é o nome do jogo?",
            "resposta": "Assassins GreenD."
        }, {
            "pergunta": "Por que não podemos levar cães pros Estados Unidos?",
            "resposta": "Porque lá fura-cão."
        }, {
            "pergunta": "Qual é o país feminino?",
            "resposta": "VenezuELA."
        }, {
            "pergunta": "Qual a meditação que se faz acordado?",
            "resposta": "ONnnn..."
        }, {
            "pergunta": "O que a legume é do filho do filho dela?",
            "resposta": "Avóbora."
        }, {
            "pergunta": "O que o zero dise para o oito?",
            "resposta": "Nossa, que cinto apertado!"
        }, {
            "pergunta": "O que passa por todas as casas mas não sai do lugar?",
            "resposta": "A rua."
        }, {
            "pergunta": "Cinco políticos estavam em uma lancha que acabou virando no meio do mar. Você sabe como salvá-los?",
            "resposta": "Não? Perfeito!"
        }, {
            "pergunta": "Qual é o bicho que anda com as patas?",
            "resposta": "O pato."
        }, {
            "pergunta": "O que o Thor gosta de ser no tempo livre?",
            "resposta": "Fo-THOR-grafo."
        }, {
            "pergunta": "Por que as mulheres não sentem frio?",
            "resposta": "Porque elas estão cobertas de razão."
        }, {
            "pergunta": "Por que em Minas Gerais não tem mar?",
            "resposta": "Porque lá eles rezam livrai-nos de todos os mar."
        }, {
            "pergunta": "Qual o animal que a gordinha não quer encontrar de jeito nenhum quando fica magra?",
            "resposta": "O ex-quilo."
        }, {
            "pergunta": "Quem é a mãe da cozinha?",
            "resposta": "A mãezena."
        }, {
            "pergunta": "O que o Thor usa nos pés para não se machucar enquanto corre?",
            "resposta": "Thor-nozeleiras."
        }, {
            "pergunta": "Qual o doce favorito do Thor?",
            "resposta": "Thortuguita."
        }, {
            "pergunta": "Do que o Thor faz parte?",
            "resposta": "Da Thorcida."
        }, {
            "pergunta": "O que Michael Phelps disse para Sócrates?",
            "resposta": "Só sei que nadar sei."
        }, {
            "pergunta": "O que o Batman mais sente no peito?",
            "resposta": "Bat-mentos."
        }, {
            "pergunta": "Por que  o filho do joalheiro estuda tanto?",
            "resposta": "Pra ser um adulto joia."
        }, {
            "pergunta": "Por que o surfista não gosta da cozinha?",
            "resposta": "Porque lá só tem micro-ondas."
        }, {
            "pergunta": "Qual é o time preferido do Thor?",
            "resposta": "Thorino."
        }, {
            "pergunta": "Qual é a cidade preferida do Thor?",
            "resposta": "Thoronto."
        }, {
            "pergunta": "Qual é a parte do quarto que o Thor mais gosta?",
            "resposta": "Thormada."
        }, {
            "pergunta": "O que acontece se colocarmos sal em um boi bem pequeno?",
            "resposta": "Vira um sal-gadinho."
        }, {
            "pergunta": "O que até o mais pobre de todos tem?",
            "resposta": "Nome."
        }, {
            "pergunta": "Quantas sílaba tem a palavra Trissílaba?",
            "resposta": "Uma, se fosse mais seria Trissílabasílabasílaba..."
        }, {
            "pergunta": "O que para ser direito tem que ser torto?",
            "resposta": "Anzol."
        }, {
            "pergunta": "Qual o remédio que contém álcool e gasolina?",
            "resposta": "Dorflex."
        }, {
            "pergunta": "Qual é o animal favorito dos pintores?",
            "resposta": "Onça pintada."
        }, {
            "pergunta": "Qual a especialidade de Thor?",
            "resposta": "OrTHORpedista."
        }, {
            "pergunta": "Qual o tênis quer ser uma majestade?",
            "resposta": "Rainha."
        }, {
            "pergunta": "Qual é o corte de cabelo preferido do Thor?",
            "resposta": "THORpete."
        }, {
            "pergunta": "Qual a semelhança de um sapo e uma vassoura?",
            "resposta": "Com nenhum dos dois dá pra fazer pastel."
        }, {
            "pergunta": "Qual a Profissão preferida do Thor?",
            "resposta": "THORpógrafo."
        }, {
            "pergunta": "Qual é a luta dos Gaúchos?",
            "resposta": "KaraTCHÊ."
        }, {
            "pergunta": "Qual é o carro movido a suco?",
            "resposta": "MusTANG"
        }, {
            "pergunta": "Qual é a roupa preferido do macaco?",
            "resposta": "Macacão."
        }, {
            "pergunta": "Qual é o fenômeno da Natureza que o Thor tem medo?",
            "resposta": "Thornado."
        }, {
            "pergunta": "Qual a cidade do Thor?",
            "resposta": "Thórquio."
        }, {
            "pergunta": "Tenho 40 laranjas, tiro 20. Quantas laranjas eu tenho?",
            "resposta": "Eu sabia isso com maçãs."
        }, {
            "pergunta": "Qual a cantora que mais gosta de rir?",
            "resposta": "Ri-hanna."
        }, {
            "pergunta": "Qual a parte do corpo do Thor que ele mais gosta?",
            "resposta": "THORax."
        }, {
            "pergunta": "Qual a cantora gosta muito de tomar chá?",
            "resposta": "Chá-quira."
        }, {
            "pergunta": "Tenho cinco laranjas, João roubou três. Quantas laranjas eu tenho?",
            "resposta": "Cinco."
        }, {
            "pergunta": "Qual é a semelhança de uma dentadura e um chifre?",
            "resposta": "Ambos machucam mas acostumam."
        }, {
            "pergunta": "Qual é o fruto preferido do Thor?",
            "resposta": "Thormate."
        }, {
            "pergunta": "Qual é a atriz preferida do tamanduá?",
            "resposta": "Vera Farmiga"
        }, {
            "pergunta": "Qual o time o Thor torce?",
            "resposta": "Thorttenham."
        }, {
            "pergunta": "Quando foi a primeira vez que os povos da América comeram carne?",
            "resposta": "Quando chegou Cristóvão Com-lombo."
        }, {
            "pergunta": "Qual é o carro está sempre chateado?",
            "resposta": "Bravo."
        }, {
            "pergunta": "Por que na floresta tem sal?",
            "resposta": "Porque ela é temperada."
        }, {
            "pergunta": "O que o Mickey foi fazer no espaço?",
            "resposta": "Procurar o pai do seu cachorro, o Plutão."
        }, {
            "pergunta": "Por que a loira tomou o remédio antes da hora certa?",
            "resposta": "Pra pegar a doença de surpresa!"
        }, {
            "pergunta": "Qual é a parte do banheiro que o Thor mais gosta?",
            "resposta": "Da Thorneira."
        }, {
            "pergunta": "Qual é a cidade preferida do tamanduá?",
            "resposta": "Formiga."
        }, {
            "pergunta": "Qual é o país preferido no Natal?",
            "resposta": "Peru."
        }, {
            "pergunta": "Qual é a tinta que quer ser uma cobra?",
            "resposta": "Coral."
        }, {
            "pergunta": "Qual é a cidade preferida do Thor?",
            "resposta": "Thórquio."
        }, {
            "pergunta": "O que o pastel falou para o outro pastel?",
            "resposta": "Estamos fritos."
        }, {
            "pergunta": "Hoje não tenho valor, mas já vali muito. O que sou?",
            "resposta": "História."
        }, {
            "pergunta": "O que nasce uma vez, nasce duas vezes, mas na terceira não nasce mais?",
            "resposta": "Dente."
        }, {
            "pergunta": "Em qual estado brasileiro as pessoas mais gostam de tomar suco?",
            "resposta": "Rio Grande do Suco."
        }, {
            "pergunta": "O que o aluno fala para a professora e gosta de receber dos pais?",
            "resposta": "Presente."
        }, {
            "pergunta": "O que acontece se um ciclista entrar em campo?",
            "resposta": "Ele faz um gol de bicicleta."
        }, {
            "pergunta": "Qual é o estado preferido do Thor?",
            "resposta": "THORcantins."
        }, {
            "pergunta": "Nunca para frente, sempre para trás, para crianças sou muito devagar, para adultos fui rápido demais. O que sou?",
            "resposta": "Infância."
        }, {
            "pergunta": "Nos vire ao avesso, e abra nossas vísceras, você será o mais sábio dos homens, mas, sem nós, será um idiota. O que sou?",
            "resposta": "Livro."
        }, {
            "pergunta": "De mim, surge vida, para mim, a vida retorna. Homens brigam pela minha posse, mas nenhum deles é meu dono. Água me cerca, mas ao redor dela eu vivo. Quem sou eu, meu amigo?",
            "resposta": "Terra."
        }, {
            "pergunta": "Assisti ao nascimento de reis e rainhas, meus pés vão mais fundo e minha cabeça mais alto do que tudo que o homem cria. Muitos buscam algo no interior do meu coração, mas, amor, não é algo que encontrarão, como vocês me chamarão?",
            "resposta": "Montanha."
        }, {
            "pergunta": "Por que os robôs nao sentem medo?",
            "resposta": "Porque eles têm nervos de aço."
        }, {
            "pergunta": "Qual é estado que gosta de cavar buracos?",
            "resposta": "Ama-pá."
        }
    ]

    def initialize(self):
        self.register_fallback(self.handle_pun_fallback, 99)

    def translate_to_portuguese(self, text):
        translated = translate(text, "pt")
        self.speak_portuguese(translated)

    def speak_portuguese(self, sentence):
        wait_while_speaking()
        get_sentence = 'wget -q -U Mozilla -O ' + self.path_translated_file + \
                       '"https://translate.google.com/translate_tts?ie=UTF-8&tl=pt&q=' + \
                       str(sentence) + '&client=tw-ob' + '"'

        os.system(get_sentence)
        play_mp3(self.path_translated_file)
        self.set_context("previous_speech", sentence)
        self.set_context("google_tx")

    @intent_file_handler("hello_in_portuguese.intent")
    def handle_hello(self, message):
        self.speak_dialog("hello_in_portuguese", wait=True)
        self.speak_portuguese("olá")

    @intent_handler(IntentBuilder("ThankYouIntent").require("ThankYou")
                    .require("inPortuguese").optionally("gender"))
    def handle_thank_you(self, message):
        gender = message.data.get("gender")
        if not gender:
            self.speak_dialog("if_male", wait=True)
            self.speak_portuguese("obrigado")
        elif gender == "male":
            self.speak_portuguese("obrigado")
        elif gender == "female":
            self.speak_portuguese("obrigada")

    @intent_file_handler("say.intent")
    def handle_say(self, message):
        words = message.data["words"]
        self.translate_to_portuguese(words)

    @intent_handler(IntentBuilder("RepeatIntent")
                    .require("repeat")
                    .require("previous_speech"))
    def handle_repeat(self, message):
        text = message.data.get("previous_speech")
        self.speak_portuguese(text)

    @intent_handler(IntentBuilder("HowDoYouKnowIntent")
                    .require("question").require("know")
                    .require("google_tx"))
    def handle_how_do_you_know(self, message):
        self.speak_dialog("google")

    @intent_handler(IntentBuilder("ExplainInPortugueseIntent")
                    .require("SampleWord").require("inPortuguese"))
    def handle_explain(self, message):
        word = message.data["SampleWord"]
        dictionary = PyDictionary()
        dictionary.meaning(word)
        meaning = dictionary.get("Noun") or dictionary.get("Verb")
        self.translate_to_portuguese(meaning)

    @intent_handler(IntentBuilder("NumberInPortugueseIntent")
                    .require("inPortuguese").require("number").require("say"))
    def handle_number(self, message):
        text = message.utterance_remainder()
        # lets get a number from the utterance
        number = extract_number(text, lang=self.lang)
        # portuguese uses long scale, lets take that into account!
        # in long scale 1 billion = 1e12 instead of 1e9
        spoken_number = pronounce_number(number, short_scale=False)
        self.translate_to_portuguese(spoken_number)

    @intent_handler(IntentBuilder("DateInPortugueseIntent")
                    .require("inPortuguese").require("date").require("say"))
    def handle_date(self, message):
        date, text_remainder = extract_datetime(message.data["utterance"], lang=self.lang)
        pronounced_date = nice_date(date)
        self.translate_to_portuguese(pronounced_date)

    @intent_file_handler("live_translate_portuguese.intent")
    def handle_live_translate(self, message):
        self.speak_dialog("start_tx", wait=True)
        self.speak_portuguese("iniciando tradução automática")
        self.intercepting = True

    def stop(self):
        if self.intercepting:
            self.speak_dialog("stop_tx", wait=True)
            self.speak_portuguese("parando tradução automática")
            self.intercepting = False

    def converse(self, transcript, lang="en-us"):
        utterance = transcript[0]
        if self.intercepting:
            if self.voc_match(self, utterance, "cancel", lang=lang):
                self.stop()
            else:
                self.translate_to_portuguese(utterance)
            return True
        return False

    def handle_pun_fallback(self, utterance):
        if self.voc_match(self, utterance, "pt_pun"):
            pun = random.choice(self.puns)
            question = pun["pergunta"]
            answer = pun["resposta"]
            self.speak_portuguese(question + ".\n" + answer)
            return True
        return False


def create_skill():
    return LearnPortugueseSkill()
