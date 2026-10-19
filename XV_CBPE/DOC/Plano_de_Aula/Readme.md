# Plano de Aula — Energia Eólica I (EES7470)

## Estudo de caso PBL+SHES: turbina eólica de eixo vertical para instalação residencial no Cabo de Santa Marta, Laguna (SC)

**Data:** 05/10/2026  
**Curso:** Bacharelado em Engenharia de Energia — UFSC, campus Araranguá  
**Disciplina:** Energia Eólica I  
**Carga horária sugerida:** 2 horas-aula  
**Tema:** Proposição preliminar de uma turbina Darrieus de eixo vertical (VAWT) para geração complementar de energia residencial em ambiente costeiro.

## Apresentação

Esta aula consolida conceitos de vento como recurso energético, potencial eólico e energia eólica onshore por meio de um estudo de caso aplicado. A atividade é estruturada como a fase de Problematização de um itinerário de Aprendizagem Baseada em Problemas (PBL), integrada à abordagem Sustainable Human and Environmental Systems (SHES).

Os estudantes analisam uma situação-problema aberta: uma residência próxima ao Farol de Santa Marta deseja instalar uma turbina eólica de pequeno porte para geração complementar de energia. A proposta considera tanto os aspectos técnicos do recurso eólico e do rotor quanto as necessidades do usuário, as condições de instalação e as dimensões sociais e ambientais.

## Objetivos

### Objetivo geral

Aplicar conceitos de vento como recurso energético, potencial eólico e energia eólica onshore na proposição fundamentada de uma turbina Darrieus para instalação residencial em ambiente costeiro, articulando conhecimentos técnicos e competências de sustentabilidade por meio da metodologia PBL+SHES.

### Objetivos específicos

Ao final da aula, espera-se que os estudantes possam retomar conceitos de perfil de vento e camada limite atmosférica; estimar o potencial eólico a partir da densidade de potência e de distribuições estatísticas de velocidade, como a distribuição de Weibull; relacionar as características do sítio à escolha de uma turbina de eixo vertical; dimensionar preliminarmente um rotor Darrieus compatível com a carga residencial e o recurso eólico local; e discutir as vantagens e limitações da microgeração eólica em ambiente residencial.

A aula também inicia o desenvolvimento de competências SHES. Os estudantes mapeiam os elementos e as interdependências do problema, consideram as necessidades de um usuário ou comunidade e praticam a colaboração em pequenos grupos na resolução de um problema pouco estruturado.

## Contexto do estudo de caso

O Farol de Santa Marta está localizado no litoral sul de Santa Catarina, em um promontório exposto ao oceano Atlântico. Para fins didáticos, considera-se uma residência próxima ao farol, mas não necessariamente situada no ponto de maior exposição do promontório. A turbina seria instalada perto das edificações, em telhado ou mastro de poucos metros, onde a rugosidade, os obstáculos e a turbulência podem afetar o recurso eólico.

A aula utiliza dois cenários preliminares de velocidade média: 5 m/s, como referência para um regime residencial com obstáculos e rugosidade, e 9 m/s, como cenário de maior exposição. Esses valores são estimativas didáticas e devem ser confirmados por medições locais antes de qualquer decisão de instalação.

## Fundamentação metodológica

### Aprendizagem Baseada em Problemas (PBL)

A Aprendizagem Baseada em Problemas coloca os estudantes diante de problemas reais, complexos e abertos. Nesta aula, trabalha-se a fase de Problematização: os grupos identificam o problema, organizam as informações disponíveis, reconhecem lacunas de conhecimento e definem objetivos de aprendizagem para as etapas posteriores de pesquisa, discussão, síntese, projeto, manufatura e avaliação.

### Abordagem SHES

A abordagem Sustainable Human and Environmental Systems (SHES) reconhece a interdependência entre sistemas humanos — sociais, econômicos e políticos — e sistemas ambientais — ecológicos e biofísicos. O dimensionamento da turbina, portanto, não é tratado apenas como um problema técnico: também considera o contexto residencial, as restrições de instalação, as necessidades dos usuários e os impactos ambientais.

