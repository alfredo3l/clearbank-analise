Desafio prático: Análise Financeira com Python
Desafio prático: Análise Financeira com Python
Conheça o projeto
Neste desafio, você vai desenvolver um notebook Python que lê e valida um arquivo CSV de transações bancárias, além de agrupar os dados por mês, calcular métricas financeiras, sinaliza movimentações e exportar o resultado em JSON.

Instruções
Estrutura, regras e requisitos do projeto

Análise Financeira com Python
Introdução
Ao longo deste módulo você aprendeu os fundamentos práticos de Python aplicados à análise de dados: funções e organização de código, tratamento de erros e validação, manipulação de arquivos CSV e JSON, trabalho com datas, uso de bibliotecas e estruturas de repetição. Este desafio final é o momento de unir tudo isso em um único projeto real.

Cenário
Você foi contratado como analista de dados júnior por uma fintech chamada ClearBank. A equipe de operações exporta mensalmente o histórico de transações dos clientes em um arquivo CSV, mas esse arquivo chega com problemas frequentes: campos vazios, valores inválidos, datas mal formatadas e registros duplicados.

Sua missão é desenvolver um notebook Python (.ipynb) que:

Leia e valide o arquivo de transações.
Processe os dados limpos para gerar métricas financeiras mensais.
Sinalize transações potencialmente suspeitas.
Exiba um relatório formatado no terminal.
Salve o resultado da análise em um arquivo JSON.
O arquivo de entrada que você receberá (ou criará para testes) é o transacoes.csv, com as seguintes colunas:

Coluna	Tipo esperado	Descrição
id	inteiro	Identificador único da transação
data	texto	Data no formato AAAA-MM-DD
cliente_id	texto	Código do cliente (não pode ser vazio)
tipo	texto	credito ou debito
valor	decimal	Valor da transação (deve ser maior que 0)
descricao	texto	Descrição livre da operação
categoria	texto	Ex.: salario, compra, transferencia
Exemplo de arquivo transacoes.csv:

id,data,cliente_id,tipo,valor,descricao,categoria
1,2026-01-05,CLI001,credito,3500.00,Salário janeiro,salario
2,2026-01-12,CLI002,debito,180.50,Supermercado,compra
3,2026-01-20,CLI001,debito,abc,Erro de sistema,compra
4,2026-02-03,,debito,200.00,Sem cliente,transferencia
5,2026-02-14,CLI003,credito,15000.00,Transferência suspeita,transferencia
6,2026-02-18,CLI002,debito,320.00,Conta de luz,conta
7,2026-03-01,CLI001,credito,3500.00,Salário março,salario
8,2026-03-10,CLI003,debito,99.90,Streaming,assinatura
Atenção: Você deve criar o arquivo transacoes.csv manualmente antes de executar o notebook. O arquivo deve seguir a estrutura de colunas acima, conter pelo menos 15 registros válidos distribuídos em 3 ou mais meses, 5 registros inválidos para testar a validação e pelo menos 2 transações com valor acima de R$ 10.000,00. Consulte a célula de instruções no início do notebook para mais detalhes.

Requisitos do Desafio
Requisitos Obrigatórios
Cada requisito está mapeado para os conteúdos estudados. Todos precisam estar presentes e funcionando corretamente.

Leitura do arquivo CSV com módulo nativo
Conteúdo relacionado: Manipulação de Arquivos CSV e JSON

Utilize o módulo csv nativo do Python (sem pandas) para leitura.
Use csv.DictReader para acessar as colunas pelo nome.
Trate o caso em que o arquivo não existe (FileNotFoundError).
Validação e limpeza dos dados
Conteúdo relacionado: Tratamento de Erros e Validação de Dados

Antes de processar qualquer transação, valide cada linha. Descarte silenciosamente (sem parar o programa) as linhas que tiverem:

id vazio ou não numérico.
cliente_id vazio.
data em formato inválido (diferente de AAAA-MM-DD).
tipo diferente de credito ou debito.
valor não numérico ou menor ou igual a zero.
Ao final da leitura, exiba no terminal um resumo da limpeza:

Total de linhas lidas: 8
Linhas válidas: 6
Linhas inválidas: 2
Organização do código em funções
Conteúdo relacionado: Funções e Organização do Código

O script deve ter no mínimo quatro funções com responsabilidades claramente separadas. Sugestão de divisão:

Função	Responsabilidade
ler_transacoes()	Lê o CSV e retorna a lista de transações brutas
validar_transacao()	Valida uma única linha e retorna o registro limpo
gerar_relatorio()	Agrupa os dados e calcula as métricas
salvar_json()	Salva o resultado no arquivo relatorio.json
exibir_relatorio()	Formata e imprime os resultados no terminal
Você pode criar mais funções se achar necessário. O importante é que o código não seja um bloco único e que cada função tenha uma responsabilidade clara.

Manipulação de datas com datetime
Conteúdo relacionado: Datas e Tempo para Análise de Dados

