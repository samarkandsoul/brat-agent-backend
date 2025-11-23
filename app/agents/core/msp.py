class MSP:
    def __init__(self):
        pass

    def process(self, command: str):
        text = command.lower().strip()

        # 1) Shopify ilə bağlı komanda
        if "shopify" in text:
            return "Shopify komandası qəbul edildi. Tezliklə inteqrasiya əlavə olunacaq."

        # 2) Google Drive komanda
        if "drive" in text or "google" in text:
            return "Google Drive komandası qəbul edildi. Qovluq sistemi üçün modul hazırlanır."

        # 3) Market analizi komanda
        if "market" in text or "niş" in text:
            return "Market Research komandası MSP-ə çatdı. DS-01 moduluna yönləndiriləcək."

        # 4) Gündəlik plan / idarəetmə
        if "plan" in text or "tapşırıq" in text:
            return "Planlaşdırma və gündəlik idarəetmə komandası qəbul edildi."

        # 5) Agent statusu / sistem
        if "status" in text or "agent" in text or "sistem" in text:
            return "Sistem statusu hazırdır. Agentlərin vəziyyəti üçün modul hazırlanırr."

        # 6) Default cavab — tanımadısa
        return f"MSP sənin dediyini qəbul etdi, amma komandaya uyğun modul hələ hazır deyil: {command}"
