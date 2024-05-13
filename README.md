
Đảm bảo bạn đã cài đặt Docker trên máy tính của mình. Kiểm tra bằng cách chạy:

```bash
docker --version
```

## Bước 1: Xây dựng Docker Image

Di chuyển đến thư mục chứa Dockerfile của ứng dụng backend:

```bash
cd backend
```

Xây dựng image Docker từ Dockerfile:

```bash
docker build -t backend .
```

## Bước 2: Chạy Ứng dụng Backend

Chạy ứng dụng backend trong một container Docker:

```bash
docker run -p 8000:8000 backend
```

Ứng dụng sẽ chạy và lắng nghe trên cổng 8000.

## Bước 3: Đăng nhập Docker Hub

Đăng nhập vào Docker Hub từ terminal:

```bash
docker login
```

Nhập tên đăng nhập và mật khẩu của bạn khi được yêu cầu.

## Bước 4: Tag và Đẩy Docker Image lên Docker Hub

Tag Docker image của bạn với tên repository trên Docker Hub:

```bash
docker tag backend:latest diends/backend:de
```

Đẩy Docker image lên Docker Hub:

```bash
docker push diends/backend:de
```

## Bước 5: Chạy Ứng dụng từ Docker Hub

Bây giờ, bạn có thể chạy ứng dụng backend từ image đã được đẩy lên Docker Hub:

```bash
docker run -it --name backend -p 8000:8000 diends/backend:de
```

---

Đảm bảo thay thế `diends` bằng tên đăng nhập Docker Hub của bạn và `backend` bằng tên ứng dụng/backend của bạn.