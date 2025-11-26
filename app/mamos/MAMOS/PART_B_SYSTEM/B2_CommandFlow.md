# B2 — Command Flow Specification  
Version: 1.0  
Status: ACTIVE  
Maintainer: SYS01_Knowledge_Librarian  
Last Updated: 2025

---

# 1. Purpose  
Bu sənəd Samarkand Soul ekosistemində **əmr axınının (Command Flow)** tam iş mexanizmini müəyyən edir.  
Hər bir komanda bu ardıcıllıqla icra olunmalıdır:

**Commander → MSP → Agent → MSP → Commander**

Düzgün komanda axını olmadan sistem xaos yaradar.  
Bu sənəd həmin xaosu sıfıra endirmək üçün mövcuddur.

---

# 2. High-Level Command Pipeline  

Komanda sistemi 6 əsas mərhələdə çalışır:

1. **Input Reception (Commander → MSP)**  
2. **Primary MAMOS Filter**  
3. **Command Parsing & Target Identification**  
4. **Agent Execution (MSP → DS/LIFE/SYS)**  
5. **Secondary MAMOS Filter**  
6. **Output Delivery (MSP → Commander)**  

Bu ardıcıllıq _heç vaxt pozulmur_.

---

# 3. Step-by-Step Flow Definition  

## Step 1 — Input Reception  
MSP komandiri tərəfindən göndərilən əmri qəbul edir.  
Qəbul prosesi aşağıdakı parametrləri qeyd edir:

- komanda mənbəyi  
- vaxt damğası  
- əmrin növü  
- giriş uzunluğu  
- mümkün risk göstəriciləri  

Əgər komanda sintaksis baxımından qeyri-adi görünsə → MSP sorğu verir.

---

## Step 2 — Primary MAMOS Filter  
MSP əmri MAMOS qaydalarının ilk səviyyəsinə qarşı yoxlayır:

- brend tonu  
- premium dil  
- mədəni təhlükəsizlik  
- etik normalar  
- yanlış iddialar  

Əgər pozuntu varsa, aşağıdakı formatda ESCALATION çıxar:

    [ESCALATION]
    Stage: Primary Filter
    Issue: MAMOS violation detected
    Action: Command blocked — Human validation required
    Status: Halted

Əgər pozuntu yoxdursa → Step 3.

---

## Step 3 — Command Parsing  
MSP sintaksisi açır və 5 əsas elementi ayırır:

- **intent** — əmrin məqsədi  
- **target agent group** (DS/LIFE/SYS)  
- **operation type** (create / analyze / plan / generate / evaluate)  
- **priority**  
- **risk level**  

Parsing zamanı MSP tapır:

- məhsul əmri
- rəqəmsal əməliyyat
- idarəetmə əmri
- sağlamlıq əmri
- sistem əmri
- yüksək riskli əmri

Əgər target müəyyən edilə bilməzsə → eskalasiya edir.

---

## Step 4 — Agent Selection & Execution  
Parsing tamamlandıqdan sonra MSP uyğun agenti seçir:

- `DS` → dropshipping, marketing, SEO, vizual sistemlər  
- `LIFE` → sağlamlıq, vaxt, fokus, bərpa  
- `SYS` → təhlükəsizlik, bilik, strukturlar  

MSP aşağıdakıları təmin edir:

- agent lazımi səlahiyyətdədir  
- agentin funksiyası əmrin məqsədi ilə uyğundur  
- agent MAMOS qaydalarını pozmur  

Seçim sonrası:

**MSP → Agent: “Execute this task.”**

Agent nəticəni MSP-yə qaytarır.

---

## Step 5 — Secondary MAMOS Filter  
Agent cavabı MSP-yə qayıtdıqdan sonra ikinci yoxlama olunur:

Yoxlanılanlar:

- Ton — premium? sakit? minimal?  
- Estetika — vizual uyğunluq varmı?  
- Etika — manipulyativ və ya yanlış iddia yoxdur?  
- Faktlar — reallığa uyğundur?  
- Struktur — nəticə “Summary → Output → Notes” quruluşundadır?  
- Mədəni uyğunluq — Samarkand ruhuna hörmət?  
- Təhlükəsizlik — riskli əmrlər varmı?  

