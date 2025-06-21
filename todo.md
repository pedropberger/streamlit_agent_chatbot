TODO - Chatbot Interface com Streamlit

Tarefas Pendentes

1. Configuração Inicial




[x] Configurar o ambiente virtual Python e instalar dependências (streamlit, requests).



[x] Criar o arquivo app.py com a estrutura básica do Streamlit.



[x] Configurar o arquivo requirements.txt com dependências necessárias.

2. Integração com a API




[x] Implementar função para enviar POST requests para localhost:1234 com payload {"prompt": "texto do prompt"}.



[x] Tratar erros da API (ex.: timeout, resposta inválida) e exibir mensagens amigáveis ao usuário.



[x] Testar a integração com a API em localhost:1234.

3. Interface do Usuário




[x] Criar layout com Streamlit:




[x] Área principal com campo de texto para prompt e botão "Enviar".



[x] Exibição da resposta da API abaixo do campo de texto.



[x] Barra lateral para histórico de chats.



[x] Adicionar botões de interação:




[x] Botão "Copiar" para copiar a resposta para a área de transferência.



[x] Botões de avaliação (polegares para cima/baixo) para cada resposta.



[x] Garantir design responsivo e feedback visual (ex.: confirmação de cópia).

4. Histórico de Chats




[x] Implementar armazenamento do histórico (prompt + resposta + avaliação) em memória (ex.: lista no st.session_state).



[x] Adicionar suporte opcional para salvar o histórico em um arquivo JSON (history.json).



[x] Exibir histórico na barra lateral com resumo (ex.: trecho do prompt e resposta).



[x] Permitir clique em um chat do histórico para exibir detalhes na área principal.

5. Testes




[x] Testar envio de prompts e recebimento de respostas em diferentes cenários.



[x] Testar funcionalidades de copiar e avaliar respostas.



[x] Testar o histórico de chats (exibição e navegação).



[x] Verificar tratamento de erros (API indisponível, entrada inválida).

6. Melhorias Implementadas




[x] Implementar interface de chat moderna com bolhas de mensagens.



[x] Implementar busca no histórico de chats.



[x] Adicionar suporte a conversas contínuas com contexto.



[x] Adicionar botão para limpar todo o histórico de chats.



[x] Melhorar a organização do histórico por data.



[x] Adicionar indicadores visuais para o status da API.

7. Melhorias Futuras




[ ] Adicionar suporte a temas (claro/escuro) no Streamlit.



[ ] Adicionar suporte a armazenamento persistente em banco de dados (ex.: SQLite).



[ ] Permitir edição de prompts diretamente no histórico.



[ ] Implementar exportação de conversas em formato PDF ou texto.



[ ] Adicionar suporte a anexos e imagens nas conversas.

8. Documentação




[x] Atualizar README.md com instruções detalhadas de instalação e uso.



[x] Documentar funções principais no código (app.py).



[ ] Revisar e completar PRD.md com eventuais ajustes.

Prioridades Atuais




Melhorar a experiência do usuário com interface mais intuitiva.



Adicionar funcionalidades para gerenciamento de conversas.



Implementar recursos avançados de busca e filtragem no histórico.



Expandir a documentação do projeto.



Adicionar testes automatizados para garantir estabilidade.