# Acompanhamento - Mini Desafio RAG VendeFácil

**Integrante 1:** Luiz Carlos Gomes da Silva Junior - [@luizcarlos001](https://github.com/luizcarlos001)

**Integrante 2:** Silvio Lima - [@silviolima07](https://github.com/silviolima07)

**Repositório:** `rag-vendefacil-residencia-ia-rag-9`

---

## Encontro 0 - 2026-08-24

**Etapa:** 0 - Criação de organização, repositório e preparação do mini-desafio

### Relato individual - Luiz Carlos Gomes da Silva Junior

Neste primeiro encontro, comecei pela organização do ambiente e pela análise da estrutura do desafio. Revisei os tipos de arquivos presentes na base e procurei entender como cada formato deveria ser tratado nas próximas etapas.

Também analisei as estratégias de chunking e os metadados obrigatórios que deveriam acompanhar os documentos, como `source_file`, `doc_type`, `chunk_id` e `sensitivity`. Além disso, ajudei na organização inicial do repositório e deixei preparado o ambiente para começar a implementação da etapa de ingestão.

Utilizei o ChatGPT como apoio para entender melhor os requisitos da atividade, organizar a divisão do trabalho e revisar as estratégias possíveis para o processamento dos diferentes formatos. Neste encontro ainda não comecei a implementação dos loaders.

### Relato individual - Silvio Lima

Fomos divididos em duplas e fiz o processo de criação de organização, fiz criação do repositório e fiz um fork do repositório do professor.

### Resumo do dia (escrito em conjunto)

Preparação do ambiente.

- Criação da organização;

- Criação do repositório `rag-ia-puc-9`;

- Fork do repositório do professor: VendeFácil;

- Análise inicial da estrutura dos dados;

- Levantamento dos formatos e estratégias de ingestão.

**Ficou pendente:**

- Implementação dos loaders;

- Geração dos chunks e metadados;

- Criação do índice vetorial.

**Bloqueios em aberto:**

- Nenhum bloqueio técnico neste momento.

**Próximo passo (início do encontro 1):**

- Iniciar a implementação da Etapa 1, começando pelos loaders e pela padronização dos metadados.

**Uso de assistentes de IA:**

- ChatGPT utilizado como apoio na análise dos requisitos, organização da atividade e estudo das estratégias de chunking e metadados.

---

## Encontro 1 - 2026-08-26

**Etapa:** 1 - Ingestão heterogênea, metadados e indexação vetorial

### Relato individual - Luiz Carlos Gomes da Silva Junior

Neste encontro trabalhei diretamente na implementação da Etapa 1 do desafio. Comecei desenvolvendo e testando os loaders dos arquivos estruturados, tratando os arquivos CSV de clientes, funcionários, vendas e logs, além dos arquivos JSON de produtos e lojas.

Depois avancei para os demais formatos presentes na base, incluindo JSONL, Markdown, TXT e PDF. A estratégia de chunking foi adaptada de acordo com o tipo de documento. Nos arquivos CSV e JSON, cada registro foi mantido como um chunk. Nos tickets em JSONL, cada ticket foi tratado como uma unidade. Nos arquivos Markdown, foi utilizada a estrutura de cabeçalhos para preservar melhor as seções dos documentos, enquanto TXT e PDF receberam estratégias específicas de divisão.

Também trabalhei na padronização dos metadados. Todos os chunks passaram a possuir os campos obrigatórios `source_file`, `doc_type`, `chunk_id` e `sensitivity`. Quando disponíveis, também foram adicionados campos como `customer_id`, `state`, `module`, `priority`, `status`, `date` e `section`.

Após integrar e revisar os loaders, executei a validação dos documentos e obtive um total de 5.720 chunks válidos. Em seguida, gerei os embeddings utilizando o modelo `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, criei o índice vetorial utilizando FAISS e salvei o índice em disco.

Também implementei e executei o teste de sanidade. O índice FAISS foi recarregado utilizando `load_local`, sem realizar uma nova indexação, e foram realizadas três consultas de teste, retornando os cinco chunks mais similares para cada pergunta.

Utilizei o ChatGPT como apoio durante a implementação para revisar a estrutura dos loaders, identificar erros, adaptar o código à estrutura real dos dados e organizar os testes. As sugestões utilizadas foram revisadas, ajustadas e testadas diretamente no projeto.

### Relato individual - Silvio Lima

Fiz a leitura dos dados, no inicio estava fazendo apenas de semi_structured. Depois Luiz dividiu por tipo e fiquei com md, txt, pdf, json e jsonl.

Acabei pegando os diretórios de unstructured e structured. Fiz a compressão dos diretórios e no colab fiz a extração.

Mas como o trabalho pediu para criar apenas uma função para ler todos os formatos de dados e aplicar estrategia adaptiva para cada tipo.

Fiz isso e para cada tipo uma estrategia diferente foi usada.

Foram gerados os indexes FAISS, os indexes foram comprimidos em podem ser salvos localmente.

Fiz um teste recuperação com 3 perguntas sobre os documentos lidos, recuperando corretamente, 5 chunks mais semelhantes.

Fiz um teste usando a informação de ano-mes que existe como metadado em cada chunk, resultado correto.

Em todos os 3 testes feitos, as 5 respostas foram corretas.

### Resumo do dia (escrito em conjunto)

**Entregamos hoje:**

- Etapa 1 finalizada;

- Arquivos lidos e estratégias aplicadas de acordo com cada tipo;

- Implementação dos loaders para CSV, JSON, JSONL, Markdown, TXT e PDF;

- Padronização e validação dos metadados;

- 5.720 chunks validados;

- Geração dos embeddings;

- Índice FAISS criado e salvo localmente;

- Recarga do índice sem necessidade de reindexação;

- Teste de recuperação com três perguntas e cinco chunks mais semelhantes;

- Testes dos metadados e recuperação realizados com resultado correto;

- Gerado notebook com os códigos aplicados.

**Ficou pendente:**

- Revisão conjunta da implementação;

- Organização final dos commits da dupla;

- Início da Etapa 2.

**Bloqueios em aberto:**

- Nenhum bloqueio técnico no momento.

**Próximo passo (início do encontro 2):**

- Iniciar a implementação da busca híbrida, combinando busca vetorial e BM25;

- Implementar análise e normalização das consultas;

- Adicionar filtragem utilizando os metadados já preparados na Etapa 1.

**Uso de assistentes de IA:**

- Luiz: ChatGPT utilizado como apoio na implementação e revisão dos loaders, organização dos metadados, correção de erros durante os testes e estruturação da indexação vetorial com FAISS.

- Silvio: Sim, para criar as funções usadas.

---

## Encontro 2 - 2026-08-28

**Etapa:** 2 - Busca híbrida e filtragem por metadados

### Relato individual - Luiz Carlos Gomes da Silva Junior

Neste encontro trabalhei na implementação da Etapa 2, responsável pela recuperação híbrida e pela utilização dos metadados durante as buscas.

Implementei um Query Analyzer baseado em regras para identificar informações presentes na pergunta, como estado, módulo e tipo de documento. Também foi adicionada normalização dos valores, tratando diferenças de caixa e acentuação, além da validação dos filtros com os valores que realmente existem nos documentos indexados.

Na recuperação, combinei a busca vetorial utilizando o índice FAISS da Etapa 1 com uma busca lexical utilizando BM25. Para combinar os resultados das duas estratégias, implementei o Reciprocal Rank Fusion (RRF), utilizando `k=60`.

Também implementei a filtragem por metadados durante a recuperação. Foram realizados testes comparando os resultados com e sem filtros para consultas relacionadas a tickets de Minas Gerais no módulo estoque, São Paulo no módulo Pay e Rio de Janeiro no módulo PDV.

Nos testes sem filtro foram retornados documentos de diferentes tipos, como atas, e-mails, clientes e logs. Com os filtros ativados, os resultados ficaram restritos aos tickets correspondentes ao estado e módulo solicitados, mostrando que a filtragem estava funcionando corretamente.

Também iniciei a Etapa 3 criando o schema de saída com Pydantic. Foram definidos os modelos `SourceEvidence` e `RAGResponse`, incluindo validação para impedir respostas sem evidências e garantir consistência nas recusas. Iniciei ainda os guardrails de LGPD e validei um teste de recusa para consulta de salário individual.

Utilizei o ChatGPT como apoio para revisar a implementação da busca híbrida, simplificar o código, estruturar o RRF, validar o uso dos filtros e revisar as regras de saída estruturada e LGPD. As implementações foram executadas e testadas localmente antes do commit.

### Relato individual - Silvio Lima

Tive alguns problemas com a versão das libs, resolveu quando usei o requirements gerado na etapa1.
Fiz a implementacao da busca por FAISS e BM25.
A partir das respostas de cada um foi aplicado o RRF.
Achei bem interessante a lógica de busca hibrida, não conhecia esse algoritmo.
A função analyze_query, não tinha a informação de source e inclui pois indicar a origem de uma resposta, aumenta a confiabilidade e rastreabilidade.
Fiz os testes com 3 perguntas enviadas para cada buscador, antes identifiquei os metadados extraidos e seus valores. 
Os valores que apareciam na query foram usados como filtros nos buscadores.
As respostas de cada buscador foram combinadas. Quando um documento esta presente em ambos, apenas um é considerado e o resultado enviado ao RRF.


### Resumo do dia (escrito em conjunto)

**Entregamos hoje:**

- Etapa 2 finalizada.
- notebook gerado com os codigos e testes realizados.

- Implementação do Query Analyzer baseado em regras;

- Normalização e validação dos filtros extraídos das perguntas;

- Busca vetorial utilizando FAISS;

- Busca lexical utilizando BM25;

- Implementação da fusão dos rankings utilizando RRF com `k=60`;

- Aplicação de filtros por `state`, `module` e `doc_type`;

- Comparação dos resultados com e sem filtros em três consultas;

- Testes da busca híbrida executados com sucesso;

- Início da Etapa 3 com criação do schema Pydantic;

- Implementação inicial dos guardrails de LGPD;

- Teste de recusa para solicitação de salário individual realizado com sucesso.

**Ficou pendente:**

- Finalizar os testes da Etapa 3;

- Testar respostas normais com geração pelo LLM;

- Testar mascaramento de dados pessoais;

- Testar perguntas fora do escopo;

- Revisar a integração entre recuperação, geração e saída estruturada.

**Bloqueios em aberto:**

- Configuração e validação da chave de API para execução das consultas que utilizam o LLM.

**Próximo passo (início do encontro 3):**

- Continuar a Etapa 3;

- Finalizar os guardrails de LGPD;

- Validar respostas com evidências e citações;

- Testar recusas, mascaramento e perguntas fora do escopo.

**Uso de assistentes de IA:**

- Luiz: ChatGPT utilizado como apoio na implementação e revisão da busca híbrida, filtros, RRF, schema Pydantic e guardrails de LGPD.

- Silvio: Usei para gerar as funções, entender o funcionamento e estudos.

---

## Encontro 3 - AAAA-MM-DD

**Etapa:** 3 - Síntese estruturada, evidência e guardrails de LGPD

### Relato individual - [Nome do Integrante 1]

### Relato individual - [Nome do Integrante 2]

### Resumo do dia (escrito em conjunto)

**Entregamos hoje:**

-

**Ficou pendente:**

-

**Bloqueios em aberto:**

-

**Próximo passo (início do encontro 4):**

-

**Uso de assistentes de IA:**

-

---

## Encontro 4 - AAAA-MM-DD

**Etapa:** 4 - Avaliação (RAG Triad), interface e relatório

### Relato individual - [Nome do Integrante 1]

### Relato individual - [Nome do Integrante 2]

### Resumo do dia (escrito em conjunto)

**Entregamos hoje:**

-

**Ficou pendente:**

-

**Bloqueios em aberto:**

-

**Preparação para o Demo Day:**

-

**Uso de assistentes de IA:**

-

---

*TIC em Trilhas · PUC-Rio · Instituto ECOA · MCTI Futuro · Softex*