＃ pip install cryptography==44.0.0

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import pkcs12

def extract_pfx_to_nginx_format(pfx_file, pfx_password, output_cert_key_file, output_cert_chain_file):
    # 讀取 PFX 檔案
    with open(pfx_file, "rb") as f:
        pfx_data = f.read()

    # 解密 PFX 檔案
    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
        pfx_data, pfx_password.encode(), backend=default_backend()
    )

    # 將私鑰寫入檔案
    if private_key:
        with open(output_cert_key_file, "wb") as key_file:
            key_file.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )

    # 將憑證和 CA 憑證鏈合併寫入檔案
    if certificate:
        with open(output_cert_chain_file, "wb") as chain_file:
            # 寫入伺服器憑證
            chain_file.write(
                certificate.public_bytes(encoding=serialization.Encoding.PEM)
            )
            # 寫入 CA 憑證鏈
            if additional_certificates:
                for cert in additional_certificates:
                    chain_file.write(
                        cert.public_bytes(encoding=serialization.Encoding.PEM)
                    )

# 使用範例
extract_pfx_to_nginx_format(
    pfx_file=r"C:\Users\Administrator\Downloads\kutwch.tw_20250110.pfx",
    pfx_password="password",
    output_cert_key_file="cert.key",  # 私鑰
    output_cert_chain_file="cert.crt"  # 合併的伺服器憑證和 CA 憑證
)


