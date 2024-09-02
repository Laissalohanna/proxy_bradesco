import subprocess


def generate_signature(request_data, signature_txt_path):
    http_method = request_data["http_method"]
    endpoint = request_data["endpoint"]
    parameters = request_data["parameters"]
    token = request_data["token"]
    nonce = request_data["nonce"]
    timestamp_iso, timestamp_int = request_data["timestamp"]
    algorithm = "SHA256"

    if http_method == "GET":
        request_content = (
            f"{http_method}\n{endpoint}\n{parameters}\n\n"
            f"{token}\n{nonce}000\n{timestamp_iso}\n{algorithm}"
        )
    elif http_method == "POST":
        request_content = (
            f"{http_method}\n{endpoint}\n\n{parameters}\n"
            f"{token}\n{nonce}000\n{timestamp_iso}\n{algorithm}"
        )
    else:

        raise ValueError(f"Método HTTP desconhecido: {http_method}")

    with open(signature_txt_path, "w") as file:
        file.write(request_content)

    command = """echo -n "$(cat request.txt)" | openssl dgst -sha256 -keyform pem -sign private_certificate.com.key.pem | base64 | tr -d '=[:space:]' | tr '+/' '-_'"""

    try:
        signature = subprocess.check_output(command, shell=True).decode().strip()
        print(f"Assinatura gerada: {signature}")
        return signature
    except subprocess.CalledProcessError as e:
        print(f"Erro ao gerar assinatura: {e}")
        return None
