"""
Script pour créer un certificat SSL auto-signé pour HTTPS local
"""

try:
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from datetime import datetime, timedelta
    import os
    
    print("Creation du certificat SSL auto-signe...")
    
    # Générer une clé privée
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Créer le certificat
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "TD"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Tchad"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Local"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Tchad Langues AI"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName("localhost"),
            x509.DNSName("127.0.0.1"),
        ]),
        critical=False,
    ).sign(key, hashes.SHA256())
    
    # Sauvegarder le certificat et la clé
    with open("cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    with open("key.pem", "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    print("OK - Certificat cree avec succes !")
    print("   - cert.pem")
    print("   - key.pem")
    print("\nNote: Le navigateur affichera un avertissement de securite")
    print("car c'est un certificat auto-signe. C'est normal pour un usage local.")
    print("Clique sur 'Avance' puis 'Continuer vers localhost' pour acceder a l'application.")
    
except ImportError:
    print("ERREUR: La bibliotheque 'cryptography' n'est pas installee.")
    print("Installation en cours...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
    print("OK - Installation terminee. Relance ce script.")
    print("   python create_ssl_cert.py")

