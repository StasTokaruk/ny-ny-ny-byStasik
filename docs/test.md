# Тестування працездатності системи

## POST
### *Create Role*
```bash
{
  "name": "Stas",
  "description": "Info1"
}
```
![image](https://github.com/user-attachments/assets/96a0499a-b76c-482c-873c-7b6050e61771)
### *Create User*
```bash
{
  "email": "stastokaruk@gmail.com",
  "password": "admin",
  "name": "admin",
  "surname": "Stanislav",
  "nickname": "Tokariuk"
}
```
![image](https://github.com/user-attachments/assets/a3ac4746-5b1e-4731-b5ec-c1e6a6f7a629)
### *Create Expertise Category*
```bash
{
  "name": "category1",
  "description": "Info1"
}
```
![image](https://github.com/user-attachments/assets/9bdb6f28-00b5-4b5f-8d80-211a5581ca57)

### *Create User Expertise*
```bash
{
  "User_id": 2,
  "ExpertiseCategory_id": 1
}
```
![image](https://github.com/user-attachments/assets/3e868a13-7fff-4c3f-bef2-9775426050b5)

### *Create Quiz*
```bash
{
  "name": "quiz1",
  "description": "opys",
  "User_id": 2
}
```
![image](https://github.com/user-attachments/assets/1cfd42c8-0018-4119-9a9a-0fbdb78598eb)

### *Create Question*
```bash
{
  "Quiz_id": 1,
  "number": 1,
  "description": "question1",
  "type": "easy"
}
```
![image](https://github.com/user-attachments/assets/96a0499a-b76c-482c-873c-7b6050e61771)
### *Create Option*
```bash
{
  "Question_id": 1,
  "number": 1,
  "description": "info"
}
```
![image](https://github.com/user-attachments/assets/a067a046-d057-43c6-80ee-98a45c6a5793)


## GET
### *Read Roles*
![image](https://github.com/user-attachments/assets/3b3325a0-184d-4426-b225-257741df8d90)

### *Read Users*
![image](https://github.com/user-attachments/assets/e10dc90f-4f64-4f73-9d56-5f6af812b052)

### *Read Expertise Categories*
![image](https://github.com/user-attachments/assets/748c34fa-a352-4b7d-9b1d-0486838f479c)

### *Read User Expertise *
![image](https://github.com/user-attachments/assets/133bea42-7571-4a8b-b9cc-cab0c8c21ad8)

### *Read Quizzes*
![image](https://github.com/user-attachments/assets/76cfc368-2882-446f-81c4-298addbc23b7)

### *Read Quizzes By User*
![image](https://github.com/user-attachments/assets/6b258f34-17ee-4801-9999-6279620cbdfb)

### *Read Question*
![image](https://github.com/user-attachments/assets/6b2f182a-ecae-4514-95bb-ea2fa42fef8a)

## PUT
### *Update Expertise Category*
```bash
{
  "name": "category1v2",
  "description": "info"
}
```
![image](https://github.com/user-attachments/assets/b8ea8c4f-a5ca-40d6-ba5f-7ec6b18cf61d)

### *Update Quiz*
```bash
{
  "name": "Quiz1v2",
  "description": "info",
  "User_id": 2
}
```
![image](https://github.com/user-attachments/assets/0148799f-266b-471a-ab08-d5f50a4ada5d)

### *Update Question*
```bash
{
  "Quiz_id": 1,
  "number": 1,
  "description": "info",
  "type": "hard"
}
```
![image](https://github.com/user-attachments/assets/0f9e174a-a4b7-4553-8f7f-e986c34c96a5)

## DELETE
### *Delete Expertise Category*
![image](https://github.com/user-attachments/assets/99233cfa-e56c-4f85-948e-060225f66082)

### *Delete User Expertise*
![image](https://github.com/user-attachments/assets/15773b8e-ec71-442b-9e54-8e367494af96)

### *Delete Quiz*
![image](https://github.com/user-attachments/assets/2b279990-1536-403e-825c-57148d6ab2ea)

### *Delete Question*
![image](https://github.com/user-attachments/assets/f43f082e-7284-4887-8ff2-cecf8a1fbba2)

