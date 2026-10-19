# Itinerário de cálculo e projeto de uma turbina eólica de eixo vertical

Este repositório apresenta um itinerário de cálculo e projeto para uma turbina eólica de eixo vertical (VAWT) de baixa potência. O roteiro combina o método paramétrico para VAWTs de baixa potência, de Díaz-Canul et al. (2025), com a análise de turbinas helicoidais de Hassan et al. (2024).

O itinerário acompanha o projeto desde a caracterização do vento e a seleção do perfil aerodinâmico até o dimensionamento, as simulações, a análise estrutural e a validação experimental. Os valores descritos são referências dos estudos citados e devem ser tratados como pontos de partida, não como especificações universais.

## Objetivos

- Caracterizar o recurso eólico e definir os requisitos do projeto.
- Selecionar uma topologia e um perfil aerodinâmico adequados.
- Dimensionar o rotor com base em parâmetros geométricos e adimensionais.
- Simular e comparar configurações de rotor.
- Avaliar o desempenho aerodinâmico, estrutural e operacional.
- Orientar a fabricação de um protótipo e sua validação em bancada ou em campo.

## Etapas do itinerário

### Etapa 0 — Recurso eólico e definição do projeto

Caracterize o local de instalação, incluindo velocidade e variabilidade do vento, obstáculos e regime de uso. A velocidade média influencia a potência esperada e o número de Reynolds. Em aplicações urbanas ou residenciais, os ventos fracos e intermitentes tornam especialmente importante avaliar o torque de partida.

O documento cita, como resultados de um caso de referência, uma potência de 136 W a 220 rpm para vento de 5 m/s e 932 W a 380 rpm para vento de 9 m/s. Esses valores pertencem ao estudo citado e não representam uma previsão para qualquer local ou configuração.

### Etapa 1 — Topologia e perfil aerodinâmico

A metodologia considera VAWTs Darrieus de pás retas e helicoidais. A configuração helicoidal acrescenta torção ao longo da altura da pá. O estudo de Hassan et al. (2024) utiliza uma geometria de referência com perfil NACA 0018, ângulo de hélice de 25° e ângulo de passo de −2°.

A seleção do perfil deve considerar as polares aerodinâmicas em diferentes números de Reynolds, a relação entre coeficientes de sustentação e ângulo de ataque e o desempenho em curvas de coeficiente de potência em função da razão de velocidade de ponta.

Díaz-Canul et al. (2025) avaliaram nove perfis. Entre os resultados reportados, S1046 e NACA 0018 apresentaram desempenho elevado no caso estudado. O documento também destaca a queda de desempenho em números de Reynolds muito baixos e recomenda considerar a faixa de operação ao selecionar o perfil.

### Etapa 2 — Espaço paramétrico

Os principais parâmetros de projeto são:

- Solidez (|$\sigma$|).
- Razão de aspecto (|$Ar = H/R$|).
- Número de pás (|$N$|).
- Corda da pá (|$C$|).
- Raio (|$R$|) e altura (|$H$|).
- Área varrida (|$A$|).

Como referências, o documento apresenta área varrida de 4 m², solidez entre 0,20 e 0,30, razão de aspecto entre 2,6 e 3,0 e número de pás entre 2 e 5.

Há compromissos entre os parâmetros. Menos pás podem aumentar o coeficiente de potência, mas reduzir o torque de partida e aumentar as variações de torque. Uma solidez maior pode favorecer a partida, mas também altera a corda e o regime de operação.

### Etapa 3 — Dimensionamento paramétrico

Para a definição de área varrida usada no documento:

|$$
A = H \cdot D = 2ArR^2
$$|

O raio pode ser obtido por:

|$$
R = \sqrt{\frac{A}{2Ar}}
$$|

A altura é calculada por:

|$$
H = Ar \cdot R
$$|

A corda é determinada a partir da solidez e do número de pás:

|$$
C = \frac{R\sigma}{N}
$$|

Para a variante helicoidal, Hassan et al. (2024) apresentam uma parametrização baseada em múltiplos da corda para o raio e o comprimento da pá. Essas relações pertencem à configuração analisada nesse estudo e devem ser conferidas antes de serem aplicadas a outro projeto.

### Etapa 4 — Simulação aerodinâmica

O roteiro recomenda simulações com o método DMS no QBlade, incluindo uma triagem inicial pelo número de pás e uma varredura de solidez e razão de aspecto.

