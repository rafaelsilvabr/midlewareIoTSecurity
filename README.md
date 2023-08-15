*Projeto para Disciplina Computação Móvel e Ubíqua

# Middleware de Segurança para Dispositivos IoT

Este projeto implementa um middleware de segurança que permite a comunicação segura entre dispositivos IoT e um serviço de mensagens Kafka. O middleware oferece suporte a diferentes protocolos de segurança, dependendo das características do dispositivo e do contexto de comunicação.

## Funcionalidades

- Comunicação segura entre dispositivos IoT e Kafka.
- Suporte a diferentes protocolos de segurança.
- Threaded para melhor desempenho no envio para o Kafka.

## Protocolos e Contextos

A escolha do protocolo criptográfico e do tamanho de chave depende das características do dispositivo IoT e do contexto de comunicação. Aqui estão as recomendações para diferentes contextos:

## Estratégias de Criptografia Disponíveis

O middleware suporta as seguintes estratégias de criptografia:

1. **ECDHE (Diffie-Hellman Elíptico Efêmero):** Adequado para dispositivos com recursos limitados e ambientes com alta latência.

2. **AES (Advanced Encryption Standard):** Ideal para dispositivos com recursos suficientes e ênfase na confidencialidade dos dados.

3. **TLS/SSL (Transport Layer Security / Secure Sockets Layer):** Oferece autenticação do servidor e criptografia da comunicação. Adequado para ambientes onde a comunicação segura é primordial.

4. **Token-Based Authentication:** Útil para autenticar dispositivos em um sistema baseado em APIs.

5. **API Keys:** Recomendado para autenticação básica em dispositivos que não requerem criptografia completa dos dados.

## Recomendações por Contexto

### ECDHE

- Recursos de IoT: Limitados
- Latência de Rede: Alta/Baixa
- Tamanho de Chave: 256+ bits
- Autenticação Mútua: Sim
- Criptografia de Mensagem: Sim
- Complexidade: Moderada

### AES

- Recursos de IoT: Suficientes
- Latência de Rede: Baixa
- Tamanho de Chave: 128/192/256 bits
- Autenticação Mútua: Não
- Criptografia de Mensagem: Sim
- Complexidade: Baixa

### TLS/SSL

- Recursos de IoT: Suficientes
- Latência de Rede: Baixa
- Tamanho de Chave: 2048+ bits
- Autenticação Mútua: Sim
- Criptografia de Mensagem: Sim
- Complexidade: Alta

### Token-Based Authentication

- Recursos de IoT: Todos
- Latência de Rede: Baixa
- Autenticação Mútua: Sim
- Criptografia de Mensagem: Não
- Complexidade: Baixa

### API Keys

- Recursos de IoT: Todos
- Latência de Rede: Baixa
- Tamanho de Chave: 128+ bits
- Autenticação Mútua: Não
- Criptografia de Mensagem: Não
- Complexidade: Baixa

## Tabela de Comparação de Estratégias de Criptografia

| Estratégia                  | Recursos de IoT     | Latência de Rede     | Tamanho de Chave | Autenticação Mútua | Criptografia de Mensagem | Complexidade |
|-----------------------------|---------------------|-----------------------|------------------|-------------------|--------------------------|--------------|
| ECDHE                       | Limitados           | Alta/Baixa            | 256+ bits        | Sim               | Sim                      | Moderada     |
| AES                         | Suficientes         | Baixa                 | 128/192/256 bits| Não               | Sim                      | Baixa        |
| TLS/SSL                     | Suficientes         | Baixa                 | 2048+ bits       | Sim               | Sim                      | Alta         |
| Token-Based Authentication  | Todos               | Baixa                 | Não aplicável    | Sim               | Não                      | Baixa        |
| API Keys                    | Todos               | Baixa                 | 128+ bits        | Não               | Não                      | Baixa        |

## Aviso

Este projeto é um exemplo de implementação de segurança e não deve ser usado em produção sem uma análise completa de segurança e ajustes necessários.
