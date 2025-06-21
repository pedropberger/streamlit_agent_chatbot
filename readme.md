# Chatbot Interface com Histórico

## Visão Geral

Esta é uma aplicação web construída com Streamlit que permite interagir com um agente de IA via API. Os usuários podem enviar prompts, visualizar respostas, acessar o histórico de chats na barra lateral e interagir com as respostas (copiar ou avaliar). A aplicação se integra a uma API em localhost:1234 que recebe um payload no formato {"prompt": "texto do prompt"} e retorna {"resposta": "texto da resposta"}.

![Chatbot Interface Screenshot](https://via.placeholder.com/800x450.png?text=Chatbot+Interface+Screenshot)

## Funcionalidades

- **Interface de Chat Moderna**: Design intuitivo com bolhas de mensagens para uma experiência de chat natural.
- **Envio de Prompts**: Insira um prompt e receba respostas do agente de IA.
- **Histórico de Chats**: Visualize e pesquise conversas anteriores na barra lateral, organizadas por data.
- **Conversas Contínuas**: Opção para manter o contexto da conversa, enviando o histórico completo para a API.
- **Interação com Respostas**: Copie respostas para a área de transferência ou avalie-as (positivo/negativo).
- **Gerenciamento de Histórico**: Capacidade de limpar todo o histórico de conversas.
- **Indicador de Status da API**: Visualização clara do status da conexão com a API.

## Pré-requisitos

- Python 3.8 ou superior
- Streamlit (pip install streamlit)
- Biblioteca requests (pip install requests)
- API do agente de IA rodando em localhost:1234

## Instalação

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/chatbot-interface.git
cd chatbot-interface
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Certifique-se de que a API do agente de IA está rodando em localhost:1234.

4. Execute a aplicação:
```bash
streamlit run app.py
```
ou
```bash
python run.py
```

## Como Usar

1. **Iniciar a Aplicação**: Acesse a interface no navegador (geralmente em http://localhost:8501).

2. **Enviar uma Mensagem**:
   - Digite seu prompt no campo de texto na parte inferior
   - Marque "Remember conversation context" se desejar manter o contexto da conversa
   - Clique em "Send Message"

3. **Visualizar Respostas**:
   - As respostas aparecem em bolhas de mensagem na área principal
   - Use os botões abaixo da resposta para avaliar (👍/👎) ou copiar o texto

4. **Gerenciar Histórico**:
   - Visualize conversas anteriores na barra lateral
   - Use a caixa de pesquisa para encontrar conversas específicas
   - Clique em uma conversa para revisá-la
   - Use o botão "🗑️ Clear" para limpar todo o histórico

5. **Continuar Conversas**:
   - Ao visualizar uma conversa do histórico, clique em "Continue This Conversation" para retomá-la
   - Use "Start New Chat" para iniciar uma nova conversa

## Modos de Conversa

A aplicação suporta dois modos de conversa:

1. **Modo Padrão**: Cada prompt é enviado independentemente para a API.
2. **Modo Contínuo**: O histórico completo da conversa é enviado com cada novo prompt, permitindo que a API mantenha o contexto da conversa.

Para ativar o modo contínuo, marque a opção "Remember conversation context" ao enviar uma mensagem.

## Estrutura do Projeto

- **app.py**: Arquivo principal da aplicação Streamlit.
- **run.py**: Script auxiliar para verificar dependências e iniciar a aplicação.
- **test_api.py**: Script para testar a conexão e funcionalidade da API.
- **requirements.txt**: Lista de dependências do Python.
- **history.json**: Arquivo para armazenar o histórico de chats localmente.
- **PRD.md**: Documento de requisitos do produto.
- **TODO.md**: Lista de tarefas pendentes.
- **api_howtouse.md**: Documentação sobre como usar a API.

## Consumindo a API Diretamente

Para consumir a API diretamente, você pode usar:

### Usando cURL:
```bash
curl -X POST http://localhost:1234/api/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Olá, esta é uma mensagem de teste"}'
```

### Usando Python:
```python
import requests
import json

url = "http://localhost:1234/api/prompt"
payload = {"prompt": "texto string aqui"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
```

## Funcionalidades da API

- **Endpoint principal**: POST /api/prompt
- **Porta**: 1234
- **Formato de entrada**: {'prompt': "texto string aqui"}
- **Formato de saída**: {'resposta': "texto string aqui recebido com sucesso"}
- **Endpoint de saúde**: GET /health para verificar se a API está funcionando

## Contribuição

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (git checkout -b feature/nova-funcionalidade).
3. Commit suas alterações (git commit -m 'Adiciona nova funcionalidade').
4. Envie para o repositório remoto (git push origin feature/nova-funcionalidade).
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

## Contato

Para dúvidas ou sugestões, entre em contato com [seu-email@exemplo.com].