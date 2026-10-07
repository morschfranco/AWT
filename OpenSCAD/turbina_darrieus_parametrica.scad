/* =====================================================================
TURBINA EÓLICA DARRIEUS — PÁS HELICOIDAIS COM PERFIL ALINHADO
RADIALMENTE AO EIXO DE GIRO
Modelo paramétrico em OpenSCAD com:
- Seleção de perfil NACA (0015, 0018, 0024)
- Torção e inclinação da pá totalmente parametrizadas
- Discos de fixação nas extremidades, harmonizados ao círculo da pá
- Defasagem angular entre discos e inclinação de cada disco
- Conexão física garantida entre pás e discos (sobreposição real,
  calculada a partir de uma única fonte de posição por extremidade)
===================================================================== */

// ----------------------------------------------------------------
// 1. PARÂMETROS GERAIS
// ----------------------------------------------------------------
raio_mm = 276.9;
altura_mm = 1439.7;
corda_mm = 174.0;

n_pas = 3;
sentido_helice = 1;

// ----------------------------------------------------------------
// 2. TORÇÃO E INCLINAÇÃO DA PÁ
// ----------------------------------------------------------------
modo_torcao = "direto";
torcao_total_graus_param = 25;

angulo_helice_graus = 60;
convencao_helice = "vertical";

function torcao_calculada_por_angulo() =
    let (phi = convencao_helice == "vertical"
        ? (altura_mm / raio_mm) * tan(angulo_helice_graus)
        : (altura_mm / raio_mm) / tan(angulo_helice_graus))
    phi * 180 / PI;

function torcao_total_graus() =
    sentido_helice * (modo_torcao == "direto"
        ? torcao_total_graus_param
        : torcao_calculada_por_angulo());

inclinacao_graus = 0;

function deslocamento_radial_topo() =
    altura_mm * tan(inclinacao_graus);

// ----------------------------------------------------------------
// 2.1 DEFASAGEM ANGULAR E INCLINAÇÃO DOS DISCOS
// ----------------------------------------------------------------
defasagem_angular_discos_graus = 0;
inclinacao_disco_inferior_graus = 0;
inclinacao_disco_superior_graus = 0;

// ----------------------------------------------------------------
// 3. SELEÇÃO DO PERFIL NACA
// ----------------------------------------------------------------
perfil_escolhido = "NACA0018";

function obter_espessura(perfil) =
    perfil == "NACA0015" ? 0.15 :
    perfil == "NACA0018" ? 0.18 :
    perfil == "NACA0024" ? 0.24 :
    0.18;

t_perfil = obter_espessura(perfil_escolhido);
n_pontos_perfil = 60;

// ----------------------------------------------------------------
// 4. REGIÕES FUNCIONAIS DA PÁ
// ----------------------------------------------------------------
diametro_encaixe_mm = 30;
comprimento_encaixe_mm = 60;

// Sobreposição (mm) que o cilindro de encaixe penetra PARA DENTRO do
// disco, além da espessura do próprio disco. Valor generoso para
// eliminar qualquer gap visível — ajuste se necessário.
sobreposicao_contato_mm = 10;

// ----------------------------------------------------------------
// 5. CUBO CENTRAL
// ----------------------------------------------------------------
diametro_cubo_mm = 80;
diametro_eixo_mm = 20;

// ----------------------------------------------------------------
// 6. DISCOS DE FIXAÇÃO
// ----------------------------------------------------------------
espessura_disco_mm = 15;

raio_max_pa_base = (raio_mm - corda_mm / 2) + diametro_encaixe_mm / 2;
raio_max_pa_topo = (raio_mm - corda_mm / 2) + abs(deslocamento_radial_topo())
    + diametro_encaixe_mm / 2;

folga_disco_inferior_mm = 2;
folga_disco_superior_mm = 2;

fator_escala_disco_inferior = 1.0;
fator_escala_disco_superior = 1.0;

diametro_disco_inferior_mm =
    (2 * (raio_max_pa_base + folga_disco_inferior_mm))
    * fator_escala_disco_inferior;
diametro_disco_superior_mm =
    (2 * (raio_max_pa_topo + folga_disco_superior_mm))
    * fator_escala_disco_superior;

$fn = 48;

// ----------------------------------------------------------------
// 6.1 POSIÇÃO CENTRALIZADA DE CADA EXTREMIDADE DA PÁ (fonte única)
// ----------------------------------------------------------------
// Estas funções calculam a posição radial e angular do centro do
// encaixe cilíndrico em cada extremidade, para serem usadas tanto
// pela pá quanto pelos discos — evitando duplicação de fórmulas em
// lugares diferentes, que é a causa mais comum de desalinhamento.
function raio_encaixe_base() = raio_mm - corda_mm / 2;
function raio_encaixe_topo() = raio_mm - corda_mm / 2 + deslocamento_radial_topo();
function angulo_encaixe_base() = 0;
function angulo_encaixe_topo() = torcao_total_graus() + defasagem_angular_discos_graus;

// ----------------------------------------------------------------
// 7. PERFIL AERODINÂMICO (NACA 4 dígitos, simétrico)
// ----------------------------------------------------------------
function y_naca(t, x) =
    (t / 0.2) * (0.2969 * sqrt(x) - 0.1260 * x - 0.3516 * pow(x, 2)
        + 0.2843 * pow(x, 3) - 0.1015 * pow(x, 4));

