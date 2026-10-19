# Turbina Eólica Darrieus com Pás Helicoidais

Modelo paramétrico em OpenSCAD de um rotor eólico do tipo Darrieus, com três pás helicoidais, perfil simétrico NACA selecionável, discos de fixação nas extremidades e cubos com furo para eixo. O projeto foi estruturado para permitir ajustar dimensões e geometria diretamente nos parâmetros do código.

> **Conteúdo do repositório:** este README documenta o código-fonte OpenSCAD (`.scad`). Não há, neste material, código Python.

## Recursos

- Geração de perfil aerodinâmico simétrico NACA de quatro dígitos: NACA 0015, 0018 ou 0024.
- Pás helicoidais com torção definida diretamente em graus ou calculada a partir de um ângulo de hélice.
- Ajuste do sentido da hélice, inclinação radial das pás e defasagem angular dos discos.
- Discos superior e inferior dimensionados a partir do raio máximo das pás, com folgas configuráveis.
- Encaixes cilíndricos nas pontas das pás com sobreposição geométrica nos discos.
- Cubos centrais com furo para eixo.
- Construção do rotor completo com número de pás configurável.

## Requisitos

- [OpenSCAD](https://openscad.org/) instalado.
- Um arquivo de projeto com extensão `.scad` contendo o código-fonte do modelo.

## Como abrir e gerar o modelo

1. Salve o código-fonte em um arquivo, por exemplo, `turbina_darrieus.scad`.
2. Abra o arquivo no OpenSCAD.
3. Pressione **F5** para pré-visualizar ou **F6** para renderizar o modelo completo.
4. Para exportar o modelo, use **File → Export → Export as STL** após a renderização.

Também é possível executar pelo terminal, se o OpenSCAD estiver disponível no sistema:

```bash
openscad -o turbina_darrieus.stl turbina_darrieus.scad
```

## Parâmetros principais

Os valores abaixo são os definidos inicialmente no código fornecido. Todas as dimensões lineares estão em milímetros, salvo indicação diferente.

| Parâmetro | Valor inicial | Descrição |
|---|---:|---|
| `raio_mm` | 276,9 | Raio de referência do rotor. |
| `altura_mm` | 1439,7 | Altura das pás. |
| `corda_mm` | 174,0 | Corda do perfil aerodinâmico. |
| `n_pas` | 3 | Número de pás. |
| `sentido_helice` | 1 | Sinal aplicado à torção; use `-1` para inverter o sentido. |
| `modo_torcao` | `"direto"` | Define se a torção é informada diretamente (`"direto"`) ou calculada pelo ângulo de hélice. |
| `torcao_total_graus_param` | 25 | Torção total em graus quando `modo_torcao = "direto"`. |
| `angulo_helice_graus` | 60 | Ângulo usado no cálculo quando selecionado o modo por ângulo. |
| `convencao_helice` | `"vertical"` | Convenção usada pela função de cálculo: `"vertical"` ou outra opção, tratada como convenção alternativa. |
| `inclinacao_graus` | 0 | Inclinação usada para calcular o deslocamento radial do topo. |
| `defasagem_angular_discos_graus` | 0 | Defasagem angular aplicada ao topo da pá e ao disco superior. |
| `perfil_escolhido` | `"NACA0018"` | Perfil selecionado: `"NACA0015"`, `"NACA0018"` ou `"NACA0024"`. |
| `n_pontos_perfil` | 60 | Resolução usada na definição de cada lado do perfil. |
| `diametro_encaixe_mm` | 30 | Diâmetro dos encaixes cilíndricos das pás. |
| `comprimento_encaixe_mm` | 60 | Comprimento nominal dos encaixes nas extremidades. |
| `sobreposicao_contato_mm` | 10 | Sobreposição adicional do encaixe em relação ao disco. |
| `diametro_cubo_mm` | 80 | Diâmetro externo dos cubos centrais. |
| `diametro_eixo_mm` | 20 | Diâmetro do furo para o eixo. |
| `espessura_disco_mm` | 15 | Espessura dos discos de fixação e dos cubos. |
| `folga_disco_inferior_mm` / `folga_disco_superior_mm` | 2 / 2 | Folgas adicionadas ao dimensionamento dos discos. |
| `fator_escala_disco_inferior` / `fator_escala_disco_superior` | 1,0 / 1,0 | Fatores de escala dos diâmetros dos discos. |

Para alterar a configuração, modifique os valores na seção correspondente do arquivo `.scad`. Por exemplo, para usar o perfil NACA 0015, altere `perfil_escolhido` para `"NACA0015"`.

## Organização do código

O código está dividido em seções funcionais:

1. Parâmetros gerais, torção, inclinação e defasagem angular.
2. Seleção e espessura do perfil NACA.
3. Encaixes, cubo central e dimensões dos discos.
4. Funções para calcular a posição radial e angular dos encaixes nas extremidades.
5. Geração dos pontos do perfil aerodinâmico.
6. Módulos `pal_helicoidal()`, `cubo_central()`, `disco_fixacao()` e `rotor_completo()`.
7. Chamada final de `rotor_completo()` para gerar o conjunto.

As funções `raio_encaixe_base()`, `raio_encaixe_topo()`, `angulo_encaixe_base()` e `angulo_encaixe_topo()` concentram as posições de referência dos encaixes, evitando manter fórmulas independentes para posicioná-los no rotor.

## Observações importantes

- Os discos são sólidos, exceto pelo furo central do eixo. Os encaixes das pás intersectam o volume dos discos para produzir sobreposição geométrica; não são furos individuais para cada pá.
- A sobreposição geométrica no modelo não substitui a verificação de resistência mecânica, tolerâncias de fabricação ou adequação do material. Confira o conjunto no fatiador e valide o projeto para a aplicação pretendida.
- O código define `inclinacao_disco_inferior_graus` e `inclinacao_disco_superior_graus`, mas a rotação do disco é aplicada em torno do eixo X. Verifique o comportamento desejado caso altere esses parâmetros.
- A variável `convencao_helice` possui duas ramificações no cálculo; qualquer valor diferente de `"vertical"` utiliza a fórmula alternativa. Use os valores esperados pelo código.
- O comando de exportação pressupõe que o arquivo tenha sido salvo com o nome indicado. Ajuste os nomes conforme necessário.

## Licença

