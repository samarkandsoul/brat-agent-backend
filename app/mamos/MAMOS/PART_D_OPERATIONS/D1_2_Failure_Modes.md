# D1_2 — Failure Modes  
**Category:** PART_D_OPERATIONS  
**Version:** 1.0  
**Status:** ACTIVE  
**Owner:** SYS_D1_FAILURE  
**Supervisor:** SYSTEM COMMANDER  

---

## 1. Purpose

D1_2 Failure Modes modulu Samarkand Soul sistemində **potensial səhv növlərini, riskləri və sistemin hansı hallarda pozula biləcəyini müəyyən edən** əsas idarəetmə mexanizmidir.

Onun missiyası:

- bütün agentlərin zəif nöqtələrini aşkarlamaq  
- prosesləri risklərdən qorumaq  
- sistem pozuntularını qabaqlamaq  
- sürətli diaqnostika və bərpa mexanizmi təmin etmək  

Bu modul — Samarkand Soul-un **səhv profilaktikası və diaqnostika beyni**dir.

---

## 2. Failure Mode nədir?

Failure Mode — sistemdə baş verən və ya baş verə biləcək:

- pozuntu  
- ziddiyyət  
- uyğunsuzluq  
- riskli nəticə  
- səhv çıxış  
- agent davranışında problem  

deməkdir.

Failure Mode müəyyən edildikdən sonra əməliyyat **dayandırılır** və ya **ESCALATE** olunur.

---

## 3. Classification of Failure Modes

D1_2 modulu failure-ları 7 əsas kateqoriyaya bölür:

---

### F1 — Input-Level Failure  
Bu hallar daxildir:

- natamam input  
- yanlış format  
- məhsul məlumatı ziddiyyətli  
- agent nə etməli olduğunu anlaya bilmir  
- required fields boşdur  

Nümunə:

```
[FAILURE F1]  
Reason: Missing input  
Action: ESCALATE
```

---

### F2 — Logic Failure  
Aşağıdakılar baş verəndə sistem bunu F2 hesab edir:

- nəticə məntiqə uyğun gəlmir  
- data uyğunsuzdur  
- nəticə workflow ilə uyğun deyil  
- agent ziddiyyətli hesablama aparıb  

Nümunə:

```
[FAILURE F2]  
Reason: Logical contradiction  
Action: Operation stopped
```

---

### F3 — Structural Failure  
MAMOS qovluq və sənəd strukturu pozularsa:

- yanlış file adı  
- yanlış folder adı  
- struktur daxili sənəd itməsi  
- qovluq ardıcıllığı pozulub  
- yazı formatı zədələnib  

Nümunə:

```
[FAILURE F3]  
Reason: Structural integrity violation  
Action: System locked
```

---

### F4 — Agent Behavior Failure  
Agent aşağıdakıları edəndə F4 tetiklenir:

- öz rolundan kənara çıxmaq  
- başqa agentin səlahiyyətinə müdaxilə  
- ardıcıllığı pozmaq  
- qeyri-sabit davranış  
- output-da brand pozuntusu  

Nümunə:

```
[FAILURE F4]  
Reason: Agent role violation  
Action: ESCALATE
```

---

### F5 — Brand Violation Failure  
Brendin premium, calm luxury və səmimi estetikasına zidd olan istənilən nəticə:

- clickbait  
- aqressiv ton  
- ucuz dropshipping vibe  
- şişirdilmiş iddialar  
- "limited offer" manipulyasiyası  
- sayqısız mədəniyyət təsviri  

Brend pozuntusu sistemin **ən ağır** failure-larından biridir.

Nümunə:

```
[FAILURE F5]  
Reason: Brand integrity risk  
Action: Blocked
```

---

### F6 — Performance Failure  
Aşağıdakılar olur:

- agent çox yavaş cavab verir  
- sistem yorğunluq göstərir  
- yük “overload” dərəcəsinə çatır  
- agent eyni işi dəfələrlə edir  

Nümunə:

```
[FAILURE F6]  
Reason: Performance degradation  
Action: Throttle load
```

---

### F7 — Security Failure  
Security Guardian tərəfindən aşkarlanan bütün təhlükələr:

- unauthorized access  
- identity spoof  
- manipulated data  
- sensitive breach attempt  
- API conflict  

Nümunə:

```
[FAILURE F7]  
Reason: Security threat  
Action: Immediate shutdown
```

---

## 4. Mandatory Failure Response Protocol

Hər bir failure aşağıdakı ardıcıllıqla idarə olunmalıdır:

```
Detection → Classification → Block → ESCALATION → Commander Decision → Resume/Rewrite/Stop
```

Bu ardıcıllıq dəyişdirilə bilməz.

---

## 5. Failure Mode Severity Levels

D1_2 aşağıdakı şiddət səviyyələrindən istifadə edir:

### LEVEL 1 — Minor  
- kiçik input səhvi  
- düzəldilə biləndir  

### LEVEL 2 — Moderate  
- proses pozulub  
- workflow təsdiqi lazımdır  

### LEVEL 3 — Major  
- agent davranışı səhvdir  
- sistem risk edir  

### LEVEL 4 — Critical  
- təhlükəsizlik  
- struktur pozuntusu  
- brend pozuntusu  
- sistem sabitliyi təhlükə altındadır  

LEVEL 4 → dərhal Komander çağırılır.

---

## 6. Escalation Connection  

D1_2 Failure Modes → D1_1 Escalation Rules ilə **birbaşa əlaqəlidir**.

Failure Mode aşkar ediləndə sistem aşağıdakı formatı işə salır:

```
[ESCALATION]  
Reason: (Failure Mode description)  
Action: Human validation required  
Summary: System halted for safety
```

---

## 7. Failure Logging

Hər Failure Mode aşağıdakılarla loglanır:

- failure ID  
- növ (F1–F7)  
- agent adı  
- workflow adı  
- timestamp  
- təsvir  
- şiddət  
- nəticə (resolved / unresolved)  

Bu loglar optimallaşdırma üçün istifadə olunur.

---

## 8. Document Integrity Notes

- Sənəd SYS_D1_FAILURE moduluna məxsusdur  
- Dəyişiklik yalnız Commander təsdiqi ilə mümkündür  
- GitHub version control məcburidir  
- Failure Mode qaydaları dəyişdirilə bilməz  

---

## 9. Final Statement

D1_2 Failure Modes Samarkand Soul sisteminin:

- risk radar sistemidir  
- diaqnostika panelidir  
- agent davranış kontrol mərkəzidir  
- brend qoruma qalxanıdır  
- sistem sağlamlığının siqnalizasiyasıdır  

Bu sənəd Failure Mode mexanizminin **dəyişməz qanunudur**.

---

**END OF DOCUMENT — D1_2_Failure_Modes.md**
