# Hệ Thống Gợi Ý Việc Làm Tích Hợp AI

- Backend được xây dựng bằng FastAPI, nhằm mục đích đi hỗ trợ gợi ý việc làm dựa trên CV (chưa phát triển upload cv) bằng kỹ thuật Machine Learning, Feature Engineering và dựa trên các phân tích hành vi của người dùng.

Hệ thống xếp hạng các công việc phù hợp với hồ sơ các bạn sinh viên dựa trên mức độ tương đồng như:
- NỘI DUNG
- KỸ NĂNG CHUYÊN MÔN
- ĐỘ PHỔ BIẾN của công việc
- LỊCH SỬ (hành vi) của người dùng

---
---

## Tổng qua về các tính Năng Chính

* Backend được phát triển bằng FastAPI
* Dùng cơ sở dữ liệu PostgreSQL (chỉ mới biết sql này nên xài, và nó khá phổ biển)
* SQLAlchemy ORM
* Docker Compose cơ bản (học qua môn Điện toán đám mây)
* Quản lý dữ liệu CV và việc làm và lịch sử tương tác người dùng
* API gợi ý việc làm
* API ghi nhận hành vi người dùng
* Bộ nhớ đệm embedding trong RAM
* Pipeline Feature Engineering
* Xài Logistic Regression để xếp hạng -> nhẹ, dễ, nổi, cơ bản nhất -> nếu thành công sẽ dễ nâng cấp <- chọn mô hình quá nặng sẽ dấn đến khó test do mất thời gian để train
* Dữ liệu huấn luyện mô phỏng (100cty được gen tự động)
* Hỗ trợ huấn luyện lại từ dữ liệu tương tác thực tế
* Tự động sinh dữ liệu mẫu khi khởi động
* Bộ kiểm thử bằng Pytest

---
---

## Tổng qua về kiến Trúc Hệ Thống

```text
FastAPI
   |
   +-- API Layer
   |
   +-- Service Layer
   |
   +-- Feature Engineering
   |
   +-- Machine Learning Ranking Model
   |
   +-- PostgreSQL
```

---

## Tổng qua về cấu trúc cái project này
```text
app/

  main.py

  api/
    recommendation.py
    events.py

  db/
    models.py
    session.py
    seed.py

  ml/
    train_model.py
    model.pkl

  schemas/
    recommendation.py
    events.py

  services/
    embedding_service.py
    feature_engineering.py
    ranking_model.py
    recommendation_service.py

tests/
  test_app.py

README.md
```

---
---

## DOCKER

project xài docker cho cơ bản, dưới đây là cách chạy:


```bash
docker compose up --build
```
Kiểm tra:

```text
http://localhost:8000/docs
```

---
---


## Sử Dụng API

### Gợi Ý Việc Làm

Lấy danh sách công việc phù hợp nhất cho CV có ID = 1:

```bash
curl "http://localhost:8000/recommend/jobs/1?user_id=10"
```

