# Define connection parameters
server = 'saleemihomeplus'
# server = '182.191.76.96'
database = 'SaleemiHomePlusDataBaseV5'
username = 'sa'
password = '8ax7zey9'

# Create connection string
conn_str = (
    f'DRIVER={{SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    f'Trusted_Connection=no;'
)