import streamlit as st
import pandas as pd

st.set_page_config(page_title='Finanças', page_icon='💵')

st.markdown("""

# Boas vindas!
            
## Nosso APP Financeiro!

Espero que você goste da experiência da nossa solução para organização financeira.             


            """)
# Widget de upload
file_upload = st.file_uploader(label='Faça o upload do seu arquivo aqui:', type=['csv'])
if file_upload:

    #Leitura do arquivo
    df = pd.read_csv(file_upload)
    df['Data'] = pd.to_datetime(df['Data'], format='%m/%d/%Y').dt.date
    
    #exibição do arquivo no App
    exp1 = st.expander('Dados brutos')
    columns_fmt = {"Valor": st.column_config.NumberColumn('Valor', format='%.0f Kz')}
    exp1.dataframe(df, hide_index=True, column_config=columns_fmt)

    #Visão instituição
    exp2 = st.expander('Instituições')
    df_instituicoes = df.pivot_table(index='Data', columns='Instituição', values='Valor')

    tab_data, tab_history, tab_share = exp2.tabs(['Dados', 'Histórico', 'Distribuição'])

    with tab_data:
        st.dataframe(df_instituicoes)

    with tab_history:    
        st.line_chart(df_instituicoes)

    # Obtém a última data dos dados
    with tab_share: 
        date = st.date_input('Data para a distribuição',
                            min_value=df_instituicoes.index.min(),
                            max_value=df_instituicoes.index.max())
        
        if date not in df_instituicoes.index:
            st.warning('Ponha uma data válida!')

        else:


            st.bar_chart(df_instituicoes.loc[date])