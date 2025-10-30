# hud_tkinter.py
# ===========================================
# Interface gráfica (HUD) com Tkinter
# ===========================================

import tkinter as tk
from tkinter import messagebox
from logica import montar_arvore, Fila


class TriagemHUD:
    def __init__(self, master):
        self.master = master
        master.title("Protocolo de Manchester")
        master.geometry("550x460")
        master.configure(bg="#202225")

        # Montar lógica
        self.arvore = montar_arvore()
        self.filas = {cor: Fila() for cor in ["Vermelho", "Laranja", "Amarelo", "Verde", "Azul"]}

        # Elementos visuais
        tk.Label(
            master, text="Nome do Paciente:",
            fg="white", bg="#202225", font=("Segoe UI", 11)
        ).pack(pady=5)

        self.entry_nome = tk.Entry(master, width=40, font=("Segoe UI", 11))
        self.entry_nome.pack(pady=5)

        tk.Button(
            master, text="Cadastrar Paciente", font=("Segoe UI", 10, "bold"),
            bg="#3a82f7", fg="white", command=self.iniciar_triagem
        ).pack(pady=10)

        tk.Button(
            master, text="Chamar Próximo Paciente", font=("Segoe UI", 10, "bold"),
            bg="#3af77c", fg="black", command=self.chamar_paciente
        ).pack(pady=5)

        # Caixa de status das filas (atualizada automaticamente)
        tk.Label(
            master, text="Status das Filas (atualiza automaticamente):",
            fg="white", bg="#202225", font=("Segoe UI", 10, "italic")
        ).pack(pady=(15, 5))

        self.text_status = tk.Text(
            master, height=10, width=60,
            bg="#2f3136", fg="white",
            font=("Consolas", 10),
            relief="flat", wrap="word"
        )
        self.text_status.pack(pady=5)

        # Botão de saída
        tk.Button(
            master, text="Encerrar", bg="#d63a3a", fg="white",
            font=("Segoe UI", 10, "bold"), command=self.master.quit
        ).pack(pady=10)

        # Atualiza o status inicial e agenda atualização automática
        self.mostrar_status()
        self.atualizar_periodicamente()

    # ---------------------------
    # Funções principais
    # ---------------------------
    def iniciar_triagem(self):
        nome = self.entry_nome.get().strip()
        if not nome:
            messagebox.showwarning("Erro", "Digite o nome do paciente.")
            return

        cor = self.perguntar(self.arvore)
        self.filas[cor].enqueue(nome)
        messagebox.showinfo("Classificação", f"{nome} foi classificado como {cor}.")
        self.entry_nome.delete(0, tk.END)
        self.mostrar_status()

    def perguntar(self, nodo):
        """Percorre a árvore usando popups para cada pergunta."""
        if nodo.is_leaf():
            return nodo.cor
        resposta = messagebox.askyesno("Pergunta", nodo.question)
        return self.perguntar(nodo.yes if resposta else nodo.no)

    def chamar_paciente(self):
        for cor in ["Vermelho", "Laranja", "Amarelo", "Verde", "Azul"]:
            if len(self.filas[cor]) > 0:
                nome = self.filas[cor].dequeue()
                messagebox.showinfo("Chamando Paciente", f"Chamando {nome} ({cor})")
                self.mostrar_status()
                return
        messagebox.showinfo("Info", "Nenhum paciente nas filas.")

    def mostrar_status(self):
        """Atualiza o painel de status com as filas coloridas."""
        self.text_status.delete("1.0", tk.END)
        cores_visual = {
            "Vermelho": "#ff4b4b",
            "Laranja": "#ff914d",
            "Amarelo": "#ffde59",
            "Verde": "#9aff71",
            "Azul": "#5bc0de"
        }
        for cor, fila in self.filas.items():
            cor_formatada = f"{cor:<9}"
            self.text_status.insert(tk.END, f"{cor_formatada}: {len(fila)} paciente(s)\n", (cor,))
            self.text_status.tag_config(cor, foreground=cores_visual[cor])

    def atualizar_periodicamente(self):
        """Atualiza o status das filas automaticamente a cada 5 segundos."""
        self.mostrar_status()
        self.master.after(5000, self.atualizar_periodicamente)  # 5000 ms = 5 segundos


# ---------------------------
# Execução do programa
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TriagemHUD(root)
    root.mainloop()
