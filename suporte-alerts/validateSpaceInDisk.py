import psutil
import requests

# Verifica o armazenamento do disco D: em gigabytes
directories = ['//suporte/soft$','//suporte/backup_maquinas$','//suporte/backup_ex_colaboradores$']

for directory in directories:
    storage = psutil.disk_usage(directory).free / 1024 / 1024 / 1024

    # Define o limite de armazenamento para notificação
    total = psutil.disk_usage(directory).total  / 1024 / 1024 / 1024 # Em gigabytes

    print("Diretório: ", directory)
    print("Total: {:.2f}".format(total))
    print("Usado: {:.2f}".format(total-storage))
    print("Livre: {:.2f}".format(storage))

    # Verifica se o armazenamento está abaixo do limite
    if storage <= 100:
        # Cria a mensagem que será enviada para o Microsoft Teams
        message = {
            "@type": "MessageCard",
            "themeColor": "0072C6",
            "title": f"Aviso de armazenamento de disco do diretório {directory}",
            "text": f"O armazenamento em disco está acabando. \n O armazenamento livre é de {storage:.2f} GB"
        }
        
        # Define a URL da webhook do Microsoft Teams
        webhook_url = "https://cnpemcamp.webhook.office.com/webhookb2/670371e4-8d5e-4443-86f0-0022979b2d18@ed764e1f-b3b8-4aaf-8fb2-1d05be08443b/IncomingWebhook/aa6a310ac2f84be4a187008241bde4aa/cf4b81dc-bd24-40ab-9611-8b2942a37aff"
        
        # Envia a mensagem para a webhook do Microsoft Teams
        response = requests.post(webhook_url, json=message)

        if response.status_code == 200:
            print("Notification sent successfully.")
        else:
            print("Error sending notification.")
    else:
        print("Ainda existe um total livre de {:.2f} GB".format(storage))    
        # Verifica se a mensagem foi enviada com sucesso