A competência SHES central desta aula é o pensamento holístico e sistêmico, exercitado por meio do mapeamento da residência, do vento, da tecnologia disponível e das condições locais, além das relações entre esses elementos.

## Referências técnicas para a atividade

O vento disponível depende da circulação atmosférica, da camada limite, da rugosidade do terreno, dos obstáculos e das condições locais, como brisas marítimas e terrestres. Próximo à superfície, a velocidade varia com a altura, a hora do dia e a estação do ano. Em áreas costeiras, a baixa rugosidade do mar pode favorecer ventos mais intensos, enquanto a transição entre terra e mar e a presença de edificações podem alterar o escoamento.

A potência aproveitável depende da velocidade do vento, da área varrida pelo rotor e do coeficiente de potência. Para aplicações residenciais de pequeno porte, a faixa de potência considerada no material é de aproximadamente 100 W a 1 kW. Em ambientes urbanos ou residenciais, a turbulência e a variação direcional do vento podem favorecer turbinas de eixo vertical, que não necessitam de mecanismo de orientação ao vento.

## Proposta preliminar de turbina

A configuração de referência é uma turbina Darrieus helicoidal de três pás, com perfil aerodinâmico simétrico S1046 ou NACA 0018, solidez próxima de 0,30, razão de aspecto altura/diâmetro próxima de 2,6 e razão de velocidade de ponta (TSR) próxima de 3,75.

Para uma área varrida aproximada de 4 m², o material estima um raio entre 0,82 m e 0,88 m e uma corda de pá entre 5 cm e 9 cm. A escolha de três pás busca equilibrar desempenho e torque de partida em condições de vento variável, embora uma configuração com duas pás possa apresentar coeficiente de potência máximo ligeiramente superior em determinadas simulações.

Esses parâmetros são referências preliminares da literatura, não especificações definitivas. O projeto deve ser recalculado e validado com dados anemométricos e requisitos reais da residência.

## Estimativa do potencial eólico

Adotando massa específica do ar |$\rho = 1{,}225\ \text{kg/m}^3$| e área varrida |$A \approx 4\ \text{m}^2$|, a potência disponível no vento pode ser estimada por:

|$$
P_{\text{vento}} = \frac{1}{2}\rho A v^3
$$|

A densidade de potência do vento é:

|$$
\frac{P_{\text{vento}}}{A} = \frac{1}{2}\rho v^3
$$|

Para os cenários utilizados na aula:

| Velocidade do vento | Densidade de potência aproximada | Potência disponível em 4 m² |
|---|---:|---:|
| 5 m/s | 76,6 W/m² | 306 W |
| 9 m/s | 446,4 W/m² | 1.785 W |

A potência mecânica estimada depende do coeficiente de potência do rotor. O plano de aula apresenta uma faixa de |$C_P$| entre 0,20 e 0,48, com valor típico de projeto próximo de 0,40. Os resultados de referência indicados são aproximadamente 136 W a 220 rpm para vento de 5 m/s e 932 W a 380 rpm para vento de 9 m/s. Esses valores pertencem ao caso citado e não devem ser interpretados como garantia de desempenho para outro rotor ou local.

## Sequência didática

| Atividade | Duração sugerida | Descrição |
|---|---:|---|
| Apresentação do problema | 10 min | Apresentar o caso da residência próxima ao Cabo de Santa Marta, sem fornecer uma solução pronta. |
| Formação das equipes e mapeamento inicial | 20 min | Organizar pequenos grupos com papéis definidos e mapear residência, demanda, vento, obstáculos, restrições e tecnologia. |
| Estudo dirigido de cálculo | 10 min | Estimar a densidade de potência e a potência disponível nos dois cenários de vento. |
| Discussão coletiva | 30 min | Comparar os resultados, discutir a escolha da turbina vertical e relacionar decisões técnicas ao contexto residencial. |
| Fechamento e objetivos de aprendizagem | 10 min | Sistematizar conclusões e registrar o que cada grupo precisa pesquisar nas próximas fases. |
| Sistematização adicional, se disponível | 10–20 min | Organizar os resultados dos grupos e definir questões para as próximas etapas do itinerário. |

