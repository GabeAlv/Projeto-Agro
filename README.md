# STS - Dashboard de Monitoramento Agrícola & Sensoriamento Espacial

Frontend desenvolvido em **Python** utilizando **Flet** com foco em agricultura de precisão, monitoramento via satélite/drones (NDVI), telemetria climática e previsão com Machine Learning.
Frontend desenvolvido em **Python** utilizando **Flet** com foco em agricultura de precisão, monitoramento de talhões agrícolas, telemetria climática e previsão com Machine Learning.

---

## 📸 Layout e Funcionalidades

- **Sidebar de Navegação**: Acesso rápido a Dashboard, Mapa de Talhões, Sensores IoT, Relatórios, Notificações e Configurações.
- **Sidebar de Navegação**: Acesso dinâmico a Dashboard, Mapa de Talhões, Sensores IoT, Relatórios, Notificações e Configurações.
- **Cabeçalho STS**: Identidade visual moderna com indicador de sincronização em tempo real e thumbnail da propriedade.
- **Monitoramento Espacial (NDVI)**:
  - Sobreposição interativa dos talhões agrícolas (*Norte 01*, *Leste 02*, *Sul 03*, *Oeste 04*).
- **Monitoramento Espacial dos Talhões**:
  - Sobreposição interativa dos talhões agrícolas (*Norte 01*, *Leste 02*, *Sul 03*, *Oeste 04*) sobre imagem aérea de alta resolução (`assets/crop_field.jpg`).
  - Coordenadas geográficas em tempo real (`19°45'08"S | 47°55'42"W`).
  - Caixa de Legenda NDVI por faixas de produtividade e estresse.
- **Página do Mapa de Talhões**:
  - Opção de **Ampliar / Reduzir Mapa** para visualização imersiva.
  - Painel de detalhes agronômicos do talhão selecionado (Cultura, Variedade, Plantio, DAP, Umidade por profundidade, Fitossanitário e Manejo).
  - Tabela resumo dos talhões com seleção bidirecional.
- **Parâmetros Climáticos**:
  - Destaque para temperatura atual (30°C) e condição de céu ("Sol com Nuvens").
  - Indicadores de Umidade do Ar (58%), Velocidade do Vento (12 km/h) e Insolação (0.4 W/m²).
- **Alertas & Notificações Preditivas**:
  - Alerta de Estresse Hídrico (Talhão Sul 03 - Previsão de ML).
  - Alerta de Queda de Umidade do Solo (Talhão Oeste 04 - Modelo Preditivo).
- **Métricas Históricas 24h (Gráficos Sparkline)**:
  - Temperatura do Ar (28°C / +1.2)
  - Umidade do Ar (65% / -3)
  - Temperatura do Solo (24°C / +0.8)
  - Umidade do Solo (42% / -2)

---

## 📁 Estrutura do Projeto

```
Projeto Agro/
├── assets/
│   ├── satellite_field.png   # Imagem de fundo aérea dos talhões
│   ├── drone_crop_field.jpg  # Fundo alternativo em alta resolução
│   ├── crop_field.jpg        # Imagem de fundo aérea dos talhões
│   └── farm_thumb.png        # Miniatura da fazenda
├── components/
│   ├── __init__.py
│   ├── sidebar.py            # Navegação vertical
│   ├── base_card.py          # Card base compartilhado
│   ├── sidebar.py            # Navegação vertical com rotas dinâmicas
│   ├── header.py             # Topbar com logo e status
│   ├── map_card.py           # Painel de satélite com talhões e legenda NDVI
│   ├── map_card.py           # Painel de mapa do dashboard
│   ├── map_full_view.py      # Mapa expandido com ferramentas e talhões interativos
│   ├── talhao_detail_card.py # Painel de detalhes agronômicos do talhão
│   ├── talhoes_table_card.py # Tabela resumo dos talhões
│   ├── weather_card.py       # Card de parâmetros atuais do clima
│   ├── alerts_card.py        # Alertas e notificações de IA/ML
│   └── sensor_chart_card.py  # Gráficos em canvas de 24h dos sensores
├── pages/
│   ├── __init__.py
│   ├── dashboard_page.py     # Página do Dashboard Geral
│   └── map_page.py           # Página do Mapa de Talhões
├── mock_data.py              # Dados chumbados desacoplados
├── database.py               # Estrutura e migração SQLite
├── theme.py                  # Paleta de cores dark e constantes
├── main.py                   # Ponto de entrada da aplicação Flet
├── main.py                   # Ponto de entrada da aplicação Flet com roteamento
└── README.md
```

---

## 🚀 Como Executar

### 1. Pré-requisitos
Certifique-se de ter o Python instalado e instale os pacotes:
```bash
pip install flet matplotlib pillow
```

### 2. Executar como Aplicativo Desktop
```bash
python main.py
```

### 3. Executar como Aplicativo Web no Navegador
```bash
flet run main.py --web
```

### Novas seções

- **Sensores IoT:** seleção de um dispositivo por talhão, com temperatura do ar, umidade do solo, umidade do ar, histórico ilustrativo e estado offline.
- **Relatórios:** escolha de todos os dispositivos ou de um talhão, geração de prévia e download de PDF A4 com as leituras e notificações relacionadas. O PDF é gerado com a biblioteca padrão do Python.
- **Notificações:** alertas e indicações com filtros por tipo e dispositivo.
- **Configurações:** dados da propriedade, regras de alerta, apelidos e vínculos dos sensores, dados do relatório e página inicial. A página mantém o rascunho ao navegar, valida os campos e permite salvar, descartar ou revisar os valores padrão antes de restaurar.

As três seções usam dados de demonstração centralizados em `telemetry.py`, pois a tabela `sensor_readings` do SQLite ainda não contém leituras. A data do relatório identifica a geração do arquivo, não a coleta das leituras.

As configurações são salvas em `user_settings.json`, na pasta do projeto, e compartilhadas pelas sessões desta instalação. O arquivo é local e não é versionado. O nome da propriedade aparece no cabeçalho; os dados da propriedade e o responsável técnico aparecem na prévia e no PDF. A seleção padrão do relatório é por talhão ou todos os dispositivos. Alterar a página inicial vale na próxima abertura.

As regras de alerta são aplicadas ao mesmo conjunto de demonstração no Dashboard, em Notificações e nos relatórios: temperatura acima do limite, umidades abaixo dos limites e ausência de comunicação a partir do tempo definido. O sensor STS-IOT-04 simula 45 minutos sem comunicação; os limites iniciais são exemplos, não recomendações agronômicas. Desativar os alertas mantém as indicações informativas. O vínculo entre sensor e talhão é único; ao trocar um sensor de talhão, suas leituras de demonstração acompanham o dispositivo. A prévia e o PDF preservam os dados e configurações do momento da geração.

Para verificar persistência, validação e integrações:

```bash
python -m unittest discover -s tests -v
```

---

## 🗄️ Integração com Banco de Dados SQLite

O arquivo `database.py` já contém a estrutura das tabelas criada (`talhoes`, `weather_parameters`, `notifications`, `sensor_readings`). Quando quiser alternar dos dados mockados para o SQLite, basta ler diretamente dessas tabelas.

