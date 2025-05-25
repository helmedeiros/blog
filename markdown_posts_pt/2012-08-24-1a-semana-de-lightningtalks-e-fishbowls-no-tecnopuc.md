---
title: "1ª Semana de LightningTalks e FishBowls no TecnoPUC"
date: 2012-08-24
slug: 1a-semana-de-lightningtalks-e-fishbowls-no-tecnopuc
draft: false
language: pt
---

Aconteceu há algumas horas o 4º dia da 1ª Semana de LightningTalks e FishBowls no TecnoPUC onde apresentei a Lightning Talk Test Driven Development – Em busca de feedback útil e concreto, que abordava o conceito de feedback validado na construção de software.
Muito se tem falado por equipes e comunidades por onde transito sobre testes e QA, mas aparentemente muitas delas ainda estão correndo e lutando as mesmas batalhas todos os dias. Quando digo as mesmas, não falo a alto nível como falta de especificação dos critérios de aceitação ou negligenciar completamente a opinião final do usuário, e sim de bugs nos softwares, tipo a empresa X no produto Y já entregou 3 versões este ano com o “botão de enviar” totalmente invisível ao cliente. Como podemos ainda cometer estes tipos de erro? Lembram aquele velho ditado fazer errado uma vez, tudo bem! Mas cometer o mesmo erro …
Muitas empresas tem se mantido congelados na estratégia inicial de cenários de teste, onde os mesmos funcionam como checklists intermináveis de ações que devem ser repetidas sempre que uma versão for ser lançada, e cada erro encontrado aparentemente está sendo adicionado neste documento. Ótimo para um primeiro passo, mas a anos-luz de iniciarmos a arranhar a superfície da eficiência. Aqui não se trata de por quanto tempo iremos nos lembrar de executar, por que a falha acontecerá e será evidente na única vez que você esquece-lo. Planos são ótimos pontos de partida, mas você deve estar pronto para evoluí-lo a qualquer custo.
> Todos tem um plano, até serem socados na cara-Mike Tyson

É muito difícil seguir um script com perfeição quando se tem tanto a perder, ou a impactar ao mínimo erro. Neste ponto que stress e execução dos testes entram no que foi definido como relações diretas de influência, de forma que quanto maior o stress, menor atenção e qualidade na realização dos testes, e assim a incerteza sobre a qualidade dos testes gera mais stress sobre o que pode acontecer (Gráfico de influência de Gerald Weinberg). Neste ponto o stress pode ser ainda mais destruidor, imagine quantas vezes um hotfix furou toda a lista de priorizações e, após os 30min mais alucinantes de desenvolvimento foi direto a produção porque não havia tempo para ser testado, uma alteração tão pequena não poderia gerar maiores problemas… OUTRO ERRO APARECEU!
O Desenvolvimento Orientado a Testes ou TDD, é uma técnica para desenvolvimento de software, criada/apresentada pelo Kent Beck, que nos direciona ao trabalho baseado em escolhas conscientes e minimamente viáveis, estimulando o aumento na confiança sobre oque está sendo entregue. O TDD trabalha a ordem e o modo que entregamos novas funcionalidades, automatizando nossas listas de critérios de aceitação ou funcionalidades internas do sistema, com pequenos passos seguros que permitem num curto tempo a execução destes planos, assim como crescimentos de aplicações de forma a sabermos quando tudo está certo ou não!! Valores como CORAGEM e FEEDBACK da Extreme Programming são reforçados, quanto mais você anda com feedback constante sobre o efeito de suas alterações no resto do código, maior sua coragem para abraçar mudanças e realmente evoluir sua aplicação.
[slideshare id=14055677&doc=testdrivendevelopment-embuscadefeedbackutileconcreto-120823190008-phpapp02]
- __
- __
- __
- __
- __
- __