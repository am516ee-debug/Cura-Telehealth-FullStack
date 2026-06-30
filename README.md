# Cura Telehealth Hub 🩺🩵

**Cura** هو تطبيق طبي متكامل ومبتكر للاستشارات الطبية عن بعد (Telehealth)، مصمم لتقديم تجربة مستخدم (UX) فائقة السلاسة والجمال، ومربوط بسيرفر وقاعدة بيانات حقيقية لإدارة شؤون المرضى.

هذا المشروع مصمم ليكون نموذج عملي قوي (Full-Stack Portfolio Project) يجمع بين قوة التصميم وسلاسة البرمجة.

---

## 🎨 مميزات تجربة المستخدم (UI/UX Features)
* **نظام التصميم (Design System):** خط **Cairo** المتميز، وألوان لبنية طبية هادئة وجذابة تعزز ثقة المريض.
* **الوضع الداكن (Dark Mode):** واجهة متكاملة تدعم التغيير اللحظي والكامل للمظهر (Light/Dark Mode).
* **شاشة ترحيب تفاعلية (Multi-page Onboarding):** 3 صفحات ترحيبية سلسة مع مؤشرات نقطية متحركة.
* **فلترة التخصصات الفورية:** تصفية الأطباء لحظياً بضغطة زر بناءً على التخصص.
* **محاكاة مكالمة الفيديو (Video Call Simulation):** واجهة اتصال فيديو كاملة مع مؤقت للثواني ودقائق المكالمة، وإمكانية كتم المايك أو قفل الكاميرا.

---

## ⚙️ المعمارية البرمجية (Full-Stack Architecture)

### 1️⃣ الواجهة الأمامية (Frontend - Flutter)
* **إدارة الحالة (State Management):** باستخدام مكتبة `Provider` لإدارة بيانات الجلسة والحجوزات بشكل مركزي ومزامنتها لحظياً.
* **الاتصال بالشبكة:** استخدام مكتبة `http` لإرسال واستقبال البيانات بصيغة JSON من السيرفر.

### 2️⃣ السيرفر وقاعدة البيانات (Backend - Python)
* **السيرفر (API):** مبني بلغة بايثون باستخدام إطار عمل **Flask**، ويحتوي على منافذ RESTful مؤمنة.
* **تشفير كلمات المرور:** يتم تشفير كلمات المرور في قاعدة البيانات باستخدام خوارزمية **SHA-256**.
* **قاعدة البيانات:** **SQLite** خفيفة وسريعة وتخزن البيانات في ملف محلي (`database.db`).

---

## 💾 هيكل جداول قاعدة البيانات (Database Schema)

* **جدول المستخدمين (`users`):**
  * `id` (INTEGER PRIMARY KEY)
  * `name` (TEXT)
  * `email` (TEXT UNIQUE)
  * `password` (TEXT - Hashed)

* **جدول الحجوزات (`bookings`):**
  * `id` (INTEGER PRIMARY KEY)
  * `user_id` (INTEGER - Foreign Key)
  * `doctor_name` (TEXT)
  * `doctor_specialty` (TEXT)
  * `doctor_image` (TEXT)
  * `date` (TEXT)
  * `time` (TEXT)

* **جدول التقارير الطبية (`records`):**
  * `id` (INTEGER PRIMARY KEY)
  * `user_id` (INTEGER - Foreign Key)
  * `title` (TEXT)
  * `doctor` (TEXT)
  * `date` (TEXT)
  * `type` (TEXT - PDF/Image)

---

## 🚀 كيفية تشغيل المشروع محلياً (How to Run)

### 1. تشغيل السيرفر (Backend)
1. انتقل لمجلد السيرفر:
   ```bash
   cd cura_backend
