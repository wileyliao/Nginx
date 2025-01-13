# Nginx
nginx on docker(include SSL)

## SSL
>- Decode pfx file see `pfx2pem.py`
>- Combine cert.crt & ca_bundle.crt to one file
`Get-Content cert.crt, ca_bundle.crt | Out-File -Encoding ascii full_chain.crt`
>- Dockerfile
```
FROM nginx:alpine

# 複製 NGINX 配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 建立證書目錄
RUN mkdir -p /etc/nginx/ssl

# 複製 SSL 證書文件
COPY full_chain.crt /etc/nginx/ssl/
COPY cert.key /etc/nginx/ssl/

# 設置證書文件權限
RUN chmod 600 /etc/nginx/ssl/*

# 暴露 HTTPS 端口
EXPOSE 3003

# 啟動 NGINX
CMD ["nginx", "-g", "daemon off;"]
```

>- nginx.conf
```
server {
    listen 3003 ssl;
    server_name www.kutech.tw;
    
    ssl_certificate /etc/nginx/ssl/full_chain.crt;
    ssl_certificate_key /etc/nginx/ssl/cert.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location /gpu_status {
        proxy_pass http://gpu_status_ssl:3001/gpu_status;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    ... ...
}
```

## NORMAL
>- Dockerfile
```
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
```

>- nginx.conf
```
server {
    listen 3000;

    location /gpu_status {
        proxy_pass http://gpu_status:3001/gpu_status;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
   
    location /po_vision {
        proxy_pass http://po_vision:3001/po_vision;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        client_max_body_size 20M;
        client_body_buffer_size 10M;
    }
    ... ...
}
```
