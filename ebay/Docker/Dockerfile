# Sử dụng image chứa Python 3.7
FROM base_web_sale:latest

# Thiết lập thư mục làm việc cho container
WORKDIR /app

# Sao chép mã nguồn của Flask app vào thư mục làm việc của container
COPY . .
# Chỉ định cổng mà Flask app sẽ lắng nghe
EXPOSE 81
# Chạy Flask app
CMD ["sh", "-c", "cd main && python app.py"]

#CMD [ "python", "app.py" ]
