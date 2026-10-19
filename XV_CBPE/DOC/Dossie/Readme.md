# Projeto VAWT — Itinerário de projeto eólico de eixo vertical

Este repositório documenta um itinerário de aprendizagem baseado em projeto para conceber, fabricar e avaliar uma turbina eólica de eixo vertical (VAWT) de baixa potência. O projeto integra engenharia, sustentabilidade e colaboração com a comunidade, desde a caracterização do problema até o monitoramento de uma instalação piloto.

O material está organizado em sete fases e sete anexos, com atividades, decisões de projeto, procedimentos de ensaio e instrumentos de avaliação. Os valores citados são referências da literatura, não resultados experimentais deste projeto. Devem ser verificados e ajustados conforme os dados do local, as necessidades da comunidade e a validação dos protótipos.

## Objetivos

- Caracterizar as necessidades energéticas da comunidade e o recurso eólico local.
- Dimensionar preliminarmente o rotor e definir requisitos técnicos.
- Avaliar materiais para fabricação por impressão 3D.
- Desenvolver modelos matemáticos e CAD paramétricos.
- Fabricar e testar um protótipo funcional.
- Avaliar os resultados técnicos, sociais e ambientais.
- Desenvolver competências de sustentabilidade humana e ambiental (SHES), incluindo pensamento sistêmico, colaboração e planejamento de projetos.

## Fases do projeto

| Fase | Anexo | Foco | Entregável principal |
|---|---|---|---|
| 1 | A — Dossiê do problema | Comunidade, usos de energia, vento preliminar, potência-alvo e objetivos de aprendizagem | Dossiê inicial do problema |
| 2 | B — Revisão e dados do vento | Revisão bibliográfica e coleta ou organização de dados anemométricos | Relatório, fichas de leitura e banco de dados do vento |
| 3 | C — Documento de requisitos | Decisões aerodinâmicas e seleção de materiais com trade-offs justificados | Requisitos e matriz de materiais |
| 4 | D — Modelo matemático | Dimensionamento, estimativas de potência e energia, documentação e rastreabilidade | Código Python e relatório de parâmetros |
| 5 | E — CAD e PMSG | Modelagem paramétrica, análise estrutural/modal e especificação do gerador | Modelo CAD, laudo de análise e ficha do gerador |
| 6 | F — Protótipo e testes | Impressão, montagem, ensaios de bancada e análise de resultados | Protótipo e registros experimentais |
| 7 | G — Monitoramento e pacote didático | Avaliação da instalação piloto e das competências SHES | Relatório de monitoramento e materiais de replicação |

## Parâmetros de referência

O projeto considera como ponto de partida uma turbina Darrieus helicoidal com perfil S1046, solidez σ = 0,3, razão de aspecto Ar = 2,6, razão de velocidade de ponta (TSR) próxima de 3,75, três pás e ângulo de hélice de 60°. Esses parâmetros são referências de projeto citadas na literatura e não especificações universais.

A seleção de materiais considera compósitos para impressão FFF, incluindo ABS/CF, ASA/CF, PLA/CF e PETG/CF. A avaliação deve ponderar resistência mecânica, imprimibilidade, durabilidade UV, custo e reciclabilidade, além das condições específicas de fabricação e uso.

## Conteúdo dos anexos

O Anexo A apresenta o roteiro para caracterização da comunidade, levantamento preliminar do vento, definição da potência-alvo e objetivos de aprendizagem. O Anexo B orienta a revisão bibliográfica, a elaboração de fichas de leitura e o registro de dados anemométricos. O Anexo C documenta as decisões aerodinâmicas e a matriz de seleção de materiais.

O Anexo D especifica o modelo matemático em Python para estimar dimensões do rotor, rotação, potência e energia. O Anexo E orienta a modelagem CAD paramétrica da pá helicoidal, a análise estrutural e modal e a especificação do gerador PMSG. O Anexo F reúne o planejamento de experimentos de impressão, os parâmetros de fabricação e o protocolo de testes de bancada. O Anexo G propõe indicadores de monitoramento, rubricas de avaliação de competências SHES e uma estrutura para o pacote didático.

## Modelo matemático e CAD

O modelo da Fase 4 relaciona a potência-alvo e as condições de vento aos parâmetros geométricos e operacionais do rotor. As saídas previstas incluem área varrida, diâmetro, altura, corda, rotação e estimativas de potência e energia. Dados de Weibull ou séries de vento medidas devem ser preenchidos com informações obtidas para o local estudado.

Confira as equações, unidades, hipóteses e limites de operação da implementação antes de utilizar os resultados na fabricação. As estimativas não substituem medições, análise estrutural ou validação experimental.

Na Fase 5, o CAD paramétrico recebe as dimensões calculadas para o caso estudado. O material descreve o uso de uma aproximação NACA 0018 enquanto as coordenadas verificadas do perfil S1046 não estiverem disponíveis. Essa aproximação não deve ser identificada como uma representação fiel do S1046.

O modelo OpenSCAD pode ser explorado nos seguintes editores:

- [OpenSCAD2](https://ochafik.com/openscad2/)
- [OpenSCAD Cloud](https://openscad.cloud/openscad/)

## Ensaios e validação

Os ensaios de bancada propostos registram simultaneamente a velocidade do vento, a rotação e as grandezas elétricas do gerador. Quando houver medição de torque, também será possível estimar a potência mecânica e analisar o desempenho aerodinâmico e eletromecânico.

Registre as condições do ensaio, os instrumentos utilizados, a calibração, as incertezas, a configuração da carga e os dados medidos. Os valores publicados citados nos anexos são benchmarks da literatura, não resultados deste projeto. Comparações devem considerar diferenças de escala e de método experimental.

## Segurança e limitações

Um rotor em operação pode causar ferimentos, falhas mecânicas ou danos materiais. A fabricação, a montagem e os ensaios devem ocorrer sob supervisão adequada, com proteção contra partes móveis e procedimentos de desligamento.

Antes de qualquer instalação comunitária, avalie a integridade estrutural, o sistema elétrico, a ancoragem, a exposição ao vento e o plano de manutenção. Os anexos servem como roteiro de projeto e aprendizagem; não constituem certificação de segurança nem garantia de desempenho.

## Referências

As referências bibliográficas completas, com DOI e demais dados disponíveis, estão documentadas no material dos anexos. Consulte-as para identificar as fontes dos parâmetros de projeto, dos benchmarks experimentais, das abordagens pedagógicas e das competências SHES.

## Licença e citação

