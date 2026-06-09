import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Configurações de malha
u = np.linspace(0, 2 * np.pi, 60)
v = np.linspace(0, np.pi, 60)
U, V = np.meshgrid(u, v)

# Cores da pele e escalas (Mantendo sua iluminação original)
cores_pele = [(240/255, 210/255, 180/255, 0.35), (230/255, 150/255, 150/255, 0.4), (255/255, 230/255, 120/255, 0.3)]
scales = [1, 0.98, 0.97]

# Músculo Rosa Opaco
cor_musculo = (230/255, 80/255, 110/255, 1.0) 

# Cores de destaque para os elementos faciais (mais escuras para contraste)
cor_rosto_detalhe = (160/255, 110/255, 90/255, 1.0) 
cor_boca = (140/255, 40/255, 40/255, 1.0)

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='3d')

def gerar_elipsoide(a, b, c, ox, oy, oz):
    X = a * np.cos(U) * np.sin(V) + ox
    Y = b * np.sin(U) * np.sin(V) + oy
    Z = c * np.cos(V) + oz
    return X, Y, Z

def update(frame):
    ax.clear()
    ax.set_facecolor("cyan")
    fig.patch.set_facecolor("cyan")

    # --- CAMADAS DE PELE (Tronco e Cabeça) ---
    for i, scale in enumerate(scales):
        # Tronco
        Xt, Yt, Zt = gerar_elipsoide(3.0*scale, 1.2*scale, 1.8*scale, 0, 0, -0.5)
        ax.plot_surface(Xt, Yt, Zt, color=cores_pele[i], edgecolor='none', antialiased=True, shade=True)
        
        # Cabeça (Pele externa)
        Xh, Yh, Zh = gerar_elipsoide(1.2*scale, 1.1*scale, 1.5*scale, 0, 0, 2.0)
        ax.plot_surface(Xh, Yh, Zh, color=cores_pele[i], edgecolor='none', antialiased=True, shade=True)

    # --- MÚSCULO INTERNO (Opaco e visível por baixo) ---
    Xm, Ym, Zm = gerar_elipsoide(0.9, 0.8, 1.2, 0, -0.1, 2.0)
    ax.plot_surface(Xm, Ym, Zm, color=cor_musculo, edgecolor='none', alpha=1.0, shade=True)

    # --- ELEMENTOS FACIAIS COM DESTAQUE ---
    
    # Nariz (Levemente mais escuro que a pele)
    Xn, Yn, Zn = gerar_elipsoide(0.18, 0.28, 0.38, 0, -1.08, 2.0)
    ax.plot_surface(Xn, Yn, Zn, color=cor_rosto_detalhe, alpha=1.0, shade=True)

    # Orelhas (Destaque lateral)
    for side in [-1.15, 1.15]:
        Xe, Ye, Ze = gerar_elipsoide(0.15, 0.12, 0.38, side, 0, 2.1)
        ax.plot_surface(Xe, Ye, Ze, color=cor_rosto_detalhe, alpha=1.0, shade=True)

    # Boca (Tom vinho escuro para contraste máximo)
    Xb, Yb, Zb = gerar_elipsoide(0.38, 0.12, 0.06, 0, -0.98, 1.55)
    ax.plot_surface(Xb, Yb, Zb, color=cor_boca, alpha=1.0)

    # Olhos (Branco Puro e Brilhante)
    for side in [-0.4, 0.4]:
        Xeye, Yeye, Zeye = gerar_elipsoide(0.14, 0.1, 0.12, side, -0.95, 2.3)
        # shade=False faz com que o branco fique "aceso" e constante
        ax.plot_surface(Xeye, Yeye, Zeye, color=(1, 1, 1), alpha=1.0, shade=False)

    # Configurações de visualização
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-1, 4)
    ax.set_box_aspect([1, 1, 1])
    ax.set_axis_off()
    ax.view_init(elev=15, azim=frame)

# Configuração da animação
fps = 120 
frames = np.linspace(0, 360, fps)
ani = FuncAnimation(fig, update, frames=frames, interval=50)

# Salvar o GIF
ani.save('busto_anatomico_destaque.gif', writer='pillow', fps=20)
plt.show()