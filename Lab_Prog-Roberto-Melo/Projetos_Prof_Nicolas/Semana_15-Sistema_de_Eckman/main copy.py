

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.gridspec as gridspec

# ──────────────────────────────────────────────
# GEOMETRIA 3D COM DEFORMAÇÃO ANATÓMICA
# ──────────────────────────────────────────────

def cabeca_realista(expr_id, u_res=50, v_res=50):
    u = np.linspace(0, 2*np.pi, u_res)
    v = np.linspace(0, np.pi, v_res)
    U, V = np.meshgrid(u, v)
    
    # Raios base do crânio/rosto
    rx, ry, rz = 0.63, 0.58, 0.75
    
    # Esfera base centralizada em (0, 0, 0.1)
    X = rx * np.cos(U) * np.sin(V)
    Y = ry * np.sin(U) * np.sin(V)
    Z = 0.1 + rz * np.cos(V)
    
    # Aplicar deformações na malha dependendo da expressão
    if expr_id == "alegria":
        # Inflar as bochechas (Z entre -0.1 e 0.3, e para a frente em Y)
        mascara_bochechas = (Z > -0.1) & (Z < 0.3) & (Y > 0)
        Y[mascara_bochechas] += 0.08 * np.sin(V[mascara_bochechas])
        X[mascara_bochechas] *= 1.05
    elif expr_id == "tristeza":
        # Rosto "caído", estica para baixo no queixo
        mascara_queixo = (Z < -0.2)
        Z[mascara_queixo] -= 0.06 * (0.1 - Z[mascara_queixo])
    elif expr_id == "raiva":
        # Testa proeminente franzida (Z alto e Y para a frente)
        mascara_testa = (Z > 0.3) & (Y > 0)
        Y[mascara_testa] += 0.05 * np.cos(U[mascara_testa])
        # Comprimir os lados da face
        X[(Z < 0.2)] *= 0.96
    elif expr_id == "surpresa":
        # Alongamento vertical de toda a cabeça (maxilar desce)
        Z[(Z < 0)] -= 0.12 * np.abs(Z[Z < 0])
        Y[(Z < 0)] -= 0.03 # Recua ligeiramente o maxilar aberto
    elif expr_id == "medo":
        # Rosto tenso, contraído nas laterais e ligeiramente mais alto
        X *= 0.95
        Z[(Z > 0)] += 0.04
        
    return X, Y, Z

def cilindro(cx, cy, z0, z1, r, res=30):
    theta = np.linspace(0, 2*np.pi, res)
    z = np.array([z0, z1])
    theta_g, z_g = np.meshgrid(theta, z)
    x = cx + r * np.cos(theta_g)
    y = cy + r * np.sin(theta_g)
    return x, y, z_g

def micro_esfera_olho(cx, cy, cz, rx, ry, rz, u_res=20, v_res=20):
    # Gerador de malha para os olhos saltarem à frente sem oclusão
    u = np.linspace(0, 2*np.pi, u_res)
    v = np.linspace(0, np.pi, v_res)
    x = cx + rx * np.outer(np.cos(u), np.sin(v))
    y = cy + ry * np.outer(np.sin(u), np.sin(v))
    z = cz + rz * np.outer(np.ones(u_res), np.cos(v))
    return x, y, z

# ──────────────────────────────────────────────
# CONFIGURAÇÃO DE EXPRESSÕES
# ──────────────────────────────────────────────

EXPRESSOES = {
    "Neutro":    {"id": "neutro"},
    "Alegria":   {"id": "alegria"},
    "Tristeza":  {"id": "tristeza"},
    "Raiva":     {"id": "raiva"},
    "Medo":      {"id": "medo"},
    "Surpresa":  {"id": "surpresa"},
    "Nojo":      {"id": "nojo"},
}

CORES_BOTOES = {
    "Neutro":   "#888888",
    "Alegria":  "#F0B429",
    "Tristeza": "#5B9BD5",
    "Raiva":    "#E04040",
    "Medo":     "#9B59B6",
    "Surpresa": "#27AE60",
    "Nojo":     "#8BC34A",
}

