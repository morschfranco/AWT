/* =====================================================================
TURBINA EÓLICA DARRIEUS — PÁS HELICOIDAIS COM PERFIL ALINHADO
RADIALMENTE AO EIXO DE GIRO (Compatível com OpenSCAD Customizer / Web)
===================================================================== */

/* [1. Perfil e Visualizacao] */
// Perfil aerodinâmico da pá
perfil_escolhido = "SD7080"; // ["SD7080", "NACA0012", "NACA0015", "NACA0018", "NACA0024", "NACA0025"]

// Orientação do arqueamento (camber) para o perfil assimétrico SD7080
orientacao_camber_sd7080 = 1; // [1:Extradorso para fora (+1), -1:Extradorso para dentro (-1)]

// Componente a exibir na tela
peca_exibida = "rotor_completo"; // ["rotor_completo", "pa_unica", "perfil_2d"]

/* [2. Geometria do Rotor] */
// Raio do rotor (mm)
raio_mm = 276.9; // [50:0.1:2000]

// Altura útil da pá (mm)
altura_mm = 1439.7; // [100:0.1:4000]

// Corda do perfil aerodinâmico (mm)
corda_mm = 174.0; // [20:0.1:600]

// Número de pás
n_pas = 3; // [1:1:8]

/* [3. Torcao e Inclinacao da Pa] */
// Sentido da hélice
sentido_helice = 1; // [1:Horário (+1), -1:Anti-horário (-1)]

// Modo de definição da torção
modo_torcao = "direto"; // ["direto", "angulo"]

// Torção total da pá quando modo_torcao = "direto" (graus)
torcao_total_graus_param = 25; // [-180:1:180]

// Ângulo de hélice quando modo_torcao = "angulo" (graus)
angulo_helice_graus = 60; // [5:1:85]

// Convenção de medição do ângulo de hélice
convencao_helice = "vertical"; // ["vertical", "horizontal"]

// Inclinação radial da pá do pé ao topo (graus)
inclinacao_graus = 0; // [-30:0.5:30]

/* [4. Discos e Defasagem] */
// Exibir discos de fixação nas extremidades
mostrar_discos = true;

// Defasagem angular extra entre disco inferior e superior (graus)
defasagem_angular_discos_graus = 0; // [-180:1:180]

// Inclinação do disco inferior (graus)
inclinacao_disco_inferior_graus = 0; // [-45:0.5:45]

// Inclinação do disco superior (graus)
inclinacao_disco_superior_graus = 0; // [-45:0.5:45]

// Espessura dos discos de fixação (mm)
espessura_disco_mm = 15; // [2:0.5:60]

// Folga radial da borda do disco inferior (mm)
folga_disco_inferior_mm = 2; // [0:0.5:50]

// Folga radial da borda do disco superior (mm)
folga_disco_superior_mm = 2; // [0:0.5:50]

// Fator de escala no diâmetro do disco inferior
fator_escala_disco_inferior = 1.0; // [0.5:0.05:2.0]

// Fator de escala no diâmetro do disco superior
fator_escala_disco_superior = 1.0; // [0.5:0.05:2.0]

/* [5. Encaixes e Cubo Central] */
// Diâmetro do pino/cilindro de encaixe da pá (mm)
diametro_encaixe_mm = 30; // [5:1:100]

// Comprimento livre do encaixe entre pá e disco (mm)
comprimento_encaixe_mm = 60; // [5:1:200]

// Penetração extra do encaixe para dentro do disco (mm)
sobreposicao_contato_mm = 10; // [1:1:50]

// Diâmetro externo do cubo central (mm)
diametro_cubo_mm = 80; // [20:1:300]

// Diâmetro do furo do eixo central (mm)
diametro_eixo_mm = 20; // [5:1:150]

/* [6. Resolucao de Malha] */
// Pontos por face no perfil NACA
n_pontos_perfil = 60; // [20:5:150]

// Resolução circular ($fn)
resolucao_fn = 48; // [16:4:128]

/* [Hidden] */
$fn = resolucao_fn;

// ----------------------------------------------------------------
// CÁLCULOS DERIVADOS DE TORÇÃO, INCLINAÇÃO E DISCOS
// ----------------------------------------------------------------
function torcao_calculada_por_angulo() =
    let (phi = convencao_helice == "vertical"
        ? (altura_mm / raio_mm) * tan(angulo_helice_graus)
        : (altura_mm / raio_mm) / tan(angulo_helice_graus))
    phi * 180 / PI;

function torcao_total_graus() =
    sentido_helice * (modo_torcao == "direto"
        ? torcao_total_graus_param
        : torcao_calculada_por_angulo());

function deslocamento_radial_topo() =
    altura_mm * tan(inclinacao_graus);

function obter_espessura(perfil) =
    perfil == "NACA0012" ? 0.12 :
    perfil == "NACA0015" ? 0.15 :
    perfil == "NACA0018" ? 0.18 :
    perfil == "NACA0024" ? 0.24 :
    perfil == "NACA0025" ? 0.25 :
    0.18;

t_perfil = obter_espessura(perfil_escolhido);

raio_max_pa_base = (raio_mm - corda_mm / 2) + diametro_encaixe_mm / 2;
raio_max_pa_topo = (raio_mm - corda_mm / 2) + abs(deslocamento_radial_topo())
    + diametro_encaixe_mm / 2;

diametro_disco_inferior_mm =
    (2 * (raio_max_pa_base + folga_disco_inferior_mm))
    * fator_escala_disco_inferior;
diametro_disco_superior_mm =
    (2 * (raio_max_pa_topo + folga_disco_superior_mm))
    * fator_escala_disco_superior;

