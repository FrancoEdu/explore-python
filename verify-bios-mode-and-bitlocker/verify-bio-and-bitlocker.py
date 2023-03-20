import wmi
import pyad.adquery
import requests

# Define as credenciais de um usuário com permissões para ler informações no Active Directory
username = "nikola.tesla@abtlus.org.br"
password = "sua_senha"
server = "abtlus.org.br"

# Configura as credenciais e o servidor padrão para a conexão com o Active Directory
pyad.set_defaults(username=username, password=password, server=server)

# Conecta ao namespace WMI do computador remoto
c = wmi.WMI()

# Define a consulta que será executada no Active Directory
query = pyad.adquery.ADQuery()
query.execute_query(
    attributes=["Name", "distinguishedName", "msFVE-RecoveryInformation", "msFVE-VolumeStatus"],
    where_clause="objectClass='computer'"
)

# Itera sobre os resultados da consulta e verifica o modo de inicialização do BIOS
for computer in query.get_results():
    try:
        # Obtém o objeto WMI para o computador remoto
        computer_wmi = c.Win32_ComputerSystem(Name=computer["Name"])[0]
        
        # Verifica o modo de inicialização do BIOS
        if computer_wmi.BootupState == 2:
            if computer.get("msFVE-VolumeStatus") == "FullyEncrypted":
                message = {
                    "@type": "MessageCard",
                    "themeColor": "0072C6",
                    "title": f"{computer['Name']}",
                    "text": f"O computador {computer['Name']} está configurado para inicializar em modo UEFI e com o Bitlocker ativado."
                }   
            else:
                message = {
                    "@type": "MessageCard",
                    "themeColor": "0072C6",
                    "title": f"{computer['Name']}",
                    "text": f"O computador {computer['Name']} está configurado para inicializar em modo UEFI e com o Bitlocker desativado."
                } 
        elif computer_wmi.BootupState == 1:
            message = {
                "@type": "MessageCard",
                "themeColor": "0072C6",
                "title": f"{computer['Name']}",
                "text": f"O computador {computer['Name']} está configurado para inicializar em modo Leagcy, necessária formatação do mesmo."
            } 
        else:
            message = {
                "@type": "MessageCard",
                "themeColor": "0072C6",
                "title": f"{computer['Name']}",
                "text": f"Não foi possível determinar o modo de inicialização do BIOS para o computador {computer['Name']}."
            }
    except:
        message = {
            "@type": "MessageCard",
            "themeColor": "0072C6",
            "title": f"{computer['Name']}",
            "text": f"Não foi possível obter informações do WMI para o computador {computer['Name']}."
        }
    webhook_url = "https://cnpemcamp.webhook.office.com/webhookb2/670371e4-8d5e-4443-86f0-0022979b2d18@ed764e1f-b3b8-4aaf-8fb2-1d05be08443b/IncomingWebhook/0521d1a5655340018228b3dd502aaf75/cf4b81dc-bd24-40ab-9611-8b2942a37aff"
    # Envia a mensagem para a webhook do Microsoft Teams
    response = requests.post(webhook_url, json=message)
    if response.status_code == 200:
        print("Mensagem enviada com sucesso.")
    else:
        print("Erro ao enviar a mensagem.")
