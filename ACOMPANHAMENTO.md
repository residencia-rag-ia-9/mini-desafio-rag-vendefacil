# Acompanhamento - Mini Desafio RAG VendeFácil

**Integrante 1:** Luiz Carlos Gomes da Silva Junior - @luizcarlos001
**Integrante 2:** Silvio Lima - @silviolima07

**Repositório:** `rag-vendefacil-residencia-ia-rag-9`

## Encontro 0 - 2026-08-24

**Etapa:** 0 - Criação de organização, repositorio e fork do template do mini-desafio

### Relato individual - [Nome do Integrante 1]

### Relato individual - Silvio Lima

 Fomos divididos em duplas e fiz o processo de criação de organização, fiz criação do repositório e fiz um fork do repósitorio do professor.

### Resumo do dia (escrito em conjunto)

Preparação do ambiente.
- criação de organização
- criação de repositório -rag-ia-puc-9
- fork do repositório do professor: vendefacil

**Ficou pendente:**
-

**Bloqueios em aberto:**
-

**Próximo passo (início do encontro 2):**
-

**Uso de assistentes de IA:**
-

---




## Encontro 1 - 2026-08-26

**Etapa:** 1 - Ingestão heterogênea, metadados e indexação vetorial

### Relato individual - [Nome do Integrante 1]

<!-- Escreva você mesmo, em primeira pessoa. O que implementou, que decisão tomou e por quê, onde travou. -->

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
- Etapa 1 finalizada.
- arquivos lidos, estrategias aplicadas por tipo, indices FAISS criados, teste de recuperação e busca feitos com resultado ok.
- gerado notebook com os codigos aplicados.

**Ficou pendente:**
-

**Bloqueios em aberto:**
-

**Próximo passo (início do encontro 2):**
-

**Uso de assistentes de IA:**
- Sim, para criar as funções usadas.

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
