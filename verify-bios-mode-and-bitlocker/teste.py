import wmi
from pyad import *
import requests

# Define as credenciais de um usuário com permissões para ler informações no Active Directory
q = adquery.ADQuery()

q.execute_query(
    attributes=["name", "operatingSystem"],
    where_clause="objectClass='computer' AND name='S-DIR06-W'",
    base_dn="DC=abtlus,DC=org,DC=br"
)

for computer in q.get_results():
    print(computer["name"], computer["operatingSystem"])
    
    # Conecta ao WMI do computador
    conn = wmi.WMI(computer=computer["name"])

    # Consulta o WMI para verificar o status do BitLocker
    for drive in conn.Win32_EncryptableVolume():
        if drive.DriveLetter:
            if drive.ProtectionStatus == 1:
                print(f"BitLocker ativado na unidade {drive.DriveLetter}")
            elif drive.ProtectionStatus == 0:
                print(f"BitLocker desativado na unidade {drive.DriveLetter}")
            else:
                print(f"BitLocker não está configurado na unidade {drive.DriveLetter}")