# Blog Style Guide — PT-BR (a minha voz)

Companion to [`STYLE_GUIDE.md`](STYLE_GUIDE.md).

Este guia descreve a voz em que eu escrevo em **português brasileiro
(PT-BR)** neste blog. Eu não escrevo nem falo em português de
Portugal — quando este guia diz "português", o assunto é sempre PT-BR.

Não é um guia de tradução. Não é um guia de "como adaptar um post EN".
É um guia sobre **quem eu sou no texto** — pra que qualquer pessoa
revisando, escrevendo comigo, ou usando uma ferramenta no meu lugar
consiga manter a mesma voz sem precisar adivinhar.

## Quem eu sou

Nasci em Brasília, Distrito Federal, mas me mudei pra Natal, Rio
Grande do Norte, com cinco anos. Cresci em Natal e passei lá toda a
infância e juventude antes de sair pra trabalhar. A maior parte da
minha carreira como engenheiro de software e como gestor aconteceu
fora — primeiro em Porto Alegre, Rio Grande do Sul, depois fora do
Brasil.

Essas camadas — o potiguar de criação, o tempo em Porto Alegre, os
anos fora — moldam como eu escrevo em português. Nenhuma delas
sumiu, nenhuma delas domina. A voz é o que sobra quando elas se
encostam.

## A voz numa frase

Um engenheiro brasileiro de Natal, com anos de carreira em Porto
Alegre e fora do Brasil, escrevendo em PT-BR pra outros engenheiros
brasileiros — informal mas profissional, claro porque precisou ser
claro pra gente de fora, leve porque é Natal.

## O que eu naturalmente uso

- **`a gente`** quase sempre. `nós` aparece raríssimo, em frase com
  peso extra.
- **`pra`** sempre. `para` só em contexto formal real.
- **`tá` / `tava` / `tô`** quando o tom pede. Em parágrafo mais
  reflexivo, `está / estava / estou` voltam.
- **Sujeito implícito** quando o contexto deixa: "Roda. O teste passa.
  Sobe na sexta."
- **Primeira pessoa**: `eu` pra experiência pessoal, `a gente` pro
  trabalho de time.
- **Frases que variam de tamanho**: curta declarativa + média
  reflexiva + curta de fechamento. É um ritmo, não uma regra.
- **Code-switching pra termos técnicos**: `deploy`, `rollback`,
  `shadow mode`, `feature flag`, `wrapper`, `snapshot`, `fixture`,
  `seed`, `runner`, `sink`, `markup`, `fee`, `add-on`, `lead time` —
  ficam em inglês. É como a gente conversa no trabalho.
- **Anglicismos verbais** que o dev brasileiro usa: `shippei`,
  `deployei`, `buildou`, `mockou`, `replayar`, `parsei`, `rebootou`.
  Quando aparecem, ficam — é a lingua franca.
- **Calor leve do nordeste**: "caiu a ficha", "a sacada é",
  "rapidinho", "sobe (em produção)", "botar". Aparece quando o assunto
  é prático ou quando a frase quer um pulso a mais.
- **Clareza ganha do sul**: depois de anos escrevendo pra time
  distribuído primeiro em Porto Alegre e depois fora do país, eu tendo
  a fechar parágrafo numa frase que carrega a conclusão sozinha. É um
  hábito que peguei trabalhando com pessoas que iam ler o texto sem
  contexto.

## O que eu não uso

- **Português de Portugal (PT-PT)**. Eu não escrevo em PT-PT, ponto.
  `tu` como sujeito, `vós`, `deveras`, `outrora`, `todavia`,
  `destarte`, mesóclise ("dir-te-ei"), pretérito-mais-que-perfeito
  sintético ("falara") — nada disso. Se uma palavra ou construção é
  claramente lusitana, não vai num post meu.
- **Gíria nordestina pesada que precisa de tradução**. `vixe`, `eita`,
  `macho`, `caba`, `mainha` — não escrevo assim por hábito. Saí de
  Natal cedo demais na carreira pra esse registro virar minha voz
  escrita, e os leitores em SP, RJ, PoA, e fora do Brasil acompanham
  melhor sem.
- **Português formal cartorial**. `permite`, `devemos`, `é
  necessário`, `possuir`, `realizar` (no sentido de fazer), `efetuar`,
  `proceder com` — soa rígido pro tom do blog. Quando o sentido cabe,
  uso `deixa`, `precisa`, `tem que`, `ter`, `fazer`.
- **Tradução literal do inglês**. Eu penso em inglês uma parte do dia
  por causa do trabalho, mas o que sai em português tem que soar como
  português escrito por uma pessoa, não como inglês com palavras em
  português.

## Vocabulário técnico — o que fica em inglês

| Fica em inglês | Tem versão em português que uso |
|---|---|
| `deploy`, `rollback`, `shadow`, `replay`, `runner`, `sink` | regra, motor, ciclo de vida |
| `feature flag`, `wrapper`, `snapshot`, `fixture`, `seed`, `bucket` | fronteira, explicação |
| `markup`, `fee`, `add-on`, `lead time` | preço, taxa (quando o contexto é o produto, não o sistema) |
| Nome de variável, função, tipo, struct, campo | modelo de regra (em prosa, não em código) |

A decisão é por consistência dentro do post: se um termo apareceu em
inglês na primeira menção, fica em inglês até o fim.

## Como eu escrevo um parágrafo

Eu começo com uma frase curta que coloca o leitor numa cena ou numa
afirmação. A segunda frase amplia ou contradiz. A terceira fecha. Em
posts mais longos, esse ritmo se repete; em posts mais densos, eu
abro a estrutura com lista ou tabela em vez de prosa.

Hook de abertura é quase sempre concreto — uma cena, um número, uma
fala, uma decisão específica — em vez de uma framing abstrata.
Aprendi isso de tanto reler post meu que não tinha hook e perceber
que eu mesmo não voltaria pra ler.

## Concordância — onde eu tropeço naturalmente

`a gente` é singular feminino na concordância. Adjetivo e particípio
têm que casar:

- "A gente tava **travada** por práticas manuais." ✅
- "A gente tava **travado** por práticas manuais." ❌

Substantivo feminino que aparece muito em texto técnico meu:
`mutação`, `regra`, `decisão`, `restrição`, `fronteira`, `camada`,
`política`, `suíte`. Adjetivo e particípio acompanham.

## Sobre traduzir post EN pro PT-BR

Quando uma versão em PT-BR nasce de uma versão em inglês, **as duas
não precisam ficar espelhadas**. O PT-BR flui no próprio ritmo. Se
uma frase em inglês tem três orações encaixadas e o PT-BR pede pra
quebrar em duas frases, quebra. Se um parágrafo em inglês abre com
uma framing abstrata e o PT-BR pede pra começar pela cena, começa
pela cena.

O leitor brasileiro não precisa de uma tradução fiel. Precisa de um
post bem escrito em PT-BR que diz a mesma coisa.

## A pergunta que eu faço quando tô em dúvida

Eu leio a frase em voz alta. Se soa como algo que eu falaria
explicando o sistema pro colega brasileiro no café — ou no Slack,
depois de uma reunião — tá certo. Se soa como livro didático, como
tradução, ou como correspondente lusitano, eu reescrevo.

O alvo é **PT-BR escrito com cuidado**, não "traduzido bem do
inglês" e não "português genérico". São coisas diferentes.