def get_cor_pele(expr_id):
    if expr_id == "raiva":   return "#C2634D"
    if expr_id == "medo":    return "#CBD0D6"
    if expr_id == "nojo":    return "#A9B890"
    return "#D4956A"

# ──────────────────────────────────────────────
# INTERFACE E RENDER
# ──────────────────────────────────────────────

class BustoInterativo:
    def __init__(self):
        self.expressao_atual = "Neutro"

        self.fig = plt.figure(figsize=(12, 8), facecolor="#11111e")
        self.fig.canvas.manager.set_window_title("Busto 3D Avançado — Expressões Realistas")

        gs = gridspec.GridSpec(
            len(EXPRESSOES) + 2, 5,
            figure=self.fig,
            left=0.02, right=0.98, top=0.95, bottom=0.05,
            hspace=0.3
        )

        self.ax = self.fig.add_subplot(gs[:, 1:], projection='3d')
        self.ax.set_facecolor("#07070f")
        self.ax.grid(False)
        self.ax.set_axis_off()

        self._criar_painel(gs)
        self._desenhar_busto()

        plt.show()

    def _criar_painel(self, gs):
        ax_titulo = self.fig.add_subplot(gs[0, 0])
        ax_titulo.set_facecolor("#11111e")
        ax_titulo.axis('off')
        ax_titulo.text(0.5, 0.5, "EXPRESSÃO", ha='center', va='center',
                       fontsize=11, fontweight='bold', color='white',
                       transform=ax_titulo.transAxes)

        self.botoes = {}
        for i, (nome, color_hex) in enumerate(CORES_BOTOES.items()):
            ax_btn = self.fig.add_subplot(gs[i + 1, 0])
            btn = Button(ax_btn, nome,
                         color=color_hex if nome == self.expressao_atual else "#22223b",
                         hovercolor=color_hex)
            btn.label.set_color('white')
            btn.label.set_fontsize(10)
            btn.label.set_fontweight('bold')
            btn.on_clicked(self._fazer_expressao(nome))
            self.botoes[nome] = (btn, ax_btn, color_hex)

    def _fazer_expressao(self, nome):
        def callback(event):
            self.expressao_atual = nome
            self._atualizar_botoes()
            self._desenhar_busto()
        return callback

    def _atualizar_botoes(self):
        for nome, (btn, ax_btn, cor_hex) in self.botoes.items():
            ativo = (nome == self.expressao_atual)
            btn.color = cor_hex if ativo else "#22223b"
            ax_btn.set_facecolor(cor_hex if ativo else "#22223b")
        self.fig.canvas.draw_idle()

    def _desenhar_busto(self):
        self.ax.cla()
        self.ax.set_facecolor("#07070f")
        self.ax.set_axis_off()
        
        # Visão frontal absoluta travada no eixo Y
        self.ax.view_init(elev=4, azim=-90)

        expr = self.expressao_atual
        expr_id = EXPRESSOES[expr]["id"]
        cor_pele = get_cor_pele(expr_id)

        # 1. PESCOÇO E OMBROS BASE
        xc, yc, zc = cilindro(0, 0.0, -1.8, -0.4, 0.25)
        self.ax.plot_surface(xc, yc, zc, color=cor_pele, alpha=0.85, linewidth=0.1, edgecolors='#3a2214', zorder=1)

        theta = np.linspace(0, 2*np.pi, 30)
        self.ax.plot_trisurf(0.85 * np.cos(theta), 0.25 * np.sin(theta), np.full_like(theta, -1.8), color=cor_pele, alpha=0.8, zorder=1)

        # 2. MALHA DA CABEÇA MODELADA DINAMICAMENTE
        xh, yh, zh = cabeca_realista(expr_id)
        self.ax.plot_surface(xh, yh, zh, color=cor_pele, alpha=0.98, linewidth=0.2, edgecolors='#4d301f', zorder=2)

        # 3. ORELHAS ANATÓMICAS
        for lado in [-1, 1]:
            xe, ye, ze = micro_esfera_olho(lado * 0.62, 0.0, 0.1, 0.07, 0.09, 0.16)
            self.ax.plot_surface(xe, ye, ze, color=cor_pele, alpha=0.95, linewidth=0, zorder=2)

        # 4. NARIZ MODELADO NO CENTRO
        zn_alvo = -0.02 if expr_id == "surpresa" else 0.02
        xn, yn, zn = micro_esfera_olho(0, 0.46, zn_alvo, 0.07, 0.16, 0.14)
        self.ax.plot_surface(xn, yn, zn, color=cor_pele, alpha=1.0, linewidth=0, zorder=5)

        # ─────────────────────────────────────────────────────────────
        # OLHOS REALISTAS PROJETADOS (Y Avançado para garantir foco)
        # ─────────────────────────────────────────────────────────────
        y_olhos = 0.66
        z_olhos = 0.24 if expr_id != "surpresa" else 0.20 # Olhos acompanham descida da cara
        posicoes_olho = [(-0.23, z_olhos), (0.23, z_olhos)]

        for ox, oz in posicoes_olho:
            # Globo Ocular Branco Real (Com linhas concêntricas densas para volume perfeito)
            for r in np.linspace(0, 0.11, 5):
                t = np.linspace(0, 2*np.pi, 40)
                self.ax.plot(ox + r*np.cos(t), np.full_like(t, y_olhos), oz + r*0.75*np.sin(t), color='#ffffff', linewidth=3, zorder=10)
            
            # Íris Azul Dinâmica (Tamanho muda com a expressão)
            r_iris = 0.045 if expr_id != "surpresa" else 0.035 # Olho arregalado mostra mais o branco
            for r in np.linspace(0, r_iris, 4):
                t = np.linspace(0, 2*np.pi, 30)
                self.ax.plot(ox + r*np.cos(t), np.full_like(t, y_olhos + 0.01), oz + r*np.sin(t), color='#2A6496', linewidth=3.5, zorder=11)
            
            # Pupila Preta Central
            for r in np.linspace(0, 0.018, 2):
                t = np.linspace(0, 2*np.pi, 20)
                self.ax.plot(ox + r*np.cos(t), np.full_like(t, y_olhos + 0.02), oz + r*np.sin(t), color='#0a0a0a', linewidth=3, zorder=12)

            # Contorno das Pálpebras (Superior e Inferior adaptáveis)
            t_p = np.linspace(0, np.pi, 30)
            fator_abertura = 0.08 if expr_id not in ["surpresa", "medo"] else 0.11
            fator_fechamento = -0.08 if expr_id not in ["alegria", "nojo"] else -0.04
            
            # Pálpebra superior
            self.ax.plot(ox + 0.11*np.cos(t_p), np.full_like(t_p, y_olhos + 0.02), oz + fator_abertura*np.sin(t_p), color='#422617', linewidth=4, zorder=13)
            # Pálpebra inferior
            self.ax.plot(ox + 0.11*np.cos(t_p), np.full_like(t_p, y_olhos + 0.02), oz + fator_fechamento*np.sin(t_p), color='#422617', linewidth=2.5, zorder=13)

            # Sobrancelhas Tridimensionais Orgânicas
            lado_fator = 1 if ox > 0 else -1
            t_s = np.linspace(-0.13, 0.13, 15)
            xs = ox + t_s
            ys = np.full_like(t_s, y_olhos + 0.03)
            
            if expr_id == "raiva":
                zs = oz + 0.11 - (0.05 * lado_fator) + (0.04 * t_s * lado_fator)
            elif expr_id == "tristeza":
                zs = oz + 0.14 + (0.04 * lado_fator) - (0.05 * t_s * lado_fator)
            elif expr_id == "surpresa":
                zs = np.full_like(t_s, oz + 0.19)
            elif expr_id == "medo":
                zs = oz + 0.16 + (0.02 * lado_fator) * t_s
            else: # Neutro / Alegria
                zs = oz + 0.11 + 0.02 * np.sin(np.linspace(0, np.pi, 15))
                
            self.ax.plot(xs, ys, zs, color='#26140a', linewidth=6.5, solid_capstyle='round', zorder=15)

        # ─────────────────────────────────────────────────────────────
        # BOCA EXPRESSIVA PROJETADA
        # ─────────────────────────────────────────────────────────────
        y_boca = 0.64
        boca_z = -0.22 if expr_id != "surpresa" else -0.36 # Acompanha o queixo caído

        if expr_id == "alegria":
            t = np.linspace(-0.24, 0.24, 40)
            bz = boca_z + 0.15 * (t / 0.24) ** 2 - 0.04
            self.ax.plot(t, np.full_like(t, y_boca), bz, color='#B53151', linewidth=8, solid_capstyle='round', zorder=14)
            # Linha interna de dentes sorridentes
            self.ax.plot(t*0.8, np.full_like(t*0.8, y_boca + 0.01), bz + 0.03, color='#ffffff', linewidth=2.5, zorder=14)
        elif expr_id == "tristeza":
            t = np.linspace(-0.20, 0.20, 40)
            bz = boca_z - 0.12 * (t / 0.20) ** 2
            self.ax.plot(t, np.full_like(t, y_boca), bz, color='#B53151', linewidth=7.5, solid_capstyle='round', zorder=14)
        elif expr_id == "surpresa":
            # Expressão realista: Cavidade escura da boca aberta em 3D profundo
            for r in np.linspace(0, 0.12, 6):
                t = np.linspace(0, 2*np.pi, 40)
                self.ax.plot(r*0.65*np.cos(t), np.full_like(t, y_boca), boca_z + r*np.sin(t), color='#21050b', linewidth=4.5, zorder=14)
            # Contorno labial exterior
            t = np.linspace(0, 2*np.pi, 40)
            self.ax.plot(0.12*0.65*np.cos(t), np.full_like(t, y_boca + 0.01), boca_z + 0.12*np.sin(t), color='#B53151', linewidth=3, zorder=14)
        elif expr_id == "raiva":
            # Boca tensa ligeiramente aberta mostrando agressividade
            self.ax.plot([-0.16, 0.16], [y_boca, y_boca], [boca_z, boca_z], color='#B53151', linewidth=9, zorder=14)
            self.ax.plot([-0.13, 0.13], [y_boca + 0.01, y_boca + 0.01], [boca_z, boca_z], color='#ffffff', linewidth=2, zorder=15)
        elif expr_id == "medo":
            t = np.linspace(-0.19, 0.19, 40)
            bz = boca_z + 0.025 * np.sin(2 * np.pi * t * 4)
            self.ax.plot(t, np.full_like(t, y_boca), bz, color='#B53151', linewidth=6.5, zorder=14)
        elif expr_id == "nojo":
            t = np.linspace(-0.18, 0.18, 40)
            bz = boca_z + 0.05 * (t + 0.18) - 0.02
            self.ax.plot(t, np.full_like(t, y_boca), bz, color='#B53151', linewidth=7.5, zorder=14)
        else: # Neutro
            self.ax.plot([-0.18, 0.18], [y_boca, y_boca], [boca_z, boca_z], color='#B53151', linewidth=6, solid_capstyle='round', zorder=14)

        # Enquadramento rígido da cena 3D
        lim = 0.85
        self.ax.set_xlim(-lim, lim)
        self.ax.set_ylim(-lim, lim)
        self.ax.set_zlim(-1.3, lim)

        emojis = {
            "Neutro": "😐", "Alegria": "😄", "Tristeza": "😢",
            "Raiva": "😡", "Medo": "😨", "Surpresa": "😲", "Nojo": "🤢"
        }
        self.ax.set_title(f"{emojis.get(expr, '')}  {expr.upper()}  {emojis.get(expr, '')}", 
                          color='white', fontsize=16, fontweight='bold', pad=10)

        self.fig.canvas.draw_idle()

if __name__ == "__main__":
    busto = BustoInterativo()