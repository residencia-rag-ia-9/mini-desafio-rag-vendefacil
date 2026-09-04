# Relatório de Avaliação do Pipeline RAG

## Resumo Geral

- Total de Questões Avaliadas: 24
- Pontuação Média: 0.45 / 1.0
- Taxa de Acerto Total (Pontuação 1.0): 0.00%

## Detalhamento por Categoria de Pergunta

| Categoria                    |   Total de Questões |   Pontuação Média |
|:-----------------------------|--------------------:|------------------:|
| Filtragem por Metadados      |                   4 |              0.2  |
| Fácil (RAG Básico)           |                   5 |              0.5  |
| Guardrails & LGPD            |                   6 |              0.7  |
| Múltiplas Fontes (Multi-hop) |                   3 |              0.37 |
| Políticas Internas           |                   2 |              0.2  |
| Razão & Solução de Problemas |                   4 |              0.45 |

## Análise das 3 Piores Falhas

### Falha: Q04 - Qual é a política de home office para os funcionários da equipe de Engenharia?
- **Pontuação Obtida:** 0.20 / 1.0
- **Diagnóstico da Falha:** Falha na Etapa de Recuperação/Geração (Falso Positivo de Recusa): Uma pergunta que deveria ter sido respondida foi recusada, provavelmente devido à falta de evidências recuperadas ou uma interpretação excessivamente conservadora do LLM.
- **Detalhes:**
```
Query: Qual é a política de home office para os funcionários da equipe de Engenharia?
Ground Truth Answer: A equipe de Engenharia funciona no modelo Remoto First (100% Home Office), com encontros presenciais trimestrais na matriz da empresa.
Ground Truth Expected Sources: ['data/unstructured/policies/home_office.md']
RAG Answer: Não encontrei evidências suficientes para responder.
RAG Confidence: recusado
RAG Is Refusal: True
RAG Refusal Reason: sem_evidencia
RAG Sources Used: []

```

### Falha: Q07 - Listar os logs de erro registrados para o cliente 'CUST008' (Auto Peças Central) no serviço de pagamento (pay).
- **Pontuação Obtida:** 0.20 / 1.0
- **Diagnóstico da Falha:** Falha na Etapa de Recuperação/Geração (Falso Positivo de Recusa): Uma pergunta que deveria ter sido respondida foi recusada, provavelmente devido à falta de evidências recuperadas ou uma interpretação excessivamente conservadora do LLM.
- **Detalhes:**
```
Query: Listar os logs de erro registrados para o cliente 'CUST008' (Auto Peças Central) no serviço de pagamento (pay).
Ground Truth Answer: Os logs para o cliente CUST008 no serviço vendefacil-pay são: 1) TEF_TIMEOUT (Erro PAY-504) - Timeout aguardando resposta do Pinpad IP 192.168.1.105 na porta 6090; 2) TEF_RETRY_FAILED (Erro PAY-502) - Conexão recusada pelo Windows Firewall no host AutoPecas-Caixa01.
Ground Truth Expected Sources: ['data/semi_structured/system_logs.csv']
RAG Answer: Não encontrei evidências suficientes para responder.
RAG Confidence: recusado
RAG Is Refusal: True
RAG Refusal Reason: sem_evidencia
RAG Sources Used: []

```

### Falha: Q06 - Quais chamados com prioridade 'Crítica' foram registrados no sistema e qual é o SLA de solução para esse nível?
- **Pontuação Obtida:** 0.20 / 1.0
- **Diagnóstico da Falha:** Falha na Etapa de Recuperação/Geração (Falso Positivo de Recusa): Uma pergunta que deveria ter sido respondida foi recusada, provavelmente devido à falta de evidências recuperadas ou uma interpretação excessivamente conservadora do LLM.
- **Detalhes:**
```
Query: Quais chamados com prioridade 'Crítica' foram registrados no sistema e qual é o SLA de solução para esse nível?
Ground Truth Answer: O ticket de prioridade Crítica registrado é o TCK-1005 (Auto Peças Central - Transação de TEF aprovada na maquininha porém não finaliza venda no PDV). O SLA de solução para severidade Crítica é de até 2 horas (com primeira resposta em até 15 minutos).
Ground Truth Expected Sources: ['data/semi_structured/tickets.jsonl', 'data/unstructured/policies/atendimento_sla.md']
RAG Answer: A pergunta está fora do escopo da base VendeFácil.
RAG Confidence: recusado
RAG Is Refusal: True
RAG Refusal Reason: fora_de_escopo
RAG Sources Used: []

```

## Próximos Passos (se tivesse mais 4 horas)


- **Melhorar o Query Analyzer e Filtros de Metadados:** Expandir e refinar a lógica de identificação de filtros para o `query_analyzer`, adicionando mais termos, sinônimos e regras complexas para garantir que os filtros de metadados sejam aplicados de forma mais precisa e abrangente na etapa de recuperação. Isso inclui investigar os `table_topics` e `doc_type` nos metadados para construir filtros mais robustos.
- **Tuning Fino dos Prompts:** Realizar testes A/B com diferentes versões dos prompts fornecidos ao LLM, focando na clareza das instruções sobre o uso de evidências, formatação da resposta e critérios para recusa. Isso pode melhorar a aderência do LLM às regras e a qualidade da síntese.
- **Implementar um Avaliador de Respostas com LLM (LLM as a judge):** Desenvolver um módulo separado que utilize um LLM como juiz para comparar semanticamente a `rag_answer` gerada com a `ground_truth_answer` esperada. Isso forneceria uma avaliação mais objetiva e escalável da correção da resposta, superando as limitações da comparação baseada em strings ou heurísticas.
- **Análise Detalhada de Casos de `sem_evidencia`:** Para perguntas que resultaram em recusa por `sem_evidencia`, investigar manualmente os documentos na base de conhecimento para determinar se a informação realmente está ausente ou se a falha ocorreu na recuperação (os documentos relevantes não foram encontrados) ou na interpretação do LLM (os documentos foram encontrados, mas não foram usados).
- **Ajuste dos Parâmetros do RRF e Retrievers:** Experimentar diferentes valores para `k_rrf` e `k` nos retrievers (FAISS e BM25) para otimizar o equilíbrio entre precisão e recall na recuperação de documentos, garantindo que os documentos mais relevantes sejam apresentados ao LLM.
