# SIMPPGES_26-rev07 — Dimensionamento de Rotor Eólico H-Darrieus e Itinerário PBL-SHES

## Sobre este documento

Este arquivo é a exportação em PDF de um notebook do Google Colab (`SIMPPGES_26-rev07.ipynb`), contendo um complemento textual a um artigo sobre o dimensionamento paramétrico de um rotor eólico de eixo vertical do tipo Darrieus (pás helicoidais), voltado à microgeração, desenvolvido dentro de um itinerário didático PBL-SHES (Problem-Based Learning associado à abordagem de Sustainable Human and Environmental Systems).

## Conteúdo

O documento possui 9 páginas e está estruturado da seguinte forma:

**Parâmetros e considerações complementares ao artigo** (páginas 1 a 3): apresenta os parâmetros principais de projeto de um rotor Darrieus (solidez, razão altura/diâmetro, razão corda/diâmetro, área varrida, perfil aerodinâmico e estrutura de suporte), as relações entre eles, e as faixas de referência da literatura (Díaz-Canul et al., 2025; Hassan et al., 2024) usadas para justificar os valores adotados. Inclui o Quadro 1, com os parâmetros de dimensionamento, o valor adotado e o critério de adoção de cada um.

**Figuras** (páginas 4 a 6): três páginas contendo gráficos/imagens do notebook, sem legenda textual extraída neste PDF.

**Considerações finais** (páginas 7 e 8): resume o itinerário PBL-SHES em sete fases, o dimensionamento final do rotor (três pás, razão altura/diâmetro de 2,6, solidez de 0,30, coeficiente de potência de 0,23, razão de velocidade de ponta de 3,75, diâmetro de 1,144 m, altura de 2,974 m, corda de 0,114 m, potência nominal de 1000 W a 10 m/s), a comparação entre os perfis aerodinâmicos avaliados (NACA 0025, SD7080, NACA 0012, NACA 0018, com o SD7080 apresentando a maior razão sustentação-arrasto) e a discussão de materiais compósitos reforçados com fibra de carbono (ABS/CF, ASA/CF, PLA/CF, PETG/CF) para manufatura aditiva. Também registra três limitações do trabalho (experimental, de transferência de evidência e de escopo) e aponta frentes de continuidade.

**Referências** (páginas 8 e 9): lista bibliográfica com as fontes citadas ao longo do texto, cobrindo tanto os temas de dimensionamento aerodinâmico quanto os de metodologias de ensino (PBL, SHES).

## Principais resultados reportados

- Rotor: 3 pás, H/D = 2,6, solidez (σ) = 0,30, Cp = 0,23, TSR (λ) = 3,75
- Dimensões: diâmetro de 1,144 m, altura de 2,974 m, corda de 0,114 m
- Potência nominal: 1000 W a 10 m/s
- Perfil com melhor razão sustentação-arrasto entre os avaliados: SD7080
- Coeficiente de potência obtido por modelagem matemática, não por medição experimental

## Limitações registradas no documento

1. Robustez do ASA sob radiação ultravioleta e carga cíclica ainda não caracterizada experimentalmente.
2. Estudos de preenchimento e espessura de camada citados na literatura (Said et al., 2025) referem-se a outros compósitos/polímeros, não necessariamente ao ASA sugerido.
3. Dimensionamento baseado em modelagem e simulação, sem ensaio do rotor em túnel de vento ou em campo; resultados devem ser lidos como previsão de modelo, a confirmar experimentalmente.

## Observação sobre este Readme

Este arquivo descreve o conteúdo textual do PDF conforme extraído. As figuras das páginas 4 a 6 não possuem texto, legendas ou valores numéricos capturados nesta extração, de modo que não são descritas em detalhe aqui.
