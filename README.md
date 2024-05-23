### Background
- Công ty thương mại điện tử mới thành lập, có lượng truy cập cao nhưng tỷ lệ chuyển đổi web sang mua hàng thấp. Vì vậy, chúng tôi dự đoán khả năng mua hàng của từng người dùng và triển khai chính sách giảm giá nhắm mục tiêu để thúc đẩy họ mua hàng.

### Achievements
- Phân tích RFM: Thực hiện phân tích RFM (Recency, Frequency, Monetary) chi tiết để phân loại người dùng dựa trên hành vi mua hàng của họ.
- Mô hình Khả năng Mua hàng: Sử dụng mô hình khả năng để dự báo hành vi người dùng và xác định những người cần khuyến khích để thực hiện mua hàng.

---
## Run docker
Đảm bảo bạn đã cài đặt Docker trên máy tính của mình. Kiểm tra bằng cách chạy:

```bash
docker --version
```

### Bước 1: Xây dựng Docker Image

Di chuyển đến thư mục chứa Dockerfile của ứng dụng Customer-propensity-to-purchase:

```bash
cd Customer-propensity-to-purchase
```

Xây dựng image Docker từ Dockerfile:

```bash
docker build -t customer-propensity-to-purchase .
```

### Bước 2: Chạy Ứng dụng Customer-propensity-to-purchase

Chạy ứng dụng Customer-propensity-to-purchase trong một container Docker:

```bash
docker run -p 8000:8000 customer-propensity-to-purchase
```

Ứng dụng sẽ chạy và lắng nghe trên cổng 8000.

### Bước 3: Đăng nhập Docker Hub

Đăng nhập vào Docker Hub từ terminal:

```bash
docker login
```

Nhập tên đăng nhập và mật khẩu của bạn khi được yêu cầu.

### Bước 4: Tag và Đẩy Docker Image lên Docker Hub

Tag Docker image của bạn với tên repository trên Docker Hub:

```bash
docker tag customer-propensity-to-purchase:latest diends/yourname:image_name
```

Đẩy Docker image lên Docker Hub:

```bash
docker push diends/yourname:image_name
```

### Bước 5: Chạy Ứng dụng từ Docker Hub

Bây giờ, bạn có thể chạy ứng dụng backend từ image đã được đẩy lên Docker Hub:

```bash
docker run -it --name customer-propensity-to-purchase -p 8000:8000 diends/yourname:image_name
```

---

Đảm bảo thay thế `diends` bằng tên đăng nhập Docker Hub của bạn và `yourname` bằng tên ứng dụng/yourname của bạn.