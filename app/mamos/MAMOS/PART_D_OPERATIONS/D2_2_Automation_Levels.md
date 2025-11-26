# D2.2 — Automation Levels  
**Category:** PART_D_OPERATIONS  
**Version:** 1.0  
**Status:** ACTIVE  
**Owner:** SYS_AUTOMATION  
**Supervisor:** SYSTEM COMMANDER  

---

## 1. Purpose

D2.2 Automation Levels sənədi Samarkand Soul sistemində:

- hansı işlərin avtomat,  
- hansının yarı-avtomat,  
- hansının tam manual  

olduğunu rəsmi şəkildə müəyyən edir.

Bu sənəd bütün agentlərə “sərhədlərini” göstərir və sistemin stabilliyini qoruyur.

---

## 2. Automation Tier Overview

Bütün əməliyyatlar 4 səviyyəyə bölünür:

```
LEVEL 0 — Manual Only  
LEVEL 1 — Assisted Automation  
LEVEL 2 — Semi-Automation  
LEVEL 3 — Full Automation  
LEVEL 4 — Autonomous Operation (Commander-level only)
```

---

## 3. LEVEL 0 — Manual Only

Bu səviyyədə olan işlər insansız icra oluna bilməz.

### 3.1 Human Decision Required
- Final pricing approval  
- Campaign budget approval  
- Rebranding və vizual dəyişikliklər  
- Supplier dəyişdirmə qərarı  
- Riskli məhsulun satışa buraxılması  

### 3.2 Prohibited for Agents
- İnsan emosional qərarları əvəz etmək  
- Brendin əsas dəyərlərini dəyişmək  
- Storytelling və mədəni narrativləri manipulyasiya etmək  

---

## 4. LEVEL 1 — Assisted Automation

Agent strukturu insana “yardım edir”, icra etmir.

### 4.1 Agent Assistance Includes:
- Research summarization  
- Trend mapping  
- KPI visualization  
- HTML preview  
- SEO keyword suggestion  
- Competitor signals overview  

### 4.2 Restrictions:
- Agentlər final qərar verə bilməz  
- Heç bir dəyişiklik Shopify-da canlı şəkildə edilə bilməz  

---

## 5. LEVEL 2 — Semi-Automation

Bu səviyyədə agent işin 50%-ni avtomatik, 50%-ni istifadəçi ilə birlikdə edir.

### 5.1 Examples:
- Product JSON generation → automatic  
- Human review → required  
- HTML product description → automatic  
- Publish → manual  
- Ads creative text → automatic  
- Launch → manual  

### 5.2 Safe Zone
Semi-automation yalnız **təhlükəsiz** və **brend uyumlu** bloklarda icazəlidir.

---

## 6. LEVEL 3 — Full Automation

Bu səviyyədə agent tam icra edir — lakin yalnız “low-risk lanes” daxilində.

### 6.1 Allowed Full Automation Tasks:
- KPI dashboard updates  
- Daily reports  
- Non-sensitive data syncing  
- Log management  
- Image compression  
- Inventory simulation  
- Page speed monitoring  

### 6.2 Forbidden in Full Automation:
- Shopify məhsul dərc edilməsi  
- Reklam kampaniyası aktivləşdirmə  
- High-risk operational changes  
- Real customer communication  

### 6.3 System Safety:
Full automation yalnız **SYS_SECURITY → GREEN STATUS** olduqda açıqdır.

---

## 7. LEVEL 4 — Autonomous Mode (Commander-Only)

Bu səviyyə yalnız SYSTEM COMMANDER tərəfindən aktivləşdirilə bilər.

### 7.1 Capabilities:
- Multi-agent coordination  
- Workflow chaining  
- Independent decision routing  
- Real-time data correction  
- Priority queuing  

### 7.2 Commander Override
Autonomous mode yalnız aşağıdakı hallarda açılır:

- Qısa vaxtda yüksək məhsuldarlıq lazımdır  
- Böyük kampaniyaya hazırlıq  
- Sistem yük balansı optimizasiyası  
- Qlobal satış analitikası  

### 7.3 Restrictions:
- Customer-facing actions icazəli deyil  
- Shopify, Meta, TikTok üzərində heç bir dəyişiklik edilə bilməz  
- Brend transformasiyasına toxunmaq qadağandır  

---

## 8. Safety Rules Across All Levels

### 8.1 If Risk → STOP
Agent risk hiss edirsə → dərhal ESCALATE.

### 8.2 No Automation in Critical Zones:
- Payment data  
- Customer data  
- Legal documents  
- Supplier contracts  
- High risk campaigns  
- Price changes  

### 8.3 Automation Must Be Reversible
Hər avtomat əməliyyat:

- traceable  
- reversible  
- logged  

olmalıdır.

### 8.4 Logging Requirements
Hər agent əməliyyatı:

```
Timestamp  
Agent Code  
Operation  
Input  
Output  
Status (SUCCESS/FAIL/ESCALATE)
```

şəklində loglanmalıdır.

---

## 9. Escalation During Automation

Aşağı hallarda dərhal ESCALATE edilməlidir:

- agent gözlənilməz loop-a düşür  
- output uyğunsuzdur  
- potensial policy violation  
- data conflict yaranır  
- JSON/HTML strukturu təhlükəlidir  
- təhlükəsizlik layer-i RED statusdadır  

Escalation mesajı:

```
[ESCALATION]  
Reason: Automation integrity risk  
Action: Stop operation and request Commander review  
```

---

## 10. Document Integrity

- Bu sənəd yalnız SYS_AUTOMATION tərəfindən dəyişdirilə bilər  
- Commander təsdiqi olmadan dəyişiklik edilə bilməz  
- GitHub versiya nəzarəti məcburidir  
- Agentlər bu sənədə zidd davranış göstərə bilməz  

---

## 11. Final Statement

D2.2 Automation Levels sənədi Samarkand Soul sisteminin **avtomatlaşdırma strategiyasını** müəyyən edir.  
Bu sənəd bütün agentlərə nəyi edə biləcəyini və edə bilməyəcəyini göstərir.

Bu çərçivə sayəsində:

- sistem təhlükəsiz qalır  
- brend toxunulmaz qalır  
- əməliyyatlar sabit qalır  
- risklər minimuma enir  
- agentlər nəzarətli şəkildə işləyir  

Samarkand Soul-un uzunömürlü olmasının əsas səbəblərindən biri — **bu avtomatlaşdırma qanunudur.**

---

**END OF DOCUMENT — D2_2_Automation_Levels.md**