// ----------------------------------------------------------------
// POSIÇÃO CENTRALIZADA DE CADA EXTREMIDADE DA PÁ (fonte única)
// ----------------------------------------------------------------
function raio_encaixe_base() = raio_mm - corda_mm / 2;
function raio_encaixe_topo() = raio_mm - corda_mm / 2 + deslocamento_radial_topo();
function angulo_encaixe_base() = 0;
function angulo_encaixe_topo() = torcao_total_graus() + defasagem_angular_discos_graus;

// ----------------------------------------------------------------
// PERFIL AERODINÂMICO (SD7080 TABULADO E NACA 4 DÍGITOS SIMÉTRICO)
// ----------------------------------------------------------------
sd7080_norm_pts = [
    // Extradorso (x=0 -> x=1)
    [0.00000,  0.00000], [0.00107, -0.00297], [0.01190, -0.00059],
    [0.03200,  0.00703], [0.05808,  0.01638], [0.08926,  0.02627],
    [0.12497,  0.03609], [0.16462,  0.04538], [0.20767,  0.05379],
    [0.25357,  0.06104], [0.30177,  0.06694], [0.35174,  0.07131],
    [0.40297,  0.07403], [0.45498,  0.07503], [0.50729,  0.07428],
    [0.55948,  0.07189], [0.61116,  0.06808], [0.66183,  0.06307],
    [0.71099,  0.05710], [0.75815,  0.05040], [0.80279,  0.04321],
    [0.84438,  0.03577], [0.88233,  0.02833], [0.91605,  0.02116],
    [0.94494,  0.01451], [0.96838,  0.00868], [0.98572,  0.00405],
    [0.99639,  0.00105], [1.00000,  0.00000],
    // Intradorso (x=1 -> x=0)
    [0.98739,  0.00004], [0.95508,  0.00028], [0.91068,  0.00067],
    [0.85832,  0.00100], [0.79981,  0.00099], [0.73642,  0.00038],
    [0.66939, -0.00100], [0.59999, -0.00319], [0.52946, -0.00612],
    [0.45907, -0.00956], [0.39006, -0.01319], [0.32356, -0.01662],
    [0.26071, -0.01950], [0.20257, -0.02153], [0.15014, -0.02247],
    [0.10435, -0.02212], [0.06599, -0.02032], [0.03576, -0.01696],
    [0.01424, -0.01194], [0.00201, -0.00520]
];

function perfil_pontos_sd7080() =
    [ for (p = sd7080_norm_pts)
        [p[0] * corda_mm, orientacao_camber_sd7080 * p[1] * corda_mm] ];

function y_naca(t, x) =
    (t / 0.2) * (0.2969 * sqrt(x) - 0.1260 * x - 0.3516 * pow(x, 2)
        + 0.2843 * pow(x, 3) - 0.1015 * pow(x, 4));

function perfil_pontos_naca(t, n) =
    concat(
        [ for (i = [0 : n - 1]) let (x = i / (n - 1))
            [x * corda_mm, y_naca(t, x) * corda_mm] ],
        [ for (i = [0 : n - 1]) let (x = (n - 1 - i) / (n - 1))
            [x * corda_mm, -y_naca(t, x) * corda_mm] ]
    );

function perfil_pontos_selecionado(perfil, t, n) =
    (perfil == "SD7080" || perfil == "sd7080")
        ? perfil_pontos_sd7080()
        : perfil_pontos_naca(t, n);

module perfil_2d() {
    rotate([0, 0, 90])
        polygon(perfil_pontos_selecionado(perfil_escolhido, t_perfil, n_pontos_perfil));
}

// ----------------------------------------------------------------
// PÁ HELICOIDAL
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

    // Encaixe inferior
    translate([raio_encaixe_base(), 0,
        -(comprimento_encaixe_mm + espessura_disco_mm + sobreposicao_contato_mm)])
        cylinder(d = diametro_encaixe_mm,
            h = comprimento_encaixe_mm + espessura_disco_mm + sobreposicao_contato_mm);

    // Encaixe superior
    rotate([0, 0, torcao_efetiva_topo])
        translate([raio_encaixe_topo(), 0, altura_mm])
            cylinder(d = diametro_encaixe_mm,
                h = comprimento_encaixe_mm + espessura_disco_mm + sobreposicao_contato_mm);
}

// ----------------------------------------------------------------
// CUBO CENTRAL E DISCOS DE FIXAÇÃO
// ----------------------------------------------------------------
module cubo_central() {
    alt = espessura_disco_mm;
    difference() {
        cylinder(d = diametro_cubo_mm, h = alt, center = true);
        cylinder(d = diametro_eixo_mm, h = alt + 2, center = true);
    }
}

module disco_fixacao(diametro_disco, inclinacao_disco) 
    rotate([inclinacao_disco, 0, 0])
        difference() {
            cylinder(d = diametro_disco, h = espessura_disco_mm, center = true);
            cylinder(d = diametro_eixo_mm, h = espessura_disco_mm + 2, center = true);
        }
}

// ----------------------------------------------------------------
// CONJUNTO DO ROTOR
// ----------------------------------------------------------------
module rotor_completo() {
    union() {
        for (i = [0 : n_pas - 1]) {
            rotate([0, 0, i * 360 / n_pas])
                pal_helicoidal();
        }

        if (mostrar_discos) {
            translate([0, 0, -comprimento_encaixe_mm / 2])
                disco_fixacao(diametro_disco_inferior_mm,
                    inclinacao_disco_inferior_graus);

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
}

// ----------------------------------------------------------------
// EXECUÇÃO CONTROLADA PELO CUSTOMIZER
// ----------------------------------------------------------------
if (peca_exibida == "rotor_completo") {
    rotor_completo();
} else if (peca_exibida == "pa_unica") {
    pal_helicoidal();
} else if (peca_exibida == "perfil_2d") {
    perfil_2d();
}
