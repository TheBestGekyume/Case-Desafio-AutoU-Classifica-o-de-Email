# Email Classifier - Sistema de Classificação de Emails

## ✏️ Descrição
O email Email Classifier é uma aplicação web que classifica um email enviado como produtivo ou improdutivo com base nos seguintes parâmetros: 
Produtivo -> Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema).
Improdutivo -> Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos).


## 🚀 Tecnologias Utilizadas

### Backend
- **Python** com FastAPI para a API REST  
- **spaCy** para processamento de linguagem natural em português  
- **Google Gemini API** para classificação via IA  
- **Hugging Face Inference API** caso o Gemini esteja indisponível
- **PyPDF2** para extração de texto de arquivos PDF  
- **Unidecode** para normalização de texto
- **Fallback** caso os serviços de IA estejam indisponíveis

### Frontend
- **React** com TypeScript  
- **Bootstrap** para estilização responsiva  
- **SCSS** para estilos customizados  
- **React Router** para navegação 

### Infraestrutura
- **Render** para deploy do backend  
- **Vercel** para deploy do frontend  
- **Variáveis de ambiente** para configuração de APIs  

---

## 📋 Funcionalidades Principais

### Classificação Inteligente de Emails
- Sistema de fallback hierárquico (**Gemini → Hugging Face → Fallback local**)  
- Processamento de texto com **lematização em português**  
- Identificação de padrões e palavras-chave  

### Múltiplos Métodos de Entrada
- Formulário para inserção manual de **assunto** e **mensagem**  
- Upload de arquivos (**PDF** e **TXT**) com extração automática de conteúdo  

### Sistema de Respostas Automáticas
- Geração de respostas contextualizadas baseadas na categoria  
- Personalização com **nome do remetente**  

### Interface Responsiva
- Design adaptado para **desktop** e **dispositivos móveis**  
- Visualização em tabela dos resultados históricos  
- Experiência de usuário intuitiva  

---

## 🏗️ Estrutura do Projeto

```text
projeto/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── email.py                # Modelo para padronizar o email
│   │   ├── services/
│   │   │   ├── classify_service.py     # Serviço principal de classificação
│   │   │   ├── fallback_service.py     # Classificação local de fallback
│   │   │   ├── file_service.py         # Processamento de arquivos
│   │   │   ├── gemini_service.py       # Integração com Gemini AI
│   │   │   └── huggingface_service.py  # Integração com Hugging Face
│   │   ├── routes/
│   │   │   └── classify.py             # Endpoints da API
│   │   ├── config.py                   # Configurações
│   │   └── main.py                     # Arquivo principal
│   ├── .env                            # Variáveis do backend
│   ├── requirements.txt                # Dependências do backend
│   └── run.py                          # Para rodar o projeto
│                            
└── frontend/
    ├── components/
    │   └── Classifier/
    │       ├── Form/                   # Componente de formulário
    │       └── Result/                 # Componente de resultados
    ├── home.scss                        # Estilos da página inicial
    ├── classifier.scss                  # Estilos do classificador
    ├── Home.tsx                         # Página inicial
    └── Classifier.tsx                   # Página do classificador
```

## 🌐 Endpoints da API

- POST /api/classify - Classifica um email com base no texto ou arquivo
Parâmetros: sender, subject, message ou file
