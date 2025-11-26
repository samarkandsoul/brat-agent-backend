# D1_1 — Escalation Rules  
**Category:** PART_D_OPERATIONS  
**Version:** 1.0  
**Status:** ACTIVE  
**Owner:** SYS_D1_ESCALATION  
**Supervisor:** SYSTEM COMMANDER  

---

## 1. Purpose

Escalation Rules MAMOS ekosisteminin **təhlükəsizlik əyləcəyi və sistem qoruma mexanizmidir**.

Onun əsas missiyası:

- səhv, riskli və ya ziddiyyətli prosesləri dərhal dayandırmaq  
- agentlərin nəticələrinin təhlükəsizliyini təmin etmək  
- Komandera kritik məlumat çatdırmaq  
- sistem pozuntularının qarşısını almaq  

ESCALATION — sistemin “STOP & VERIFY” funksiyasıdır.

---

## 2. Escalation nədir?

ESCALATION aşağıdakı deməkdir:

- agent əməliyyatı davam etdirə bilmir  
- risk mövcuddur  
- nəticə etibarsızdır  
- proses davam etsə sistem pozula bilər  
- insan (Commander) təsdiqi lazımdır  

ESCALATION — panika deyil, **intellektual qoruma mexanizmidir**.

---

## 3. Escalation Trigger Types

D1_1 modul ESCALATION-i 6 əsas səbəbə görə aktivləşdirir.

---

### 3.1 Input Triggers  
Aşağı input halları ESCALATE:

- natamam məlumat  
- səhv format  
- məhsul məlumatı qeyri-dəqiq  
- workflow üçün lazımi data yoxdur  
- agent yanlış input alıb  

---

### 3.2 Logical Triggers  
Aşağı hal ESCALATE edir:

- agent nəticəsi məntiqsizdir  
- ziddiyyətli məlumat  
- struktura qarşı çıxır  
- workflow addımlarına uyğun deyil  
- nəticə real deyil  

---

### 3.3 Brand Triggers  
Samarkand Soul brendinə zərər verə biləcək istənilən output ESCALATE olunur:

- clickbait dil  
- agresiv üslub  
- ucuz dropshipping tonu  
- premium tonun pozulması  
- cultural disrespect  

---

### 3.4 Security Triggers  
Security Guardian siqnal verərsə → dərhal ESCALATE:

- unauthorized access  
- identity conflict  
- agent overlap  
- data integrity risk  
- API manipulyasiyası şübhəsi  

---

### 3.5 System Triggers  
System Health ciddi problem aşkarlasa:

- overload  
- conflict  
- stability risk  
- structural threat  

---

### 3.6 Ethical Triggers  
Etik qaydalar pozulanda:

- uydurma məlumat  
- qeyri-real iddialar  
- manipulyasiya  
- şişirtmə  
- fraud riskləri  

---

## 4. Mandatory Escalation Output Format

Bütün ESCALATION cavabları **dəqiq bu formatda** olmalıdır:

```
[ESCALATION]  
Reason: (short and clear description)  
Action: Human validation required  
Summary: (2–3 sentence overview of the issue)
```

Bu format dəyişdirilə bilməz.  
Başqa variant — qadağandır.

---

## 5. Escalation Levels (4 Stage Emergency System)

### LEVEL 1 — Soft Escalation  
- Kiçik uyğunsuzluq  
- Agent daha çox data istəyir  

```
[ESCALATION]  
Reason: Missing or unclear input  
Action: Provide corrected data  
```

---

### LEVEL 2 — Process Escalation  
- Workflow pozulub  
- Addımlar uyğun gəlmir  

```
[ESCALATION]  
Reason: Workflow integrity issue  
Action: Commander must validate sequence  
```

---

### LEVEL 3 — System Escalation  
- Stability risk  
- Conflict  
- Security warning  

```
[ESCALATION]  
Reason: System-level risk  
Action: Operations paused until approval  
```

---

### LEVEL 4 — Critical Shutdown Escalation  
- sistem zədələnə bilər  
- təhlükəsizlik pozuntusu güclüdür  

```
[ESCALATION]  
Reason: Critical system threat  
Action: Immediate Commander intervention required  
```

Bu səviyyədə agentlər öz-özünə davam edə bilməz.

---

## 6. Escalation Workflow (Mandatory Sequence)

Bütün ESCALATION-lar aşağıdakı ardıcıllıqla getməlidir:

```
Trigger → Detection → Block → ESCALATION Message → Commander → Resume/Rewrite/Stop
```

Heç bir agent bu ardıcıllıqdan yayınmamalıdır.

---

## 7. Forbidden Actions (Strict)

ESCALATION zamanı **qəti qadağandır**:

- boşluqları uydurma məlumatla doldurmaq  
- nəticəni “təxmini” yaratmaq  
- riskli workflow-u davam etdirmək  
- manipulyativ dil işlətmək  
- brand tonunu pozmaq  
- natamam məlumatı tam kimi göstərmək  

Hər bir qadağa Samarkand Soul sistemini qorumağa xidmət edir.

---

## 8. Responsibility Mapping

ESCALATION hallarında rolu olan komponentlər:

| Komponent | Rol |
|----------|-----|
| Agent | Ziddiyyət aşkar edəndə xəbər verir |
| Workflow Discipline | Proses ardıcıllığını yoxlayır |
| System Health | yük və stabilik riskini aşkar edir |
| Security Guardian | təhlükəsizlik riskini bloklayır |
| Commander | son qərar verən şəxs |

Sistem yalnız bu qaydada çalışa bilər.

---

## 9. Escalation Logging

Hər ESCALATION aşağıdakılarla loglanır:

- timestamp  
- səbəb  
- agent adı  
- workflow adı  
- status (open/closed)  
- Commander qərarı  
- düzəliş addımları  

Bu loglar sonradan optimallaşdırma üçün istifadə olunur.

---

## 10. Document Integrity

- Sənəd D1 ESCALATION moduluna məxsusdur  
- Dəyişiklik yalnız Commander təsdiqi ilə aparıla bilər  
- GitHub version control mütləqdir  
- Format və qaydalar dəyişdirilə bilməz  

---

## 11. Final Statement

D1_1 ESCALATION RULES Samarkand Soul sisteminin:

- qoruyucu qalxanıdır  
- səhvlərin qarşısını alan beyin mexanizmidir  
- brendin təhlükəsizlik qarantıdır  
- xaosdan qoruyan əməliyyat polisidir  

Bu sənəd ESCALATION sisteminin **dəyişməz qanunudur.**

---

**END OF DOCUMENT — D1_1_Escalation_Rules.md**
