# D2.1 — Security Framework  
**Category:** PART_D_OPERATIONS  
**Version:** 1.0  
**Status:** ACTIVE  
**Owner:** SYS_SECURITY  
**Supervisor:** SYSTEM COMMANDER  

---

## 1. Purpose

D2.1 Security Framework Samarkand Soul ekosistemində:

- məlumat təhlükəsizliyi  
- əməliyyat təhlükəsizliyi  
- agent davranış təhlükəsizliyi  
- infrastruktur təhlükəsizliyi  
- brend reputasiya qoruması  

üçün mərkəzi qanunverici sənəddir.

Bu sənəd bütün agentlərin təhlükəsizlik baxımından necə davranmalı olduğunu **əmr dili ilə** müəyyən edir.

---

## 2. Security Layers Overview

Təhlükəsizlik 4 əsas təbəqədən ibarətdir:

```
LAYER 1 → Data Security  
LAYER 2 → System & Infrastructure Security  
LAYER 3 → Brand & Compliance Security  
LAYER 4 → Behavioral & Ethical Security
```

Hər bir layer dəyişdirilməz qaydalarla idarə olunur.

---

## 3. Layer 1 — Data Security

### 3.1 Data Access Rules
- Agentlər yalnız onlara ayrılmış məlumatlara giriş əldə edə bilər.  
- “Cross-module access” yalnız Commander təsdiqi ilə mümkündür.  
- Xüsusi məlumatlar (user info, payment, analytics) şifrələnmiş şəkildə işlənilməlidir.  

### 3.2 Storage Protocol
- GitHub reposunda yalnız şifrəli və ya maskalanmış məlumat saxlanıla bilər.  
- Real şəxsi məlumatlar → NOT ALLOWED.  
- Loglar yalnız daxili istifadəyə uyğundur.  

### 3.3 Data Transmission
- API kommunikasiya yalnız HTTPS üzərindən.  
- Plain text olaraq həssas data göndərilməsi → QADAĞANDIR.  
- Agentlər məlumatı üçüncü tərəfə ötürə bilməz.  

---

## 4. Layer 2 — System & Infrastructure Security

### 4.1 API Security
- Shopify, Meta, TikTok, Google API key-ləri hiçbir agent tərəfindən göstərilə bilməz.  
- Keys yalnız “environment variable” olaraq saxlanmalıdır.  

### 4.2 Infrastructure Protection
- Server tərəf (Render) yalnız Komanderin təsdiq etdiyi modullar tərəfindən istifadə edilə bilər.  
- Unauthorized deployment → BLOCK.  
- System overload signal → AUTO SAFE MODE açılır.  

### 4.3 Backup Protocol
- Bütün sənədlər və agentlər üçün 24h interval ilə auto-backup.  
- Backup-lar maskalanmış məlumatla aparılmalıdır.  

### 4.4 System Monitoring
- SYS04_SystemHealth agenti hər 1 saatdan bir:  
  - CPU  
  - Memory  
  - API rate limit  
  - Latency  
  - Error frequency  
  - Shopify/Meta/TikTok connection status  
  yoxlamalıdır.  

---

## 5. Layer 3 — Brand & Compliance Security

### 5.1 Brand Protection
Samarkand Soul brendinə zərər verə biləcək hər hansı hərəkət → AUTO BLOCK.

Bura daxildir:

- clickbait dil  
- exaggerated iddialar  
- yanlış material məlumatı  
- yalan heritage hekayələri  
- ucuz dropshipping vizualları  
- manipulyativ reklam  

### 5.2 Platform Compliance
Agentlər aşağı platforma qaydalarını pozmamalıdır:

- Shopify policy  
- Meta Ads policy  
- TikTok Ads policy  
- Email deliverability rules  
- Consumer protection laws  

Pozuntu halında:

```
[AUTO_ESCALATE]  
Reason: Compliance violation detected  
Action: Commander review required
```

### 5.3 Customer Data Protection
- Müştəri məlumatı heç vaxt kopyalanmamalıdır.  
- Email, telefon, sifariş məlumatı → MASKED FORMAT.  
- Data üçüncü tərəfə ötürülə bilməz.  

---

## 6. Layer 4 — Behavioral & Ethical Security

### 6.1 Agent Behavior Rules
Agentlər:

- manipulyasiya edə bilməz  
- müştərini aldatmaq üçün dil istifadə edə bilməz  
- “fake urgency”, “fake scarcity” qəti qadağandır  
- həqiqəti gizlətmək olmaz  
- clickbait → 0 tolerans  

### 6.2 Ethical Constraints
Samarkand Soul sistemi aşağıdakı dəyərlərə sadiqdir:

- dürüstlük  
- şəffaflıq  
- premium keyfiyyət  
- brend və mədəniyyətə hörmət  
- uzunmüddətli düşüncə  

### 6.3 Bias & Distortion Prevention
Agentlər:

- rəqib haqqında manipulyativ məlumat yaza bilməz  
- ölkə, mədəniyyət və ya insan qrupu haqqında stereotip yarada bilməz  
- SEO məqsədilə yanlış məlumat doldura bilməz  

---

## 7. Escalation & Safe Mode Rules

### 7.1 Mandatory Escalation Conditions
Aşağı hallarda sistem **ESCALATE** etməlidir:

- şübhəli API aktivliyi  
- sistem overload  
- vaxtı keçmiş API key  
- uyğunsuz data giriş cəhdi  
- uyğunsuz agent davranışı  
- brend qaydası pozuntusu  
- policy violation şübhəsi  

### 7.2 Escalation Format
```
[ESCALATION]  
Reason: Security violation  
Action: System lockdown until Commander approval  
Summary: Immediate review required
```

### 7.3 Auto Safe Mode
Sistem özünü aşağı hallarda qoruma rejiminə salır:

- çoxlu error (1 dəqiqədə 5+)  
- API timeout artımı  
- çox sürətli loop davranışı  
- şübhəli data pattern  
- unauthorized module çağırışı  

Safe Mode aktivləşdikdə:

- bütün agentlər STOP  
- yalnız SYS_SECURITY və COMMANDER işləyir  

---

## 8. Red Flag Conditions (STOP THE SYSTEM)

Sistem dərhal DAYANDIRILMALIDIR əgər:

- Payment info exposed  
- Customer data leak  
- API compromised  
- Unauthorized access attempt  
- Brend reputasiyası riskə düşür  
- Shopify store policy warning gəlir  

Bu hallarda:

```
[SYSTEM HALT]  
Severity: CRITICAL  
Action: Stop all agents  
Commander Override Required
```

---

## 9. Document Integrity Rules

- Bu sənəd sistemin təhlükəsizlik qanunudur  
- Dəyişiklik yalnız Commander təsdiqi ilə mümkündür  
- GitHub-da versiya nəzarəti aparılmalıdır  
- Agentlər bu sənədi ignor edə bilməz  
- Təhlükəsizlik qaydaları brend qaydalarından üstün tutulur  

---

## 10. Final Statement

D2.1 Security Framework Samarkand Soul sisteminin **təhlükəsizlik onurğasıdır**.  
Bu sənəd olmadan sistem fəaliyyət göstərə bilməz.

Bu sənəd:

- brendi qoruyur  
- müştərini qoruyur  
- sistemi qoruyur  
- məlumatı qoruyur  
- agent davranışını tənzimləyir  
- genişlənmə zamanı riskləri bloklayır  

Samarkand Soul-un dayanıqlı olmasının səbəbi — **bu sənədin mövcudluğudur.**

---

**END OF DOCUMENT — D2_1_Security_Framework.md**
