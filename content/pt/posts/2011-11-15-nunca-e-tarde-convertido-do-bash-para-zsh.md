---
title: Nunca é tarde! Convertido do Bash para ZSH!
author: helio
layout: post
date: 2011-11-15T20:23:19+00:00
url: /2011/11/15/nunca-e-tarde-convertido-do-bash-para-zsh/
embed:
  - This is the default text
seo_follow:
  - 'false'
seo_noindex:
  - 'false'
categories:
  - zsh
tags:
  - bash
  - oh-my-zsh
  - shell
  - zsh

---
Após um bom tempo utilizando o zsh, apresentei recentemente a um amigo que se surpreendeu, após conversarmos um pouco surgiu a idéia de aprender um pouco mais, e compartilhar&#8230;. Fui influenciado há certo tempo pela onda [oh-my-zsh][1], mas acabei por não contribuir em nada. Quem sabe agora?!?!

Começando do inicio, acredito que a maior parte de nós em algum momento já se deparou com um <a href="http://en.wikipedia.org/wiki/Shell_%28computing%29" target="_blank">shell</a> de linha de comandos.O shell como é mais utilizado é uma interface textual para as funcionalidades do sistema operacional, no MacOS você o acessa por meio do Terminal ou [iTerm2][2]. Existem muitos shells a serem escolhidas, e a maioria dos sistemas operacionais/distribuições acabam &#8220;facilitando&#8221; esta escolha definindo alguma padrão. Durante muito tempo só conhecia o mais popular deles GNU Bourne Again Shell ou [bash][3], uma excelente escolha quando você precisa repetir os mesmos comandos que já estão no histórico, para iniciar algum container ou ver logs&#8230; mas uma péssima, quando você passa certo tempo usando [Git][4] e [RVM][5] (

<div class="codecolorer-container text railscasts" style="overflow:auto;white-space:nowrap;width:435px;">
  <table cellspacing="0" cellpadding="0">
    <tr>
      <td class="line-numbers">
        <div>
          1<br />
        </div>
      </td>
      
      <td>
        <div class="text codecolorer">
          git branch
        </div>
      </td>
    </tr>
  </table>
</div>

 para lembrar o branch que estou e 

<div class="codecolorer-container text railscasts" style="overflow:auto;white-space:nowrap;width:435px;">
  <table cellspacing="0" cellpadding="0">
    <tr>
      <td class="line-numbers">
        <div>
          1<br />
        </div>
      </td>
      
      <td>
        <div class="text codecolorer">
          rvm gemdir
        </div>
      </td>
    </tr>
  </table>
</div>

 para ver a versão do ruby e gems) ou aprendendo comandos novos e utilizando novas técnicas do universo [devops][6] (fiz recentemente o curso da [egenial][7] de [imersão sys deploy][8]).

## zsh?

O Z-shell ou [zsh][9] é um dos shells mais completos em termos de funcionalidades e usabilidade dentre os disponíveis no [Darwin][10] que traz como default o tsch desde a v.7.0 presente no Mac Os X Panther. A [equipe do zsh][11] já faz um excelente trabalho explicando e e advogando ao seu respeito, mas como todos tenho meus pontos preferidos.

  1. **Corretor ortográfico**: Quem nunca escreveu _rmv, fnd, mkdr _ou qualquer outro comando incorretamente? O zsh possui um corretor que varre e apresenta entre comandos e sub-comandos o mais próximo ao incorreto informado. Estava errado me corrija?
  
    _zsh: correct &#8216;rmv&#8217; to &#8216;rvm&#8217; [nyae]?_
  2. **Tab completion:** A maior parte dos shells como o bash possuem tab completion, mas não tão simples ou amigável quanto o zsh. Tanto no sentido de configuração quanto de usabilidade, o zsh dá um banho. Ele apresenta em um menu navegável de sub-comandos e opções de preenchimento como a lista de diretórios quando executamos um ls, ou a lista de processos quando executamos um kill.
  3. **Compartilhamento de histórico:** Manter histórico entre as sessões ao invés de sobrepor-las, não tem nada pior do que perder o histórico de comandos executados pois uma sessão havia sido sobreposta, o zsh mantem o histórico das várias sessões.
  4. **Globbing**. O zsh se preocupou muito com seus wildcards, e o resultados foram incríveis _ls git\*~\*flow* _ou _ls (GOL|TAM)\*POA\*_, sempre dou uma olhada  [na introdução do zsh][12].
  5. **Criar funções com aliases**. O zsh permite a criação de funções chamadas pelos seus aliases, de forma fácil e ágil. <div class="codecolorer-container bash railscasts" style="overflow:auto;white-space:nowrap;width:435px;">
      <table cellspacing="0" cellpadding="0">
        <tr>
          <td class="line-numbers">
            <div>
              1<br />
            </div>
          </td>
          
          <td>
            <div class="bash codecolorer">
              <span class="kw1">function</span> juntarpdfs <span class="br0">&#123;</span> <span class="kw2">gs</span> <span class="re5">-q</span> <span class="re5">-dNOPAUSE</span> <span class="re5">-dBATCH</span> <span class="re5">-sDEVICE</span>=pdfwrite <span class="re5">-sOutputFile</span>=merged.pdf <span class="st0">"$@"</span> <span class="br0">&#125;</span>
            </div>
          </td>
        </tr>
      </table>
    </div>

  6. **É bem parecido com o bash**. Passei um bom tempo utilizando o zsh exatamente como fazia no trabalho com o bash, e mesmo assim foi impossível não aprender algo novo e que aumentasse minha produtividade, ele é simples e amigável.

