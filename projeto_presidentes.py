{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 244,
   "id": "79290c7b-eb94-49af-b48c-f08651cf44bf",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "from datetime import datetime"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 246,
   "id": "17e6b680-9ab7-4b90-905a-2f5e57099012",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Leitura do CSV com os dados dos presidentes\n",
    "df = pd.read_csv(\"presidentes.csv\", sep=\";\", encoding=\"latin1\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 248,
   "id": "e7dc38d0-6214-43ec-bfe4-c00c5c2e7bd8",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Convertendo as colunas de datas para o formato datetime\n",
    "def to_date(val):\n",
    "    try:\n",
    "        return pd.to_datetime(val, format=\"%Y-%m-%d\", errors=\"coerce\")  # 'coerce' transforma erros em NaT\n",
    "    except Exception as e:\n",
    "        print(f\"Erro ao converter a data: {val} - Erro: {e}\")\n",
    "        return None\n",
    "\n",
    "df[\"mandato_inicio\"] = df[\"mandato_inicio\"].apply(to_date)\n",
    "df[\"mandato_fim\"] = df[\"mandato_fim\"].apply(to_date)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 250,
   "id": "d10c1360-7d43-4aed-8cd0-507571b3500c",
   "metadata": {},
   "outputs": [
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "Digite sua idade:  29\n"
     ]
    }
   ],
   "source": [
    "# Pegando a idade do usuário e a data de hoje\n",
    "idade_usuario = int(input(\"Digite sua idade: \"))\n",
    "hoje = datetime.today()\n",
    "ano_nasc_usuario = hoje.year - idade_usuario\n",
    "periodo_inicio = datetime(ano_nasc_usuario, 1, 1)\n",
    "periodo_fim = hoje"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 252,
   "id": "f275f413-1c52-4cd2-805e-6dab2637b1f8",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Ajustando a máscara para filtrar corretamente os presidentes\n",
    "mask = (\n",
    "    (df[\"mandato_inicio\"] <= periodo_fim) &  # Mandato começou antes ou durante a vida do usuário\n",
    "    ((df[\"mandato_fim\"].isna()) | (df[\"mandato_fim\"] >= periodo_inicio))  # Mandato terminou depois ou ainda está em andamento\n",
    ")\n",
    "\n",
    "df_filtrado = df[mask].copy()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 254,
   "id": "a5387f38-cc4c-4449-9dcc-819ee3040b57",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Substituindo valores NaN na coluna 'idade_morte' por 'Vivo' ou 'Em exercício'\n",
    "df_filtrado[\"idade_morte\"] = df_filtrado[\"idade_morte\"].fillna(\n",
    "    \"Vivo\" if df_filtrado[\"mandato_fim\"].isna().any() else \"Em exercício\"\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 256,
   "id": "430c4a04-5c37-4db2-9c06-0bc567eccb65",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Formatando as datas para exibição mais legível\n",
    "df_filtrado[\"mandato_inicio\"] = df_filtrado[\"mandato_inicio\"].dt.strftime(\"%d/%m/%Y\")\n",
    "df_filtrado[\"mandato_fim\"] = df_filtrado[\"mandato_fim\"].dt.strftime(\"%d/%m/%Y\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 258,
   "id": "37cea7f6-2ebf-4be6-a8fe-b4d0d9668e28",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Exibindo os resultados com os presidentes e informações\n",
    "resultado = df_filtrado[[\"nome\", \"mandato_inicio\", \"mandato_fim\", \"idade_morte\"]].reset_index(drop=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 260,
   "id": "3838c680-f96b-4461-8002-64da642f236d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "Presidentes em exercício na sua vida:\n",
      "\n",
      "                     nome mandato_inicio mandato_fim  idade_morte\n",
      "Fernando Henrique Cardoso     01/01/1995  01/01/2003         93.0\n",
      "Luiz Inácio Lula da Silva     01/01/2003  01/01/2011 Em exercício\n",
      "           Dilma Rousseff     01/01/2011  31/08/2016 Em exercício\n",
      "             Michel Temer     31/08/2016  01/01/2019 Em exercício\n",
      "           Jair Bolsonaro     01/01/2019  01/01/2023 Em exercício\n",
      "Luiz Inácio Lula da Silva     01/01/2023  23/04/2025 Em exercício\n"
     ]
    }
   ],
   "source": [
    "# Exibindo os presidentes que estavam no cargo na vida do usuário\n",
    "print(\"\\nPresidentes em exercício na sua vida:\\n\")\n",
    "print(resultado.to_string(index=False))"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
