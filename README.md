# AWT
# Turbina Eólica Vertical Darrieus — Cabo de Santa Marta (SC)

Repositório de apoio ao projeto de Ensino-Pesquisa-Extensão PJ226-2026 **Desenvolvimento e Manufatura de Geradores Eólicos de Pequeno Porte para Inclusão Energética**, registrado no câmous Araranguá do IFSC. Objetiva-se propor, dimensionar e fabricar (via impressão 3D) uma turbina eólica de eixo vertical, tipo Darrieus, para instalação em contexto residencial na região do Cabo de Santa Marta, Santa Catarina, Brasil.

O trabalho é conduzido segundo a metodologia **PBL (Project/Problem-Based Learning)** integrada à abordagem **SHES (Sustainable Human and Environmental Systems)**, articulando fundamentação teórica de recurso eólico, cálculo de potencial energético, dimensionamento paramétrico do rotor e modelagem 3D para manufatura.

## Estrutura do repositório
. ├── docs/ ├── Plano_de_Aula__Turbina_Vertical__Energia_Elica_I_EES7470_rev00_1.docx │ ├── VAWT_ANEXO_A___fase_1__DOSSIE__do_problema.docx │ ├── Itinerrio_Clculo_Turbina_Elica_rev01.docx │ └── Pesquisa_Filamentos_Impresso_3D_3.docx ├── images/ │ ├── Cl_Cd_versus_Reynolds.png │ ├── C_sustentacao_versus_reinolds.png │ ├── velocidades_diferentes.png │ ├── potencias.png │ ├── comparacao_perfis.png │ ├── cpkin_tsr.png │ └── 01.png ├── openscad/ │ └── turbina_darrieus_parametrica.scad ├── python/ │ └── fase4_sintese_modelo_turbina.py └── README.md
## Conteúdo do projeto

**Plano de aula** (`docs/Plano_de_Aula__Turbina_Vertical__Energia_Elica_I_EES7470_rev00_1.docx`): aula de estudo de caso aplicando PBL+SHES à proposição de uma turbina Darrieus para instalação residencial no Cabo de Santa Marta, com fundamentação teórica, quantificação do potencial eólico e proposta técnica do rotor.

**Dossiê do problema e anexos de itinerário** (`docs/VAWT_ANEXO_A___fase_1__DOSSIE__do_problema.docx`): documentação das sete fases do projeto — dossiê do problema, revisão bibliográfica e banco de dados do vento, documento de requisitos, código e documentação técnica, modelo CAD e especificação do gerador, protótipo e testes de bancada, e relatório de monitoramento com rubrica de avaliação da competência de pensamento holístico e sistêmico.

**Itinerário de cálculo** (`docs/Itinerrio_Clculo_Turbina_Elica_rev01.docx`): memória de cálculo consolidada a partir da literatura de referência (Díaz-Canul et al., 2025; Hassan et al., 2024), cobrindo recurso eólico, seleção de topologia e perfil aerodinâmico, dimensionamento paramétrico, simulação aerodinâmica, refino e seleção final, análise estrutural e validação.

**Pesquisa de materiais** (`docs/Pesquisa_Filamentos_Impresso_3D_3.docx`): avaliação de filamentos para impressão 3D e justificativa da escolha de material e adesivo estrutural. Material recomendado: ASA; adesivo recomendado: epóxi.

**Gráficos de apoio** (pasta `images/`): todos gerados pelo script `analise_perfis_dimensionamento_cp.py` — curva Cl/Cd versus ângulo de ataque para múltiplos Reynolds (`Cl_Cd_versus_Reynolds.png`), coeficiente de sustentação máximo por perfil e Reynolds (`C_sustentacao_versus_reinolds.png`), Reynolds de corda em operação para diferentes velocidades de vento (`velocidades_diferentes.png`), tabela de potência entregue por perfil (`potencias.png`), comparação de Cp cinemático por perfil e Reynolds em TSR = 3,75 (`comparacao_perfis.png`), envelope de Cp cinemático versus TSR (`cpkin_tsr.png`) e ângulo de melhor Cl/Cd por perfil e Reynolds (`01.png`).

**Modelo de dimensionamento — Fase 4 (Anexo D)** (`python/fase4_sintese_modelo_turbina.py`): implementa o dimensionamento geométrico do rotor a partir de uma potência-alvo e de um vento de projeto (área varrida, diâmetro, altura, corda, rotação), a curva de potência P(U), a estimativa de energia anual (série medida ou distribuição de Weibull) e a validação contra benchmarks da literatura.

**Modelo de análise de perfis e dimensionamento** (`python/analise_perfis_dimensionamento_cp.py`): script consolidado que integra três etapas do itinerário de cálculo em um único fluxo:

