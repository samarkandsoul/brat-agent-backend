class DS05ProductPageCopywriter:
    """
    DS-05: Product Page Copywriter (DEMO versiyası).
    Məhsul üçün professional product page məzmunu yaradır.
    Real AI generasiya OpenAI API açarı aktiv olanda qoşulacaq.
    """

    def generate(self, product_name: str, market: str) -> str:
        if not product_name or not market:
            return "DS-05 error: product_name və market boş ola bilməz."

        # DEMO cavab — struktur testinə görə
        return (
            "DS-05 Product Page Copywriter (DEMO):\n"
            f"Məhsul: {product_name}\n"
            f"Market: {market}\n\n"
            "Bu agent məhsul üçün aşağıdakıları yaradacaq:\n"
            " • SEO optimized başlıq\n"
            " • Professional məhsul təsviri\n"
            " • Problem → Agitation → Solution copy modeli\n"
            " • 5 əsas özəllik (bullet-lists)\n"
            " • Shopify üçün hazır HTML təsvir\n"
            " • DALL·E üçün image prompt ideyaları\n\n"
            "Real generasiya API aktivləşəndən sonra tam işə düşəcək. 🔥"
        )
