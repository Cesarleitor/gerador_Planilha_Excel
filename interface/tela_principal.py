
import json


import customtkinter as ctk
from tkinter import messagebox
import os


from services.planilha_service import exportar_planilha as gerar_arquivo_excel

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

itens = []
total_geral = 0.0

def iniciar_sistema():
    janela = ctk.CTk()
    janela.title("Arte Sul")


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def calcular_total_item(event=None):
    try:
        quantidade = int(entrada_quantidade.get())
        valor_unitario = float(entrada_valor_unitario.get().replace(",", "."))

        total = quantidade * valor_unitario

        entrada_total_item.configure(state="normal")
        entrada_total_item.delete(0, "end")
        entrada_total_item.insert(0, formatar_moeda(total))
        entrada_total_item.configure(state="disabled")

    except ValueError:
        entrada_total_item.configure(state="normal")
        entrada_total_item.delete(0, "end")
        entrada_total_item.configure(state="disabled")


def adicionar_item():
    global total_geral

    try:
        codigo = entrada_codigo.get().strip()
        nome_item = entrada_item.get().strip()
        quantidade = int(entrada_quantidade.get())
        valor_unitario = float(entrada_valor_unitario.get().replace(",", "."))

        if not codigo or not nome_item:
            messagebox.showwarning("Aviso", "Preencha o código e o nome do item.")
            return

        total_item = quantidade * valor_unitario

        item = {
            "codigo": codigo,
            "item": nome_item,
            "quantidade": quantidade,
            "valor_unitario": valor_unitario,
            "total": total_item
        }

        itens.append(item)

        linha = len(itens)

        ctk.CTkLabel(frame_lista, text=codigo, width=120, anchor="w").grid(row=linha, column=0, padx=5, pady=5)
        ctk.CTkLabel(frame_lista, text=nome_item, width=220, anchor="w").grid(row=linha, column=1, padx=5, pady=5)
        ctk.CTkLabel(frame_lista, text=str(quantidade), width=120, anchor="w").grid(row=linha, column=2, padx=5, pady=5)
        ctk.CTkLabel(frame_lista, text=formatar_moeda(valor_unitario), width=140, anchor="w").grid(row=linha, column=3, padx=5, pady=5)
        ctk.CTkLabel(frame_lista, text=formatar_moeda(total_item), width=140, anchor="w").grid(row=linha, column=4, padx=5, pady=5)

        total_geral += total_item
        label_total_geral.configure(text=f"Total geral: {formatar_moeda(total_geral)}")

        limpar_campos_item()

    except ValueError:
        messagebox.showerror("Erro", "Digite valores válidos em quantidade e valor unitário.")


def limpar_campos_item():
    entrada_codigo.delete(0, "end")
    entrada_item.delete(0, "end")
    entrada_quantidade.delete(0, "end")
    entrada_valor_unitario.delete(0, "end")

    entrada_total_item.configure(state="normal")
    entrada_total_item.delete(0, "end")
    entrada_total_item.configure(state="disabled")


janela = ctk.CTk()
janela.title("Arte Sul")
janela.geometry("1100x700")

titulo = ctk.CTkLabel(
    janela,
    text="Arte Sul Esculturas Decorativas",
    font=("Arial", 24, "bold")
)
titulo.pack(pady=20)

# Topo
frame_topo = ctk.CTkFrame(janela, fg_color="transparent")
frame_topo.pack(pady=10)

entrada_pedido = ctk.CTkEntry(
    frame_topo,
    width=220,
    height=40,
    placeholder_text="Número do pedido"
)
entrada_pedido.grid(row=0, column=0, padx=10)

entrada_cliente = ctk.CTkEntry(
    frame_topo,
    width=320,
    height=40,
    placeholder_text="Nome do cliente"
)
entrada_cliente.grid(row=0, column=1, padx=10)

# Campos de item
frame_campos = ctk.CTkFrame(janela, fg_color="transparent")
frame_campos.pack(pady=20)

entrada_codigo = ctk.CTkEntry(frame_campos, width=140, height=40, placeholder_text="Código do item")
entrada_codigo.grid(row=0, column=0, padx=5)

entrada_item = ctk.CTkEntry(frame_campos, width=220, height=40, placeholder_text="Item")
entrada_item.grid(row=0, column=1, padx=5)

entrada_quantidade = ctk.CTkEntry(frame_campos, width=120, height=40, placeholder_text="Quantidade")
entrada_quantidade.grid(row=0, column=2, padx=5)

entrada_valor_unitario = ctk.CTkEntry(frame_campos, width=140, height=40, placeholder_text="Valor unitário")
entrada_valor_unitario.grid(row=0, column=3, padx=5)

