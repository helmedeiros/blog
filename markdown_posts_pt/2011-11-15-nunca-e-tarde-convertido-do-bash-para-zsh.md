---
title: "Nunca é tarde! Convertido do Bash para ZSH!"
date: 2011-11-15
slug: nunca-e-tarde-convertido-do-bash-para-zsh
draft: false
language: pt
---

Após um bom tempo utilizando o zsh, apresentei recentemente a um amigo que se surpreendeu, após conversarmos um pouco surgiu a idéia de aprender um pouco mais, e compartilhar…. Fui influenciado há certo tempo pela onda oh-my-zsh, mas acabei por não contribuir em nada. Quem sabe agora?!?!
Começando do inicio, acredito que a maior parte de nós em algum momento já se deparou com um shell de linha de comandos.O shell como é mais utilizado é uma interface textual para as funcionalidades do sistema operacional, no MacOS você o acessa por meio do Terminal ou iTerm2. Existem muitos shells a serem escolhidas, e a maioria dos sistemas operacionais/distribuições acabam “facilitando” esta escolha definindo alguma padrão. Durante muito tempo só conhecia o mais popular deles GNU Bourne Again Shell ou bash, uma excelente escolha quando você precisa repetir os mesmos comandos que já estão no histórico, para iniciar algum container ou ver logs… mas uma péssima, quando você passa certo tempo usando Git e RVM (
1
para lembrar o branch que estou e
1
para ver a versão do ruby e gems) ou aprendendo comandos novos e utilizando novas técnicas do universo devops (fiz recentemente o curso da egenial de imersão sys deploy).
## zsh?

O Z-shell ou zsh é um dos shells mais completos em termos de funcionalidades e usabilidade dentre os disponíveis no Darwin que traz como default o tsch desde a v.7.0 presente no Mac Os X Panther. A equipe do zsh já faz um excelente trabalho explicando e e advogando ao seu respeito, mas como todos tenho meus pontos preferidos.
1. Corretor ortográfico : Quem nunca escreveu _rmv, fnd, mkdr _ou qualquer outro comando incorretamente? O zsh possui um corretor que varre e apresenta entre comandos e sub-comandos o mais próximo ao incorreto informado. Estava errado me corrija?

zsh: correct ‘rmv’ to ‘rvm’ [nyae]?
1. Tab completion: A maior parte dos shells como o bash possuem tab completion, mas não tão simples ou amigável quanto o zsh. Tanto no sentido de configuração quanto de usabilidade, o zsh dá um banho. Ele apresenta em um menu navegável de sub-comandos e opções de preenchimento como a lista de diretórios quando executamos um ls, ou a lista de processos quando executamos um kill.
2. Compartilhamento de histórico: Manter histórico entre as sessões ao invés de sobrepor-las, não tem nada pior do que perder o histórico de comandos executados pois uma sessão havia sido sobreposta, o zsh mantem o histórico das várias sessões.
3. Globbing. O zsh se preocupou muito com seus wildcards, e o resultados foram incríveis _ls git*~flow _ou ls (GOL|TAM)POA , sempre dou uma olhada na introdução do zsh.
4. Criar funções com aliases. O zsh permite a criação de funções chamadas pelos seus aliases, de forma fácil e ágil.

1
- __
- __
- __
- __
- __
- __