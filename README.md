# Relatório Técnico: Sistema de Monitoramento IoT

### Identificação do Candidato

**Nome completo:** Marcos Luiz Silva Pedroza
 **GitHub:** marcospedjk

## Visão Geral da Solução

- **Objetivo do projeto:** Desenvolver um firmware robusto em MicroPython para um sistema embarcado simulado voltado à automação e monitoramento IoT.
- **O que o sistema faz:** Realiza a leitura contínua de sensores em ambiente simulado, processa a lógica de controle de acordo com os cenários estabelecidos e reporta o status do sistema via interface serial/mensagens padronizadas.
- **Interação com o usuário:** O sistema opera de forma autônoma e reativa, respondendo a estímulos físicos dos componentes simulados (como botões e variações em sensores) e enviando logs de status em tempo de execução.

## Arquitetura do Sistema Embarcado

A arquitetura lógica foi desenhada para garantir eficiência e evitar gargalos temporais:

- **Fluxo principal (`main.py`):** Inicializa os pinos de I/O, configura os periféricos e entra em um loop principal de monitoramento contínuo.
- **Estrutura de estados e temporizações:** Utiliza uma abordagem não-bloqueante (evitando o uso excessivo de `time.sleep` longos) para garantir que as leituras dos sensores e as respostas aos testes automatizados ocorram na janela temporal correta exigida pelo simulador.
- **Interação entre componentes:** O loop central lê o estado dos sensores, processa a regra de negócio lógica e aciona os atuadores ou atualiza as mensagens de saída de forma síncrona com o clock do simulador.

## Componentes Utilizados na Simulação

Com base na especificação do projeto (`diagram.json`):
- **Unidade de Processamento:** Placa ESP32 DevKit C v4 executando firmware em MicroPython, responsável pelo controle central e gerenciamento de barramentos.

- **Sensor MPU6050:** Acelerômetro e giroscópio integrado via interface I2C (pinos SDA 21 e SCL 22), utilizado para captação de dados de movimento/inclinação.

- **Botão Push-button (Verde):** Chave táctil conectada ao pino digital 4, empregada para simular interações manuais ou eventos de entrada digital pelo usuário.

- **Interface de Comunicação:** Canal serial configurado para monitoramento e envio das mensagens de status exigidas pelos testes automatizados.

## Decisões Técnicas Relevantes

- **Organização do código:** Código modularizado e limpo no `main.py`, facilitando a legibilidade e a depuração.
- **Boas práticas de tempo real:** Abolição de rotinas bloqueantes para assegurar a sincronia exata com o Wokwi CI.
- **Rigidez nas Strings:** Garantia de correspondência exata caractere por caractere nas mensagens de status geradas pelo firmware, assegurando o sucesso nos testes automatizados.


## Resultados Obtidos

- **Comportamento do sistema:** O firmware responde de maneira determinística aos estímulos simulados.
- **Requisitos atendidos:** A comunicação serial atende estritamente ao casamento de strings esperado pela esteira de integração contínua (CI).
- **Validação:** Execução bem-sucedida nos cenários de teste propostos no ambiente do Wokwi.

## Comentários Adicionais

- **Dificuldades encontradas:** O maior desafio inicial foi garantir a precisão temporal sem recorrer a funções de espera bloqueantes (`time.sleep`), visto que a sincronia com os testes automatizados do Wokwi CI exige uma tratativa rigorosa do fluxo de execução do MicroPython.

- **Melhorias futuras:** Com mais tempo de desenvolvimento, seria interessante implementar uma máquina de estados finos (FSM) mais robusta para gerenciar transições complexas e adicionar tratamento de exceções mais refinado para eventuais falhas de leitura nos sensores.

- **Aprendizados:** O projeto proporcionou um excelente aprimoramento prático em programação não-bloqueante para sistemas embarcados, além de consolidar a importância do alinhamento estrito entre o firmware e as especificações de integração contínua (CI).