## Recursos didáticos

A aula pode utilizar quadro ou projeção, roteiro impresso ou digital, planilha ou script para os cálculos, equações de densidade de potência e dimensionamento paramétrico, imagens ou esquemas do rotor Darrieus, ficha para mapeamento do sistema e modelo paramétrico para visualização da turbina. O plano também propõe o uso de um portal de atlas eólico como apoio à discussão do recurso local.

## Avaliação

A avaliação é formativa durante o estudo dirigido, considerando a aplicação das equações de densidade de potência e o mapeamento do sistema produzido pelos grupos.

Como avaliação somativa, cada grupo prepara um relatório técnico curto contendo a memória de cálculo dos dois cenários de vento, a justificativa da escolha do número de pás e da topologia vertical, uma discussão sobre a necessidade de medições locais antes da instalação e um registro dos elementos, interdependências e restrições identificados.

As apresentações dos grupos podem apoiar a síntese coletiva e o debate. O uso de capturas de tela ou apresentações digitais deve respeitar as orientações da disciplina e a privacidade dos participantes.

## Segurança, limitações e validação

Os cenários de vento e os parâmetros do rotor são didáticos e preliminares. Uma instalação real exige medição local do vento, análise de obstáculos e turbulência, avaliação estrutural, verificação elétrica e estudo das condições de fixação e manutenção.

O plano de aula não substitui um projeto de engenharia validado nem uma avaliação de segurança. A instalação de um protótipo deve ser precedida por análise técnica e realizada com supervisão adequada.

## Referências

Barry, R. G., & Chorley, R. J. (2013). *Atmosfera, tempo e clima*. Bookman.

Burton, T. (2001). *Wind Energy: Handbook*. John Wiley & Sons.

Díaz-Canul, F., Aguilar, J. O., Hau, N. R., Simá, E., & Jaramillo, Ó. A. (2025). Design of Low-Power Vertical-Axis Wind Turbine Based on Parametric Method. *Wind, 5*(4), 35. https://doi.org/10.3390/wind5040035

Focht, W., & Barresi, P. A. (2018). The SHES approach to sustainability education. In *Routledge Handbook of Sustainability Curriculum* (pp. 62–80). https://doi.org/10.4324/9781351171601-6

Focht, W., & Bell, D. V. J. (2018). Why education for sustainable human and environmental systems? In *Routledge Handbook of Sustainability Curriculum* (pp. 3–18). https://doi.org/10.4324/9781351171601-2

Hassan, W. U., Jalal, A., Bilal, M. A., Buzal, M. Z., Asghar, H., & Ali, U. (2024). Parametric analysis of a helical-bladed vertical axis wind turbine. *Journal of Ocean Engineering and Marine Energy, 10*(2), 383–398. https://doi.org/10.1007/s40722-024-00318-0

Lozano, R., Merrill, M. Y., Sammalisto, K., Ceulemans, K., & Lozano, F. J. (2017). Connecting Competences and Pedagogical Approaches for Sustainable Development in Higher Education: A Literature Review and Framework Proposal. *Sustainability, 9*(10), 1889. https://doi.org/10.3390/su9101889

Simon, S., Erduran, S., & Osborne, J. (2013). Learning Science Through Argument and Explanation. *Science Education, 90*(3), 394–410.

Tolmasquim, M. T. (2016). *Energia Renovável: hidráulica, biomassa, eólica, solar, oceânica*. EPE.

Vian, A., et al. (2021). *Energia Eólica: Fundamentos, Tecnologia e Aplicações*. Blucher.
