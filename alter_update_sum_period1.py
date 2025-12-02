from dotenv import load_dotenv
from config import get_supabase_client, TABLE_STATICS

load_dotenv()  # Carrega as variáveis do arquivo .env

supabase = get_supabase_client()

# 1. Adiciona a coluna sum_period1 (INTEGER) na tabela se não existir
alter_table_sql = f'''
ALTER TABLE {TABLE_STATICS}
ADD COLUMN IF NOT EXISTS sum_period1 INTEGER DEFAULT 0;
'''
res = supabase.rpc('exec_sql', {'query': alter_table_sql}).execute()
print("Alter table result:", res)

# 2. Busca os dados para atualização
response = supabase.table(TABLE_STATICS).select('id, home_period1, away_period1').execute()
print("Fetch data result:", response)

# 3. Atualiza os valores da soma
for row in response.data:
    home_val = row.get('home_period1') or 0
    away_val = row.get('away_period1') or 0
    sum_val = home_val + away_val
    update_res = supabase.table(TABLE_STATICS).update({'sum_period1': sum_val}).eq('id', row['id']).execute()
    print(f"Updated row {row['id']} with sum_period1={sum_val}: ", update_res)

print("Coluna sum_period1 atualizada com sucesso.")
