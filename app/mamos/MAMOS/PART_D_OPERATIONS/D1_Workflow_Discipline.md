# D1 — Workflow Discipline  
**Category:** PART_D_OPERATIONS  
**Version:** 1.0  
**Status:** ACTIVE  
**Owner:** SYS_D1_Workflow  
**Supervisor:** SYSTEM COMMANDER  

---

## 1. Purpose

D1 Workflow Discipline Samarkand Soul sisteminin **əməliyyat nizamı, ardıcıllığı və iş axınları üzərində tam nəzarəti** təmin edən moduldur.

Onun missiyası:

- bütün agentlərin ardıcıl və sistemli işləməsini təmin etmək  
- xaosu, qarışıqlığı və özbaşına improvizasiyanı bloklamaq  
- proseslərin dəqiq, təkrar oluna bilən və sabit olmasını təmin etmək  
- hər workflow-un doğru agentdən doğru agentə keçməsini idarə etmək  
- MAMOS sisteminin “order before chaos” prinsipinə əməl etmək  

**Workflow Discipline — Samarkand Soul əməliyyat nizamının qanunudur.**

---

## 2. Core Responsibilities

### 2.1 Workflow Integrity  
D1 modul bütün workflow-lara nəzarət edir:

- hansı agent nə edəcək  
- hansı ardıcıllıqla edəcək  
- nə zaman edəcək  
- proses pozulubsa nə baş verəcək  

Hər addım dəqiq yazılmalıdır.  
Heç bir agent özbaşına workflow-u dəyişdirə bilməz.

---

### 2.2 Cross-Agent Sequencing  
Bütün workflow-lar ardıcıllıqla aparılmalıdır.

Misal:

```
DS01 → DS04 → DS05 → DS03 → DS13 → DS14 → DS16
```

Agentlər bu sıradan kənara çıxa bilməz.

Əgər ardıcıllıq pozularsa:

```
[WORKFLOW BLOCKED]  
Reason: Invalid sequence  
Action: Workflow halted
```

---

### 2.3 Workflow Categories  
D1 modul 3 tip workflow-u idarə edir:

#### **1) Operational Workflows**  
- Dropshipping  
- Product Creation  
- Pricing  
- Market Research  
- Creative Pipelines  

#### **2) Strategic Workflows**  
- Scaling  
- Expansion  
- AI-reinforcement  
- Marketplace girişləri  

#### **3) Life System Workflows**  
- Health  
- Fitness  
- Time Architecture  

Hər bir workflow öz kateqoriyasına uyğun davranmalıdır.

---

### 2.4 Process Prioritization  
Prioritet qaydalar:

1. **Blocking Tasks** — təxirəsalınmaz (system-level, security, conflicts)  
2. **Primary Tasks** — satışa birbaşa təsir edən proseslər  
3. **Secondary Tasks** — optimizasiya, kreativ, təkmilləşmə  
4. **Tertiary Tasks** — uzunmüddətli roadmap addımları  

Sistem doğru prioriteti seçməlidir.

---

## 3. Workflow Rules (Mandatory)

### 3.1 No Random Execution  
Agentlər yalnız workflow daxilində hərəkət edə bilər.  
Özbaşına addım yoxdur.

---

### 3.2 Every Workflow MUST End with One of These:

- `SUCCESS`  
- `WARNING`  
- `BLOCKED`  
- `ESCALATION`  

Başqa status yoxdur.

---

### 3.3 Workflow MUST Have:

- Start trigger  
- Clear input  
- Expected output  
- Defined steps  
- Owner agent  
- Dependencies  
- Failure modes  
- Escalation conditions  

Bunların biri çatışmazsa → workflow natamamdır.

---

### 3.4 Mandatory Naming Format

Workflow sənədləri bu formatda olmalıdır:

```
WF_[AGENT]_[FUNCTION].md
```

Misal:

```
WF_DS03_CreateProduct.md  
WF_DS01_FullMarketScan.md  
WF_DS14_LaunchTikTokCampaign.md  
```

---

### 3.5 Calm Luxury Rule  
Samarkand Soul-un brend estetikasına zidd workflow qadağandır:

- tələsiklik yoxdur  
- aqressivlik yoxdur  
- xaos yoxdur  
- brendin sükunəti və dərinliyi qorunmalıdır  

---

## 4. Failure Modes

D1 modul aşağıdakı 7 kritik failure mode-u yoxlayır:

### F1 — Wrong Agent Sequence  
Yanlış ardıcıllıq → workflow dayandırılır.

### F2 — Missing Input  
Gərəksiz dərəcədə boş input → ESCALATE.

### F3 — Undefined Process  
Addımların təsviri natamamdır → BLOCKED.

### F4 — Conflict Between Agents  
İki agent eyni rolu yerinə yetirir → STOP.

### F5 — Logic Loop  
Workflow öz-özünə qayıdır → STOP.

### F6 — Performance Overload  
Agent overload → slowdown → WARNING.

### F7 — Brand Violation  
Output brend tonundan çıxır → BLOCKED.

---

## 5. Escalation Rules

Workflow ESCALATE edilməlidir:

- agent ardıcıllığı pozulub  
- input natamamdır  
- nəticə qeyri-realdır  
- məlumat ziddiyyətlidir  
- brendə zərər vura bilər  
- sistem sabitliyi risk altındadır  

Format:

```
[ESCALATION]  
Reason: Workflow integrity violation  
Action: Commander validation required
```

---

## 6. Workflow Completion Status

Nəticə dörd formatdan biri olmalıdır:

### **SUCCESS**  
```
[WORKFLOW SUCCESS]  
All steps completed correctly.
```

### **WARNING**  
```
[WORKFLOW WARNING]  
Minor issues detected. System continues.
```

### **BLOCKED**  
```
[WORKFLOW BLOCKED]  
Reason: Invalid input or sequence  
Action: Operation stopped
```

### **ESCALATION**  
```
[ESCALATION]  
Reason: Critical workflow issue  
Action: Commander required
```

---

## 7. Document Integrity

- D1 sənədi SYS_D1 tərəfindən qorunur  
- Dəyişiklik yalnız Commander təsdiqi ilə mümkündür  
- GitHub versiya nəzarəti məcburidir  
- Bu sənəd bütün workflow-lar üçün “qanun kitabıdır”  

---

## 8. Final Statement

D1 Workflow Discipline Samarkand Soul sisteminin:

- nizam memarı  
- ardıcıllıq qoruyucusu  
- proses hakimi  
- əməliyyat mentorudur  

Heç bir agent bu sənədin kənarına çıxaraq işləyə bilməz.

Bu sənədlə workflow-lar dağınıq deyil — **nizamlı, sabit və premium** olur.

---

**END OF DOCUMENT — D1_Workflow_Discipline.md**
