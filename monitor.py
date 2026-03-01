import json
import os
from datetime import datetime

# ==============================
# CONFIGURAÇÕES
# ==============================

LOG_FILE = "logs/batch.log"
INCIDENT_FILE = "incidents/incidents.json"

ERROR_KEYWORDS = ["ERROR", "ALERT"]


# ==============================
# UTILIDADES
# ==============================

def ensure_structure():
    """Garante que pastas e arquivos existam"""
    os.makedirs("logs", exist_ok=True)
    os.makedirs("incidents", exist_ok=True)

    if not os.path.exists(INCIDENT_FILE):
        with open(INCIDENT_FILE, "w") as f:
            json.dump([], f)


def read_logs():
    with open(LOG_FILE, "r") as file:
        return file.readlines()


# ==============================
# DETECÇÃO DE INCIDENTES
# ==============================

def detect_incidents(lines):
    incidents = []

    for line in lines:
        if any(keyword in line for keyword in ERROR_KEYWORDS):
            incidents.append({
                "timestamp": datetime.now().isoformat(),
                "event": line.strip(),
                "status": "OPEN"
            })

    return incidents


# ==============================
# FLUXO N1 (SIMULAÇÃO)
# ==============================

def acknowledge_incident(incident):
    """Simula analista N1 assumindo incidente"""
    incident["status"] = "ACK"


def close_incident(incident):
    """Simula resolução do incidente"""
    incident["status"] = "CLOSED"


# ==============================
# PERSISTÊNCIA
# ==============================

def save_incidents(new_incidents):
    try:
        with open(INCIDENT_FILE, "r") as file:
            existing = json.load(file)
    except:
        existing = []

    existing.extend(new_incidents)

    with open(INCIDENT_FILE, "w") as file:
        json.dump(existing, file, indent=4)


# ==============================
# EXECUÇÃO PRINCIPAL
# ==============================

def main():
    print("[INFO] Batch Monitoring iniciado")

    ensure_structure()

    logs = read_logs()
    incidents = detect_incidents(logs)

    if incidents:
        print("[ALERT] Incidentes detectados:")

        for incident in incidents:
            print(f" -> {incident['event']}")

            acknowledge_incident(incident)
            print("[N1] Incidente reconhecido (ACK)")

            close_incident(incident)
            print("[RESOLVED] Incidente encerrado (CLOSED)")

        save_incidents(incidents)
        print("[INFO] Incidentes registrados com sucesso.")

    else:
        print("[INFO] Sistema saudável.")


if __name__ == "__main__":
    main()
