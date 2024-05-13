Thứ nhất : cd backend
thứ 2: docker build -t backend .
thứ 3: docker run -p 8000:8000 backend    


build dockerhub
- đăng nhập và tạo repository 
docker tag backend:latest diends/backend:de
docker push diends/backend:de

chay lenh nay
docker run -it --name backend  -p 8000:8000 diends/backend:de