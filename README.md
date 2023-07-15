📜 Índice
===

- [Grupo](#group)
- [Sobre o trabalho](#about)
- [Pré-requisitos](#install)
- [Configuração](#setup)
- [Entrada](#input)
- [Execução](#exe)

## 👥 Grupo <a name="group"></a>

- Manoel Silva
- Daniel Arruda Ponte
- Dhener Rosemiro

## 📚 Sobre o projeto <a name="about"></a>
Este trabalho trata-se de um algoritmo que faz a análise léxica de um arquivo com variáveis e expressões numéricas e o transforma em uma árvore sintática,
calculando seus valores sem ambiguidade.

## 🔨 Pré-requisitos <a name="install"></a>

Para executar o projeto você precisará ter instaladas as seguintes ferramentas:

### Ferramentas
- [Python](https://www.python.org/downloads/)

### Versões das Ferramentas
- Python (>= 3.10)

## 🔧 Configuração <a name="setup"></a>

- Extraia o projeto e abra o terminal no diretório raiz.

## 💾 Entrada <a name="input"></a>
Todas as entradas devem respeitar o seguinte padrão:
- Atribuições devem ser instanciadas como:
   ```
   x = exp
   ``` 
- Comandos de impressão devem ser instanciadas como:
   ```
   @exp
   ``` 

> **⚠️ Atenção: Após os comandos, é obrigatório pular uma linha (opcional no final do arquivo).**
## 🚀 Execução <a name="exe"></a>
Há várias formas de executar o programa, no diretório raiz do projeto:

1. Execute o seguinte comando no terminal para passar a entrada como *entrada padrão*:

   ```bash
   python3 main.py < entrada.txt
   ```
2. Execute o seguinte comando no terminal para passar a entrada como *argumento*:

   ```bash
   python3 main.py entrada.txt
   ```
> 💡 Caso queira executar a rotina de teste embutida no projeto, execute o seguinte comando:

   ```bash
   python3 main.py -test
   ```

<p align="right"><a href="#top">Voltar ao topo</a></p>
