from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do arquivo .env

url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')

supabase = create_client(url, key)

# 1. Adiciona a coluna sum_period1 (INTEGER) na tabela se não existir
alter_table_sql = '''
ALTER TABLE table_statics
ADD COLUMN IF NOT EXISTS sum_period1 INTEGER DEFAULT 0;
'''
res = supabase.rpc('exec_sql', {'query': alter_table_sql}).execute()
print("Alter table result:", res)

# 2. Busca os dados para atualização
response = supabase.table('table_statics').select('id, home_period1, away_period1').execute()
print("Fetch data result:", response)

# 3. Atualiza os valores da soma
for row in response.data:
    home_val = row.get('home_period1') or 0
    away_val = row.get('away_period1') or 0
    sum_val = home_val + away_val
    update_res = supabase.table('table_statics').update({'sum_period1': sum_val}).eq('id', row['id']).execute()
    print(f"Updated row {row['id']} with sum_period1={sum_val}: ", update_res)

print("Coluna sum_period1 atualizada com sucesso.")
