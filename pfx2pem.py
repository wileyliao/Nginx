＃ pip install cryptography==44.0.0

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import pkcs12

def extract_pfx_to_pem(pfx_file, pfx_password, output_cert_file, output_key_file, output_ca_file=None):
    # 讀取 PFX 檔案
    with open(pfx_file, "rb") as f:
        pfx_data = f.read()

    # 解密 PFX 檔案
    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
        pfx_data, pfx_password.encode(), backend=default_backend()
    )

    # 將憑證寫入檔案
    if certificate:
        with open(output_cert_file, "wb") as cert_file:
            cert_file.write(
                certificate.public_bytes(encoding=serialization.Encoding.PEM)
            )

    # 將私鑰寫入檔案
    if private_key:
        with open(output_key_file, "wb") as key_file:
            key_file.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )

    print(f"Additional certificates: {additional_certificates}")
    # 如果有額外的 CA 憑證鏈，將其寫入檔案
    if additional_certificates and output_ca_file:
        with open(output_ca_file, "wb") as ca_file:
            for cert in additional_certificates:
                ca_file.write(
                    cert.public_bytes(encoding=serialization.Encoding.PEM)
                )

# 使用範例
extract_pfx_to_pem(
    pfx_file=r"C:\Users\Administrator\Downloads\kutwch.tw_20250110.pfx",
    pfx_password="user82822040",
    output_cert_file="cert.crt",
    output_key_file="cert.key",
    output_ca_file="ca_bundle.crt"
)


