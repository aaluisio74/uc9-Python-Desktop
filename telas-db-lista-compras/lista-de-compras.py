import tkinter as tk
from tkinter import messagebox
import sqlite3

class ListaCompras:
    def __init__(self, janela):
        self.janela = janela 
        self.janela.title("🛒 Lista de Compras")
        self.janela.geometry("600x550")
        
        self.categorias = ["Hortifrúti", "Mercearia", "Limpeza", "Bebidas", "Padaria"]
        
        self.criar_banco()
        self.criar_interface()
        self.atualizar_lista()
        
    def criar_banco(self):
        conexao = sqlite3.connect("compras.db")
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS itens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade TEXT,
                categoria TEXT 
                )
        """)
        conexao.commit()
        conexao.close()
        
    def criar_interface(self):
        # Título
        tk.Label(
            self.janela, text="🛒 LISTA DE COMPRAS INTELIGENTE",
            font=("Arial", 14, "bold"),
            fg="darkgreen"
        ).pack(pady=10)

            # Frame de entrada
        frame_entrada = tk.LabelFrame(self.janela, text="Novo Item", padx=10, pady=10)
        frame_entrada.pack(pady=10, padx=10, fill="x")
            
            # Nome do item
        tk.Label(frame_entrada, text="Item:").grid(row=0, column=0, pady=5, sticky="w")
        self.entry_nome = tk.Entry(frame_entrada, width=30)
        self.entry_nome.grid(row=0, column=1, pady=5, padx=5)

        # Quantidade
        tk.Label(frame_entrada, text="Quantidade:").grid(row=1, column=0, pady=5, sticky="w")
        self.entry_quantidade = tk.Entry(frame_entrada, width=30)
        self.entry_quantidade.grid(row=1, column=1, pady=5, padx=5)
        self.entry_quantidade.insert(0, "1") # Valor padrão
        
        # Categoria (usando Listbox)
        tk.Label(frame_entrada, text="Categoria:").grid(row=2, column=0, pady=5, sticky="w")
        
        frame_categoria = tk.Frame(frame_entrada)
        frame_categoria.grid(row=2, column=1, pady=5, sticky="w")
        
        self.listbox_categorias = tk.Listbox(
            frame_categoria,
            height=5,
            width=25,
            selectmode="single"
        )
            
        self.listbox_categorias.pack(side="left")
        
        # Preencher categorias
        for cat in self.categorias:
            self.listbox_categorias.insert("end", cat)
        
        # Selecionar primeira categoria por padrão
        self.listbox_categorias.selection_set(0)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(frame_categoria)
        scrollbar.pack(side="right", fill="y")
        self.listbox_categorias.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox_categorias.yview)
        
        # Botões
        frame_botoes = tk.Frame(self.janela)
        frame_botoes.pack(pady=10)
        
        tk.Button(
            frame_botoes,
            text="➕ Adicionar",
            command=self.adicionar_item,
            bg="green",
            fg="white",
            width=12
        ).pack(side="left", padx=5)
        
        tk.Button(
            frame_botoes,
            text="🔄 Limpar",
            command=self.limpar_campos,
            bg="orange",
            fg="white",
            width=12
        ).pack(side="left", padx=5)
        
        tk.Button(
            frame_botoes,
            text="🗑️ Remover",
            command=self.remover_item,
            bg="red",
            fg="white",
            width=12
        ).pack(side="left", padx=5)
        
        # Lista de itens
        frame_lista = tk.LabelFrame(self.janela, text="Itens da Lista", padx=10, pady=10)
        frame_lista.pack(pady=10, padx=10, fill="both", expand=True)
        
        scrollbar_lista = tk.Scrollbar(frame_lista)
        scrollbar_lista.pack(side="right", fill="y")
        
        self.listbox_itens = tk.Listbox(
            frame_lista,
            height=8,
            font=("Courier", 10),
            yscrollcommand=scrollbar_lista.set
        ) 
        self.listbox_itens.pack(side="left", fill="both", expand=True)
        
        scrollbar_lista.config(command=self.listbox_itens.yview)
        
        # Bind de seleção
        self.listbox_itens.bind("<<ListboxSelect>>", self.mostrar_detalhes)
        
        # Label de detalhes
        self.label_detalhes = tk.Label(
            self.janela,
            text="",
            font=("Arial", 10),
            justify="left",
            relief="sunken",
            padx=5,
            pady=5
        )
        self.label_detalhes.pack(pady=5, padx=10, fill="x")
        
    def adicionar_item(self):
        nome = self.entry_nome.get().strip()
        quantidade = self.entry_quantidade.get().strip()
        
        # Pegar categoria selecionada
        selecao_cat = self.listbox_categorias.curselection()
                    
        if not selecao_cat:
            messagebox.showwarning("Aviso", "Selecione uma categoria!")
            return
        categoria = self.listbox_categorias.get(selecao_cat[0])
        
        if not nome:
            messagebox.showwarning("Aviso", "Digite o nome do item!")
            return            
        
        try:
            conexao = sqlite3.connect("compras.db")
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO itens (nome, quantidade, categoria) VALUES (?, ?, ?)
                """, (nome, quantidade, categoria))
            conexao.commit()
            conexao.close()
        
            messagebox.showinfo("Sucesso", "Item adicionado!")
            self.limpar_campos()
            self.atualizar_lista()

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao adicionar: {erro}")
    
    def atualizar_lista(self):
        self.listbox_itens.delete(0, tk.END)
        
        try:
            conexao = sqlite3.connect("compras.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, quantidade, categoria FROM itens ORDER BY categoria, nome")
            itens = cursor.fetchall()
            conexao.close()
        
            for item in itens:
                texto = f"[{item[0]:03d}] {item[1]}"
                if item[2]:
                    texto += f" - {item[2]}"
                texto += f" ({item[3]})"
                self.listbox_itens.insert("end", texto)
        
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao listar: {erro}")
        
    def mostrar_detalhes(self, event):
        selecao = self.listbox_itens.curselection()
        if not selecao:
            return
        
        texto = self.listbox_itens.get(selecao[0])
        try:
            id_str = texto.split("]")[0].replace("[", "")
            id_item = int(id_str)
        
            conexao = sqlite3.connect("compras.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM itens WHERE id = ?", (id_item,))
            item = cursor.fetchone()
            conexao.close()
            
            if item:
                detalhes = f"📦 ID: {item[0]} | Item: {item[1]}\n"
                detalhes += f"🔢 Quantidade: {item[2] if item[2] else 'Não especificada'}\n"
                detalhes += f"📌 Categoria: {item[3]}"
                self.label_detalhes.config(text=detalhes)
        
        except (ValueError, sqlite3.Error):
            self.label_detalhes.config(text="Erro ao carregar detalhes")
            
    def remover_item(self):
        selecao = self.listbox_itens.curselection()
        if not selecao:
            messagebox.showinfo("Aviso", "Selecione um item para remover!")
            return
        
        if messagebox.askyesno("Confirmar", "Remover este item da lista?"):
            texto = self.listbox_itens.get(selecao[0])
            try:
                id_str = texto.split("]")[0].replace("[", "")
                id_item = int(id_str)
                
                conexao = sqlite3.connect("compras.db")
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM itens WHERE id = ?", (id_item,))
                conexao.commit()
                conexao.close()
                
                self.atualizar_lista()
                self.label_detalhes.config(text="")
                messagebox.showinfo("Sucesso", "Item removido!")
            
            except (ValueError, sqlite3.Error):
                messagebox.showerror("Erro", "Falha ao remover item")
                
    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.entry_quantidade.insert(0, "1")
        self.listbox_categorias.selection_clear(0, "end")
        self.listbox_categorias.selection_set(0)
        self.entry_nome.focus()
        
janela = tk.Tk()
app = ListaCompras(janela)
janela.mainloop()