Converta a coluna data de texto para objeto datetime usando strptime.
Use a data para extrair o mês de cada transação no formato AAAA-MM.
Calcule quantos dias se passaram desde a transação mais antiga e a mais recente presentes nos dados.
Agrupamento mensal e métricas
Conteúdo relacionado: Estruturas de Repetição, Datas e Tempo

Para cada mês presente nos dados, calcule:

Quantidade total de transações.
Soma dos valores de transações do tipo credito.
Soma dos valores de transações do tipo debito.
Saldo do mês (credito - debito).
Valor médio por transação.
Transação de maior valor no mês.
Transação de menor valor no mês.
Exemplo de saída esperada no terminal:

===== RELATÓRIO MENSAL =====

Mês: 2026-01
  Transações: 2
  Total crédito: R$ 3.500,00
  Total débito:  R$ 180,50
  Saldo:         R$ 3.319,50
  Média:         R$ 1.840,25
  Maior valor:   R$ 3.500,00
  Menor valor:   R$ 180,50
Identificação de transações suspeitas
Conteúdo relacionado: Tratamento de Erros e Validação, Estruturas Condicionais

Defina no início do script uma constante:

LIMITE_SUSPEITO = 10000.00
Qualquer transação com valor acima desse limite deve ser marcada como suspeita. Ao final do relatório, liste as transações suspeitas com id, cliente_id, data e valor.

Exemplo:

===== TRANSAÇÕES SUSPEITAS =====
ID: 5 | Cliente: CLI003 | Data: 2026-02-14 | Valor: R$ 15.000,00
Se não houver transações suspeitas, exiba: Nenhuma transação suspeita encontrada.

Exportação do relatório em JSON
Conteúdo relacionado: Manipulação de Arquivos CSV e JSON

Salve o relatório no arquivo relatorio.json com a seguinte estrutura:

