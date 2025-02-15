import os
import json
from dataclasses import dataclass
from typing import List, Optional
import sys
from pathlib import Path

@dataclass
class Aluno:
    matricula: int
    nome: str
    nota: float

class SistemaAlunos:
    def __init__(self, arquivo_dados: str = "alunos.json"):
        self.arquivo_dados = arquivo_dados
        self.alunos: List[Aluno] = []
        self.carregar_dados()

    def carregar_dados(self) -> None:
        """Carrega os dados dos alunos do arquivo JSON."""
        try:
            if Path(self.arquivo_dados).exists():
                with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.alunos = [Aluno(**aluno) for aluno in dados]
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")

    def salvar_dados(self) -> None:
        """Salva os dados dos alunos em arquivo JSON."""
        try:
            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                json.dump([vars(aluno) for aluno in self.alunos], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")

    def buscar_aluno(self, matricula: int) -> Optional[Aluno]:
        """Busca um aluno pela matrícula."""
        return next((aluno for aluno in self.alunos if aluno.matricula == matricula), None)

    def cadastrar_aluno(self) -> None:
        """Cadastra um novo aluno."""
        try:
            matricula = int(input("Matrícula do Aluno: "))
            if self.buscar_aluno(matricula):
                print("Erro: Matrícula já existe!")
                return

            nome = input("Nome do Aluno: ").strip()
            if not nome:
                print("Erro: Nome não pode ser vazio!")
                return

            nota = float(input("Nota do Aluno: "))
            if not 0 <= nota <= 10:
                print("Erro: Nota deve estar entre 0 e 10!")
                return

            self.alunos.append(Aluno(matricula=matricula, nome=nome, nota=nota))
            self.salvar_dados()
            print("Aluno cadastrado com sucesso!")
        except ValueError:
            print("Erro: Digite valores válidos!")

    def listar_alunos(self) -> None:
        """Lista todos os alunos cadastrados."""
        if not self.alunos:
            print("Nenhum aluno cadastrado.")
            return

        print("\nLista de Alunos:")
        print("-" * 50)
        print(f"{'Matrícula':<10} {'Nome':<30} {'Nota':<10}")
        print("-" * 50)
        for aluno in self.alunos:
            print(f"{aluno.matricula:<10} {aluno.nome:<30} {aluno.nota:<10.2f}")
        print("-" * 50)

    def alterar_nota(self) -> None:
        """Altera a nota de um aluno."""
        try:
            matricula = int(input("Matrícula do aluno: "))
            aluno = self.buscar_aluno(matricula)
            if not aluno:
                print("Aluno não encontrado!")
                return

            print(f"Nota atual: {aluno.nota}")
            nova_nota = float(input("Digite a nova nota: "))
            if not 0 <= nova_nota <= 10:
                print("Erro: Nota deve estar entre 0 e 10!")
                return

            aluno.nota = nova_nota
            self.salvar_dados()
            print("Nota atualizada com sucesso!")
        except ValueError:
            print("Erro: Digite valores válidos!")

    def excluir_aluno(self) -> None:
        """Exclui um aluno do sistema."""
        try:
            matricula = int(input("Matrícula do aluno: "))
            aluno = self.buscar_aluno(matricula)
            if not aluno:
                print("Aluno não encontrado!")
                return

            self.alunos.remove(aluno)
            self.salvar_dados()
            print("Aluno excluído com sucesso!")
        except ValueError:
            print("Erro: Digite uma matrícula válida!")

def limpar_tela():
    """Limpa a tela do console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_menu():
    """Exibe o menu principal."""
    return """
    === Sistema de Gestão de Alunos ===

    1 - Cadastrar Aluno
    2 - Listar Alunos
    3 - Alterar Nota
    4 - Excluir Aluno
    5 - Sair

    Escolha uma opção: """

def main():
    sistema = SistemaAlunos()
    
    while True:
        limpar_tela()
        try:
            opcao = int(input(exibir_menu()))
            
            if opcao == 1:
                sistema.cadastrar_aluno()
            elif opcao == 2:
                sistema.listar_alunos()
                input("\nPressione Enter para continuar...")
            elif opcao == 3:
                sistema.alterar_nota()
            elif opcao == 4:
                sistema.excluir_aluno()
            elif opcao == 5:
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida!")
            
        except ValueError:
            print("Por favor, digite um número válido!")
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            sys.exit(0)
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()