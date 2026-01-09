@echo off
echo Creation d'un certificat SSL auto-signe pour HTTPS local...
echo.

REM Installer OpenSSL si necessaire, ou utiliser Python pour creer le certificat
python -c "from cryptography import x509; from cryptography.x509.oid import NameOID; from cryptography.hazmat.primitives import hashes, serialization; from cryptography.hazmat.primitives.asymmetric import rsa; from datetime import datetime, timedelta; import os; key = rsa.generate_private_key(public_exponent=65537, key_size=2048); subject = issuer = x509.Name([x509.NameAttribute(NameOID.COUNTRY_NAME, 'TD'), x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'Tchad'), x509.NameAttribute(NameOID.LOCALITY_NAME, 'Local'), x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'Tchad Langues AI'), x509.NameAttribute(NameOID.COMMON_NAME, 'localhost')]); cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(datetime.utcnow()).not_valid_after(datetime.utcnow() + timedelta(days=365)).add_extension(x509.SubjectAlternativeName([x509.DNSName('localhost'), x509.DNSName('127.0.0.1')]), critical=False).sign(key, hashes.SHA256()); open('cert.pem', 'wb').write(cert.public_bytes(serialization.Encoding.PEM)); open('key.pem', 'wb').write(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())); print('Certificat cree avec succes!')" 2>nul

if %errorlevel% neq 0 (
    echo Erreur: La bibliotheque cryptography n'est pas installee.
    echo Installation de cryptography...
    pip install cryptography
    python -c "from cryptography import x509; from cryptography.x509.oid import NameOID; from cryptography.hazmat.primitives import hashes, serialization; from cryptography.hazmat.primitives.asymmetric import rsa; from datetime import datetime, timedelta; import os; key = rsa.generate_private_key(public_exponent=65537, key_size=2048); subject = issuer = x509.Name([x509.NameAttribute(NameOID.COUNTRY_NAME, 'TD'), x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'Tchad'), x509.NameAttribute(NameOID.LOCALITY_NAME, 'Local'), x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'Tchad Langues AI'), x509.NameAttribute(NameOID.COMMON_NAME, 'localhost')]); cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(datetime.utcnow()).not_valid_after(datetime.utcnow() + timedelta(days=365)).add_extension(x509.SubjectAlternativeName([x509.DNSName('localhost'), x509.DNSName('127.0.0.1')]), critical=False).sign(key, hashes.SHA256()); open('cert.pem', 'wb').write(cert.public_bytes(serialization.Encoding.PEM)); open('key.pem', 'wb').write(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())); print('Certificat cree avec succes!')"
)

echo.
echo Certificats crees: cert.pem et key.pem
echo Vous pouvez maintenant lancer l'application avec HTTPS.
pause