entrada_total_item = ctk.CTkEntry(frame_campos, width=140, height=40, placeholder_text="Total dos itens")
entrada_total_item.grid(row=0, column=4, padx=5)
entrada_total_item.configure(state="disabled")

entrada_quantidade.bind("<KeyRelease>", calcular_total_item)
entrada_valor_unitario.bind("<KeyRelease>", calcular_total_item)


def novo_pedido():
    global itens, total_geral

    # limpa campos do topo
    entrada_pedido.delete(0, "end")
    entrada_cliente.delete(0, "end")

    # limpa campos do item
    limpar_campos_item()

    # zera dados
    itens.clear()
    total_geral = 0.0
    label_total_geral.configure(text="Total geral: R$ 0,00")

    # remove itens exibidos da lista, mantendo o cabeçalho
    for widget in frame_lista.winfo_children():
        info = widget.grid_info()
        if int(info["row"]) > 0:
            widget.destroy()

    # foca no número do pedido
    entrada_pedido.focus()

# Botão adicionar
botao_adicionar = ctk.CTkButton(
    janela,
    text="Adicionar item",
    width=160,
    height=40,
    command=adicionar_item
)
botao_adicionar.pack(pady=10)

# Lista de itens
frame_lista_container = ctk.CTkFrame(janela, fg_color="transparent")
frame_lista_container.pack(padx=20, pady=20, fill="both", expand=True)

canvas = ctk.CTkCanvas(frame_lista_container)
canvas.pack(side="left", fill="both", expand=True)


scrollbar = ctk.CTkScrollbar(
    frame_lista_container,
    orientation="vertical",
    command=canvas.yview
)
scrollbar.pack(side="right", fill="y")

frame_lista = ctk.CTkFrame(canvas)

frame_lista.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=frame_lista, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

cabecalhos = ["Código", "Item", "Quantidade", "Valor unitário", "Total"]
larguras = [120, 220, 120, 140, 140]

for i, cabecalho in enumerate(cabecalhos):
    ctk.CTkLabel(
        frame_lista,
        text=cabecalho,
        width=larguras[i],
        anchor="w",
        font=("Arial", 14, "bold")
    ).grid(row=0, column=i, padx=5, pady=8)

# Rodapé
frame_rodape = ctk.CTkFrame(janela, fg_color="transparent")
frame_rodape.pack(fill="x", padx=20, pady=20)

label_total_geral = ctk.CTkLabel(
    frame_rodape,
    text="Total geral: R$ 0,00",
    font=("Arial", 18, "bold")
)
label_total_geral.pack(side="left")


def salvar_dados():
    numero_pedido = entrada_pedido.get().strip()
    nome_cliente = entrada_cliente.get().strip()

    if not numero_pedido or not nome_cliente:
        messagebox.showwarning("Aviso", "Preencha o número do pedido e o nome do cliente.")
        return

    if not itens:
        messagebox.showwarning("Aviso", "Preencha ao menos um item do pedido.")
        return

    dados = {
        "pedido": numero_pedido,
        "cliente": nome_cliente,
        "itens": itens,
        "total_geral": total_geral
    }

    nome_arquivo = f"pedido_{numero_pedido}.json"
    caminho_completo = os.path.abspath(nome_arquivo)

    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    messagebox.showinfo("Sucesso", f"Dados salvos em:\n{caminho_completo}")


def exportar_planilha_interface():
    numero_pedido = entrada_pedido.get().strip()
    nome_cliente = entrada_cliente.get().strip()

    if not numero_pedido or not nome_cliente:
        messagebox.showwarning("Aviso", "Preencha o número do pedido e o nome do cliente.")
        return

    if not itens:
        messagebox.showwarning("Aviso", "Adicione ao menos um item ao pedido antes de exportar.")
        return

    nome_arquivo = gerar_arquivo_excel(numero_pedido, nome_cliente, itens)
    caminho_completo = os.path.abspath(nome_arquivo)

    messagebox.showinfo("Exportação concluída", f"Planilha exportada em:\n{caminho_completo}")


frame_botoes = ctk.CTkFrame(frame_rodape, fg_color="transparent")
frame_botoes.pack(fill="x", padx=20, pady=20)


botao_salvar = ctk.CTkButton(
    frame_botoes,
    text="Salvar",
    width=120,
    height=40,
    command=salvar_dados
)
botao_salvar.pack(side="left", padx=5)

botao_exportar = ctk.CTkButton(
    frame_botoes,
    text="Exportar",
    width=120,
    height=40,
    command=exportar_planilha_interface
)
botao_exportar.pack(side="left", padx=5)

botao_novo_pedido = ctk.CTkButton(
    frame_botoes,
    text="Novo Pedido",
    width=120,
    height=40,
    command=novo_pedido
)
botao_novo_pedido.pack(side="left", padx=5)


janela.mainloop()