function perfil_pontos(t, n) =
    concat(
        [ for (i = [0 : n - 1]) let (x = i / (n - 1))
            [x * corda_mm, y_naca(t, x) * corda_mm] ],
        [ for (i = [0 : n - 1]) let (x = (n - 1 - i) / (n - 1))
            [x * corda_mm, -y_naca(t, x) * corda_mm] ]
    );

module perfil_2d() {
    rotate([0, 0, 90])
        polygon(perfil_pontos(t_perfil, n_pontos_perfil));
}

// ----------------------------------------------------------------
// 8. PÁ HELICOIDAL
// ----------------------------------------------------------------
module pal_helicoidal() {
    torcao = torcao_total_graus();
    fatias = max(40, ceil(abs(torcao) + abs(defasagem_angular_discos_graus) + 1));
    desloc_topo = deslocamento_radial_topo();
    torcao_efetiva_topo = angulo_encaixe_topo();

    if (inclinacao_graus == 0 && defasagem_angular_discos_graus == 0) {
        linear_extrude(height = altura_mm, twist = torcao,
            slices = fatias, convexity = 4)
            translate([raio_mm - corda_mm, 0, 0])
                perfil_2d();
    } else {
        n_camadas = fatias;
        for (k = [0 : n_camadas - 1]) {
            z0 = altura_mm * k / n_camadas;
            z1 = altura_mm * (k + 1) / n_camadas;
            ang0 = torcao * (k / n_camadas)
                + defasagem_angular_discos_graus * (k / n_camadas);
            ang1 = torcao * ((k + 1) / n_camadas)
                + defasagem_angular_discos_graus * ((k + 1) / n_camadas);
            r0 = (raio_mm - corda_mm) + desloc_topo * (z0 / altura_mm);
            r1 = (raio_mm - corda_mm) + desloc_topo * (z1 / altura_mm);
            hull() {
                translate([0, 0, z0])
                    rotate([0, 0, ang0])
                        translate([r0, 0, 0])
                            linear_extrude(height = 0.01)
                                perfil_2d();
                translate([0, 0, z1])
                    rotate([0, 0, ang1])
                        translate([r1, 0, 0])
                            linear_extrude(height = 0.01)
                                perfil_2d();
            }
        }
    }

    // Encaixe inferior: cilindro GRANDE o suficiente para atravessar
    // o disco inteiro + sobreposição, usando a mesma posição
    // (raio_encaixe_base / angulo_encaixe_base) que o disco usará
    // para localizar seu furo, se houver.
    translate([raio_encaixe_base(), 0,
        -(comprimento_encaixe_mm + espessura_disco_mm + sobreposicao_contato_mm)])
        cylinder(d = diametro_encaixe_mm,
            h = comprimento_encaixe_mm + espessura_disco_mm + sobreposicao_contato_mm);

    // Encaixe superior: mesma lógica, na posição angular/radial do topo
    rotate([0, 0, torcao_efetiva_topo])
        translate([raio_encaixe_topo(), 0, altura_mm])
            cylinder(d = diametro_encaixe_mm,
                h = comprimento_encaixe_mm + espessura_disco_mm + sobreposicao_contato_mm);
}

// ----------------------------------------------------------------
// 9. CUBO CENTRAL
// ----------------------------------------------------------------
module cubo_central() {
    alt = espessura_disco_mm;
    difference() {
        cylinder(d = diametro_cubo_mm, h = alt, center = true);
        cylinder(d = diametro_eixo_mm, h = alt + 2, center = true);
    }
}

// ----------------------------------------------------------------
// 10. DISCO DE FIXAÇÃO (sólido cheio, sem furos de pá — a pá penetra
// fisicamente nele e a união garante contato)
// ----------------------------------------------------------------
module disco_fixacao(diametro_disco, inclinacao_disco) {
    rotate([inclinacao_disco, 0, 0])
        difference() {
            cylinder(d = diametro_disco, h = espessura_disco_mm, center = true);
            cylinder(d = diametro_eixo_mm, h = espessura_disco_mm + 2, center = true);
        }
}

// ----------------------------------------------------------------
// 11. CONJUNTO DO ROTOR
// ----------------------------------------------------------------
module rotor_completo() {
    union() {
        for (i = [0 : n_pas - 1]) {
            rotate([0, 0, i * 360 / n_pas])
                pal_helicoidal();
        }

        // Disco inferior: centrado exatamente na posição Z onde o
        // cilindro de encaixe inferior da pá passa por dentro dele
        translate([0, 0, -comprimento_encaixe_mm / 2])
            disco_fixacao(diametro_disco_inferior_mm,
                inclinacao_disco_inferior_graus);

        // Disco superior: idem, usando o mesmo ângulo efetivo de topo
        // calculado pela função central (angulo_encaixe_topo)
        translate([0, 0, altura_mm + comprimento_encaixe_mm / 2])
            rotate([0, 0, angulo_encaixe_topo()])
                disco_fixacao(diametro_disco_superior_mm,
                    inclinacao_disco_superior_graus);

        translate([0, 0, -comprimento_encaixe_mm / 2])
            cubo_central();
        translate([0, 0, altura_mm + comprimento_encaixe_mm / 2])
            cubo_central();
    }
}

// ----------------------------------------------------------------
// 12. EXECUÇÃO
// ----------------------------------------------------------------
rotor_completo();
// pal_helicoidal();