<div>
  <span class="Apple-style-span" style="font-size: 20px;font-weight: bold">Mágica com o zsh!</span>
</div>

Como já havia falado antes, o zsh está presente no darwin, ou seja, se você tem instalado em sua maquina uma nova versão ou antiga do MacOsx como eu tinha, não vai precisar realizar várias buscas no [google por zsh][13], e olhar vários how-tos. Nem mesmo para personalizar em cores, aliases, funções e auto-completes se você usar o [oh-my-zsh][14]. Como descreve no link ao lado no README do projeto, o zsh é mágico para quem não tem muito tempo a perder:

> &#8220;A community-driven framework for managing your zsh configuration. Includes optional plugins for various tools (rails, git, OSX, brew,&#8230;), nearly 80 terminal themes, and an auto-updating tool so that you can keep up with the latest improvements from the community.&#8221;

Para colocar tudo isso para funcionar,  você pode fazer o seguinte:

  * Use o instalador automático criado pelo Robby Russell: <div class="codecolorer-container bash railscasts" style="overflow:auto;white-space:nowrap;width:435px;">
      <table cellspacing="0" cellpadding="0">
        <tr>
          <td class="line-numbers">
            <div>
              1<br />
            </div>
          </td>
          
          <td>
            <div class="bash codecolorer">
              <span class="kw2">wget</span> <span class="re5">--no-check-certificate</span> https:<span class="sy0">//</span>github.com<span class="sy0">/</span>robbyrussell<span class="sy0">/</span>oh-my-zsh<span class="sy0">/</span>raw<span class="sy0">/</span>master<span class="sy0">/</span>tools<span class="sy0">/</span>install.sh <span class="re5">-O</span> - <span class="sy0">|</span> <span class="kw2">sh</span>
            </div>
          </td>
        </tr>
      </table>
    </div>

Caso você não tenha o [wget][15] instalado é bem provável que você verá um erro no console. Esta é  uma ótima oportunidade de fazer isso usando o [brew][16].

  * Para instalar o brew: <div class="codecolorer-container bash railscasts" style="overflow:auto;white-space:nowrap;width:435px;">
      <table cellspacing="0" cellpadding="0">
        <tr>
          <td class="line-numbers">
            <div>
              1<br />
            </div>
          </td>
          
          <td>
            <div class="bash codecolorer">
              curl <span class="re5">-L</span> http:<span class="sy0">//</span>github.com<span class="sy0">/</span>mxcl<span class="sy0">/</span>homebrew<span class="sy0">/</span>tarball<span class="sy0">/</span>master <span class="sy0">|</span> <span class="kw2">tar</span> xz <span class="re5">--str</span>
            </div>
          </td>
        </tr>
      </table>
    </div>

  * Para instalar o wget: <div class="codecolorer-container bash railscasts" style="overflow:auto;white-space:nowrap;width:435px;">
      <table cellspacing="0" cellpadding="0">
        <tr>
          <td class="line-numbers">
            <div>
              1<br />
            </div>
          </td>
          
          <td>
            <div class="bash codecolorer">
              brew <span class="kw2">install</span> <span class="kw2">wget</span>
            </div>
          </td>
        </tr>
      </table>
    </div>

Quando terminar tudo você verá uma tela como a seguinte, daí é só abrir uma nova sessão para ver o thema do Robby Russel fazendo a sua mágica.

<p style="text-align: center">
  <a href="/uploads/2011/11/Screen-Shot-2011-11-15-at-10.35.50-AM1.png"><img class="aligncenter size-full wp-image-415" src="/uploads/2011/11/Screen-Shot-2011-11-15-at-10.35.50-AM1.png" alt="" width="478" height="247" srcset="/uploads/2011/11/Screen-Shot-2011-11-15-at-10.35.50-AM1.png 671w, /uploads/2011/11/Screen-Shot-2011-11-15-at-10.35.50-AM1-300x155.png 300w" sizes="(max-width: 478px) 100vw, 478px" /></a>
</p>

&nbsp;

&nbsp;

 [1]: http://twitter.com/#!/ohmyzsh/status/14812098501
 [2]: http://www.iterm2.com/#/section/home "iTerm2"
 [3]: http://en.wikipedia.org/wiki/Bash_(Unix_shell) "bash"
 [4]: http://git-scm.com/
 [5]: https://rvm.beginrescueend.com/
 [6]: http://en.wikipedia.org/wiki/DevOps "devOps"
 [7]: http://www.egenial.pro/pt/site "egenial"
 [8]: http://www.egenial.pro/pt/imersaosysdeploy "Imersão Sys Deploy"
 [9]: http://en.wikipedia.org/wiki/Z_shell
 [10]: http://en.wikipedia.org/wiki/Darwin_(operating_system) "Darwin"
 [11]: http://zsh.sourceforge.net/ "ZSH site"
 [12]: http://zsh.sourceforge.net/Intro/intro_2.html
 [13]: https://www.google.com/search?aq=f&gcx=w&ix=c1&sourceid=chrome&ie=UTF-8&q=zsh "googling zsh"
 [14]: https://github.com/robbyrussell/oh-my-zsh "oh-my-zsh"
 [15]: http://mxcl.github.com/homebrew/ "instalando o wget com o brew"
 [16]: https://github.com/mxcl/homebrew/wiki/installation "instalando o brew"