* **Carregamento de polares aerodinâmicas** para quatro perfis (NACA 0012, NACA 0018, NACA 0025 e SD7080) em três números de Reynolds de referência (1×10⁵, 2×10⁵ e 3×10⁵). O script procura arquivos reais de polar XFoil (`.csv`, `.txt` ou `.dat`) na pasta `python/polars/`; na ausência deles, gera polares sintéticas de demonstração (modelo linear com estol suave), sinalizando a origem dos dados (`xfoil` ou `demo`) em todas as saídas;
* **Dimensionamento paramétrico do rotor**, para uma faixa de potência nominal de 500 a 1000 W e vento de projeto de 10 m/s, com Cp de projeto de 0,48, solidez de 0,3, razão de aspecto (H/D) de 2,6, TSR de 3,75 e 3 pás — com verificação explícita de que o Cp adotado respeita o limite de Betz (16/27);
* **Modelo cinemático simplificado de Cp** (sem indução axial), que integra a contribuição tangencial de sustentação e arrasto ao longo de uma volta completa do rotor para estimar um "Cp cinemático" por perfil e Reynolds — usado como ranking relativo entre perfis, não como valor absoluto de desempenho;
* **Geração dos sete gráficos** de apoio listados acima, incluindo uma tabela visual de potência entregue por perfil em diferentes velocidades de vento e o gráfico de Reynolds de corda em operação, usado para verificar se o rotor opera na faixa de Reynolds em que as polares são válidas.

Principais parâmetros de projeto do script (ajustáveis no topo do arquivo): `P_nominal` (500–1000 W), `V_nominal` (10 m/s), `Cp` (0,48), `N_pas` (3), `AR` (2,6), `sigma` (0,3) e `TSR` (3,75).

**Modelo paramétrico 3D** (`openscad/turbina_darrieus_parametrica.scad`): script em OpenSCAD que gera o rotor Darrieus helicoidal completo a partir dos parâmetros geométricos calculados em Python. Principais características: pás helicoidais com perfil alinhado radialmente ao eixo de giro, torção e inclinação totalmente parametrizadas; seleção de perfil aerodinâmico entre NACA 0012, 0015, 0018, 0024, 0025 e SD7080; discos de fixação nas extremidades com diâmetro calculado automaticamente a partir do círculo varrido pela pá, com defasagem angular e inclinação independentes; cubo central com furo para o eixo; e conexão física garantida entre pás e discos por cilindros de encaixe calculados a partir de uma única fonte de posição por extremidade.

Parâmetros padrão atuais do script OpenSCAD: raio de 600 mm, altura de 1439,7 mm, corda de 174 mm, três pás, perfil SD7080, espessura de disco de 80 mm e fator de escala de 0,9 no disco inferior.

## Como usar os modelos Python

**`fase4_sintese_modelo_turbina.py`**: execute com `python fase4_sintese_modelo_turbina.py` (Python 3.10 ou superior). O matplotlib é opcional; sem ele, o script roda em modo texto e imprime o relatório de dimensionamento no terminal.

**`analise_perfis_dimensionamento_cp.py`**: execute com `python analise_perfis_dimensionamento_cp.py` (Python 3.8 ou superior, graças ao uso de `from __future__ import annotations`, que permite anotações de tipo modernas como `list[float]` e `float | None` mesmo em versões mais antigas do interpretador)<sources>[5]</sources>. Requer as bibliotecas `matplotlib`, `numpy` e `pandas` instaladas — diferentemente do script da Fase 4, aqui elas não são opcionais. O script usa a decoração `@dataclass` do módulo padrão `dataclasses` para as classes `Polar`, `Parametros` e `Rotor`<sources>[6]</sources>. Para usar polares reais em vez das sintéticas, crie a pasta `polars/` no mesmo diretório do script e adicione arquivos nomeados como `NACA0012_Re100000.csv` (perfil + `_Re` + Reynolds, sem separador decimal), com colunas de ângulo de ataque, Cl e Cd.

## Metodologia

O desenvolvimento segue as sete fases do itinerário PBL adotado no projeto: Problematização, Pesquisa, Discussão, Síntese, Projeto, Manufatura e Disseminação/Avaliação, com mobilização simultânea de competências técnicas (vento como recurso energético, potencial eólico, eólica onshore, aerodinâmica de pás) e competências de sustentabilidade do marco SHES (pensamento sistêmico, engajamento com necessidades reais da comunidade, planejamento de projeto).

## Autoria
Desenvolvido e Coordenado por mim.
Socializado em:
05/10/2026: disciplina Energia Eólica I (EES7470), curso de Engenharia de Energia, Centro de Ciências, Tecnologias e Saúde (CTS), Universidade Federal de Santa Catarina (UFSC), Campus Araranguá.

## Licença
