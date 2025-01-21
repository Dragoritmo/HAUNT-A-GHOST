def generate_tombstone(url, message, timestamp):
    tombstone = f"""
    ╔══════════════════════════╗
    ║        R.I.P.            ║
    ║     ┏━━━━━━━━┓          ║
    ║     ┃   †    ┃          ║
    ║     ┃        ┃          ║
    ║     ┃ {message[:10]}... ┃          ║
    ║     ┗━━━━━━━━┛          ║
    ║                         ║
    ║ Aquí yace:             ║
    ║ {url[:30]}...          ║
    ║                         ║
    ║ Fecha de defunción:    ║
    ║ {timestamp[:10]}        ║
    ╚══════════════════════════╝
    
    """
    return tombstone 