O documento reporta, para as configurações analisadas, coeficientes de potência máximos próximos de 0,47 para uma configuração de duas pás e de 0,45 para três pás. Esses resultados são específicos do estudo citado. A escolha final também deve considerar partida, vibração, cargas cíclicas e condições reais de operação.

Para a turbina helicoidal, Hassan et al. (2024) analisam o efeito do raio e do comprimento da pá sobre o desempenho e reportam variações no coeficiente de potência conforme a geometria e a velocidade do vento.

### Etapa 5 — Refinamento e seleção final

O documento compara resultados de DMS e QLLT. A recomendação de referência apresentada é uma turbina com três pás, razão de aspecto de 2,6, solidez de 0,30, perfil S1046 ou NACA 0018 e operação próxima de |$\lambda \approx 3{,}75$|.

A seleção de três pás é apresentada como um compromisso entre eficiência, torque de partida e suavização das cargas. A configuração escolhida deve ser validada para o local, o perfil, os materiais e o sistema de geração adotados.

### Etapa 6 — Análise estrutural e regime de operação

Antes da fabricação, o roteiro prevê análises estruturais estáticas e modais para avaliar tensões, deformações, frequências naturais e possíveis riscos de ressonância.

Também recomenda construir curvas de potência e rotação para as velocidades de vento de interesse. Esses resultados ajudam a definir a faixa de operação e os requisitos do gerador.

Os valores estruturais apresentados no documento, como propriedades do alumínio 6061-T6, fator de segurança e frequências modais, são referências da configuração estudada por Hassan et al. (2024). Não devem ser aplicados diretamente a pás fabricadas com outros materiais ou geometrias.

### Etapa 7 — Validação e testes

A validação deve combinar comparação numérica e experimental. O desempenho real depende das condições locais e de fatores que podem não estar representados integralmente nos modelos, como a inércia do rotor e as condições de partida.

O roteiro recomenda confrontar os resultados simulados com dados experimentais publicados e realizar testes de campo para verificar o funcionamento do protótipo no local de instalação.

## Equações de referência

A razão de aspecto é definida como:

|$$
Ar = \frac{H}{R}
$$|

A área varrida é:

|$$
A = H \cdot D = 2ArR^2
$$|

O documento registra duas definições de solidez encontradas nas fontes consultadas:

|$$
\sigma = \frac{NC}{R}
$$|

e

|$$
\sigma = \frac{NC}{2\pi R}
$$|

Como as definições diferem, confirme qual convenção está sendo utilizada antes de comparar parâmetros ou reproduzir cálculos.

A razão de velocidade de ponta é:

|$$
\lambda = \frac{\omega R}{U}
$$|

O coeficiente de potência é:

|$$
C_P = \frac{P_{out}}{\frac{1}{2}\rho A U^3}
$$|

em que |$P_{out}$| é a potência de saída, |$\rho$| é a massa específica do ar, |$A$| é a área varrida e |$U$| é a velocidade do vento.

O torque e a potência mecânica podem ser relacionados por:

|$$
T = N F_{t,av} R
$$|

|$$
P = T\omega
$$|

## Apêndices técnicos

O documento inclui apêndices com definições geométricas e adimensionais, relações de velocidade e forças aerodinâmicas, equações de torque e potência, dimensionamento para área varrida fixa, equações de governo das simulações e dados estruturais de referência.

As equações e os parâmetros devem ser verificados em relação às fontes originais antes de serem usados em dimensionamento, fabricação ou análise de segurança.

## Referências principais

Díaz-Canul, F., Aguilar, J. O., Hau, N. R., Simá, E., & Jaramillo, Ó. A. (2025). Design of Low-Power Vertical-Axis Wind Turbine Based on Parametric Method. *Wind*, 5(4), 35. https://doi.org/10.3390/wind5040035

Hassan, W. U., Jalal, A., Bilal, M. A., Buzal, M. Z., Asghar, H., & Ali, U. (2024). Parametric analysis of a helical-bladed vertical axis wind turbine. *Journal of Ocean Engineering and Marine Energy*, 10(2), 383–398. https://doi.org/10.1007/s40722-024-00318-0

## Segurança e limitações

O dimensionamento descrito é uma base de estudo e não substitui a validação de engenharia, a análise de riscos nem a certificação aplicável. A fabricação e os testes de rotores devem ser realizados com supervisão adequada, proteção contra partes móveis e procedimentos de desligamento.

Antes de instalar uma turbina, avalie a integridade estrutural, as cargas de vento, a fixação, o sistema elétrico, a manutenção e as condições específicas do local.

## Licença e citação

