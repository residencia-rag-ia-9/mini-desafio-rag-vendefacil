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

Depois avancei para os demais formatos presentes na base, incluindo JSONL, Markdown, TXT e PDF. A estratégia de chunking foi adaptada de acordo com o tipo de documento. Nos arquivos CSV e JSON, cada registro foi mantido como um chunk. Nos tickets em JSONL, cada ticket foi tratado como uma unidade, com possibilidade de divisão apenas quando o conteúdo fosse muito extenso. Nos arquivos Markdown, utilizei a estrutura de cabeçalhos para preservar melhor as seções dos documentos. Para TXT e PDF, foi utilizada divisão por tamanho com sobreposição quando necessário.

Também trabalhei na padronização dos metadados. Todos os chunks passaram a possuir os campos obrigatórios `source_file`, `doc_type`, `chunk_id` e `sensitivity`. Quando disponíveis, também foram adicionados campos como `customer_id`, `state`, `module`, `priority`, `status`, `date` e `section`.

Após a integração dos documentos, executei a validação dos chunks e gerei os embeddings utilizando o modelo `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`. Em seguida, criei o índice vetorial utilizando FAISS e salvei o índice em disco.

Também implementei e executei um teste de sanidade para verificar a persistência do índice. O FAISS foi recarregado utilizando `load_local`, sem necessidade de realizar uma nova indexação, e foram realizadas três consultas de teste, recuperando os cinco chunks mais similares para cada pergunta.

Utilizei o ChatGPT como apoio durante a implementação para revisar a estrutura dos loaders, identificar erros, adaptar o código para a estrutura real dos dados e organizar os testes. As sugestões foram ajustadas e testadas diretamente no projeto antes da integração.

### Relato individual - Silvio Lima

<!-- Escreva você mesmo, em primeira pessoa. O que implementou, que decisão tomou e por quê, onde travou. -->

### Resumo do dia (escrito em conjunto)

**Entregamos hoje:**

- Implementação dos loaders para os seis formatos: CSV, JSON, JSONL, Markdown, TXT e PDF;
- Estratégias de chunking adaptadas de acordo com cada tipo de documento;
- Padronização dos metadados dos chunks;
- Validação dos documentos processados;
- Geração dos embeddings;
- Criação e persistência do índice vetorial utilizando FAISS;
- Recarga do índice sem necessidade de reindexação;
- Teste de sanidade com três consultas e recuperação dos cinco chunks mais similares.

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

- ChatGPT utilizado como apoio na implementação e revisão dos loaders, organização dos metadados, correção de erros durante os testes e estruturação da indexação vetorial com FAISS.

---

## Encontro 2 - AAAA-MM-DD

**Etapa:** 2 - Busca híbrida e filtragem por metadados

### Relato individual - [Nome do Integrante 1]

### Relato individual - [Nome do Integrante 2]

### Resumo do dia (escrito em conjunto)

**Entregamos hoje:**

-

**Ficou pendente:**

-

**Bloqueios em aberto:**

-

**Próximo passo (início do encontro 3):**

-

**Uso de assistentes de IA:**

-

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