```text
(.venv)% curl "http://localhost:8000/recommend/jobs/1?user_id=10"
[{"job_id":9,"title":"Backend Engineer Intern","company":"TalentGraph","score":0.9991,"matched_skills":["Python","FastAPI","PostgreSQL","Docker","REST API"],"missing_skills":[],"reason":"resume text is semantically close to the job description; 5 required skills matched; the job is recent"},{"job_id":17,"title":"Backend Engineer Intern","company":"DevPath","score":0.9988,"matched_skills":["Python","FastAPI","PostgreSQL","Docker","REST API"],"missing_skills":[],"reason":"resume text is semantically close to the job description; 5 required skills matched; the job is recent"},{"job_id":25,"title":"Backend Engineer Intern","company":"DockerWorks","score":0.9988,"matched_skills":["Python","FastAPI","PostgreSQL","Docker","REST API"],"missing_skills":[],"reason":"resume text is semantically close to the job description; 5 required skills matched; the job is recent"},{"job_id":33,"title":"Backend Engineer Intern","company":"StackMakers","score":0.9988,"matched_skills":["Python","FastAPI","PostgreSQL","Docker","REST API"],"missing_skills":[],"reason":"resume text is semantically close to the job description; 5 required skills matched; the job is recent"},{"job_id":41,"title":"Backend Engineer Intern","company":"FeatureLab","score":0.9988,"matched_skills":["Python","FastAPI","PostgreSQL","Docker","REST API"],"missing_skills":[],"reason":"resume text is semantically close to the job description; 5 required skills matched; the job is recent"},{"job_id":1,"title":"Backend Engineer Intern","company":"TechStart Labs","score":0.9987,"matched_skills":["Python","FastAPI","PostgreSQL","Docker","REST API"],"missing_skills":[],"reason":"resume text is semantically close to the job description; 5 required skills matched; the job is recent"},{"job_id":49,"title":"Backend Engineer Intern","company":"TalentSpark","score":0.9987,"matched_skills":["Python","FastAPI","PostgreSQL","Docker","REST API"],"missing_skills":[],"reason":"resume text is semantically close to the job description; 5 required skills matched; the job is recent"},{"job_id":57,"title":"Backend Engineer Intern","company":"JobVector","score":0.9987,"matched_skills":["Python","FastAPI","PostgreSQL","Docker","REST API"],"missing_skills":[],"reason":"resume text is semantically close to the job description; 5 required skills matched; the job is recent"},{"job_id":27,"title":"Search and NLP Engineer Intern","company":"ModelOps","score":0.8823,"matched_skills":["Python","NLP","PostgreSQL"],"missing_skills":["Search","Ranking"],"reason":"3 required skills matched; the job is recent; missing skills: Search, Ranking"},{"job_id":19,"title":"Search and NLP Engineer Intern","company":"BackendForge","score":0.8614,"matched_skills":["Python","NLP","PostgreSQL"],"missing_skills":["Search","Ranking"],"reason":"3 required skills matched; the job is recent; missing skills: Search, Ranking"}]%    
```
---

### Gửi Phản Hồi Hành Vi Người Dùng

Ví dụ người dùng lưu một công việc:

```bash
curl -X POST http://localhost:8000/events/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 10,
    "job_id": 1,
    "event_type": "save"
  }'
```

```text
(.venv)% curl -X POST http://localhost:8000/events/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 10,
    "job_id": 1,
    "event_type": "save"
  }'
{"id":1,"user_id":10,"job_id":1,"event_type":"save","timestamp":"2026-06-16T08:21:58.185284Z"}%   
```

Các loại sự kiện hỗ trợ:

```text
click
save
apply
```

---

## Huấn Luyện Mô Hình

Huấn luyện lại mô hình nếu cần thiết:

```bash
python -m app.ml.train_model
```

Huấn luyện lại có sử dụng dữ liệu tương tác người dùng:

```bash
RETRAIN_WITH_USER_EVENTS=true python -m app.ml.train_model
```

---

## Chạy Kiểm Thử

```bash
pytest
```

---

## Cách Hệ Thống Xếp Hạng Hoạt Động

Mỗi công việc được biểu diễn bằng một vector đặc trưng:

```text
[
  embedding_similarity,
  skill_overlap_score,
  job_popularity_score,
  user_click_score,
  recency_score
]
```

Ý nghĩa:

* embedding_similarity -> dùng để độ tương đồng ngữ nghĩa giữa CV và mô tả công việc
* skill_overlap_score: -> thể hiện mức độ khớp kỹ năng
* job_popularity_score -> thể hiện độ phổ biến của công việc
* user_click_score -> thể hiện mức độ quan tâm của người dùng
* recency_score -> thể hiện độ mới của tin tuyển dụng

---
---

## Pipeline Chạy

```text
CV
 |
 v
Tính toán đặc trưng
 |
 v
Machine Learning Ranking Model
 |
 v
Điều chỉnh theo hành vi người dùng
 |
 v
Sắp xếp điểm số
 |
 v
Trả về Top 10 công việc phù hợp nhất
```

---

## Kiến Thức Áp Dụng

Mục tiêu là để tìm hiểu:

* Backend Engineering
* RESTful API
* PostgreSQL
* SQLAlchemy ORM
* Docker
* Machine Learning
* Recommendation System
* Feature Engineering
* Learning To Rank
* NLP Embeddings
* User Behavior Analytics
* AI Engineering