# app/agents/core/msp.py

class MSP:
    """
    MSP (Main Service Processor) - Samarkand Soul botunun əsas router-i.
    Buraya gələn "msp: ..." komandalarını oxuyub uyğun agenta yönləndirir.
    """

    def __init__(self) -> None:
        # Gələcəkdə bura config, token və s. əlavə edə bilərik
        pass

    def process(self, raw_text: str) -> str:
        """
        Telegramdan gələn bütün MSP komandaları üçün giriş nöqtəsi.
        Nümunələr:
          - 'msp: market: pet hair remover | US'
          - 'msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master'
          - 'msp: offer: premium blanket | US market'
        """

        if not raw_text:
            return "MSP error: boş mesaj gəldi."

        # Baş-boşluqları təmizləyək
        text = raw_text.strip()

        # Əgər 'msp:' ilə başlayırsa, onu kəsək ki, iç router sadə işləsin
        lowered = text.lower()
        if lowered.startswith("msp:"):
            text = text[4:].strip()  # 'msp:' 4 simvol

        # ==========================================================
        # 1) DRIVE KOMANDASI (full debug-lu)
        # ----------------------------------------------------------
        # Nümunə:
        #   msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master
        # ==========================================================
        if text.lower().startswith("drive:"):
            path = text[len("drive:"):].strip()

            if not path:
                return (
                    "MSP error: drive path boşdur.\n"
                    "Nümunə: msp: drive: SamarkandSoulSystem / DS System / "
                    "DS-01 - Market-Research-Master"
                )

            # 1) Import-u ayrıca yoxlayaq
            try:
                from app.agents.ds.ds02_drive_agent import DriveAgent
            except Exception as e:
                return f"MSP error: DriveAgent import xətası: {e}"

            # 2
