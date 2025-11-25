# app/agents/ds/ds02_drive_agent.py

class DriveAgent:
    """
    DEMO DriveAgent.

    Hələlik Google Drive API-dən istifadə etmir,
    sadəcə MSP-dən ona siqnal gəlib-gəlmədiyini yoxlayırıq.
    """

    def __init__(self) -> None:
        # Burda real credentials yoxdur, sadəcə log üçün.
        print("DriveAgent DEMO init oldu.")

    def create_folder_path(self, path: str) -> str:
        clean = (path or "").strip()
        if not clean:
            return "Drive DEMO: path boşdur."

        # Burda hələ real qovluq yaratmırıq, sadəcə cavab formalaşdırırıq.
        return (
            "Drive DEMO cavabı:\n"
            f"Bu path üçün qovluq strukturu yaradılmalı idi: {clean}\n"
            "Google Drive real inteqrasiyasını ayrıca test edib qoşacağıq. 🚧"
        )