{
  "gerado_em": "2026-05-14",
  "total_transacoes_validas": 6,
  "total_transacoes_invalidas": 2,
  "resumo_mensal": {
    "2026-01": {
      "quantidade": 2,
      "total_credito": 3500.00,
      "total_debito": 180.50,
      "saldo": 3319.50,

Tratamento de erros com try/except
Conteúdo relacionado: Tratamento de Erros e Validação de Dados

Use try/except em pelo menos três situações distintas:

Abertura do arquivo CSV (caso o arquivo não exista).
Conversão do campo valor para float.
Conversão do campo data para datetime.
O programa não pode encerrar abruptamente por causa de um dado inválido em uma linha. Erros em linhas individuais devem ser capturados, a linha descartada e o processamento continua normalmente.

Exibição formatada no terminal
Conteúdo relacionado: Funções e Organização do Código, Estruturas de Repetição

O relatório exibido no terminal deve ser legível e organizado. Requisitos mínimos:

Separadores visuais entre seções (ex.: =====).
Valores monetários formatados com duas casas decimais e o prefixo R$.
Exibição do período analisado (data mais antiga → data mais recente).
Exibição do total de transações válidas e inválidas.
Requisitos Opcionais
Os requisitos opcionais não são obrigatórios, mas demonstram domínio de ferramentas profissionais de análise de dados. Implemente um ou ambos para obter os pontos extras.

Análise com pandas
Conteúdo relacionado: Bibliotecas e pip

Implemente uma versão alternativa da leitura e do agrupamento usando pandas:

Use pd.read_csv() para carregar os dados.
Use groupby para agrupar por mês e calcular as métricas.
Compare os resultados com os obtidos pela solução nativa (os valores devem ser iguais).
Crie essa versão em um arquivo separado chamado analise_pandas.py para não misturar com a solução principal.

Visualização com matplotlib
Conteúdo relacionado: Bibliotecas e pip

Gere ao menos um gráfico com matplotlib e salve como imagem (grafico.png):

Opção A: Gráfico de barras com o saldo mensal (crédito − débito por mês).
Opção B: Gráfico de linha com a evolução do total de débitos ao longo dos meses.
Opção C: Gráfico de barras empilhadas com crédito e débito por mês.
O gráfico deve ter: título, rótulos nos eixos e legenda quando aplicável.

Checklist Antes de Enviar o Projeto
Antes de publicar o repositório no GitHub, revise cada item abaixo:

Código
 A Célula de Execução Principal roda do início ao fim sem erros.
 O código possui pelo menos 4 funções com responsabilidades separadas.
 try/except está presente em pelo menos 3 situações distintas.
 O arquivo relatorio.json é gerado corretamente ao executar o notebook.
 O relatório formatado é exibido no terminal (saída da célula de execução).
Notebook
 Todas as células foram executadas — sem nenhuma com erro ou saída em branco.
 As saídas das células de teste estão visíveis no notebook.
 O notebook está salvo com as saídas (File → Save no Colab).
Repositório
 O repositório no GitHub está público.
 O notebook .ipynb está no repositório com as saídas salvas.
 O repositório possui um README.md básico.
Opcional
 Se implementou RO1: a célula de pandas está funcionando e exibe o resultado.
 Se implementou RO2: grafico.png está salvo e incluído no repositório.
Observações Finais sobre a Entrega
Formato obrigatório: O projeto deve ser publicado em um repositório público no GitHub contendo o notebook .ipynb. Entregas por e-mail, Google Drive ou qualquer outro meio não serão aceitas.

Notebook com saídas salvas: O notebook deve ser entregue com todas as células executadas e as saídas visíveis. Um notebook sem saídas não permite avaliar se o código funciona.

Código todo em uma única célula não será aceito: Toda a lógica concentrada em uma célula sem funções resultará em desconto automático no critério de organização (R3).

Plágio: O projeto é individual. Código idêntico ou muito semelhante ao de outro aluno resultará em nota zero para ambos, sem exceções.

Bibliotecas externas: Se optar por usar pandas ou matplotlib (requisitos opcionais), o Colab já os possui instalados. Para rodar localmente, use:

pip install pandas matplotlib
Compatibilidade: O notebook deve rodar com Python 3.10 ou superior, tanto no Google Colab quanto no Jupyter Notebook local.

Nomeação dos arquivos de saída: Os arquivos gerados devem se chamar exatamente relatorio.json e, se houver gráfico, grafico.png. Nomes diferentes serão desconsiderados na avaliação.

Dicas para Realizar o Desafio
Por onde começar?
Crie o transacoes.csv antes de tudo. Monte o arquivo com dados variados: registros válidos, campos vazios, valores inválidos e datas mal formatadas. Isso garante que você terá dados para testar cada parte do notebook.

Siga a ordem das células. O notebook já está organizado na sequência correta: leitura → validação → datas → métricas → JSON → relatório.

Use os testes rápidos de cada parte. Cada célula tem um bloco de teste no final. Execute-a após implementar para confirmar que está correto antes de avançar.

Só execute a Célula Principal quando tudo estiver implementado. Ela chama todas as funções juntas — use-a como validação final.

Salve o notebook com as saídas antes de enviar. No Colab: File → Save ou Ctrl+S.

Dicas por requisito
Requisito	Dica
CSV	Use with open(...) para garantir que o arquivo seja fechado mesmo em caso de erro.
Validação	Crie uma função só para validar a data e outra só para validar o valor. Isso facilita o reuso e os testes.
Funções	Se uma função está passando de 20 linhas, provavelmente ela faz coisa demais. Divida.
Datas	Use datetime.strptime(data_texto, "%Y-%m-%d") para converter e strftime("%Y-%m") para extrair o mês.
Métricas	Use um dicionário com o mês como chave. Ex.: resumo["2026-01"]["total_credito"] += valor.
Suspeitas	Defina LIMITE_SUSPEITO = 10000.00 no topo do arquivo. Dentro do laço de validação, compare e adicione a uma lista separada.
JSON	Use json.dump(dados, arquivo, ensure_ascii=False, indent=2) para gerar o JSON formatado e com acentos corretos.
try/except	Nunca use except genérico sem intenção. Prefira capturar ValueError, FileNotFoundError ou KeyError de forma específica.
Terminal	Use f-strings para formatar valores monetários: f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") para o padrão brasileiro.
Módulos de referência
Consulte os materiais estudados durante o módulo conforme avança no desafio:

Funções → 01-funcoes-e-organizacao-do-codigo.md
Validação e erros → 02-tratamento-de-erros-e-validacao.md
CSV e JSON → 03-manipulacao-de-arquivos-csv-json.md
Datas → 04-datas-e-tempo-para-analise.md
Bibliotecas e pip → 05-bibliotecas-e-pip.md
Laços de repetição → 06-estruturas-de-repeticao.md
Como Será Feita a Entrega
A entrega é feita exclusivamente via repositório público no GitHub contendo o notebook .ipynb.

Estrutura esperada do repositório
clearbank-analise/
├── desafio-final.ipynb     ← notebook com seu código e saídas salvas  ✅ obrigatório
├── grafico.png             ← (opcional) gráfico do matplotlib
└── README.md               ← descrição básica do projeto               ✅ obrigatório
Passo a passo
Salve o notebook com todas as células executadas — no Colab: File → Save (ou Ctrl+S).
Baixe o arquivo — no Colab: File → Download → Download .ipynb.
Crie um repositório público no 
github.com
 com o nome clearbank-analise.
Faça o upload do notebook .ipynb e, se houver, do grafico.png.
Envie o link do repositório conforme o canal de entrega indicado pelo professor.
O que deve constar no README.md
O README.md deve conter no mínimo:

Título e descrição do projeto.
Como executar (abrir no Colab ou Jupyter e rodar todas as células em ordem).
O que o notebook gera como saída.
Exemplo mínimo de README.md:

Link de entrega
Após publicar o repositório, envie o link público do repositório no GitHub, no desafio, assim seu desafio será avaliado pelo nosso time.

Considerações Finais
Este desafio representa um projeto de análise de dados de verdade. Não é apenas sobre fazer o código funcionar, é sobre escrever código que outra pessoa consegue ler, entender e executar.

Se em algum momento você travar, releia o material do módulo correspondente ao requisito que está tentando implementar. Os exemplos dos arquivos de referência foram pensados exatamente para situações como essa.