Əgər uyğunsuzluq varsa:

    [ESCALATION]
    Stage: Secondary Filter
    Issue: Output violates brand or ethical standards
    Action: Output rejected — Requires human correction
    Status: Paused

Əgər hər şey təmizdirsə → Step 6.

---

## Step 6 — Output Delivery  
MSP cavabı son olaraq Komandira təqdim edir.

Çıxış formatı:

1. **Summary**  
2. **Main Output**  
3. **Notes (MAMOS Compliance)**  
4. **Escalation (if required)**  

MSP cavabı heç vaxt:

- dağıdıq  
- qaralama  
- nizamsız  
- sərt  
- emosional  
- aqressiv  

şəkildə vermir.

---

# 4. Command Flow Types  

Aşağıdakı 5 tip əmrlər müəyyən olunub:

### 4.1 Standard Operational Flow  
Əsas biznes əmrləri:

- Shopify əməliyyatları  
- məhsul araşdırması  
- kontent planları  
- vizual brief  
- KPI analizi  

### 4.2 Analytical Flow  
Əmrlər:

- analiz  
- hesabat  
- dərin öyrənmə  
- rəqəm çıxarışı  

### 4.3 Creative Flow  
Əmrlər:

- copywriting  
- skript  
- vizual ideya  
- moodboard  

### 4.4 System Flow  
Əmrlər:

- təhlükəsizlik  
- strukturlar  
- SOP-lar  
- MAMOS audit  

### 4.5 Human Support Flow  
LIFE Layer ilə əlaqəli:

- diet  
- sağlamlıq  
- fokus planı  
- info-detox  

---

# 5. High-Risk Command Handling  

Aşağıdakı əmrlər “HIGH RISK” olaraq işarələnir:

- kredit kart / ödəniş əməliyyatı  
- Shopify-də silmə / dəyişmə  
- qiymət dəyişikliyi  
- böyük reklam kampaniyası başlatmaq  
- məlumat bazası modifikasiyası  

Belə əmrlərdə MSP cavabı vermir, yalnız soruşur:

    [CONFIRMATION REQUIRED]
    This command has HIGH RISK impact.
    Please confirm: YES / NO

Komandir “YES” demədən sistem davam etməz.

---

# 6. Multi-Agent Conflict Resolution  

Əgər iki agent zidd cavab verirsə:

1. MSP cavabı saxlayır  
2. SYS Layer-i çağırır  
3. SYS Layer konfliktin səbəbini analiz edir  
4. Komandir son qərarı verir  

Konflikt ssenarisi formatı:

    [CONFLICT]
    Agents: C2_03 vs C2_12
    Issue: Output misalignment
    Action: Re-route to SYS Layer
    Status: Pending human decision

---

# 7. Timeout & Overload Protection  

### 7.1 Timeout  
Əgər agent 15 saniyədən çox cavab vermirsə:

- tapşırıq dondurulur  
- SYS Layer xəbərdar edilir  
- Komandirə info verilir  

### 7.2 Overload  
Uzun əmrlər zamanı MSP cavabı hissələrə bölür, amma:

- ardıcıllıq qorunur  
- MAMOS dəyişmir  
- struktur pozulmur  

---

# 8. Command Logging  
Bütün əmrlər aşağıdakı məlumatlarla loglanır:

- vaxt  
- mənbə  
- agent  
- risk səviyyəsi  
- nəticə  
- filtr statusu  
- eskalasiya olub-olmaması  

Loglar SYS-01 tərəfindən idarə olunur.

---

# 9. Core Philosophy  

Komanda axınının üç dəyişməz qaydası:

### Qanun 1 — Nizam, Xaos Yox  
Hər əmrin gedişi ardıcıllıqla olmalıdır.

### Qanun 2 — MAMOS Üstün Dəyərlərdir  
Axın MAMOS-u pozursa → komanda ləğv olunur.

### Qanun 3 — Brend Tonu Hər Şeydən Vacibdir  
Çıxış premium olmazsa, çıxış qəbul deyil.

---

END OF DOCUMENT — B2_CommandFlow.md
